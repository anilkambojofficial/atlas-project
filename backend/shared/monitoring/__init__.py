"""Shared monitoring package (IP-001 §9 — monitoring package).

Approved interpretation (Stage S1.4): monitoring = health, readiness,
and liveness signals; metrics/tracing live in ``shared.telemetry``.
"""

from shared.monitoring.health import CheckResult, HealthCheck, HealthRegistry

__all__ = ["CheckResult", "HealthCheck", "HealthRegistry"]
