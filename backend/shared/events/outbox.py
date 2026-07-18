"""Transactional outbox contract (interface layer).

Governing documents:
- RA-006 §10 — reliable publication uses the Outbox Pattern: the event
  record commits in the same transaction as the business state change
  and is drained to the Event Bus afterwards.
- D-S001-01 (Sprint-001 Execution Log) — live-infrastructure behavior is
  verified from Stage S1.6; per the approved S1.4 plan, this stage
  defines the contract (entry shape + store protocol) and the ORM model
  lives in the infrastructure layer. The drain worker and migration
  follow with the first live-database stage.

Framework-free by rule: the ORM binding is
``infrastructure.messaging.outbox_model.OutboxRecord``, which maps this
entry shape onto the ES-003 base mixins; shared/* holds only the
abstractions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Protocol, Sequence, runtime_checkable

from shared.events.envelope import EventEnvelope


class OutboxStatus(str, Enum):
    """Lifecycle of one outbox record (RA-006 §10/§15)."""

    PENDING = "pending"
    PUBLISHED = "published"
    FAILED = "failed"


@dataclass
class OutboxEntry:
    """One event awaiting reliable publication."""

    envelope: EventEnvelope
    status: OutboxStatus = OutboxStatus.PENDING
    attempts: int = 0
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    published_at: datetime | None = None
    last_error: str | None = None


@runtime_checkable
class OutboxStore(Protocol):
    """Persistence contract the infrastructure outbox implements."""

    async def add(self, entry: OutboxEntry) -> None:  # pragma: no cover
        """Persist an entry inside the caller's open transaction."""
        ...

    async def pending(self, *, limit: int) -> Sequence[OutboxEntry]:  # pragma: no cover
        """Fetch entries awaiting publication, oldest first."""
        ...

    async def mark_published(self, entry: OutboxEntry) -> None:  # pragma: no cover
        """Record successful publication."""
        ...

    async def mark_failed(self, entry: OutboxEntry, error: str) -> None:  # pragma: no cover
        """Record a failed attempt (DLQ escalation per RA-006 §15)."""
        ...
