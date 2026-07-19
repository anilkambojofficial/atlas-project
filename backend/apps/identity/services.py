"""Identity application services (RA-001 application layer).

One public service method = one use case = one Unit of Work transaction
(CON-001 §5); domain events reach the Event Bus through the ADR-002
outbox by collection on the Unit of Work. Authorization decisions flow
through the PDP (BP-003 ED-002); services never inline permission logic
for other modules.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from apps.identity import security
from apps.identity.domain import (
    SYSTEM_ROLES,
    validate_organization_slug,
    validate_password_policy,
)
from apps.identity.models import (
    AuditLogEntry,
    Membership,
    Organization,
    RefreshSession,
    Role,
    TokenPurpose,
    User,
    UserStatus,
    VerificationToken,
)
from apps.identity.repositories import (
    MembershipRepository,
    OrganizationRepository,
    RoleRepository,
    SessionRepository,
    UserRepository,
    VerificationTokenRepository,
)
from infrastructure.database.unit_of_work import UnitOfWork
from shared.auth import AccessDecision, Principal
from shared.config import Settings
from shared.events import EventCategory, EventEnvelope
from shared.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BusinessError,
    NotFoundError,
)
from shared.logging import get_logger
from shared.logging.context import get_correlation_id
from shared.utils import uuid7

_logger = get_logger("atlas.identity.services")

_VERIFICATION_TTL = timedelta(hours=48)
_RESET_TTL = timedelta(hours=2)


@dataclass(frozen=True)
class IssuedTokens:
    """Result of a successful authentication or rotation."""

    access_token: str
    refresh_token: str
    refresh_expires_at: datetime
    user: User
    organization_id: uuid.UUID | None
    roles: tuple[str, ...]
    permissions: tuple[str, ...]


def _now() -> datetime:
    return datetime.now(timezone.utc)


class _IdentityServiceBase:
    def __init__(self, uow: UnitOfWork, settings: Settings) -> None:
        self._uow = uow
        self._settings = settings
        self.users = UserRepository(uow.session)
        self.organizations = OrganizationRepository(uow.session)
        self.roles = RoleRepository(uow.session)
        self.memberships = MembershipRepository(uow.session)
        self.sessions = SessionRepository(uow.session)
        self.tokens = VerificationTokenRepository(uow.session)

    def _audit(
        self,
        action: str,
        *,
        organization_id: uuid.UUID | None = None,
        actor_user_id: uuid.UUID | None = None,
        target: str | None = None,
        detail: dict | None = None,
    ) -> None:
        """Immutable audit row in the same transaction (BP-003: audit
        drop = incident — the row commits atomically with the change)."""
        self._uow.session.add(
            AuditLogEntry(
                occurred_at=_now(),
                organization_id=organization_id,
                actor_user_id=actor_user_id,
                action=action,
                target=target,
                detail=detail or {},
                correlation_id=get_correlation_id(),
            )
        )

    def _emit(
        self,
        event_type: str,
        category: EventCategory,
        *,
        organization_id: uuid.UUID | None = None,
        payload: dict | None = None,
    ) -> None:
        self._uow.collect_event(
            EventEnvelope.create(
                event_type=event_type,
                category=category,
                producer=self._settings.service_name,
                organization_id=str(organization_id) if organization_id else None,
                payload=payload or {},
            )
        )

    async def _permissions_for(
        self, user_id: uuid.UUID
    ) -> tuple[uuid.UUID | None, tuple[str, ...], tuple[str, ...]]:
        """Resolve the session tenant context: the user's first active
        membership (session binds to one active tenant, CON-001)."""
        memberships = await self.memberships.active_for_user(user_id)
        if not memberships:
            return None, (), ()
        membership = memberships[0]
        role = await self.roles.get_by_id(membership.role_id)
        if role is None:
            return membership.organization_id, (), ()
        return (
            membership.organization_id,
            (role.name,),
            tuple(role.permissions),
        )


class RegistrationService(_IdentityServiceBase):
    async def register(
        self,
        *,
        email: str,
        password: str,
        display_name: str,
        organization_name: str | None = None,
        organization_slug: str | None = None,
    ) -> tuple[User, str]:
        """Create a user (and optionally their first organization).

        Returns the user and the raw email-verification token for the
        delivery framework (delivery itself is feature-flagged; the token
        is never persisted raw — ES-004 §12).
        """
        normalized = email.strip().lower()
        validate_password_policy(
            password, min_length=self._settings.auth_password_min_length
        )
        if await self.users.get_by_email(normalized) is not None:
            raise BusinessError(
                "An account with this email already exists.",
                details=[{"field": "email", "issue": "already registered"}],
            )

        user = User(
            email=normalized,
            password_hash=security.hash_password(password),
            display_name=display_name.strip(),
        )
        self.users.add(user)
        await self.users.flush()

        organization: Organization | None = None
        if organization_name and organization_slug:
            organization = await self._create_organization_for(
                user, organization_name, organization_slug
            )

        raw_token = security.new_opaque_token()
        self.tokens.add(
            VerificationToken(
                user_id=user.id,
                purpose=TokenPurpose.EMAIL_VERIFICATION.value,
                token_hash=security.token_digest(raw_token),
                expires_at=_now() + _VERIFICATION_TTL,
            )
        )
        self._audit(
            "identity.user.registered",
            actor_user_id=user.id,
            organization_id=organization.id if organization else None,
            target=f"user:{user.id}",
        )
        self._emit(
            "identity.user.registered.v1",
            EventCategory.AUDIT,
            organization_id=organization.id if organization else None,
            payload={"userId": str(user.id), "email": user.email},
        )
        if not self._settings.feature_enabled("identity_email_delivery"):
            _logger.info(
                "Email delivery disabled; verification token issued silently",
                extra={"userId": str(user.id)},
            )
        return user, raw_token

    async def _create_organization_for(
        self, owner: User, name: str, slug: str
    ) -> Organization:
        validate_organization_slug(slug)
        if await self.organizations.get_by_slug(slug) is not None:
            raise BusinessError(
                "Organization slug is already taken.",
                details=[{"field": "organizationSlug", "issue": "already taken"}],
            )
        organization = Organization(name=name.strip(), slug=slug)
        self.organizations.add(organization)
        await self.organizations.flush()

        owner_role: Role | None = None
        for role_name, permissions in SYSTEM_ROLES.items():
            role = Role(
                organization_id=organization.id,
                name=role_name,
                permissions=list(permissions),
                is_system=True,
            )
            self.roles.add(role)
            if role_name == "owner":
                owner_role = role
        await self.roles.flush()
        assert owner_role is not None  # SYSTEM_ROLES always contains "owner"

        self.memberships.add(
            Membership(
                organization_id=organization.id,
                user_id=owner.id,
                role_id=owner_role.id,
            )
        )
        self._emit(
            "organization.created.v1",
            EventCategory.DOMAIN,
            organization_id=organization.id,
            payload={"name": organization.name, "slug": organization.slug},
        )
        return organization


class AuthenticationService(_IdentityServiceBase):
    async def login(
        self,
        *,
        email: str,
        password: str,
        user_agent: str | None = None,
        client_ip: str | None = None,
    ) -> IssuedTokens:
        user = await self.users.get_by_email(email)
        generic = AuthenticationError("Invalid email or password.")
        if user is None:
            # Same failure shape as a bad password: no account enumeration.
            security.verify_password(password, security.hash_password("timing-pad"))
            raise generic

        if user.locked_until is not None and user.locked_until > _now():
            self._audit(
                "identity.login.rejected_locked", actor_user_id=user.id
            )
            raise AuthenticationError(
                "Account temporarily locked. Try again later."
            )
        if user.status == UserStatus.DISABLED.value:
            raise generic

        if not security.verify_password(password, user.password_hash):
            user.failed_login_count += 1
            if user.failed_login_count >= self._settings.auth_max_failed_logins:
                user.locked_until = _now() + timedelta(
                    seconds=self._settings.auth_lockout_seconds
                )
                user.failed_login_count = 0
                self._audit("identity.user.locked", actor_user_id=user.id)
                self._emit(
                    "identity.user.locked.v1",
                    EventCategory.SECURITY,
                    payload={"userId": str(user.id)},
                )
            raise generic

        if security.password_needs_rehash(user.password_hash):
            user.password_hash = security.hash_password(password)
        user.failed_login_count = 0
        user.locked_until = None
        user.last_login_at = _now()

        tokens = await self._issue_session(
            user, family_id=uuid7(), user_agent=user_agent, client_ip=client_ip
        )
        self._audit(
            "identity.login.succeeded",
            actor_user_id=user.id,
            organization_id=tokens.organization_id,
        )
        self._emit(
            "identity.user.logged_in.v1",
            EventCategory.SECURITY,
            payload={"userId": str(user.id)},
        )
        return tokens

    async def refresh(self, raw_refresh_token: str) -> IssuedTokens:
        """Rotate a refresh session (BP-003 §8.7); replaced-token reuse
        revokes the whole family (fail secure, RA-011 §2)."""
        session = await self.sessions.get_by_token_hash(
            security.token_digest(raw_refresh_token)
        )
        invalid = AuthenticationError("Invalid or expired session.")
        if session is None:
            raise invalid
        if session.replaced_by is not None:
            revoked = await self.sessions.revoke_family(session.family_id)
            self._audit(
                "identity.session.reuse_detected",
                actor_user_id=session.user_id,
                detail={"revokedSessions": revoked},
            )
            self._emit(
                "identity.session.reuse_detected.v1",
                EventCategory.SECURITY,
                payload={"userId": str(session.user_id)},
            )
            raise invalid
        if session.revoked_at is not None or session.expires_at <= _now():
            raise invalid

        user = await self.users.get_by_id(session.user_id)
        if user is None or user.status == UserStatus.DISABLED.value:
            raise invalid

        tokens = await self._issue_session(
            user,
            family_id=session.family_id,
            user_agent=session.user_agent,
            client_ip=str(session.client_ip) if session.client_ip else None,
        )
        new_hash = security.token_digest(tokens.refresh_token)
        replacement = await self.sessions.get_by_token_hash(new_hash)
        assert replacement is not None
        session.replaced_by = replacement.id
        session.revoked_at = _now()
        return tokens

    async def logout(self, raw_refresh_token: str) -> None:
        """Revoke the presented session's whole family; idempotent."""
        session = await self.sessions.get_by_token_hash(
            security.token_digest(raw_refresh_token)
        )
        if session is None:
            return
        await self.sessions.revoke_family(session.family_id)
        self._audit("identity.logout", actor_user_id=session.user_id)
        self._emit(
            "identity.session.revoked.v1",
            EventCategory.SECURITY,
            payload={"userId": str(session.user_id)},
        )

    async def _issue_session(
        self,
        user: User,
        *,
        family_id: uuid.UUID,
        user_agent: str | None,
        client_ip: str | None,
    ) -> IssuedTokens:
        organization_id, roles, permissions = await self._permissions_for(user.id)
        raw_refresh = security.new_opaque_token()
        expires_at = _now() + timedelta(
            seconds=self._settings.auth_refresh_token_ttl_seconds
        )
        self.sessions.add(
            RefreshSession(
                user_id=user.id,
                organization_id=organization_id,
                family_id=family_id,
                refresh_token_hash=security.token_digest(raw_refresh),
                expires_at=expires_at,
                user_agent=(user_agent or "")[:400] or None,
                client_ip=client_ip,
            )
        )
        await self.sessions.flush()
        token_service = security.JwtTokenService(self._settings)
        session_row = await self.sessions.get_by_token_hash(
            security.token_digest(raw_refresh)
        )
        assert session_row is not None
        access = token_service.issue_access_token(
            user_id=str(user.id),
            organization_id=str(organization_id) if organization_id else None,
            roles=roles,
            permissions=permissions,
            display_name=user.display_name,
            session_id=str(session_row.id),
        )
        return IssuedTokens(
            access_token=access,
            refresh_token=raw_refresh,
            refresh_expires_at=expires_at,
            user=user,
            organization_id=organization_id,
            roles=roles,
            permissions=permissions,
        )


class UserService(_IdentityServiceBase):
    async def get_me(self, principal: Principal) -> tuple[User, list[Membership]]:
        user = await self.users.get_by_id(uuid.UUID(principal.subject_id))
        if user is None:
            raise NotFoundError("User not found.")
        memberships = list(await self.memberships.active_for_user(user.id))
        return user, memberships

    async def update_profile(
        self, principal: Principal, *, display_name: str
    ) -> User:
        user = await self.users.get_by_id(uuid.UUID(principal.subject_id))
        if user is None:
            raise NotFoundError("User not found.")
        user.display_name = display_name.strip()
        user.updated_by = user.id
        self._audit("identity.user.profile_updated", actor_user_id=user.id)
        return user


class PasswordService(_IdentityServiceBase):
    async def request_reset(self, email: str) -> str | None:
        """Issue a reset token. Always succeeds outwardly (no account
        enumeration); returns the raw token when a user exists so the
        delivery framework can send it."""
        user = await self.users.get_by_email(email)
        if user is None:
            return None
        raw_token = security.new_opaque_token()
        self.tokens.add(
            VerificationToken(
                user_id=user.id,
                purpose=TokenPurpose.PASSWORD_RESET.value,
                token_hash=security.token_digest(raw_token),
                expires_at=_now() + _RESET_TTL,
            )
        )
        self._audit("identity.password.reset_requested", actor_user_id=user.id)
        return raw_token

    async def confirm_reset(self, raw_token: str, new_password: str) -> None:
        record = await self.tokens.get_active(
            security.token_digest(raw_token), TokenPurpose.PASSWORD_RESET.value
        )
        if record is None:
            raise AuthenticationError("Invalid or expired reset token.")
        validate_password_policy(
            new_password, min_length=self._settings.auth_password_min_length
        )
        user = await self.users.get_by_id(record.user_id)
        if user is None:
            raise AuthenticationError("Invalid or expired reset token.")
        user.password_hash = security.hash_password(new_password)
        record.consumed_at = _now()
        # All sessions die with the credential (fail secure).
        for membership_session in await self._all_user_sessions(user.id):
            if membership_session.revoked_at is None:
                membership_session.revoked_at = _now()
        self._audit("identity.password.reset_completed", actor_user_id=user.id)
        self._emit(
            "identity.password.reset_completed.v1",
            EventCategory.SECURITY,
            payload={"userId": str(user.id)},
        )

    async def _all_user_sessions(self, user_id: uuid.UUID) -> list[RefreshSession]:
        from sqlalchemy import select

        statement = select(RefreshSession).where(RefreshSession.user_id == user_id)
        return list((await self._uow.session.execute(statement)).scalars().all())


class VerificationService(_IdentityServiceBase):
    async def confirm_email(self, raw_token: str) -> User:
        record = await self.tokens.get_active(
            security.token_digest(raw_token),
            TokenPurpose.EMAIL_VERIFICATION.value,
        )
        if record is None:
            raise AuthenticationError("Invalid or expired verification token.")
        user = await self.users.get_by_id(record.user_id)
        if user is None:
            raise AuthenticationError("Invalid or expired verification token.")
        record.consumed_at = _now()
        user.email_verified_at = _now()
        if user.status == UserStatus.PENDING_VERIFICATION.value:
            user.status = UserStatus.ACTIVE.value
        self._audit("identity.email.verified", actor_user_id=user.id)
        return user


class AuthorizationService:
    """Policy Decision Point (BP-003 §8.9) — structurally satisfies
    ``shared.auth.PolicyDecisionPoint``. Deny by default; tenant-mismatch
    denies regardless of permission (fail closed, BP-003 ED-004/005)."""

    async def authorize(
        self,
        principal: Principal,
        *,
        resource: str,
        action: str,
        organization_id: str | None = None,
    ) -> AccessDecision:
        required = f"{resource}.{action}"
        if organization_id is not None and principal.organization_id != organization_id:
            return AccessDecision(
                permit=False, reason="cross-tenant access denied (BP-004 ED-004)"
            )
        if required in principal.permissions:
            return AccessDecision(permit=True, reason=f"permission '{required}' held")
        return AccessDecision(
            permit=False, reason=f"permission '{required}' not held (deny by default)"
        )


def require_permit(decision: AccessDecision) -> None:
    """Raise the platform authorization error unless permitted."""
    if not decision.permit:
        raise AuthorizationError(decision.reason)
