"""Platform error taxonomy — framework-free.

Governing documents:
- IP-001 §13 — mandatory error categories (Validation, Authentication,
  Authorization, Business, Infrastructure, External Service, AI,
  Unexpected) with machine-readable codes.
- ES-002 §8 — HTTP status mapping uses standard codes only (the
  ``status_code`` attribute is a plain integer; no web-framework import).
- RA-001 §4/§5 — domain layers raise platform errors without depending
  on outer layers; this package is therefore importable from any layer.

Relocated from ``core/errors.py`` in Stage S1.4 (approved plan §4);
``core.errors`` re-exports these names for compatibility and keeps only
the HTTP handler wiring.
"""

from __future__ import annotations

from typing import Any


class AtlasError(Exception):
    """Base class for every platform error (IP-001 §13 taxonomy root)."""

    code: str = "INTERNAL_ERROR"
    status_code: int = 500

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status_code: int | None = None,
        details: list[Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code
        if status_code is not None:
            self.status_code = status_code
        self.details = details or []


class ValidationError(AtlasError):
    """Input failed validation (IP-001 §13 — Validation Error)."""

    code = "VALIDATION_ERROR"
    status_code = 422


class AuthenticationError(AtlasError):
    """Identity could not be authenticated (IP-001 §13)."""

    code = "AUTHENTICATION_ERROR"
    status_code = 401


class AuthorizationError(AtlasError):
    """Authenticated identity lacks permission (IP-001 §13)."""

    code = "AUTHORIZATION_ERROR"
    status_code = 403


class NotFoundError(AtlasError):
    """Requested resource does not exist (ES-002 §8/§17)."""

    code = "NOT_FOUND"
    status_code = 404


class BusinessError(AtlasError):
    """A domain business rule was violated (IP-001 §13)."""

    code = "BUSINESS_RULE_VIOLATION"
    status_code = 409


class InfrastructureError(AtlasError):
    """A platform infrastructure dependency failed (IP-001 §13)."""

    code = "INFRASTRUCTURE_ERROR"
    status_code = 503


class ExternalServiceError(AtlasError):
    """An external integration failed (IP-001 §13)."""

    code = "EXTERNAL_SERVICE_ERROR"
    status_code = 502


class AIError(AtlasError):
    """An AI platform operation failed (IP-001 §13)."""

    code = "AI_ERROR"
    status_code = 502
