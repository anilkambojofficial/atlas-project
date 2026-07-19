"""Secret management interfaces and local providers.

Governing documents:
- IP-001 §10 — configuration priority: Environment Variables > Secret
  Store > Environment Configuration > Base Configuration. This module
  supplies the Secret Store layer of that chain.
- ES-004 §12 / RA-011 §10 — secrets never live in source code or
  committed configuration; access is interface-based so the external
  vault integration (BP-002 §8.4 Secrets Service; provider selection is
  "Implementation Defined During Engineering") can replace the local
  providers without touching consumers.
- Approved S1.5 scope — interfaces plus local development providers
  only; no external secret-provider integration yet.

Two local providers implement the interface:

- ``EnvironmentSecretProvider`` — reads ``ATLAS_SECRET_<FIELD>``
  variables (the injection style used by container/Kubernetes secret
  mounts per IP-001 §17).
- ``LocalFileSecretProvider`` — reads ``configs/local/secrets.json``
  (developer-only; the ``configs/local/`` layer is excluded from
  version control).

Providers return field→value mappings restricted to known settings
fields; secret *values* are never logged (ES-004 §12).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping, Protocol, runtime_checkable

from shared.logging import get_logger

_logger = get_logger("atlas.shared.config.secrets")

#: Environment variables carrying secrets use this prefix,
#: e.g. ``ATLAS_SECRET_DATABASE_URL``.
SECRET_ENV_PREFIX = "ATLAS_SECRET_"

#: File name of the developer-local secret source inside ``configs/local``.
LOCAL_SECRETS_FILE = "secrets.json"


@runtime_checkable
class SecretProvider(Protocol):
    """Supplies the Secret Store layer of the configuration chain."""

    def get_secrets(self, field_names: Iterable[str]) -> dict[str, str]:  # pragma: no cover
        """Return values for any of ``field_names`` this provider holds."""
        ...


class EnvironmentSecretProvider:
    """Secrets injected as ``ATLAS_SECRET_<FIELD>`` environment variables."""

    def __init__(self, environ: Mapping[str, str]) -> None:
        self._environ = environ

    def get_secrets(self, field_names: Iterable[str]) -> dict[str, str]:
        secrets: dict[str, str] = {}
        for field_name in field_names:
            value = self._environ.get(f"{SECRET_ENV_PREFIX}{field_name.upper()}")
            if value is not None:
                secrets[field_name] = value
        return secrets


class LocalFileSecretProvider:
    """Developer-local secrets from ``configs/local/secrets.json``.

    The file is optional and excluded from version control; unknown keys
    are ignored with a warning (key names only — never values, ES-004 §12).
    """

    def __init__(self, configs_dir: Path) -> None:
        self._path = configs_dir / "local" / LOCAL_SECRETS_FILE

    def get_secrets(self, field_names: Iterable[str]) -> dict[str, str]:
        if not self._path.is_file():
            return {}
        try:
            content = json.loads(self._path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON in local secrets file {self._path}: {exc}"
            ) from exc
        if not isinstance(content, dict):
            raise ValueError(
                f"Local secrets file {self._path} must contain a JSON object"
            )

        known = set(field_names)
        secrets: dict[str, str] = {}
        for key, value in content.items():
            if key not in known:
                _logger.warning(
                    "Ignoring unknown key in local secrets file",
                    extra={"configKey": key},
                )
                continue
            secrets[key] = str(value)
        return secrets


def resolve_secret_layer(
    providers: Iterable[SecretProvider], field_names: Iterable[str]
) -> dict[str, str]:
    """Merge providers in order; later providers win within the layer."""
    fields = tuple(field_names)
    layer: dict[str, str] = {}
    for provider in providers:
        layer.update(provider.get_secrets(fields))
    return layer
