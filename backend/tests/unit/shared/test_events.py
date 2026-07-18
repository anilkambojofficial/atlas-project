"""Unit tests — shared.events (RA-006 §8 contract; ES-007 §5)."""

from __future__ import annotations

from typing import Any

import pytest

from shared.events import (
    EventCategory,
    EventEnvelope,
    KafkaEventPublisher,
    MessageTransport,
    topic_for,
    validate_event_type,
)
from shared.events.outbox import OutboxEntry, OutboxStatus
from shared.exceptions import ValidationError
from shared.logging import bind_request_context, clear_request_context


class FakeTransport:
    """In-memory MessageTransport double (ES-007 §5: no network)."""

    def __init__(self) -> None:
        self.published: list[dict[str, Any]] = []

    async def publish(self, topic, value, *, key=None, headers=None) -> None:
        self.published.append(
            {"topic": topic, "value": value, "key": key, "headers": headers}
        )


class TestNaming:
    @pytest.mark.parametrize(
        "name",
        [
            "organization.activated.v1",
            "subscription.plan_changed.v1",
            "tenant.isolation_violation_detected.v1",
            "platform.event_outbox.drained.v12",
        ],
    )
    def test_valid_bp004_names(self, name: str) -> None:
        validate_event_type(name)

    @pytest.mark.parametrize(
        "name",
        ["Organization.Activated.v1", "noversion.event", "org.event.v0", "single", ""],
    )
    def test_invalid_names_rejected(self, name: str) -> None:
        with pytest.raises(ValidationError):
            validate_event_type(name)

    def test_topic_namespacing(self) -> None:
        assert topic_for("organization.activated.v1") == "atlas.organization"


class TestEnvelope:
    def test_create_fills_ra006_contract_fields(self) -> None:
        bind_request_context(correlation_id="corr-123")
        try:
            envelope = EventEnvelope.create(
                event_type="organization.activated.v3",
                category=EventCategory.DOMAIN,
                producer="atlas-backend",
                organization_id="org-1",
                payload={"organizationId": "org-1"},
            )
        finally:
            clear_request_context()

        assert envelope.event_version == 3  # derived from the versioned name
        assert envelope.correlation_id == "corr-123"  # from request context
        assert envelope.payload_schema == "organization.activated.v3"
        wire = envelope.to_wire()
        # All nine RA-006 §8 contract fields present on the wire:
        for field in (
            "eventId", "eventType", "eventVersion", "timestamp",
            "organizationId", "correlationId", "producer",
            "payloadSchema", "metadata",
        ):
            assert field in wire
        assert EventEnvelope.from_wire(wire) == envelope

    def test_domain_and_integration_events_require_tenant(self) -> None:
        for category in (EventCategory.DOMAIN, EventCategory.INTEGRATION):
            with pytest.raises(ValidationError):
                EventEnvelope.create(
                    event_type="organization.activated.v1",
                    category=category,
                    producer="atlas-backend",
                )

    def test_system_events_may_be_platform_scoped(self) -> None:
        envelope = EventEnvelope.create(
            event_type="platform.started.v1",
            category=EventCategory.SYSTEM,
            producer="atlas-backend",
        )
        assert envelope.organization_id is None

    def test_envelope_is_immutable(self) -> None:
        envelope = EventEnvelope.create(
            event_type="platform.started.v1",
            category=EventCategory.SYSTEM,
            producer="atlas-backend",
        )
        with pytest.raises(Exception):
            envelope.event_type = "tampered.event.v1"  # type: ignore[misc]


class TestKafkaEventPublisher:
    async def test_publish_routes_keys_and_headers(self) -> None:
        transport = FakeTransport()
        assert isinstance(transport, MessageTransport)
        publisher = KafkaEventPublisher(transport, source="atlas-backend")

        envelope = EventEnvelope.create(
            event_type="organization.activated.v1",
            category=EventCategory.DOMAIN,
            producer="atlas-backend",
            organization_id="org-42",
            correlation_id="corr-9",
        )
        await publisher.publish(envelope)

        [message] = transport.published
        assert message["topic"] == "atlas.organization"
        assert message["key"] == "org-42"  # per-tenant ordering (RA-006 §13)
        assert message["headers"]["correlationId"] == "corr-9"
        assert message["value"]["eventId"] == envelope.event_id


class TestOutboxContract:
    def test_entry_defaults(self) -> None:
        envelope = EventEnvelope.create(
            event_type="platform.started.v1",
            category=EventCategory.SYSTEM,
            producer="atlas-backend",
        )
        entry = OutboxEntry(envelope=envelope)
        assert entry.status is OutboxStatus.PENDING
        assert entry.attempts == 0
        assert entry.published_at is None and entry.last_error is None
