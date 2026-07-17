"""Dependency-injection container.

Governing documents:
- IP-001 §11 — dependency injection is mandatory; services depend on
  interfaces rather than implementations; circular dependencies are
  prohibited. Injectable categories available at this stage:
  Configuration, Logger, Telemetry (Database, Cache, Event Bus,
  Authentication, Storage, AI Providers are wired in their governing
  Implementation Pack stages).
- RA-001 §11 — concrete implementations remain replaceable without
  changing business logic.

The container is composed once by the application factory, attached to
``app.state``, and resolved in route handlers through the FastAPI
``Depends`` providers below — handlers never construct dependencies
themselves.
"""

from __future__ import annotations

from fastapi import Request

from core.health import HealthRegistry
from shared.config import Settings
from shared.telemetry import MetricsRegistry


class ApplicationContainer:
    """Holds the platform runtime dependencies for one application instance."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.metrics = MetricsRegistry(
            service_name=settings.service_name,
            version=settings.version,
            environment=settings.environment,
        )
        self.health = HealthRegistry()
        self.health.register("configuration", self._configuration_check)

    def _configuration_check(self) -> tuple[bool, str]:
        """Configuration health check (IP-001 §14: health validates configuration).

        The settings object only exists if the IP-001 §10 resolution chain
        completed and passed validation, so this check asserts the resolved
        environment is a legal member of the IP-001 §15 environment set.
        """
        valid = self.settings.environment in (
            "development",
            "testing",
            "staging",
            "production",
        )
        detail = f"environment '{self.settings.environment}' resolved and validated"
        return valid, detail if valid else "environment failed validation"


def get_container(request: Request) -> ApplicationContainer:
    """Resolve the application container from the current request."""
    return request.app.state.container


def get_settings(request: Request) -> Settings:
    """Resolve validated settings (IP-001 §11 — Configuration dependency)."""
    return get_container(request).settings


def get_metrics(request: Request) -> MetricsRegistry:
    """Resolve the metrics registry (IP-001 §11 — telemetry dependency)."""
    return get_container(request).metrics


def get_health(request: Request) -> HealthRegistry:
    """Resolve the health-check registry (IP-001 §14)."""
    return get_container(request).health
