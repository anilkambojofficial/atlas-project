"""Platform authentication/authorization enforcement (ADR-004).

Deny by default at the ``/api/v1`` mount: every route requires a verified
``Principal`` unless its handler carries the explicit
``shared.auth.public_endpoint`` marker (ADR-004 §3). Verification and
policy failures reject — fail closed (BP-003 ED-005).

Layering: this is presentation-layer wiring (api → apps/shared is the
sanctioned mount pattern, CON-001 §6.5); ``core`` never imports ``apps``.
"""

from __future__ import annotations

from fastapi import Depends, Request

from apps.identity.security import JwtTokenService
from apps.identity.services import AuthorizationService
from core.container import get_settings
from shared.auth import Principal
from shared.config import Settings
from shared.exceptions import AuthenticationError, AuthorizationError

_pdp = AuthorizationService()


def _bearer_token(request: Request) -> str | None:
    header = request.headers.get("Authorization")
    if not header or not header.startswith("Bearer "):
        return None
    return header[len("Bearer ") :].strip() or None


async def enforce_authentication(
    request: Request, settings: Settings = Depends(get_settings)
) -> None:
    """Router-level gate applied to every ``/api/v1`` route (ADR-004 §3)."""
    route = request.scope.get("route")
    endpoint = getattr(route, "endpoint", None)
    if endpoint is not None and getattr(endpoint, "__atlas_public__", False):
        return
    token = _bearer_token(request)
    if token is None:
        raise AuthenticationError("Authentication required.")
    request.state.principal = await JwtTokenService(settings).verify(token)


async def get_current_principal(
    request: Request, settings: Settings = Depends(get_settings)
) -> Principal:
    """Resolve the verified principal for a protected handler."""
    principal = getattr(request.state, "principal", None)
    if principal is None:
        token = _bearer_token(request)
        if token is None:
            raise AuthenticationError("Authentication required.")
        principal = await JwtTokenService(settings).verify(token)
        request.state.principal = principal
    return principal


def require_permission(resource: str, action: str):
    """Dependency factory: PDP-backed permission gate (BP-003 ED-002 —
    services never inline permission logic; routes declare requirements)."""

    async def _dependency(
        principal: Principal = Depends(get_current_principal),
    ) -> Principal:
        decision = await _pdp.authorize(
            principal,
            resource=resource,
            action=action,
            organization_id=principal.organization_id,
        )
        if not decision.permit:
            raise AuthorizationError(decision.reason)
        return principal

    return _dependency
