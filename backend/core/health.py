"""Compatibility shim — the health registry now lives in
``shared.monitoring`` (Stage S1.4 relocation per IP-001 §9).

Existing imports of ``core.health`` continue to work; new code should
import from ``shared.monitoring`` directly.
"""

from shared.monitoring import CheckResult, HealthCheck, HealthRegistry

__all__ = ["CheckResult", "HealthCheck", "HealthRegistry"]
