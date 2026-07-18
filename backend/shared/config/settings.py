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

from pydantic import BaseModel, Field, field_validator

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
    """Collect environment variables for known fields.

    Canonical unprefixed names (IP-002 §18) are read first; an
    ``ATLAS_``-prefixed variable overrides its canonical alias.
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
    return layer


def load_settings() -> Settings:
    """Resolve settings through the IP-001 §10 configuration hierarchy.

    Resolution order (lowest to highest priority):
    ``configs/base`` -> ``configs/<environment>`` -> ``configs/local``
    -> environment variables. The active environment is selected by
    ``ATLAS_ENVIRONMENT`` (default: ``development``).
    """
    environment = os.environ.get(f"{ENV_PREFIX}ENVIRONMENT", "development")

    resolved: dict[str, Any] = {"environment": environment}
    resolved = _deep_merge(_read_config_file("base"), resolved)
    resolved = _deep_merge(resolved, _read_config_file(environment))
    resolved = _deep_merge(resolved, _read_config_file("local"))
    resolved = _deep_merge(resolved, _environment_variable_layer())

    return Settings.model_validate(resolved)
