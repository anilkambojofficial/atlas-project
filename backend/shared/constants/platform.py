"""Single authoritative home for platform literals.

Governing documents:
- IP-001 §9 — constants package; ES-001 §6 — magic values are prohibited
  in business logic; every previously duplicated literal now lives here.
- ES-002 §6 — correlation headers; §9 — pagination bounds.
- IP-001 §15 — environment set.
- IP-002 §18 — canonical infrastructure environment variable names.
- RA-006 / BP-004 §11 — event topic prefix convention.

Framework-independent by rule: standard library only.
"""

from __future__ import annotations

# --- HTTP headers (ES-002 §6; ARCH-001 §10) --------------------------------
HEADER_CORRELATION_ID = "X-Correlation-ID"
HEADER_REQUEST_ID = "X-Request-ID"

# --- Configuration resolution (IP-001 §10; IP-002 §18) ---------------------
ENV_PREFIX = "ATLAS_"
CANONICAL_ENV_ALIASES: dict[str, str] = {
    "DATABASE_URL": "database_url",
    "REDIS_URL": "redis_url",
    "KAFKA_BROKER": "kafka_broker",
}

# --- Environments (IP-001 §15) ---------------------------------------------
VALID_ENVIRONMENTS: tuple[str, ...] = (
    "development",
    "testing",
    "staging",
    "production",
)

# --- Pagination bounds (ES-002 §9; ES-003 §12) -----------------------------
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 500

# --- Health statuses (IP-001 §14) ------------------------------------------
STATUS_HEALTHY = "healthy"
STATUS_UNHEALTHY = "unhealthy"
STATUS_ALIVE = "alive"

# --- Eventing (RA-006; BP-004 §11 naming convention) -----------------------
#: Kafka topics are namespaced ``atlas.<domain>`` (platform convention
#: recorded here; the Enterprise Event Catalog of RA-006 §21 governs names).
EVENT_TOPIC_PREFIX = "atlas"

# --- Machine-readable platform error codes (IP-001 §13; ES-002 §17) --------
ERROR_CODES: tuple[str, ...] = (
    "VALIDATION_ERROR",
    "AUTHENTICATION_ERROR",
    "AUTHORIZATION_ERROR",
    "NOT_FOUND",
    "BUSINESS_RULE_VIOLATION",
    "INFRASTRUCTURE_ERROR",
    "EXTERNAL_SERVICE_ERROR",
    "AI_ERROR",
    "INTERNAL_ERROR",
)
