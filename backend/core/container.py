"""Dependency-injection container.

Governing documents:
- IP-001 §11 — dependency injection is mandatory; services depend on
  interfaces rather than implementations; circular dependencies are
  prohibited. Injectable categories wired at this stage: Configuration,
  Logger, Telemetry, Database, Cache, Event Bus (Authentication,
  Storage, AI Providers follow in their governing Implementation Packs).
- IP-001 §14 — health checks for configuration, PostgreSQL, Redis,
  and Kafka are registered here.
- ARCH-001 §14 — graceful degradation: infrastructure outages surface
  through readiness, they do not crash the application.
- RA-001 §11 — concrete implementations remain replaceable without
  changing business logic.

The container is composed once by the application factory, attached to
``app.state``, connected/disconnected by the application lifespan, and
resolved in route handlers through the FastAPI ``Depends`` providers
below — handlers never construct dependencies themselves.
"""

from __future__ import annotations

from typing import Any

from fastapi import Request

from infrastructure.cache import RedisManager
from infrastructure.database import DatabaseManager, UnitOfWork
from infrastructure.messaging import KafkaManager
from shared.config import Settings
from shared.events import EventEnvelope, KafkaEventPublisher
from shared.logging import get_logger
from shared.monitoring import HealthRegistry
from shared.telemetry import MetricsRegistry

_logger = get_logger("atlas.core.container")


class ApplicationContainer:
    """Holds the platform runtime dependencies for one application instance."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.metrics = MetricsRegistry(
            service_name=settings.service_name,
            version=settings.version,
            environment=settings.environment,
        )
        self.database = DatabaseManager(settings)
        self.redis = RedisManager(settings)
        self.kafka = KafkaManager(settings)
        # KafkaManager structurally satisfies shared.events.MessageTransport;
        # the binding happens here so shared/* never imports infrastructure
        # (S1.4 framework-independence rule; IP-001 §11).
        self.event_publisher = KafkaEventPublisher(
            self.kafka, source=settings.service_name
        )

        self.health = HealthRegistry()
        self.health.register("configuration", self._configuration_check)
        self.health.register("postgresql", self.database.health_check)
        self.health.register("redis", self.redis.health_check)
        self.health.register("kafka", self.kafka.health_check)

    async def startup(self) -> None:
        """Connect infrastructure dependencies (application lifespan start).

        Each connection attempt degrades gracefully (ARCH-001 §14): a
        failure is logged and reflected by the health registry — readiness
        then gates traffic — but the process keeps serving so liveness
        probes do not trigger restart loops.
        """
        try:
            await self.database.ping()
            _logger.info("PostgreSQL connection verified")
        except Exception as exc:  # noqa: BLE001 — degrade, don't crash (ARCH-001 §14)
            _logger.error("PostgreSQL unavailable at startup", exc_info=exc)

        try:
            await self.redis.ping()
            _logger.info("Redis connection verified")
        except Exception as exc:  # noqa: BLE001 — degrade, don't crash (ARCH-001 §14)
            _logger.error("Redis unavailable at startup", exc_info=exc)

        try:
            await self.kafka.start()
        except Exception as exc:  # noqa: BLE001 — degrade, don't crash (ARCH-001 §14)
            _logger.error("Kafka unavailable at startup", exc_info=exc)

    async def shutdown(self) -> None:
        """Release infrastructure resources (application lifespan stop)."""
        await self.kafka.stop()
        await self.redis.close()
        await self.database.dispose()

    def create_unit_of_work(self) -> UnitOfWork:
        """Build a Unit of Work bound to the platform session factory
        (RA-001 §10) with envelope-typed post-commit event publication
        (RA-001 §13; RA-006 §5). The transactional-outbox upgrade path
        follows D-S001-01 (drain worker + migration with the first
        live-database stage).
        """
        return UnitOfWork(
            self.database.session_factory, event_publisher=self._publish_event
        )

    async def _publish_event(self, event: Any) -> None:
        """Post-commit publication hook: only governed envelopes may enter
        the Event Bus (RA-006 §19 — publishing ungoverned events is a
        prohibited anti-pattern)."""
        if not isinstance(event, EventEnvelope):
            _logger.error(
                "Discarded non-envelope event after commit",
                extra={"eventPythonType": type(event).__name__},
            )
            return
        await self.event_publisher.publish(event)

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


def get_database(request: Request) -> DatabaseManager:
    """Resolve the database manager (IP-001 §11 — Database dependency)."""
    return get_container(request).database


def get_redis(request: Request) -> RedisManager:
    """Resolve the Redis manager (IP-001 §11 — Cache dependency)."""
    return get_container(request).redis


def get_kafka(request: Request) -> KafkaManager:
    """Resolve the Kafka manager (IP-001 §11 — Event Bus dependency)."""
    return get_container(request).kafka


def get_unit_of_work(request: Request) -> UnitOfWork:
    """Provide a fresh Unit of Work for one business use case (RA-001 §13)."""
    return get_container(request).create_unit_of_work()
