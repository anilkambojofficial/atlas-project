"""Identity & Access ORM models.

Governing documents:
- BP-003 §8 — identity lifecycle, credentials, sessions, RBAC surfaces.
- DOMAIN-002 — identity domain authority.
- ES-003 — base mixins (UUID v7 PK, audit + optimistic lock, soft delete);
  ``organization_id`` on tenant-scoped tables.
- CON-001 §6.2 — these tables are owned exclusively by the identity module.

Tenancy layout (recorded as ENG-004 in the Sprint-002 execution log):
``users`` and ``organizations`` are platform-scoped aggregates —
authentication is platform-wide while authorization is tenant-scoped
(BP-003), so the user↔tenant binding lives on ``memberships`` (and on
sessions/roles), which carry ``organization_id`` per ES-003 §9.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import (
    AtlasBase,
    AuditColumnsMixin,
    OrganizationScopedMixin,
    SoftDeleteMixin,
    UUIDPrimaryKeyMixin,
)


class UserStatus(str, Enum):
    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"
    DISABLED = "disabled"


class OrganizationStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class MembershipStatus(str, Enum):
    ACTIVE = "active"
    INVITED = "invited"
    REMOVED = "removed"


class TokenPurpose(str, Enum):
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"


class User(UUIDPrimaryKeyMixin, AuditColumnsMixin, SoftDeleteMixin, AtlasBase):
    """Platform identity (BP-003 §8.3 — human identity class)."""

    __tablename__ = "identity_users"

    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default=UserStatus.PENDING_VERIFICATION.value
    )
    identity_class: Mapped[str] = mapped_column(
        String(20), nullable=False, default="human"
    )
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    failed_login_count: Mapped[int] = mapped_column(nullable=False, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class Organization(UUIDPrimaryKeyMixin, AuditColumnsMixin, SoftDeleteMixin, AtlasBase):
    """Tenant root (identity-scope surface; full lifecycle is IP-003)."""

    __tablename__ = "identity_organizations"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default=OrganizationStatus.ACTIVE.value
    )


class Role(
    UUIDPrimaryKeyMixin, OrganizationScopedMixin, AuditColumnsMixin, AtlasBase
):
    """Org-scoped role with permission strings (BP-003 §8.9 RBAC)."""

    __tablename__ = "identity_roles"
    __table_args__ = (UniqueConstraint("organization_id", "name"),)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    #: Permission strings ``<domain>.<resource>.<action>``; JSONB array.
    permissions: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    is_system: Mapped[bool] = mapped_column(nullable=False, default=False)


class Membership(
    UUIDPrimaryKeyMixin, OrganizationScopedMixin, AuditColumnsMixin, AtlasBase
):
    """User↔organization binding carrying the role (BP-003 §8.6)."""

    __tablename__ = "identity_memberships"
    __table_args__ = (UniqueConstraint("organization_id", "user_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("identity_users.id"),
        nullable=False,
        index=True,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("identity_roles.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default=MembershipStatus.ACTIVE.value
    )


class RefreshSession(UUIDPrimaryKeyMixin, AuditColumnsMixin, AtlasBase):
    """One refresh-token session with rotation lineage (BP-003 §8.7).

    Rotation: each refresh issues a new row in the same ``family_id`` and
    marks the old row replaced; presenting a replaced token is treated as
    theft and revokes the entire family (fail secure, RA-011 §2).
    ``organization_id`` is nullable — a session binds to at most one
    active tenant (CON-001 §9-tenancy), and users without memberships may
    still authenticate to manage their account.
    """

    __tablename__ = "identity_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("identity_users.id"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True), nullable=True, index=True
    )
    family_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True), nullable=False, index=True
    )
    refresh_token_hash: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    replaced_by: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True), nullable=True
    )
    user_agent: Mapped[str | None] = mapped_column(String(400), nullable=True)
    client_ip: Mapped[str | None] = mapped_column(INET, nullable=True)


class VerificationToken(UUIDPrimaryKeyMixin, AuditColumnsMixin, AtlasBase):
    """Email-verification / password-reset token (frameworks; BP-003 §8.8).

    Only the SHA-256 hash is stored; the raw token leaves the platform
    exactly once, through the delivery channel (ES-004 §12).
    """

    __tablename__ = "identity_verification_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("identity_users.id"),
        nullable=False,
        index=True,
    )
    purpose: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    consumed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class AuditLogEntry(UUIDPrimaryKeyMixin, AtlasBase):
    """Immutable identity audit record (BP-003 ED — audit is immutable;
    no update/soft-delete mixins by design: rows are append-only)."""

    __tablename__ = "identity_audit_log"

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True), nullable=True, index=True
    )
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target: Mapped[str | None] = mapped_column(String(200), nullable=True)
    detail: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    correlation_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
