"""Canonical API response contracts.

Governing documents:
- ES-002 §7 — uniform success envelope:
  ``{"success": true, "data": {...}, "metadata": {...}, "timestamp": "...",
  "correlationId": "..."}``
- ES-002 §17 — uniform error structure:
  ``{"success": false, "error": {"code": "...", "message": "...",
  "details": [...], "correlationId": "...", "timestamp": "..."}}``

These builders are the single source of the response shapes used by the
versioned APIs and the centralized exception handlers, so every service
returns identical envelopes (ES-002 §1 "Consistent" principle).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from shared.logging.context import get_correlation_id


def _timestamp() -> str:
    """ISO-8601 UTC timestamp (IP-001 §15 shared runtime standards)."""
    return datetime.now(timezone.utc).isoformat()


def success_envelope(
    data: Any,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the ES-002 §7 success response envelope."""
    return {
        "success": True,
        "data": data,
        "metadata": metadata or {},
        "timestamp": _timestamp(),
        "correlationId": get_correlation_id(),
    }


def error_body(
    code: str,
    message: str,
    details: list[Any] | None = None,
) -> dict[str, Any]:
    """Build the ES-002 §17 error response body."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or [],
            "correlationId": get_correlation_id(),
            "timestamp": _timestamp(),
        },
    }
