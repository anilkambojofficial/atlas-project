"""Application factory.

Governing documents:
- IP-001 §7 — FastAPI application composed through a factory with
  modular architecture.
- IP-001 §10–§14 — configuration, dependency injection, structured
  logging, centralized error handling, health endpoints.
- RA-001 §3/§6 — canonical layered pipeline; cross-cutting services
  operate across all layers.
- ES-002 §16 — versioned API mounting under ``/api/v1``.

``create_app`` is the single composition root: it resolves configuration,
configures logging, builds the dependency container, installs the
middleware pipeline and exception handlers, and mounts the operational
and versioned routers. Nothing else in the codebase constructs the
application, which keeps the runtime reproducible across environments
(ES-006 §6).
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from api.health import router as health_router
from api.v1.router import router as v1_router
from core.container import ApplicationContainer
from core.errors import install_exception_handlers
from core.middleware import RequestContextMiddleware
from shared.config import Settings, load_settings
from shared.logging import configure_logging, get_logger

_logger = get_logger("atlas.core.application")


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Connect infrastructure and log start/stop (RA-001 service lifecycle).

    Infrastructure startup degrades gracefully (ARCH-001 §14): failures
    are logged and surfaced through readiness rather than crashing the
    process. Shutdown always releases Kafka, Redis, and database
    resources (IP-001 §17 — restartable, rollback-safe services).
    """
    container: ApplicationContainer = app.state.container
    await container.startup()
    _logger.info(
        "Application started",
        extra={
            "environment": container.settings.environment,
            "version": container.settings.version,
        },
    )
    yield
    await container.shutdown()
    _logger.info("Application stopped")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Compose and return the Project ATLAS backend application.

    ``settings`` may be injected for testing; production resolution goes
    through the IP-001 §10 configuration hierarchy.
    """
    resolved_settings = settings if settings is not None else load_settings()

    configure_logging(
        service_name=resolved_settings.service_name,
        log_level=resolved_settings.log_level,
    )

    app = FastAPI(
        title=resolved_settings.app_name,
        version=resolved_settings.version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=_lifespan,
    )

    app.state.container = ApplicationContainer(resolved_settings)

    app.add_middleware(RequestContextMiddleware)
    install_exception_handlers(app)

    app.include_router(health_router)
    app.include_router(v1_router, prefix=resolved_settings.api_v1_prefix)

    return app
