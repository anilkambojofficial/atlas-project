"""Platform event envelope — the RA-006 §8 Event Contract.

Governing documents:
- RA-006 §8 — mandatory contract fields: Event ID, Event Type,
  Event Version, Event Timestamp, Organization ID, Correlation ID,
  Producer, Payload Schema, Metadata.
- RA-006 §4 — event categories (Domain, Integration, System, AI,
  Security, Audit, Notification), mirrored by BP-002 §11.
- RA-006 §6 — domain events are immutable business facts; BP-002 §14 —
  business events always carry the Organization ID.
- BP-004 §11 — versioned event-type naming (``organization.activated.v1``).
- ES-002-consistent camelCase wire keys; IP-001 §15 UUID v7 + UTC.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from shared.events.naming import validate_event_type
from shared.exceptions import ValidationError
from shared.logging.context import get_correlation_id
from shared.utils import uuid7


class EventCategory(str, Enum):
    """RA-006 §4 event classification."""

    DOMAIN = "domain"
    INTEGRATION = "integration"
    SYSTEM = "system"
    AI = "ai"
    SECURITY = "security"
    AUDIT = "audit"
    NOTIFICATION = "notification"


#: Categories that represent business facts and therefore must be
#: tenant-stamped (BP-002 §14; RA-006 §6/§7).
_TENANT_MANDATORY_CATEGORIES = frozenset(
    {EventCategory.DOMAIN, EventCategory.INTEGRATION}
)


class EventEnvelope(BaseModel):
    """Immutable, validated platform event (RA-006 §8)."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    event_id: str = Field(alias="eventId")
    event_type: str = Field(alias="eventType")
    event_version: int = Field(alias="eventVersion", ge=1)
    timestamp: str = Field(alias="timestamp")
    organization_id: str | None = Field(alias="organizationId", default=None)
    correlation_id: str | None = Field(alias="correlationId", default=None)
    producer: str = Field(alias="producer")
    payload_schema: str = Field(alias="payloadSchema")
    payload: dict[str, Any] = Field(alias="payload", default_factory=dict)
    metadata: dict[str, Any] = Field(alias="metadata", default_factory=dict)
    category: EventCategory = Field(alias="category")

    @field_validator("event_type")
    @classmethod
    def _validate_type(cls, value: str) -> str:
        validate_event_type(value)
        return value

    @classmethod
    def create(
        cls,
        *,
        event_type: str,
        category: EventCategory,
        producer: str,
        payload: dict[str, Any] | None = None,
        organization_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> "EventEnvelope":
        """Build a contract-complete envelope.

        - ``event_version`` derives from the versioned event type
          (BP-004 §11 ``<domain>.<event>.v<n>``).
        - ``correlation_id`` defaults to the active request context.
        - Domain/Integration events without an ``organization_id`` are
          rejected (BP-002 §14 tenant-stamping mandate).
        """
        validate_event_type(event_type)
        if category in _TENANT_MANDATORY_CATEGORIES and not organization_id:
            raise ValidationError(
                f"{category.value} events must carry organizationId (BP-002 §14).",
                details=[{"field": "organizationId", "issue": "required"}],
            )
        version = int(event_type.rsplit(".v", 1)[1])
        return cls(
            event_id=str(uuid7()),
            event_type=event_type,
            event_version=version,
            timestamp=datetime.now(timezone.utc).isoformat(),
            organization_id=organization_id,
            correlation_id=correlation_id or get_correlation_id(),
            producer=producer,
            payload_schema=event_type,
            payload=payload or {},
            metadata=metadata or {},
            category=category,
        )

    def to_wire(self) -> dict[str, Any]:
        """Serialize to the camelCase wire representation."""
        return self.model_dump(by_alias=True, mode="json")

    @classmethod
    def from_wire(cls, data: dict[str, Any]) -> "EventEnvelope":
        """Parse and validate a wire representation."""
        return cls.model_validate(data)
