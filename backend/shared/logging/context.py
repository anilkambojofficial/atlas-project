"""Request-scoped logging context.

Governing documents:
- IP-001 §12 — every log entry carries Correlation ID, Request ID,
  Tenant ID, User ID.
- ES-001 §12 / RA-001 §18 — correlation identifiers propagate through
  every processing stage.

Context is held in ``contextvars`` so it is concurrency-safe under the
ASGI event loop. Tenant ID and User ID are populated by the Identity and
Tenant platforms (IP-002 / IP-003) once those services exist; the fields
are carried now so the logging contract is stable from first deployment
(BP-002 ED-014).
"""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass

_correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)
_request_id: ContextVar[str | None] = ContextVar("request_id", default=None)
_tenant_id: ContextVar[str | None] = ContextVar("tenant_id", default=None)
_user_id: ContextVar[str | None] = ContextVar("user_id", default=None)


@dataclass(frozen=True)
class RequestContext:
    """Immutable snapshot of the identifiers bound to the current request."""

    correlation_id: str | None
    request_id: str | None
    tenant_id: str | None
    user_id: str | None


def bind_request_context(
    *,
    correlation_id: str | None = None,
    request_id: str | None = None,
    tenant_id: str | None = None,
    user_id: str | None = None,
) -> None:
    """Bind identifiers for the current request scope."""
    if correlation_id is not None:
        _correlation_id.set(correlation_id)
    if request_id is not None:
        _request_id.set(request_id)
    if tenant_id is not None:
        _tenant_id.set(tenant_id)
    if user_id is not None:
        _user_id.set(user_id)


def clear_request_context() -> None:
    """Reset all identifiers at the end of the request scope."""
    _correlation_id.set(None)
    _request_id.set(None)
    _tenant_id.set(None)
    _user_id.set(None)


def get_correlation_id() -> str | None:
    """Return the correlation identifier bound to the current scope."""
    return _correlation_id.get()


def get_request_context() -> RequestContext:
    """Return a snapshot of the full request context."""
    return RequestContext(
        correlation_id=_correlation_id.get(),
        request_id=_request_id.get(),
        tenant_id=_tenant_id.get(),
        user_id=_user_id.get(),
    )
