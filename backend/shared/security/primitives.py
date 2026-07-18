"""Framework-free security primitives.

Governing documents:
- ES-004 §12 / ES-001 §12 — sensitive values never appear in logs or
  responses; redaction is centralized here and consumed by the logging
  package.
- RA-011 §2 — secure defaults; constant-time comparison for secret
  equality checks.

Cryptographic authentication mechanisms (Argon2id, JWT signing, key
management) are IP-002 scope and intentionally absent (approved plan §4).
"""

from __future__ import annotations

import hmac
import secrets

#: Field names whose values are always redacted (ES-004 §12).
#: Single authoritative set — the structured logger consumes it.
SENSITIVE_KEYS = frozenset(
    {
        "password",
        "secret",
        "token",
        "authorization",
        "api_key",
        "apikey",
        "credential",
        "credentials",
        "private_key",
        "refresh_token",
        "access_token",
    }
)

REDACTED = "[REDACTED]"

_MASK = "•"  # bullet character used for masked segments


def is_sensitive_key(key: str) -> bool:
    """True when a field name must never be emitted with its value."""
    return key.lower() in SENSITIVE_KEYS


def redact_mapping(mapping: dict[str, object]) -> dict[str, object]:
    """Return a copy of ``mapping`` with sensitive values replaced."""
    return {
        key: REDACTED if is_sensitive_key(key) else value
        for key, value in mapping.items()
    }


def mask_secret(value: str, *, visible: int = 4) -> str:
    """Mask a secret leaving at most ``visible`` trailing characters.

    Values shorter than ``visible + 1`` are fully masked so short secrets
    can never be reconstructed from their mask.
    """
    if visible < 0:
        raise ValueError("visible must be >= 0")
    if len(value) <= visible:
        return _MASK * len(value)
    return _MASK * (len(value) - visible) + value[-visible:]


def constant_time_equals(left: str, right: str) -> bool:
    """Timing-attack-safe string equality (RA-011 §2 secure defaults)."""
    return hmac.compare_digest(left.encode("utf-8"), right.encode("utf-8"))


def secure_random_string(length: int = 32) -> str:
    """URL-safe cryptographically secure random string of exact length."""
    if length < 1:
        raise ValueError("length must be >= 1")
    return secrets.token_urlsafe(length)[:length]
