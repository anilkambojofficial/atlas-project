"""Unit tests — shared.monitoring, shared.auth, shared.contracts,
shared.config, shared.logging (ES-007 §5)."""

from __future__ import annotations

import json
import logging as std_logging

import pytest

from shared.auth import (
    AccessDecision,
    IdentityClass,
    PolicyDecisionPoint,
    Principal,
    TokenVerifier,
)
from shared.config import load_settings
from shared.contracts.api import error_body, success_envelope
from shared.logging import bind_request_context, clear_request_context
from shared.logging.logger import JsonLogFormatter
from shared.monitoring import HealthRegistry


class TestHealthRegistry:
    async def test_sync_and_async_checks(self) -> None:
        registry = HealthRegistry()
        registry.register("sync_ok", lambda: (True, "fine"))

        async def async_bad() -> tuple[bool, str]:
            return False, "down"

        registry.register("async_bad", async_bad)
        results = {r.name: r for r in await registry.run_all()}
        assert results["sync_ok"].healthy is True
        assert results["async_bad"].healthy is False

    async def test_crashing_check_reports_unhealthy(self) -> None:
        registry = HealthRegistry()

        def boom() -> tuple[bool, str]:
            raise RuntimeError("kaput")

        registry.register("boom", boom)
        [result] = await registry.run_all()
        assert result.healthy is False
        assert "RuntimeError" in result.detail

    def test_duplicate_registration_rejected(self) -> None:
        registry = HealthRegistry()
        registry.register("x", lambda: (True, "ok"))
        with pytest.raises(ValueError):
            registry.register("x", lambda: (True, "ok"))

    def test_core_compatibility_reexport(self) -> None:
        from core.health import HealthRegistry as CoreHealthRegistry

        assert CoreHealthRegistry is HealthRegistry


class TestAuthContracts:
    def test_principal_is_immutable_with_identity_classes(self) -> None:
        principal = Principal(
            subject_id="u-1",
            identity_class=IdentityClass.HUMAN,
            organization_id="org-1",
            roles=("member",),
        )
        with pytest.raises(Exception):
            principal.subject_id = "u-2"  # type: ignore[misc]
        assert {c.value for c in IdentityClass} == {"human", "machine", "agent"}

    async def test_protocols_are_structural(self) -> None:
        class Verifier:
            async def verify(self, token: str) -> Principal:
                return Principal("u", IdentityClass.MACHINE, None)

        class PDP:
            async def authorize(self, principal, *, resource, action,
                                organization_id=None) -> AccessDecision:
                return AccessDecision(permit=False, reason="fail-closed default")

        assert isinstance(Verifier(), TokenVerifier)
        assert isinstance(PDP(), PolicyDecisionPoint)
        decision = await PDP().authorize(
            await Verifier().verify("t"), resource="meeting", action="read"
        )
        assert decision.permit is False and decision.obligations == ()


class TestApiContracts:
    def test_envelopes_carry_context_correlation(self) -> None:
        bind_request_context(correlation_id="corr-7")
        try:
            ok = success_envelope({"a": 1}, metadata={"m": 2})
            err = error_body("NOT_FOUND", "missing", [{"field": "id"}])
        finally:
            clear_request_context()
        assert ok["success"] is True and ok["correlationId"] == "corr-7"
        assert ok["metadata"] == {"m": 2}
        assert err["success"] is False
        assert err["error"]["code"] == "NOT_FOUND"
        assert err["error"]["correlationId"] == "corr-7"


class TestConfig:
    def test_env_override_and_canonical_alias(self, monkeypatch) -> None:
        monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://c/canonical")
        settings = load_settings()
        assert settings.database_url.endswith("/canonical")
        # Prefixed variable wins over the canonical alias (S1.2B rule).
        monkeypatch.setenv("ATLAS_DATABASE_URL", "postgresql+asyncpg://p/prefixed")
        assert load_settings().database_url.endswith("/prefixed")

    def test_invalid_log_level_rejected(self, monkeypatch) -> None:
        monkeypatch.setenv("ATLAS_LOG_LEVEL", "LOUD")
        with pytest.raises(Exception):
            load_settings()


class TestStructuredLogging:
    def test_formatter_emits_mandatory_fields_and_redacts(self) -> None:
        formatter = JsonLogFormatter("atlas-backend")
        record = std_logging.LogRecord(
            name="t", level=std_logging.INFO, pathname=__file__, lineno=1,
            msg="hello", args=(), exc_info=None,
        )
        record.password = "hunter2"  # extra field must be redacted
        record.custom = "keep"
        bind_request_context(correlation_id="corr-log", tenant_id="org-9")
        try:
            entry = json.loads(formatter.format(record))
        finally:
            clear_request_context()
        assert entry["severity"] == "INFO"
        assert entry["service"] == "atlas-backend"
        assert entry["correlationId"] == "corr-log"
        assert entry["tenantId"] == "org-9"
        assert entry["password"] == "[REDACTED]"
        assert entry["custom"] == "keep"
