"""Platform health-check registry.

Governing documents:
- IP-001 §14 — every deployable service exposes ``/health``, ``/ready``,
  ``/live``, ``/metrics``; health checks validate configuration,
  database, Redis, Kafka, and (in later stages) storage and AI
  providers.
- RA-001 §21 — liveness, readiness, and startup health categories with
  dependency checks supporting automated orchestration.

Checks may be synchronous (e.g. configuration) or asynchronous
(PostgreSQL/Redis/Kafka round-trips registered in Stage S1.2B); the
registry awaits awaitable results transparently, so the health endpoints
never need to distinguish the two.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Awaitable, Callable, Union

from shared.logging import get_logger

_logger = get_logger("atlas.core.health")

#: A check returns (healthy, detail) either directly or as an awaitable.
HealthCheck = Callable[[], Union[tuple[bool, str], Awaitable[tuple[bool, str]]]]


@dataclass(frozen=True)
class CheckResult:
    """Outcome of a single registered health check."""

    name: str
    healthy: bool
    detail: str


class HealthRegistry:
    """Named health checks evaluated by the health and readiness endpoints."""

    def __init__(self) -> None:
        self._checks: dict[str, HealthCheck] = {}

    def register(self, name: str, check: HealthCheck) -> None:
        """Register a dependency check under a unique name."""
        if name in self._checks:
            raise ValueError(f"Health check '{name}' is already registered")
        self._checks[name] = check

    async def run_all(self) -> list[CheckResult]:
        """Evaluate every registered check; a crashing check is unhealthy."""
        results: list[CheckResult] = []
        for name, check in self._checks.items():
            try:
                outcome = check()
                if inspect.isawaitable(outcome):
                    outcome = await outcome
                healthy, detail = outcome
            except Exception as exc:  # noqa: BLE001 — a failing probe must not crash the endpoint
                _logger.error(
                    "Health check raised an exception",
                    exc_info=exc,
                    extra={"check": name},
                )
                healthy, detail = False, f"check raised {type(exc).__name__}"
            results.append(CheckResult(name=name, healthy=healthy, detail=detail))
        return results
