"""Feature flags foundation — platform scope.

Governing documents:
- IP-001 §10 / ES-001 §11 / ARCH-007 §10 — Feature Flags are a first-class
  configuration category resolved through the configuration hierarchy.
- ARCH-002 §8 / RA-009 §12 — *tenant-scoped* feature management (feature
  enablement per organization, subscription-driven) is owned by the
  Tenant Platform (BP-004 Entitlement/Feature services, IP-003). This
  module is deliberately platform-scoped only: flags that gate platform
  behavior per environment, not per tenant.

Flags resolve through the same IP-001 §10 chain as every other setting:
``features`` objects in the configuration files, overridden per flag by
``ATLAS_FEATURE_<NAME>`` environment variables.
"""

from __future__ import annotations

from typing import Mapping

from shared.exceptions import ValidationError

#: Per-flag environment override, e.g. ``ATLAS_FEATURE_QUERY_DEVTOOLS=true``.
FEATURE_ENV_PREFIX = "ATLAS_FEATURE_"

_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
_FALSE_VALUES = frozenset({"0", "false", "no", "off"})


def coerce_flag_value(raw: str | bool, *, flag: str) -> bool:
    """Coerce a raw flag value to bool; reject ambiguous input."""
    if isinstance(raw, bool):
        return raw
    lowered = str(raw).strip().lower()
    if lowered in _TRUE_VALUES:
        return True
    if lowered in _FALSE_VALUES:
        return False
    raise ValidationError(
        f"Invalid feature flag value for '{flag}'.",
        details=[
            {
                "field": f"features.{flag}",
                "issue": "must be one of: 1/0, true/false, yes/no, on/off",
            }
        ],
    )


def parse_feature_flags_from_env(environ: Mapping[str, str]) -> dict[str, bool]:
    """Collect ``ATLAS_FEATURE_*`` overrides as a normalized flag mapping.

    Flag names are normalized to lowercase snake_case (ES-001 §7 naming).
    """
    flags: dict[str, bool] = {}
    for key, value in environ.items():
        if not key.startswith(FEATURE_ENV_PREFIX):
            continue
        name = key.removeprefix(FEATURE_ENV_PREFIX).lower()
        if name:
            flags[name] = coerce_flag_value(value, flag=name)
    return flags


def normalize_feature_mapping(raw: Mapping[str, object]) -> dict[str, bool]:
    """Validate a ``features`` object from a configuration layer."""
    return {
        str(name).lower(): coerce_flag_value(value, flag=str(name))  # type: ignore[arg-type]
        for name, value in raw.items()
    }
