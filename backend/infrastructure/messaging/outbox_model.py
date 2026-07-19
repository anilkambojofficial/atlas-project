"""Transactional outbox ORM model.

Governing documents:
- RA-006 §10 — outbox records commit with the business transaction.
- ES-003 — UUID v7 primary key, audit columns, tenant column, JSONB
  payload storage, indexed status for the drain query.
- D-S001-01 — the Alembic migration for this table and the live drain
  worker are delivered with the first live-database stage (S1.6 per the
  approved S1.4 plan); the model is DDL-verified now exactly like the
  S1.2B base mixins.

The model maps the ``shared.events.outbox`` contract onto PostgreSQL;
the store implementation that satisfies ``OutboxStore`` arrives with the
drain worker in the same stage as the migration.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import (
    AtlasBase,
    AuditColumnsMixin,
    UUIDPrimaryKeyMixin,
)
from shared.events.outbox import OutboxStatus


class OutboxRecord(UUIDPrimaryKeyMixin, AuditColumnsMixin, AtlasBase):
    """One platform event awaiting reliable publication (RA-006 §10).

    ``organization_id`` is nullable here (unlike business tables) because
    system/security/audit events may be platform-scoped (RA-006 §4);
    domain and integration events are tenant-stamped by the envelope
    validator before they can reach the outbox (BP-002 §14).
    """

    __tablename__ = "platform_event_outbox"

    event_id: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    event_type: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    organization_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True, index=True
    )
    envelope: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=OutboxStatus.PENDING.value, index=True
    )
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    #: Earliest time the drain worker may retry this entry (ADR-002 §2
    #: capped exponential backoff); NULL means eligible immediately.
    next_attempt_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
