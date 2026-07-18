"""Operational endpoints: health, readiness, liveness, metrics.

Governing documents:
- IP-001 §14 — mandatory endpoints ``/health``, ``/ready``, ``/live``,
  ``/metrics``; responses support automated orchestration.
- RA-001 §21 — liveness/readiness/startup categories with dependency
  checks.
- RA-010 — metrics feed the enterprise observability platform.

These endpoints are orchestration probes, not business APIs: they are
served at the application root (outside ``/api/v1``) in the plain JSON /
Prometheus text formats that Kubernetes probes and metric scrapers
consume (IP-001 §17 requires Kubernetes-ready services). The ES-002
response envelope governs the versioned business APIs under ``/api/v1``.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse, PlainTextResponse

from core.container import ApplicationContainer, get_container

router = APIRouter(tags=["operations"])

_STATUS_HEALTHY = "healthy"
_STATUS_UNHEALTHY = "unhealthy"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


async def _evaluate(container: ApplicationContainer) -> tuple[bool, dict[str, Any]]:
    """Run all registered checks and build the health report body."""
    results = await container.health.run_all()
    all_healthy = all(result.healthy for result in results)
    body = {
        "status": _STATUS_HEALTHY if all_healthy else _STATUS_UNHEALTHY,
        "service": container.settings.service_name,
        "version": container.settings.version,
        "environment": container.settings.environment,
        "uptimeSeconds": round(container.metrics.uptime_seconds, 3),
        "timestamp": _timestamp(),
        "checks": {
            result.name: {
                "status": _STATUS_HEALTHY if result.healthy else _STATUS_UNHEALTHY,
                "detail": result.detail,
            }
            for result in results
        },
    }
    return all_healthy, body


@router.get("/health", summary="Overall service health (IP-001 §14)")
async def health(
    container: ApplicationContainer = Depends(get_container),
) -> JSONResponse:
    """Full health report across every registered dependency check."""
    healthy, body = await _evaluate(container)
    return JSONResponse(status_code=200 if healthy else 503, content=body)


@router.get("/ready", summary="Readiness probe (IP-001 §14)")
async def ready(
    container: ApplicationContainer = Depends(get_container),
) -> JSONResponse:
    """Readiness: the service may receive traffic only if all checks pass."""
    healthy, body = await _evaluate(container)
    return JSONResponse(status_code=200 if healthy else 503, content=body)


@router.get("/live", summary="Liveness probe (IP-001 §14)")
def live() -> dict[str, str]:
    """Liveness: the process is running and able to serve this response.

    Liveness deliberately checks nothing beyond process responsiveness
    (RA-001 §21) so a failing dependency triggers no restart loop.
    """
    return {"status": "alive", "timestamp": _timestamp()}


@router.get("/metrics", summary="Operational metrics (IP-001 §14)")
def metrics(container: ApplicationContainer = Depends(get_container)) -> Response:
    """Metrics in Prometheus text exposition format (RA-010)."""
    return PlainTextResponse(
        content=container.metrics.render(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
