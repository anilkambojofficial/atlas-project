"""Backend configuration system.

Governing documents:
- IP-001 §10 — configuration hierarchy ``configs/{base,<environment>,local}``
  with resolution priority: environment variables > secret store >
  environment configuration > base configuration. Hard-coded configuration
  values are prohibited.
- IP-001 §15 — environment set: development, testing, staging, production.
- ES-001 §11 — configuration shall never be hardcoded in business logic.

The secret-store layer of the priority chain is integrated in Sprint-001
Stage S1.5 (platform Secret Manager integration point); until then the
chain resolves file layers and environment variables, which is sufficient
for the Platform Foundation runtime and requires no code change when the
secret layer is added between them.

Configuration files are JSON (standard library parsing, no additional
dependency) named ``backend.json`` inside each ``configs/`` layer. Missing
files are legal — every field carries a validated default.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from shared.config.features import (
    normalize_feature_mapping,
    parse_feature_flags_from_env,
)
from shared.config.secrets import (
    EnvironmentSecretProvider,
    LocalFileSecretProvider,
    SecretProvider,
    resolve_secret_layer,
)
from shared.security import mask_secret

from shared.constants import (  # noqa: E402 — constants are the authoritative home (S1.4)
    CANONICAL_ENV_ALIASES,
    ENV_PREFIX,
)

Environment = Literal["development", "testing", "staging", "production"]

#: Repository root, derived from this file's location:
#: backend/shared/config/settings.py -> parents[3] == repository root.
REPO_ROOT = Path(__file__).resolve().parents[3]

#: Configuration hierarchy root (IP-001 §10).
CONFIGS_DIR = REPO_ROOT / "configs"

#: Per-layer configuration file name for the backend.
CONFIG_FILE_NAME = "backend.json"

_VALID_LOG_LEVELS = {"TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

#: Settings fields whose values may embed credentials; their values are
#: masked by :meth:`Settings.safe_dump` (ES-004 §12 — secrets are never
#: exposed through logs or introspection).
SENSITIVE_SETTINGS_FIELDS = frozenset(
    {
        "database_url",
        "redis_url",
        "worker_broker_url",
        "worker_result_backend",
        "auth_jwt_secret",
    }
)

#: Development-only JWT secret; production refuses to start with it
#: (fail secure, RA-011 §2; ADR-004).
_DEV_JWT_SECRET = "atlas-dev-secret-change-me"


class Settings(BaseModel):
    """Validated backend runtime settings."""

    app_name: str = "Project ATLAS Backend"
    service_name: str = "atlas-backend"
    version: str = "0.1.0"
    environment: Environment = "development"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"

    # --- Infrastructure (IP-001 §7; S1.2B) -------------------------------
    # Development defaults are overridable through every layer of the
    # §10 hierarchy; staging/production values come from the environment
    # configuration and secret manager, never from code.
    database_url: str = "postgresql+asyncpg://atlas:atlas@localhost:5432/atlas"
    database_pool_size: int = Field(default=5, ge=1)
    database_max_overflow: int = Field(default=10, ge=0)
    database_echo: bool = False
    database_connect_timeout_seconds: int = Field(default=5, ge=1)

    redis_url: str = "redis://localhost:6379/0"
    redis_timeout_seconds: int = Field(default=2, ge=1)

    kafka_broker: str = "localhost:9092"
    kafka_client_id: str = "atlas-backend"
    kafka_timeout_seconds: int = Field(default=5, ge=1)

    #: Worker broker/result backend; when unset they resolve to the
    #: platform Redis URL (IP-001 §7 stack — Celery with Redis).
    worker_broker_url: str | None = None
    worker_result_backend: str | None = None

    #: Platform-scoped feature flags (IP-001 §10; tenant-scoped feature
    #: management belongs to IP-003 per RA-009 §12).
    features: dict[str, bool] = Field(default_factory=dict)

    # --- CORS (ADR-006, PO-approved 2026-07-19) --------------------------
    #: Empty list (the default) means the CORS middleware is not installed.
    #: Production must be same-origin (no CORS); development uses an
    #: explicit allowlist; wildcards are forbidden in every environment.
    cors_allowed_origins: list[str] = Field(default_factory=list)

    # --- Transactional outbox (ADR-002 §2) -------------------------------
    outbox_drain_interval_seconds: int = Field(default=5, ge=1)
    outbox_batch_size: int = Field(default=100, ge=1, le=1000)
    outbox_max_attempts: int = Field(default=10, ge=1)

    # --- Identity & Access (Sprint-002; BP-003, ADR-004) -----------------
    auth_jwt_secret: str = _DEV_JWT_SECRET
    auth_jwt_algorithm: str = "HS256"
    auth_jwt_issuer: str = "atlas-identity"
    auth_access_token_ttl_seconds: int = Field(default=900, ge=60)
    auth_refresh_token_ttl_seconds: int = Field(default=30 * 24 * 3600, ge=3600)
    auth_password_min_length: int = Field(default=12, ge=8)
    auth_max_failed_logins: int = Field(default=5, ge=1)
    auth_lockout_seconds: int = Field(default=900, ge=60)
    auth_refresh_cookie_name: str = "atlas_refresh"

    @property
    def worker_broker(self) -> str:
        """Effective Celery broker URL."""
        return self.worker_broker_url or self.redis_url

    @property
    def worker_backend(self) -> str:
        """Effective Celery result backend URL."""
        return self.worker_result_backend or self.redis_url

    @field_validator("log_level")
    @classmethod
    def _validate_log_level(cls, value: str) -> str:
        upper = value.upper()
        if upper not in _VALID_LOG_LEVELS:
            raise ValueError(
                f"log_level must be one of {sorted(_VALID_LOG_LEVELS)} (IP-001 §12)"
            )
        return upper

    @field_validator("database_url")
    @classmethod
    def _validate_database_url(cls, value: str) -> str:
        # IP-001 §7/§15 stack: PostgreSQL through the SQLAlchemy asyncpg driver.
        if not value.startswith("postgresql+asyncpg://"):
            raise ValueError(
                "database_url must use the 'postgresql+asyncpg://' scheme (IP-001 §7)"
            )
        return value

    @field_validator("redis_url")
    @classmethod
    def _validate_redis_url(cls, value: str) -> str:
        if not value.startswith(("redis://", "rediss://")):
            raise ValueError(
                "redis_url must use the 'redis://' or 'rediss://' scheme (IP-001 §7)"
            )
        return value

    @field_validator("features", mode="before")
    @classmethod
    def _validate_features(cls, value: object) -> dict[str, bool]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("features must be an object of flag -> boolean")
        return normalize_feature_mapping(value)

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def _validate_cors_origins(cls, value: object) -> list[str]:
        """ADR-006: explicit origins only; wildcards forbidden everywhere
        (Product Owner mandate, 2026-07-19)."""
        if value is None:
            return []
        if isinstance(value, str):
            value = [item.strip() for item in value.split(",") if item.strip()]
        if not isinstance(value, list):
            raise ValueError("cors_allowed_origins must be a list of origins")
        for origin in value:
            if not isinstance(origin, str) or "*" in origin:
                raise ValueError(
                    "Wildcard CORS origins are forbidden in every environment (ADR-006)"
                )
            if not origin.startswith(("http://", "https://")):
                raise ValueError(
                    f"CORS origin must be an absolute http(s) origin: {origin!r}"
                )
        return list(value)

    @model_validator(mode="after")
    def _validate_production_safety(self) -> "Settings":
        """Runtime cross-field validation (S1.5 scope).

        Production hardening: debug mode and SQL echo would leak internal
        detail and sensitive parameters (ES-004 §12; ARCH-007 §23
        production environment purpose) and are therefore rejected at
        configuration-resolution time — the service refuses to start
        misconfigured rather than running insecurely (RA-011 §2 fail
        secure).
        """
        if self.environment == "production":
            if self.debug:
                raise ValueError("debug must be false in production (ES-004, ARCH-007)")
            if self.database_echo:
                raise ValueError(
                    "database_echo must be false in production (ES-004 §12)"
                )
            if self.cors_allowed_origins:
                raise ValueError(
                    "Production is same-origin only: cors_allowed_origins must be "
                    "empty (ADR-006; a superseding ADR is required to change this)"
                )
            if self.auth_jwt_secret == _DEV_JWT_SECRET:
                raise ValueError(
                    "auth_jwt_secret must be overridden via the secret layer in "
                    "production (ADR-004; RA-011 §2 fail secure)"
                )
        return self

    def feature_enabled(self, name: str, *, default: bool = False) -> bool:
        """Resolve a platform feature flag (IP-001 §10 Feature Flags)."""
        return self.features.get(name.lower(), default)

    def safe_dump(self) -> dict[str, Any]:
        """Redacted configuration snapshot for logs and diagnostics.

        Credential-bearing values are masked (ES-004 §12); safe fields
        pass through unchanged.
        """
        dumped = self.model_dump()
        for field_name in SENSITIVE_SETTINGS_FIELDS:
            value = dumped.get(field_name)
            if isinstance(value, str) and value:
                dumped[field_name] = mask_secret(value, visible=4)
        return dumped


def _read_config_file(layer: str) -> dict[str, Any]:
    """Read one configuration layer file; missing files yield an empty layer."""
    path = CONFIGS_DIR / layer / CONFIG_FILE_NAME
    if not path.is_file():
        return {}
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in configuration file {path}: {exc}") from exc
    if not isinstance(content, dict):
        raise ValueError(f"Configuration file {path} must contain a JSON object")
    return content


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge ``override`` onto ``base``; nested objects merge, scalars replace."""
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _environment_variable_layer() -> dict[str, Any]:
    """Collect environment variables for known fields (priority 1).

    Canonical unprefixed names (IP-002 §18) are read first; an
    ``ATLAS_``-prefixed variable overrides its canonical alias.
    ``ATLAS_FEATURE_*`` variables override individual feature flags.
    """
    layer: dict[str, Any] = {}
    for env_name, field_name in CANONICAL_ENV_ALIASES.items():
        env_value = os.environ.get(env_name)
        if env_value is not None:
            layer[field_name] = env_value
    for field_name in Settings.model_fields:
        env_value = os.environ.get(f"{ENV_PREFIX}{field_name.upper()}")
        if env_value is not None:
            layer[field_name] = env_value
    feature_overrides = parse_feature_flags_from_env(os.environ)
    if feature_overrides:
        layer["features"] = feature_overrides
    return layer


def _default_secret_providers() -> list[SecretProvider]:
    """Local providers for the Secret Store layer (S1.5 approved scope).

    Order matters within the layer: environment-injected secrets override
    the developer-local file. The external vault provider (BP-002 Secrets
    Service) replaces or extends this chain in its governing stage
    without changes to ``load_settings`` consumers.
    """
    return [
        LocalFileSecretProvider(CONFIGS_DIR),
        EnvironmentSecretProvider(os.environ),
    ]


def load_settings(
    secret_providers: list[SecretProvider] | None = None,
) -> Settings:
    """Resolve settings through the IP-001 §10 configuration hierarchy.

    Resolution order (lowest to highest priority):

    1. ``configs/base``                (base configuration — priority 4)
    2. ``configs/<environment>``       (environment configuration — priority 3)
    3. ``configs/local``               (developer overrides; part of the
       environment-configuration tier, applied above the shared files)
    4. Secret Store layer              (priority 2 — providers above)
    5. Environment variables           (priority 1)

    The active environment is selected by ``ATLAS_ENVIRONMENT``
    (default: ``development``).
    """
    environment = os.environ.get(f"{ENV_PREFIX}ENVIRONMENT", "development")
    providers = (
        secret_providers if secret_providers is not None else _default_secret_providers()
    )

    resolved: dict[str, Any] = {"environment": environment}
    resolved = _deep_merge(_read_config_file("base"), resolved)
    resolved = _deep_merge(resolved, _read_config_file(environment))
    resolved = _deep_merge(resolved, _read_config_file("local"))
    resolved = _deep_merge(
        resolved, resolve_secret_layer(providers, Settings.model_fields.keys())
    )
    resolved = _deep_merge(resolved, _environment_variable_layer())

    return Settings.model_validate(resolved)
