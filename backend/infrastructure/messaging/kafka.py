"""Kafka client foundation.

Governing documents:
- IP-001 §7 — Kafka is the platform event transport.
- IP-001 §14 — health checks validate the Kafka dependency.
- RA-006 §5 — the Event Bus handles publication; §18 — payloads are
  validated and tenant-stamped by the event contracts.
- ARCH-001 §14 — graceful degradation: a broker outage must not crash
  the application; readiness reflects the failure instead.
- ADR-003 — reliability: supervised producer (re-)establishment with
  capped exponential backoff + jitter; startup-connect failure no longer
  condemns the process (AUD-001 C-2 closed); send errors are classified
  retriable vs fatal; repeated failure trips the health check, which
  gates readiness (the minimal circuit breaker of ADR-003 §3).

The manager owns one application-scoped producer. Consumers are created
per subscribing worker through ``create_consumer`` so that consumer
groups, offsets, and lifecycles stay owned by the consuming component
(RA-006 §11 Inbox responsibilities live with consumers).
"""

from __future__ import annotations

import asyncio
import json
import random
from typing import Any

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError

from shared.exceptions import InfrastructureError
from shared.config import Settings
from shared.logging import get_logger

_logger = get_logger("atlas.infrastructure.kafka")

#: ADR-003 §1 — capped exponential backoff parameters for the supervisor.
_BACKOFF_BASE_SECONDS = 1.0
_BACKOFF_CAP_SECONDS = 60.0


class KafkaManager:
    """Owns the application-scoped Kafka producer and consumer factory."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._producer: AIOKafkaProducer | None = None
        self._last_error: str | None = None
        self._connect_lock = asyncio.Lock()
        self._supervisor: asyncio.Task[None] | None = None
        self._stopped = False

    @property
    def is_connected(self) -> bool:
        """True when the producer is started and usable."""
        return self._producer is not None

    async def start(self) -> None:
        """Start the producer once; failures are recorded and re-raised.

        Callers wanting self-healing semantics use :meth:`start_supervised`
        (ADR-003 §1); this method stays raise-on-failure for tests and
        explicit one-shot connections.
        """
        async with self._connect_lock:
            if self._producer is not None:
                return
            producer = AIOKafkaProducer(
                bootstrap_servers=self._settings.kafka_broker,
                client_id=self._settings.kafka_client_id,
                acks="all",
                enable_idempotence=True,
                request_timeout_ms=self._settings.kafka_timeout_seconds * 1000,
            )
            try:
                await producer.start()
            except Exception as exc:
                self._last_error = type(exc).__name__
                raise
            self._producer = producer
            self._last_error = None
            _logger.info(
                "Kafka producer started",
                extra={"bootstrapServers": self._settings.kafka_broker},
            )

    async def start_supervised(self) -> None:
        """Establish the producer; on failure, keep retrying in the
        background with capped exponential backoff + jitter (ADR-003 §1).
        Never raises — degradation is visible through the health check.
        """
        self._stopped = False
        try:
            await self.start()
        except Exception as exc:  # noqa: BLE001 — supervised path degrades, never crashes
            _logger.error(
                "Kafka unavailable at startup; supervisor engaged (ADR-003)",
                exc_info=exc,
            )
            self._ensure_supervisor()

    def _ensure_supervisor(self) -> None:
        if self._supervisor is None or self._supervisor.done():
            self._supervisor = asyncio.create_task(
                self._reconnect_loop(), name="kafka-reconnect-supervisor"
            )

    async def _reconnect_loop(self) -> None:
        attempt = 0
        while not self._stopped and self._producer is None:
            attempt += 1
            delay = min(_BACKOFF_CAP_SECONDS, _BACKOFF_BASE_SECONDS * (2 ** (attempt - 1)))
            delay += random.uniform(0, delay * 0.25)
            await asyncio.sleep(delay)
            if self._stopped:
                return
            try:
                await self.start()
                _logger.info(
                    "Kafka producer recovered by supervisor",
                    extra={"attempts": attempt},
                )
                return
            except Exception as exc:  # noqa: BLE001 — retried per ADR-003 backoff policy
                self._last_error = type(exc).__name__
                _logger.warning(
                    "Kafka reconnection attempt failed",
                    extra={"attempt": attempt, "error": type(exc).__name__},
                )

    async def stop(self) -> None:
        """Stop the supervisor and the producer (application shutdown)."""
        self._stopped = True
        if self._supervisor is not None:
            self._supervisor.cancel()
            try:
                await self._supervisor
            except (asyncio.CancelledError, Exception):  # noqa: BLE001 — shutdown path
                pass
            self._supervisor = None
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None
            _logger.info("Kafka producer stopped")

    async def publish(
        self,
        topic: str,
        value: dict[str, Any],
        *,
        key: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Publish one JSON-serialized message and await broker acknowledgment
        (acks=all with idempotence — RA-006 §14 reliability posture).

        Error classification (ADR-003 §2): broker/transport failures raise
        retriable ``InfrastructureError`` (absorbed by the ADR-002 outbox
        retry); serialization failures are fatal and propagate as-is.
        """
        if self._producer is None:
            # Lazy re-establishment path (ADR-003 §1): schedule recovery and
            # fail this attempt as retriable.
            self._ensure_supervisor()
            raise InfrastructureError(
                "Kafka producer is not connected; message cannot be published"
            )
        payload = json.dumps(value, default=str).encode("utf-8")
        try:
            await self._producer.send_and_wait(
                topic,
                value=payload,
                key=key.encode("utf-8") if key is not None else None,
                headers=[(k, v.encode("utf-8")) for k, v in (headers or {}).items()],
            )
        except KafkaError as exc:
            self._last_error = type(exc).__name__
            raise InfrastructureError(
                f"Kafka publish failed ({type(exc).__name__}); retriable"
            ) from exc

    def create_consumer(self, *topics: str, group_id: str) -> AIOKafkaConsumer:
        """Build a consumer for a subscribing component; the caller owns
        its lifecycle (start/stop) and offset semantics (RA-006 §11)."""
        return AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self._settings.kafka_broker,
            client_id=self._settings.kafka_client_id,
            group_id=group_id,
            enable_auto_commit=False,
        )

    async def health_check(self) -> tuple[bool, str]:
        """Kafka health check (IP-001 §14; ADR-003 §3 readiness trip)."""
        if self._producer is None:
            detail = "producer not connected"
            if self._last_error:
                detail += f" (last error: {self._last_error})"
            return False, detail
        try:
            await self._producer.client.fetch_all_metadata()
        except Exception as exc:  # noqa: BLE001 — probe converts failures to status
            return False, f"metadata fetch failed: {type(exc).__name__}"
        return True, "connected"
