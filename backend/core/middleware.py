"""Platform middleware pipeline.

Governing documents:
- IP-001 §12 — every log entry carries Correlation ID, Request ID,
  Tenant ID, User ID.
- ES-002 §6 — every request carries ``X-Correlation-ID``; the platform
  generates one when absent.
- RA-001 §6 — every request follows the canonical observable pipeline;
  each stage is auditable.
- ARCH-001 §10 — each request receives a unique Request ID for
  traceability.

``RequestContextMiddleware`` is the single foundation middleware: it
binds the request-scoped logging context, echoes the identifiers back as
response headers, records request metrics, and emits the structured
request-completion log line. Tenant and user identifiers are bound by the
Identity/Tenant platforms (IP-002/IP-003) once implemented; the pipeline
position for them exists from first deployment (BP-002 ED-014).
"""

from __future__ import annotations

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from shared.logging import bind_request_context, clear_request_context, get_logger
from shared.utils import uuid7

_logger = get_logger("atlas.request")

CORRELATION_ID_HEADER = "X-Correlation-ID"
REQUEST_ID_HEADER = "X-Request-ID"


def _metric_path(request: Request) -> str:
    """Return the matched route template to keep metric label cardinality bounded."""
    route = request.scope.get("route")
    if isinstance(route, Route):
        return route.path
    return "unmatched"


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Binds request identity, records telemetry, logs request completion."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        correlation_id = request.headers.get(CORRELATION_ID_HEADER) or str(uuid7())
        request_id = str(uuid7())
        bind_request_context(correlation_id=correlation_id, request_id=request_id)

        metrics = request.app.state.container.metrics
        started = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            # Record the failure, then let the centralized exception
            # handlers produce the client response (IP-001 §13).
            duration = time.perf_counter() - started
            metrics.observe_request(
                request.method, _metric_path(request), 500, duration
            )
            _logger.error(
                "Request failed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "statusCode": 500,
                    "durationMs": round(duration * 1000, 2),
                },
            )
            # Context is intentionally NOT cleared here: the outermost
            # unexpected-error handler still needs the Correlation ID for
            # the error envelope (IP-001 §13). Each request runs in its
            # own task context, so the binding cannot leak across requests.
            raise

        duration = time.perf_counter() - started
        metrics.observe_request(
            request.method, _metric_path(request), response.status_code, duration
        )
        _logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "statusCode": response.status_code,
                "durationMs": round(duration * 1000, 2),
            },
        )

        response.headers[CORRELATION_ID_HEADER] = correlation_id
        response.headers[REQUEST_ID_HEADER] = request_id
        clear_request_context()
        return response
