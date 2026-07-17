"""Centralized error handling framework.

Governing documents:
- IP-001 §13 — mandatory error categories (Validation, Authentication,
  Authorization, Business, Infrastructure, External Service, AI,
  Unexpected); every error carries Error Code, Error Message,
  Correlation ID, Timestamp; internal stack traces are never exposed
  to clients.
- ES-002 §8 — standard HTTP status codes only.
- ES-002 §17 — uniform error response structure.
- RA-001 §20 — consistent, structured, auditable error handling.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from shared.contracts.api import error_body
from shared.logging import get_logger

_logger = get_logger("atlas.core.errors")


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


#: HTTP status -> machine-readable code for framework-raised HTTP errors
#: (ES-002 §8 standard codes; custom status codes are prohibited).
_HTTP_STATUS_CODES: dict[int, str] = {
    400: "BAD_REQUEST",
    401: "AUTHENTICATION_ERROR",
    403: "AUTHORIZATION_ERROR",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    429: "TOO_MANY_REQUESTS",
    500: "INTERNAL_ERROR",
    502: "BAD_GATEWAY",
    503: "SERVICE_UNAVAILABLE",
    504: "GATEWAY_TIMEOUT",
}


def _error_response(
    status_code: int, code: str, message: str, details: list[Any] | None = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content=error_body(code, message, details)
    )


async def _handle_atlas_error(request: Request, exc: AtlasError) -> JSONResponse:
    _logger.warning(
        "Platform error handled",
        extra={"errorCode": exc.code, "statusCode": exc.status_code,
               "path": request.url.path},
    )
    return _error_response(exc.status_code, exc.code, exc.message, exc.details)


async def _handle_request_validation(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [
        {"field": ".".join(str(part) for part in error.get("loc", [])),
         "issue": error.get("msg", "invalid value")}
        for error in exc.errors()
    ]
    _logger.warning(
        "Request validation failed",
        extra={"path": request.url.path, "issueCount": len(details)},
    )
    return _error_response(422, "VALIDATION_ERROR", "Request validation failed.", details)


async def _handle_http_exception(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    code = _HTTP_STATUS_CODES.get(exc.status_code, "HTTP_ERROR")
    message = str(exc.detail) if exc.detail else "Request could not be processed."
    return _error_response(exc.status_code, code, message)


async def _handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
    # Full details go to the structured log only — never to the client
    # (IP-001 §13; ES-002 §17 "avoid sensitive information").
    _logger.error(
        "Unhandled exception",
        exc_info=exc,
        extra={"path": request.url.path},
    )
    return _error_response(500, "INTERNAL_ERROR", "An unexpected error occurred.")


def install_exception_handlers(app: FastAPI) -> None:
    """Attach the centralized handlers to the application (IP-001 §13)."""
    app.add_exception_handler(AtlasError, _handle_atlas_error)
    app.add_exception_handler(RequestValidationError, _handle_request_validation)
    app.add_exception_handler(StarletteHTTPException, _handle_http_exception)
    app.add_exception_handler(Exception, _handle_unexpected)
