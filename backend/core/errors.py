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
from shared.exceptions import (  # noqa: F401 — compatibility re-exports (S1.4 relocation)
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
from shared.logging import get_logger

_logger = get_logger("atlas.core.errors")


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
