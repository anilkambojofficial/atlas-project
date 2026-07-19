"""ADR-004 enforcement-gate tests over a real ASGI app.

Uses a purpose-built FastAPI app (no database, no container) with the
production enforcement dependency and exception handlers, so the
envelope bytes and status codes are the real ones (ES-002 §17).
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.testclient import TestClient

from api.v1.security import (
    enforce_authentication,
    get_current_principal,
    require_permission,
)
from apps.identity.security import JwtTokenService
from core.errors import install_exception_handlers
from shared.auth import Principal, public_endpoint
from shared.config import Settings
from shared.contracts.api import success_envelope

_SETTINGS = Settings()


def _build_app() -> FastAPI:
    app = FastAPI()
    install_exception_handlers(app)
    app.state.container = type(
        "FakeContainer", (), {"settings": _SETTINGS}
    )()

    router = APIRouter(dependencies=[Depends(enforce_authentication)])

    @router.get("/public")
    @public_endpoint
    def public_route() -> dict[str, Any]:
        return success_envelope(data={"public": True})

    @router.get("/protected")
    def protected_route(
        principal: Principal = Depends(get_current_principal),
    ) -> dict[str, Any]:
        return success_envelope(data={"subject": principal.subject_id})

    @router.get("/admin")
    def admin_route(
        principal: Principal = Depends(
            require_permission("identity.user", "manage")
        ),
    ) -> dict[str, Any]:
        return success_envelope(data={"admin": True})

    app.include_router(router, prefix="/api/v1")
    return app


def _token(permissions: tuple[str, ...] = ()) -> str:
    return JwtTokenService(_SETTINGS).issue_access_token(
        user_id="user-1",
        organization_id="org-1",
        roles=("member",),
        permissions=permissions,
        display_name="T",
        session_id="s-1",
    )


@pytest.fixture()
def client() -> TestClient:
    return TestClient(_build_app())


class TestDenyByDefault:
    def test_public_route_reachable_anonymously(self, client: TestClient) -> None:
        response = client.get("/api/v1/public")
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_protected_route_rejects_anonymous(self, client: TestClient) -> None:
        response = client.get("/api/v1/protected")
        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == "AUTHENTICATION_ERROR"

    def test_protected_route_rejects_garbage_token(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/protected", headers={"Authorization": "Bearer garbage"}
        )
        assert response.status_code == 401

    def test_protected_route_accepts_valid_token(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/protected", headers={"Authorization": f"Bearer {_token()}"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["subject"] == "user-1"


class TestPermissionGate:
    def test_permission_missing_yields_403(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/admin", headers={"Authorization": f"Bearer {_token()}"}
        )
        assert response.status_code == 403
        assert response.json()["error"]["code"] == "AUTHORIZATION_ERROR"

    def test_permission_held_permits(self, client: TestClient) -> None:
        token = _token(("identity.user.manage",))
        response = client.get(
            "/api/v1/admin", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["admin"] is True


class TestModelMapperIntegrity:
    def test_identity_mappers_configure(self) -> None:
        # Catches FK/relationship mistakes without a database.
        import apps.identity.models  # noqa: F401
        from infrastructure.database.base import AtlasBase

        AtlasBase.registry.configure()
        tables = set(AtlasBase.metadata.tables)
        assert {
            "identity_users",
            "identity_organizations",
            "identity_roles",
            "identity_memberships",
            "identity_sessions",
            "identity_verification_tokens",
            "identity_audit_log",
            "platform_event_outbox",
        } <= tables
