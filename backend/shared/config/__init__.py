"""Shared configuration package (IP-001 §9 — config package)."""

from shared.config.features import (
    FEATURE_ENV_PREFIX,
    coerce_flag_value,
    parse_feature_flags_from_env,
)
from shared.config.secrets import (
    SECRET_ENV_PREFIX,
    EnvironmentSecretProvider,
    LocalFileSecretProvider,
    SecretProvider,
    resolve_secret_layer,
)
from shared.config.settings import Environment, Settings, load_settings

__all__ = [
    "FEATURE_ENV_PREFIX",
    "SECRET_ENV_PREFIX",
    "Environment",
    "EnvironmentSecretProvider",
    "LocalFileSecretProvider",
    "SecretProvider",
    "Settings",
    "coerce_flag_value",
    "load_settings",
    "parse_feature_flags_from_env",
    "resolve_secret_layer",
]
