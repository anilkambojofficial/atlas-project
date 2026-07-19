"""Transactional-outbox drain worker (ADR-002 §2).

Governing documents:
- RA-006 §10/§15 — outbox drain with retry and dead-letter escalation;
  at-least-once delivery (consumers are idempotent per the Inbox pattern).
- ADR-002 — polling drain via Celery beat; capped exponential backoff per
  entry (``next_attempt_at``); entries exceeding the attempt budget are
  marked ``failed`` and surfaced loudly (alerting hook — outbox age and
  failure counts are Production Ready alert conditions, CON-001 §15).
- ADR-003 — broker failures raise retriable ``InfrastructureError``;
  the entry stays pending and backs off.

Each drain run owns its event loop, database engine, and producer
lifecycle (Celery task isolation: aiokafka objects must not outlive the
loop that created them). Batch publication amortizes the connection cost.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from infrastructure.database.engine import DatabaseManager
from infrastructure.messaging.kafka import KafkaManager
from infrastructure.messaging.outbox_model import OutboxRecord
from shared.config import Settings
from shared.events import topic_for
from shared.events.outbox import OutboxStatus
from shared.logging import get_logger

_logger = get_logger("atlas.workers.outbox")

#: ADR-002 §2 backoff parameters (seconds).
_RETRY_BASE_SECONDS = 2.0
_RETRY_CAP_SECONDS = 300.0


def _next_attempt_delay(attempts: int) -> timedelta:
    """Capped exponential backoff for one failed entry."""
    return timedelta(
        seconds=min(_RETRY_CAP_SECONDS, _RETRY_BASE_SECONDS * (2**attempts))
    )


async def drain_outbox_once(settings: Settings) -> dict[str, int]:
    """Publish one batch of eligible outbox entries; returns counters.

    Eligible: ``pending`` with ``next_attempt_at`` unset or due, oldest
    first, row-locked with SKIP LOCKED so concurrent drains never double-
    publish within one database's visibility (at-least-once overall).
    """
    database = DatabaseManager(settings)
    kafka = KafkaManager(settings)
    published = failed = deferred = 0
    try:
        await kafka.start()
    except Exception as exc:  # noqa: BLE001 — broker down: nothing drains this run
        _logger.warning(
            "Outbox drain skipped; Kafka unavailable",
            extra={"error": type(exc).__name__},
        )
        await database.dispose()
        return {"published": 0, "failed": 0, "deferred": 0, "skipped": 1}

    try:
        async with database.session_factory() as session:
            now = datetime.now(timezone.utc)
            statement = (
                select(OutboxRecord)
                .where(OutboxRecord.status == OutboxStatus.PENDING.value)
                .where(
                    (OutboxRecord.next_attempt_at.is_(None))
                    | (OutboxRecord.next_attempt_at <= now)
                )
                .order_by(OutboxRecord.created_at)
                .limit(settings.outbox_batch_size)
                .with_for_update(skip_locked=True)
            )
            records = (await session.execute(statement)).scalars().all()

            for record in records:
                try:
                    await kafka.publish(
                        topic_for(record.event_type),
                        record.envelope,
                        key=record.organization_id,
                    )
                except Exception as exc:  # noqa: BLE001 — classified below per ADR-002/003
                    record.attempts += 1
                    record.last_error = f"{type(exc).__name__}: {exc}"[:2000]
                    if record.attempts >= settings.outbox_max_attempts:
                        record.status = OutboxStatus.FAILED.value
                        failed += 1
                        _logger.error(
                            "Outbox entry exhausted retry budget (ALERT)",
                            extra={
                                "eventId": record.event_id,
                                "eventType": record.event_type,
                                "attempts": record.attempts,
                            },
                        )
                    else:
                        record.next_attempt_at = datetime.now(
                            timezone.utc
                        ) + _next_attempt_delay(record.attempts)
                        deferred += 1
                else:
                    record.status = OutboxStatus.PUBLISHED.value
                    record.published_at = datetime.now(timezone.utc)
                    record.last_error = None
                    published += 1
            await session.commit()
    finally:
        await kafka.stop()
        await database.dispose()

    if published or failed or deferred:
        _logger.info(
            "Outbox drain completed",
            extra={
                "published": published,
                "failed": failed,
                "deferred": deferred,
            },
        )
    return {"published": published, "failed": failed, "deferred": deferred, "skipped": 0}
