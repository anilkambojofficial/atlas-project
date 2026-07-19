"""PDP tests (BP-003 §8.9 — deny by default; ED-004 cross-tenant deny)."""

from __future__ import annotations

import pytest

from apps.identity.services import AuthorizationService
from shared.auth import IdentityClass, Principal

ORG_A = "0198f5a0-0000-7000-8000-0000000000aa"
ORG_B = "0198f5a0-0000-7000-8000-0000000000bb"


def _principal(permissions: tuple[str, ...] = (), organization_id: str | None = ORG_A) -> Principal:
    return Principal(
        subject_id="user-1",
        identity_class=IdentityClass.HUMAN,
        organization_id=organization_id,
        roles=("member",),
        permissions=permissions,
    )


class TestPolicyDecisionPoint:
    @pytest.mark.asyncio
    async def test_permit_when_permission_held(self) -> None:
        decision = await AuthorizationService().authorize(
            _principal(("identity.user.read",)),
            resource="identity.user",
            action="read",
            organization_id=ORG_A,
        )
        assert decision.permit

    @pytest.mark.asyncio
    async def test_deny_by_default(self) -> None:
        decision = await AuthorizationService().authorize(
            _principal(()), resource="identity.user", action="read"
        )
        assert not decision.permit
        assert "deny by default" in decision.reason

    @pytest.mark.asyncio
    async def test_cross_tenant_denied_even_with_permission(self) -> None:
        decision = await AuthorizationService().authorize(
            _principal(("identity.user.read",), organization_id=ORG_A),
            resource="identity.user",
            action="read",
            organization_id=ORG_B,
        )
        assert not decision.permit
        assert "cross-tenant" in decision.reason
