"""Reusable input-validation primitives.

Governing documents:
- ES-002 §14 / ARCH-005 §14 — all externally supplied data is validated
  before processing; invalid input is rejected before business logic.
- ES-002 §9 — pagination bounds.
- IP-001 §15 — UUID and ISO-8601/UTC standards.

Failures raise the platform ``ValidationError`` (IP-001 §13) so every
layer produces the identical ES-002 §17 error envelope.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TypeVar

from shared.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from shared.exceptions import ValidationError

EnumT = TypeVar("EnumT", bound=Enum)


def parse_uuid(value: str | uuid.UUID, *, field: str = "id") -> uuid.UUID:
    """Parse a UUID, raising the platform validation error on failure."""
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError) as exc:
        raise ValidationError(
            f"Invalid UUID for '{field}'.",
            details=[{"field": field, "issue": "must be a valid UUID"}],
        ) from exc


def normalize_pagination(
    page: int | None = None, page_size: int | None = None
) -> tuple[int, int]:
    """Validate and bound pagination parameters (ES-002 §9, ES-003 §12).

    Returns ``(page, page_size)`` with ``page >= 1`` and
    ``1 <= page_size <= MAX_PAGE_SIZE``.
    """
    resolved_page = 1 if page is None else page
    resolved_size = DEFAULT_PAGE_SIZE if page_size is None else page_size
    if resolved_page < 1:
        raise ValidationError(
            "Invalid pagination.",
            details=[{"field": "page", "issue": "must be >= 1"}],
        )
    if resolved_size < 1:
        raise ValidationError(
            "Invalid pagination.",
            details=[{"field": "pageSize", "issue": "must be >= 1"}],
        )
    return resolved_page, min(resolved_size, MAX_PAGE_SIZE)


def parse_iso8601(value: str, *, field: str = "timestamp") -> datetime:
    """Parse an ISO-8601 timestamp into a timezone-aware UTC datetime."""
    try:
        parsed = datetime.fromisoformat(value)
    except (ValueError, TypeError) as exc:
        raise ValidationError(
            f"Invalid timestamp for '{field}'.",
            details=[{"field": field, "issue": "must be ISO-8601"}],
        ) from exc
    if parsed.tzinfo is None:
        # Naive timestamps are interpreted as UTC (IP-001 §15 UTC standard).
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def coerce_enum(enum_cls: type[EnumT], value: object, *, field: str) -> EnumT:
    """Coerce a raw value into an Enum member with a platform error."""
    if isinstance(value, enum_cls):
        return value
    try:
        return enum_cls(value)
    except ValueError as exc:
        allowed = ", ".join(str(member.value) for member in enum_cls)
        raise ValidationError(
            f"Invalid value for '{field}'.",
            details=[{"field": field, "issue": f"must be one of: {allowed}"}],
        ) from exc


def require_non_empty(value: str | None, *, field: str) -> str:
    """Require a non-empty, non-whitespace string."""
    if value is None or not value.strip():
        raise ValidationError(
            f"'{field}' must not be empty.",
            details=[{"field": field, "issue": "must not be empty"}],
        )
    return value.strip()
