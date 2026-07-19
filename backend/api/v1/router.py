"""Version 1 API router.

Governing documents:
- ES-002 §16 — every public API is versioned under ``/api/v1/``;
  breaking changes require a new major version.
- ES-002 §7 — responses use the uniform success envelope.
- IP-002 through IP-010 — each platform service mounts its API group
  on this router in its governing Implementation Pack stage
  (e.g. ``/api/v1/identity`` in IP-002).

At the Platform Foundation stage the router carries the API descriptor
resource, which lets clients and gateway probes discover the active API
version and documentation location. Service routers are attached here in
later sprints without modifying the application factory.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.v1.security import enforce_authentication
from apps.identity.api import router as identity_router
from core.container import get_settings
from shared.auth import public_endpoint
from shared.config import Settings
from shared.contracts.api import success_envelope

# ADR-004 §3: deny-by-default — every v1 route passes the enforcement
# gate; anonymous reachability requires the explicit public marker.
router = APIRouter(tags=["api-v1"], dependencies=[Depends(enforce_authentication)])

router.include_router(identity_router)


@router.get("", summary="API v1 descriptor")
@public_endpoint
def api_descriptor(settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    """Describe the v1 API surface (ES-002 §7 envelope)."""
    return success_envelope(
        data={
            "name": settings.app_name,
            "service": settings.service_name,
            "apiVersion": "v1",
            "environment": settings.environment,
            "documentation": "/docs",
            "openapi": "/openapi.json",
        }
    )
