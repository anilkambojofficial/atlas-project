"""Kafka client foundation.

Governing documents:
- IP-001 §7 — Kafka is the platform event transport.
- IP-001 §14 — health checks validate the Kafka dependency.
- RA-006 §5 — the Event Bus handles publication; §18 — payloads are
  validated and tenant-stamped by the event contracts (the full contract
  layer arrives with the shared ``events`` package in Sprint-001 S1.4 and
  builds on this client).
- ARCH-001 §14 — graceful degradation: a broker outage must not crash
  the application; readiness reflects the failure instead.

The manager owns one application-scoped producer. Consumers are created
per subscribing worker through ``create_consumer`` so that consumer
groups, offsets, and lifecycles stay owned by the consuming component
(RA-006 §11 Inbox responsibilities live with consumers).
"""

from __future__ import annotations

import json
from typing import Any

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from shared.exceptions import InfrastructureError
from shared.config import Settings
from shared.logging import get_logger

_logger = get_logger("atlas.infrastructure.kafka")


class KafkaManager:
    """Owns the application-scoped Kafka producer and consumer factory."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._producer: AIOKafkaProducer | None = None
        self._last_error: str | None = None

    @property
    def is_connected(self) -> bool:
        """True when the producer is started and usable."""
        return self._producer is not None

    async def start(self) -> None:
        """Start the producer; failures are recorded, logged, and re-raised
        for the caller (the container startup logs and degrades gracefully).
        """
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

    async def stop(self) -> None:
        """Stop the producer if it was started (application shutdown)."""
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
        (acks=all with idempotence — RA-006 §14 reliability posture)."""
        if self._producer is None:
            raise InfrastructureError(
                "Kafka producer is not connected; message cannot be published"
            )
        await self._producer.send_and_wait(
            topic,
            value=json.dumps(value, default=str).encode("utf-8"),
            key=key.encode("utf-8") if key is not None else None,
            headers=[(k, v.encode("utf-8")) for k, v in (headers or {}).items()],
        )

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
        """Kafka health check (IP-001 §14): verify broker metadata access."""
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
