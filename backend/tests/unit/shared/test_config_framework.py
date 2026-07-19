"""Unit tests — S1.5 Configuration Framework (ES-007 §5).

Covers: secret layer priority (IP-001 §10), local secret providers,
feature flags foundation, runtime production-safety validation,
scheme validation, redacted introspection, and the shipped environment
profiles in ``configs/``.
"""

from __future__ import annotations

import json

import pytest

from shared.config import settings as settings_module
from shared.config.features import (
    coerce_flag_value,
    normalize_feature_mapping,
    parse_feature_flags_from_env,
)
from shared.config.secrets import (
    EnvironmentSecretProvider,
    LocalFileSecretProvider,
    SecretProvider,
    resolve_secret_layer,
)
from shared.config.settings import SENSITIVE_SETTINGS_FIELDS, Settings, load_settings
from shared.exceptions import ValidationError


def _write_layer(tmp_path, layer: str, content: dict) -> None:
    (tmp_path / layer).mkdir(exist_ok=True)
    (tmp_path / layer / "backend.json").write_text(json.dumps(content))


class TestSecretProviders:
    def test_environment_secret_provider_reads_prefixed_vars(self) -> None:
        provider = EnvironmentSecretProvider(
            {"ATLAS_SECRET_DATABASE_URL": "postgresql+asyncpg://s/secret", "OTHER": "x"}
        )
        assert provider.get_secrets(["database_url", "port"]) == {
            "database_url": "postgresql+asyncpg://s/secret"
        }
        assert isinstance(provider, SecretProvider)

    def test_local_file_provider_filters_unknown_keys(self, tmp_path) -> None:
        (tmp_path / "local").mkdir()
        (tmp_path / "local" / "secrets.json").write_text(
            json.dumps({"database_url": "postgresql+asyncpg://f/file", "bogus": "x"})
        )
        provider = LocalFileSecretProvider(tmp_path)
        assert provider.get_secrets(["database_url"]) == {
            "database_url": "postgresql+asyncpg://f/file"
        }

    def test_local_file_provider_missing_file_is_empty(self, tmp_path) -> None:
        assert LocalFileSecretProvider(tmp_path).get_secrets(["database_url"]) == {}

    def test_local_file_provider_rejects_invalid_content(self, tmp_path) -> None:
        (tmp_path / "local").mkdir()
        secrets_file = tmp_path / "local" / "secrets.json"
        secrets_file.write_text("{broken")
        with pytest.raises(ValueError):
            LocalFileSecretProvider(tmp_path).get_secrets(["database_url"])
        secrets_file.write_text("[1]")
        with pytest.raises(ValueError):
            LocalFileSecretProvider(tmp_path).get_secrets(["database_url"])

    def test_resolve_secret_layer_later_provider_wins(self) -> None:
        first = EnvironmentSecretProvider({"ATLAS_SECRET_PORT": "1111"})
        second = EnvironmentSecretProvider({"ATLAS_SECRET_PORT": "2222"})
        layer = resolve_secret_layer([first, second], ["port"])
        assert layer == {"port": "2222"}


class TestHierarchyPriority:
    """IP-001 §10: env vars > secret store > env config > base."""

    def test_secret_layer_beats_files_and_loses_to_env_vars(
        self, tmp_path, monkeypatch
    ) -> None:
        _write_layer(tmp_path, "base", {"port": 1000})
        _write_layer(tmp_path, "development", {"port": 2000})
        (tmp_path / "local").mkdir()
        (tmp_path / "local" / "secrets.json").write_text(json.dumps({"port": "3000"}))
        monkeypatch.setattr(settings_module, "CONFIGS_DIR", tmp_path)

        # Secret layer (priority 2) beats environment configuration (3).
        assert load_settings().port == 3000

        # Environment variables (priority 1) beat the secret layer.
        monkeypatch.setenv("ATLAS_PORT", "4000")
        assert load_settings().port == 4000

    def test_injected_providers_are_used(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setattr(settings_module, "CONFIGS_DIR", tmp_path)
        provider = EnvironmentSecretProvider(
            {"ATLAS_SECRET_REDIS_URL": "redis://vault:6379/9"}
        )
        settings = load_settings(secret_providers=[provider])
        assert settings.redis_url == "redis://vault:6379/9"


class TestFeatureFlags:
    def test_coercion_accepts_documented_forms(self) -> None:
        for truthy in ("1", "true", "YES", "On", True):
            assert coerce_flag_value(truthy, flag="f") is True
        for falsy in ("0", "false", "NO", "Off", False):
            assert coerce_flag_value(falsy, flag="f") is False
        with pytest.raises(ValidationError):
            coerce_flag_value("maybe", flag="f")

    def test_env_parsing_normalizes_names(self) -> None:
        flags = parse_feature_flags_from_env(
            {"ATLAS_FEATURE_QUERY_DEVTOOLS": "true", "ATLAS_PORT": "1", "ATLAS_FEATURE_": "1"}
        )
        assert flags == {"query_devtools": True}

    def test_normalize_feature_mapping(self) -> None:
        assert normalize_feature_mapping({"Alpha": "on", "beta": False}) == {
            "alpha": True,
            "beta": False,
        }

    def test_flags_resolve_through_hierarchy(self, tmp_path, monkeypatch) -> None:
        _write_layer(
            tmp_path, "base", {"features": {"alpha": True, "beta": False}}
        )
        monkeypatch.setattr(settings_module, "CONFIGS_DIR", tmp_path)
        settings = load_settings()
        assert settings.feature_enabled("alpha") is True
        assert settings.feature_enabled("beta") is False
        assert settings.feature_enabled("missing") is False
        assert settings.feature_enabled("missing", default=True) is True

        monkeypatch.setenv("ATLAS_FEATURE_BETA", "true")
        assert load_settings().feature_enabled("beta") is True


class TestRuntimeValidation:
    def test_production_rejects_debug(self) -> None:
        with pytest.raises(Exception, match="debug"):
            Settings(environment="production", debug=True)

    def test_production_rejects_database_echo(self) -> None:
        with pytest.raises(Exception, match="database_echo"):
            Settings(environment="production", database_echo=True)

    def test_production_valid_when_hardened(self) -> None:
        settings = Settings(environment="production", debug=False, database_echo=False)
        assert settings.environment == "production"

    def test_database_scheme_enforced(self) -> None:
        with pytest.raises(Exception, match="postgresql\\+asyncpg"):
            Settings(database_url="mysql://nope")

    def test_redis_scheme_enforced(self) -> None:
        with pytest.raises(Exception, match="redis"):
            Settings(redis_url="http://nope")

    def test_safe_dump_masks_sensitive_fields(self) -> None:
        settings = Settings(
            database_url="postgresql+asyncpg://user:hunter2@db:5432/atlas"
        )
        dumped = settings.safe_dump()
        assert "hunter2" not in json.dumps(dumped)
        assert dumped["database_url"].endswith("tlas")  # masked, last 4 visible
        assert dumped["port"] == settings.port  # non-sensitive untouched
        assert SENSITIVE_SETTINGS_FIELDS <= set(Settings.model_fields.keys())


class TestShippedProfiles:
    """The committed configs/ profiles must parse and satisfy validation."""

    @pytest.mark.parametrize(
        "environment", ["development", "testing", "staging", "production"]
    )
    def test_each_profile_resolves(self, environment, monkeypatch) -> None:
        monkeypatch.setenv("ATLAS_ENVIRONMENT", environment)
        settings = load_settings(secret_providers=[])
        assert settings.environment == environment
        if environment == "production":
            assert settings.debug is False
            assert settings.database_echo is False
        if environment == "development":
            assert settings.debug is True
