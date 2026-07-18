"""Unit tests — shared.validation and shared.security (ES-007 §5)."""

from __future__ import annotations

import uuid
from datetime import timezone
from enum import Enum

import pytest

from shared.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from shared.exceptions import ValidationError
from shared.security import (
    REDACTED,
    constant_time_equals,
    is_sensitive_key,
    mask_secret,
    redact_mapping,
    secure_random_string,
)
from shared.utils import uuid7
from shared.validation import (
    coerce_enum,
    normalize_pagination,
    parse_iso8601,
    parse_uuid,
    require_non_empty,
)


class _Color(Enum):
    RED = "red"
    BLUE = "blue"


class TestValidation:
    def test_parse_uuid_accepts_uuid_and_string(self) -> None:
        value = uuid7()
        assert parse_uuid(value) == value
        assert parse_uuid(str(value)) == value

    def test_parse_uuid_rejects_garbage(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            parse_uuid("not-a-uuid", field="organizationId")
        assert exc_info.value.details[0]["field"] == "organizationId"

    def test_normalize_pagination_defaults(self) -> None:
        assert normalize_pagination() == (1, DEFAULT_PAGE_SIZE)

    def test_normalize_pagination_caps_page_size(self) -> None:
        assert normalize_pagination(2, MAX_PAGE_SIZE + 1000) == (2, MAX_PAGE_SIZE)

    @pytest.mark.parametrize(("page", "size"), [(0, 10), (1, 0), (-5, 10)])
    def test_normalize_pagination_rejects_invalid(self, page, size) -> None:
        with pytest.raises(ValidationError):
            normalize_pagination(page, size)

    def test_parse_iso8601_utc_and_naive(self) -> None:
        aware = parse_iso8601("2026-07-18T10:00:00+05:30")
        assert aware.tzinfo == timezone.utc
        naive = parse_iso8601("2026-07-18T10:00:00")
        assert naive.tzinfo == timezone.utc  # naive interpreted as UTC (IP-001 §15)

    def test_parse_iso8601_rejects_garbage(self) -> None:
        with pytest.raises(ValidationError):
            parse_iso8601("yesterday")

    def test_coerce_enum(self) -> None:
        assert coerce_enum(_Color, "red", field="color") is _Color.RED
        assert coerce_enum(_Color, _Color.BLUE, field="color") is _Color.BLUE
        with pytest.raises(ValidationError) as exc_info:
            coerce_enum(_Color, "green", field="color")
        assert "red" in exc_info.value.details[0]["issue"]

    def test_require_non_empty(self) -> None:
        assert require_non_empty("  value  ", field="name") == "value"
        for bad in (None, "", "   "):
            with pytest.raises(ValidationError):
                require_non_empty(bad, field="name")


class TestSecurity:
    def test_sensitive_keys_detected_case_insensitively(self) -> None:
        assert is_sensitive_key("Password")
        assert is_sensitive_key("REFRESH_TOKEN")
        assert not is_sensitive_key("username")

    def test_redact_mapping_preserves_safe_values(self) -> None:
        redacted = redact_mapping({"password": "hunter2", "user": "anil"})
        assert redacted == {"password": REDACTED, "user": "anil"}

    def test_mask_secret(self) -> None:
        assert mask_secret("abcdefgh", visible=4).endswith("efgh")
        assert "abcd" not in mask_secret("abcdefgh", visible=4)
        assert mask_secret("abc", visible=4) == "•••"  # short → fully masked
        with pytest.raises(ValueError):
            mask_secret("x", visible=-1)

    def test_constant_time_equals(self) -> None:
        assert constant_time_equals("token", "token")
        assert not constant_time_equals("token", "other")

    def test_secure_random_string_length_and_uniqueness(self) -> None:
        values = {secure_random_string(32) for _ in range(50)}
        assert len(values) == 50
        assert all(len(v) == 32 for v in values)
        with pytest.raises(ValueError):
            secure_random_string(0)


class TestUuid7:
    def test_version_variant_and_ordering(self) -> None:
        first, second = uuid7(), uuid7()
        for value in (first, second):
            assert value.version == 7
            assert value.variant == uuid.RFC_4122
        # Time-ordered: identical or increasing millisecond prefix.
        assert str(first)[:8] <= str(second)[:8]
