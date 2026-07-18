"""Shared event contracts and publication (IP-001 §9 — events package).

Implements the RA-006 §8 Event Contract as the platform envelope, the
BP-004 §11 event-naming convention, and the publisher abstraction that
the infrastructure layer's Kafka manager satisfies structurally
(framework-independence rule: shared/* never imports infrastructure).
"""

from shared.events.envelope import EventCategory, EventEnvelope
from shared.events.naming import topic_for, validate_event_type
from shared.events.outbox import OutboxEntry, OutboxStore
from shared.events.publisher import EventPublisher, KafkaEventPublisher, MessageTransport

__all__ = [
    "EventCategory",
    "EventEnvelope",
    "EventPublisher",
    "KafkaEventPublisher",
    "MessageTransport",
    "OutboxEntry",
    "OutboxStore",
    "topic_for",
    "validate_event_type",
]
