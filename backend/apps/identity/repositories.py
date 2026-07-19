"""Identity repositories (RA-001 §9; no business rules here).

Every query on tenant-scoped tables filters by ``organization_id``
explicitly (CON-001 §9-tenancy; the central enforcement library arrives
with IP-003)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import select

from apps.identity.models import (
    AuditLogEntry,
    Membership,
    MembershipStatus,
    Organization,
    RefreshSession,
    Role,
    User,
    VerificationToken,
)
from infrastructure.repositories.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        statement = self._base_statement().where(
            User.email == email.strip().lower()
        )
        return (await self.session.execute(statement)).scalar_one_or_none()


class OrganizationRepository(SqlAlchemyRepository[Organization]):
    model = Organization

    async def get_by_slug(self, slug: str) -> Organization | None:
        statement = self._base_statement().where(Organization.slug == slug)
        return (await self.session.execute(statement)).scalar_one_or_none()


class RoleRepository(SqlAlchemyRepository[Role]):
    model = Role

    async def get_named(self, organization_id: uuid.UUID, name: str) -> Role | None:
        statement = (
            self._base_statement()
            .where(Role.organization_id == organization_id)
            .where(Role.name == name)
        )
        return (await self.session.execute(statement)).scalar_one_or_none()

    async def for_organization(self, organization_id: uuid.UUID) -> Sequence[Role]:
        statement = (
            self._base_statement()
            .where(Role.organization_id == organization_id)
            .order_by(Role.id)
        )
        return (await self.session.execute(statement)).scalars().all()


class MembershipRepository(SqlAlchemyRepository[Membership]):
    model = Membership

    async def get_for_user(
        self, organization_id: uuid.UUID, user_id: uuid.UUID
    ) -> Membership | None:
        statement = (
            self._base_statement()
            .where(Membership.organization_id == organization_id)
            .where(Membership.user_id == user_id)
        )
        return (await self.session.execute(statement)).scalar_one_or_none()

    async def active_for_user(self, user_id: uuid.UUID) -> Sequence[Membership]:
        statement = (
            self._base_statement()
            .where(Membership.user_id == user_id)
            .where(Membership.status == MembershipStatus.ACTIVE.value)
            .order_by(Membership.id)
        )
        return (await self.session.execute(statement)).scalars().all()


class SessionRepository(SqlAlchemyRepository[RefreshSession]):
    model = RefreshSession

    async def get_by_token_hash(self, token_hash: str) -> RefreshSession | None:
        statement = self._base_statement().where(
            RefreshSession.refresh_token_hash == token_hash
        )
        return (await self.session.execute(statement)).scalar_one_or_none()

    async def revoke_family(self, family_id: uuid.UUID) -> int:
        """Revoke every active session in a rotation family (theft response,
        BP-003 §8.7). Returns the number of sessions revoked."""
        statement = (
            self._base_statement()
            .where(RefreshSession.family_id == family_id)
            .where(RefreshSession.revoked_at.is_(None))
        )
        sessions = (await self.session.execute(statement)).scalars().all()
        now = datetime.now(timezone.utc)
        for entry in sessions:
            entry.revoked_at = now
        return len(sessions)


class VerificationTokenRepository(SqlAlchemyRepository[VerificationToken]):
    model = VerificationToken

    async def get_active(
        self, token_hash: str, purpose: str
    ) -> VerificationToken | None:
        now = datetime.now(timezone.utc)
        statement = (
            self._base_statement()
            .where(VerificationToken.token_hash == token_hash)
            .where(VerificationToken.purpose == purpose)
            .where(VerificationToken.consumed_at.is_(None))
            .where(VerificationToken.expires_at > now)
        )
        return (await self.session.execute(statement)).scalar_one_or_none()


class AuditLogRepository(SqlAlchemyRepository[AuditLogEntry]):
    model = AuditLogEntry

    async def recent_for_organization(
        self, organization_id: uuid.UUID, *, limit: int = 50
    ) -> Sequence[AuditLogEntry]:
        statement = (
            select(AuditLogEntry)
            .where(AuditLogEntry.organization_id == organization_id)
            .order_by(AuditLogEntry.occurred_at.desc())
            .limit(limit)
        )
        return (await self.session.execute(statement)).scalars().all()
