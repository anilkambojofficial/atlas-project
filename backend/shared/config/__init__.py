"""Shared configuration package (IP-001 §9 — config package)."""

from shared.config.settings import Environment, Settings, load_settings

__all__ = ["Environment", "Settings", "load_settings"]
