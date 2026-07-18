"""Unit tests — shared.constants and shared.exceptions (ES-007 §5)."""

from __future__ import annotations

import pytest

from shared.constants import (
    CANONICAL_ENV_ALIASES,
    DEFAULT_PAGE_SIZE,
    ERROR_CODES,
    HEADER_CORRELATION_ID,
    HEADER_REQUEST_ID,
    MAX_PAGE_SIZE,
    VALID_ENVIRONMENTS,
)
from shared.exceptions import (
    AIError,
    AtlasError,
    AuthenticationError,
    AuthorizationError,
    BusinessError,
    ExternalServiceError,
    InfrastructureError,
    NotFoundError,
    ValidationError,
)


class TestConstants:
    def test_headers_match_es002(self) -> None:
        assert HEADER_CORRELATION_ID == "X-Correlation-ID"
        assert HEADER_REQUEST_ID == "X-Request-ID"

    def test_pagination_bounds_are_sane(self) -> None:
        assert 1 <= DEFAULT_PAGE_SIZE <= MAX_PAGE_SIZE

    def test_environment_set_matches_ip001(self) -> None:
        assert VALID_ENVIRONMENTS == (
            "development",
            "testing",
            "staging",
            "production",
        )

    def test_canonical_env_aliases_match_ip002(self) -> None:
        assert CANONICAL_ENV_ALIASES["DATABASE_URL"] == "database_url"
        assert CANONICAL_ENV_ALIASES["REDIS_URL"] == "redis_url"
        assert CANONICAL_ENV_ALIASES["KAFKA_BROKER"] == "kafka_broker"


class TestExceptionTaxonomy:
    @pytest.mark.parametrize(
        ("exc_cls", "code", "status"),
        [
            (ValidationError, "VALIDATION_ERROR", 422),
            (AuthenticationError, "AUTHENTICATION_ERROR", 401),
            (AuthorizationError, "AUTHORIZATION_ERROR", 403),
            (NotFoundError, "NOT_FOUND", 404),
            (BusinessError, "BUSINESS_RULE_VIOLATION", 409),
            (InfrastructureError, "INFRASTRUCTURE_ERROR", 503),
            (ExternalServiceError, "EXTERNAL_SERVICE_ERROR", 502),
            (AIError, "AI_ERROR", 502),
        ],
    )
    def test_category_codes_and_statuses(self, exc_cls, code, status) -> None:
        error = exc_cls("boom")
        assert isinstance(error, AtlasError)
        assert error.code == code
        assert error.status_code == status
        assert error.message == "boom"
        assert error.details == []
        assert error.code in ERROR_CODES

    def test_overrides_and_details(self) -> None:
        error = AtlasError(
            "custom", code="X", status_code=418, details=[{"field": "a"}]
        )
        assert (error.code, error.status_code) == ("X", 418)
        assert error.details == [{"field": "a"}]

    def test_core_compatibility_reexports(self) -> None:
        # S1.4 relocation contract: existing `core.errors` imports keep working.
        from core import errors as core_errors

        assert core_errors.AtlasError is AtlasError
        assert core_errors.ValidationError is ValidationError
