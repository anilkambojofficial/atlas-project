"""Event publication abstractions.

Governing documents:
- RA-006 §5 — the Event Bus is the sole distribution mechanism
  (BP-002 ED-011); §14 — reliable, acknowledged publication.
- RA-001 §13 — integration events are published only after successful
  commit (wired through the Unit of Work's post-commit seam).
- Framework-independence rule (S1.4): shared/* never imports the
  infrastructure layer. ``MessageTransport`` is the structural protocol
  that ``infrastructure.messaging.KafkaManager`` already satisfies; the
  application container performs the binding (IP-001 §11 — depend on
  interfaces, not implementations).
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from shared.events.envelope import EventEnvelope
from shared.events.naming import topic_for
from shared.logging import get_logger

_logger = get_logger("atlas.shared.events")


@runtime_checkable
class MessageTransport(Protocol):
    """Structural contract for the underlying message broker client."""

    async def publish(
        self,
        topic: str,
        value: dict[str, Any],
        *,
        key: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:  # pragma: no cover — protocol signature only
        ...


@runtime_checkable
class EventPublisher(Protocol):
    """Publishes validated platform events (RA-006 §5)."""

    async def publish(self, envelope: EventEnvelope) -> None:  # pragma: no cover
        ...


class KafkaEventPublisher:
    """Publishes envelopes through a :class:`MessageTransport`.

    Routing (RA-006 §13): topic ``atlas.<domain>``; the message key is the
    organization ID when present so per-tenant ordering holds within a
    partition; the correlation ID travels as a header for end-to-end
    tracing (RA-010).
    """

    def __init__(self, transport: MessageTransport, *, source: str) -> None:
        self._transport = transport
        self._source = source

    async def publish(self, envelope: EventEnvelope) -> None:
        topic = topic_for(envelope.event_type)
        headers: dict[str, str] = {"eventType": envelope.event_type}
        if envelope.correlation_id:
            headers["correlationId"] = envelope.correlation_id

        await self._transport.publish(
            topic,
            envelope.to_wire(),
            key=envelope.organization_id,
            headers=headers,
        )
        _logger.info(
            "Event published",
            extra={
                "eventType": envelope.event_type,
                "eventId": envelope.event_id,
                "topic": topic,
                "publisher": self._source,
            },
        )
