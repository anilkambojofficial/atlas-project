"""Unit tests — shared.telemetry metrics and shared.config file layers
(ES-007 §5)."""

from __future__ import annotations

import json
import logging as std_logging

import pytest

from shared.config import settings as settings_module
from shared.config.settings import _deep_merge, load_settings
from shared.logging.logger import JsonLogFormatter, configure_logging, get_logger
from shared.telemetry import MetricsRegistry


class TestMetricsRegistry:
    def test_render_includes_info_uptime_and_counts(self) -> None:
        registry = MetricsRegistry("atlas-backend", "0.1.0", "testing")
        registry.observe_request("GET", "/health", 200, 0.005)
        registry.observe_request("GET", "/health", 200, 0.007)
        registry.observe_request("POST", "/api/v1", 404, 0.001)
        output = registry.render()

        assert 'atlas_app_info{environment="testing"' in output
        assert "atlas_app_uptime_seconds" in output
        assert (
            'atlas_http_requests_total{method="GET",path="/health",status="200"} 2'
            in output
        )
        assert (
            'atlas_http_request_duration_seconds_count{method="GET",path="/health"} 2'
            in output
        )
        assert registry.uptime_seconds >= 0

    def test_label_values_are_escaped(self) -> None:
        registry = MetricsRegistry("svc", "1", "testing")
        registry.observe_request("GET", 'pa"th\n', 200, 0.001)
        rendered = registry.render()
        assert 'pa\\"th\\n' in rendered


class TestConfigFileLayers:
    def test_hierarchy_merge_and_precedence(self, tmp_path, monkeypatch) -> None:
        # Build a configs/ hierarchy per IP-001 §10: base < environment < local.
        for layer, content in {
            "base": {"port": 1111, "app_name": "Base Name"},
            "testing": {"port": 2222},
            "local": {"log_level": "WARNING"},
        }.items():
            (tmp_path / layer).mkdir()
            (tmp_path / layer / "backend.json").write_text(json.dumps(content))

        monkeypatch.setattr(settings_module, "CONFIGS_DIR", tmp_path)
        monkeypatch.setenv("ATLAS_ENVIRONMENT", "testing")
        settings = load_settings()

        assert settings.app_name == "Base Name"  # from base layer
        assert settings.port == 2222  # environment layer beats base
        assert settings.log_level == "WARNING"  # local layer beats both

        monkeypatch.setenv("ATLAS_PORT", "3333")  # env var beats every file
        assert load_settings().port == 3333

    def test_invalid_json_fails_fast(self, tmp_path, monkeypatch) -> None:
        (tmp_path / "base").mkdir()
        (tmp_path / "base" / "backend.json").write_text("{not json")
        monkeypatch.setattr(settings_module, "CONFIGS_DIR", tmp_path)
        with pytest.raises(ValueError):
            load_settings()

    def test_non_object_config_rejected(self, tmp_path, monkeypatch) -> None:
        (tmp_path / "base").mkdir()
        (tmp_path / "base" / "backend.json").write_text("[1, 2]")
        monkeypatch.setattr(settings_module, "CONFIGS_DIR", tmp_path)
        with pytest.raises(ValueError):
            load_settings()

    def test_deep_merge_nests(self) -> None:
        merged = _deep_merge({"a": {"x": 1, "y": 2}, "b": 1}, {"a": {"y": 3}})
        assert merged == {"a": {"x": 1, "y": 3}, "b": 1}


class TestLoggingConfiguration:
    def test_configure_logging_idempotent_and_trace_level(self) -> None:
        configure_logging("atlas-test", "TRACE")
        configure_logging("atlas-test", "TRACE")  # must not stack handlers
        root = std_logging.getLogger()
        atlas_handlers = [h for h in root.handlers if h.get_name() == "atlas-json"]
        assert len(atlas_handlers) == 1
        assert std_logging.getLevelName(5) == "TRACE"
        assert root.level == 5
        assert get_logger("x") is std_logging.getLogger("x")

    def test_exception_serialization(self) -> None:
        formatter = JsonLogFormatter("svc")
        try:
            raise ValueError("broken")
        except ValueError:
            import sys

            record = std_logging.LogRecord(
                name="t", level=std_logging.ERROR, pathname=__file__, lineno=1,
                msg="failed", args=(), exc_info=sys.exc_info(),
            )
        entry = json.loads(formatter.format(record))
        assert entry["exception"]["type"] == "ValueError"
        assert "broken" in entry["exception"]["message"]
        assert "Traceback" in entry["exception"]["stackTrace"]
