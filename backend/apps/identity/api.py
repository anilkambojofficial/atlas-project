"""Identity API group — mounted at ``/api/v1/identity`` (ES-002 §16).

Thin controllers (CON-001 §17.4): validation via DTOs, use cases via
services, envelopes via ``shared.contracts``. The refresh token travels
only as an httpOnly cookie (AUD-001 M-5 closed; BP-003 session design).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Request, Response, status

from api.v1.security import get_current_principal
from apps.identity.models import Membership, User
from apps.identity.schemas import (
    EmailVerifyRequest,
    LoginRequest,
    MembershipView,
    PasswordResetConfirm,
    PasswordResetRequest,
    ProfileUpdateRequest,
    RegisterRequest,
    TokenView,
    UserView,
)
from apps.identity.services import (
    AuthenticationService,
    IssuedTokens,
    PasswordService,
    RegistrationService,
    UserService,
    VerificationService,
)
from core.container import get_settings, get_unit_of_work
from infrastructure.database.unit_of_work import UnitOfWork
from shared.auth import Principal, public_endpoint
from shared.config import Settings
from shared.contracts.api import success_envelope

router = APIRouter(prefix="/identity", tags=["identity"])

_REFRESH_COOKIE_PATH = "/api/v1/identity/auth"


def _user_view(user: User, memberships: list[Membership] | None = None) -> UserView:
    return UserView(
        id=str(user.id),
        email=user.email,
        display_name=user.display_name,
        status=user.status,
        email_verified=user.email_verified_at is not None,
        created_at=user.created_at,
        last_login_at=user.last_login_at,
        memberships=[
            MembershipView(
                organization_id=str(m.organization_id),
                role_id=str(m.role_id),
                status=m.status,
            )
            for m in (memberships or [])
        ],
    )


def _set_refresh_cookie(
    response: Response, settings: Settings, tokens: IssuedTokens
) -> None:
    response.set_cookie(
        key=settings.auth_refresh_cookie_name,
        value=tokens.refresh_token,
        max_age=settings.auth_refresh_token_ttl_seconds,
        path=_REFRESH_COOKIE_PATH,
        httponly=True,
        secure=settings.environment != "development",
        samesite="lax",
    )


def _clear_refresh_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        key=settings.auth_refresh_cookie_name, path=_REFRESH_COOKIE_PATH
    )


def _token_payload(tokens: IssuedTokens, settings: Settings) -> dict[str, Any]:
    return TokenView(
        access_token=tokens.access_token,
        expires_in=settings.auth_access_token_ttl_seconds,
        organization_id=str(tokens.organization_id)
        if tokens.organization_id
        else None,
        roles=list(tokens.roles),
        permissions=list(tokens.permissions),
        user=_user_view(tokens.user),
    ).wire()


# --- Authentication (public surface, ADR-004 §3 catalogued opt-outs) -----


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
@public_endpoint
async def register(
    body: RegisterRequest,
    settings: Settings = Depends(get_settings),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    async with uow:
        user, _verification_token = await RegistrationService(
            uow, settings
        ).register(
            email=body.email,
            password=body.password,
            display_name=body.display_name,
            organization_name=body.organization_name,
            organization_slug=body.organization_slug,
        )
        payload = _user_view(user).wire()
    return success_envelope(data=payload)


@router.post("/auth/login")
@public_endpoint
async def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    settings: Settings = Depends(get_settings),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    async with uow:
        tokens = await AuthenticationService(uow, settings).login(
            email=body.email,
            password=body.password,
            user_agent=request.headers.get("User-Agent"),
            client_ip=request.client.host if request.client else None,
        )
        payload = _token_payload(tokens, settings)
    _set_refresh_cookie(response, settings, tokens)
    return success_envelope(data=payload)


@router.post("/auth/refresh")
@public_endpoint
async def refresh(
    request: Request,
    response: Response,
    settings: Settings = Depends(get_settings),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    from shared.exceptions import AuthenticationError

    raw = request.cookies.get(settings.auth_refresh_cookie_name)
    if not raw:
        raise AuthenticationError("No session.")
    async with uow:
        tokens = await AuthenticationService(uow, settings).refresh(raw)
        payload = _token_payload(tokens, settings)
    _set_refresh_cookie(response, settings, tokens)
    return success_envelope(data=payload)


@router.post("/auth/logout")
@public_endpoint
async def logout(
    request: Request,
    response: Response,
    settings: Settings = Depends(get_settings),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    raw = request.cookies.get(settings.auth_refresh_cookie_name)
    if raw:
        async with uow:
            await AuthenticationService(uow, settings).logout(raw)
    _clear_refresh_cookie(response, settings)
    return success_envelope(data={"loggedOut": True})


@router.post("/auth/password-reset/request")
@public_endpoint
async def password_reset_request(
    body: PasswordResetRequest,
    settings: Settings = Depends(get_settings),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    async with uow:
        await PasswordService(uow, settings).request_reset(body.email)
    # Uniform response regardless of account existence (no enumeration).
    return success_envelope(data={"accepted": True})


@router.post("/auth/password-reset/confirm")
@public_endpoint
async def password_reset_confirm(
    body: PasswordResetConfirm,
    settings: Settings = Depends(get_settings),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    async with uow:
        await PasswordService(uow, settings).confirm_reset(
            body.token, body.new_password
        )
    return success_envelope(data={"reset": True})


@router.post("/auth/verify-email")
@public_endpoint
async def verify_email(
    body: EmailVerifyRequest,
    settings: Settings = Depends(get_settings),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    async with uow:
        user = await VerificationService(uow, settings).confirm_email(body.token)
        payload = _user_view(user).wire()
    return success_envelope(data=payload)


# --- Current user (protected by the ADR-004 mount gate) ------------------


@router.get("/users/me")
async def get_me(
    principal: Principal = Depends(get_current_principal),
    settings: Settings = Depends(get_settings),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    async with uow:
        user, memberships = await UserService(uow, settings).get_me(principal)
        payload = _user_view(user, memberships).wire()
    return success_envelope(
        data={
            **payload,
            "roles": list(principal.roles),
            "permissions": list(principal.permissions),
            "organizationId": principal.organization_id,
        }
    )


@router.patch("/users/me")
async def update_me(
    body: ProfileUpdateRequest,
    principal: Principal = Depends(get_current_principal),
    settings: Settings = Depends(get_settings),
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    async with uow:
        user = await UserService(uow, settings).update_profile(
            principal, display_name=body.display_name
        )
        payload = _user_view(user).wire()
    return success_envelope(data=payload)
