"""SQLAlchemy declarative base and mandatory column mixins.

Governing documents:
- ES-003 §4 — snake_case naming; consistent constraint naming.
- ES-003 §5 — UUID primary keys, immutable, no business meaning
  (UUID v7 per IP-001 §15).
- ES-003 §9 — every business table carries ``organization_id``
  (tenant isolation, ARCH-002 §11).
- ES-003 §13 — optimistic locking via version columns.
- ES-003 §14 — mandatory audit fields (created/updated/deleted at/by,
  version).
- ES-003 §15 — soft delete by default (``deleted_at/by``,
  ``delete_reason``); hard delete requires architectural approval.

These are platform base classes only. Business models are defined by
their owning services in later Implementation Packs (IP-002 onward) and
compose these mixins; no business model exists at this stage.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, MetaData, String, func
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from shared.utils import uuid7

#: Deterministic constraint naming so Alembic autogenerate produces
#: stable, reviewable migrations (ES-003 §4, §16).
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class AtlasBase(DeclarativeBase):
    """Declarative base for every Project ATLAS ORM model."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class UUIDPrimaryKeyMixin:
    """UUID v7 primary key (ES-003 §5; IP-001 §15)."""

    id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid7
    )


class OrganizationScopedMixin:
    """Tenant column mandated for every business table (ES-003 §9).

    Query-level tenant filtering is enforced by the Tenant Isolation
    Enforcement Library delivered with BP-004/IP-003; the column contract
    exists from the foundation so no schema migration is needed then.
    """

    organization_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), nullable=False, index=True
    )


class AuditColumnsMixin:
    """Mandatory audit fields (ES-003 §14) with optimistic-locking version
    column (ES-003 §13).

    ``created_by``/``updated_by`` are nullable until the Identity Platform
    (IP-002) binds actor identities to requests; system-initiated writes
    remain legal afterwards.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True), nullable=True
    )
    version: Mapped[int] = mapped_column(nullable=False, default=1)

    @declared_attr.directive
    def __mapper_args__(cls) -> dict[str, object]:
        """Enable SQLAlchemy optimistic concurrency on the version column."""
        return {"version_id_col": cls.version}


class SoftDeleteMixin:
    """Soft-delete fields (ES-003 §15); records are never physically removed
    by platform code — hard deletes require explicit architectural approval.
    """

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_by: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True), nullable=True
    )
    delete_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)

    @property
    def is_deleted(self) -> bool:
        """True when the record has been soft-deleted."""
        return self.deleted_at is not None
