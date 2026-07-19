"""Celery worker application factory.

Governing documents:
- IP-001 §7 — Celery is part of the canonical backend stack; Redis is
  the platform's broker-capable store (worker broker/backend default to
  the configured Redis URL; overridable through the IP-001 §10
  configuration hierarchy).
- IP-001 §15 — UTC timezone, JSON serialization.
- IP-001 §12 / ADR-002 §5 — worker processes emit the platform's
  structured JSON logs (AUD-001 M-3 closed): the ``setup_logging``
  signal routes Celery through ``shared.logging`` instead of Celery's
  own logger tree.
- ADR-002 §2 — the transactional-outbox drain is scheduled by Celery
  beat at ``outbox_drain_interval_seconds``.

Run from ``backend/``:

    uv run celery -A workers.app worker --pool=solo --loglevel=info
    uv run celery -A workers.app beat --loglevel=info
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from celery import Celery
from celery.signals import setup_logging

from shared.config import Settings, load_settings
from shared.logging import configure_logging


@lru_cache(maxsize=1)
def worker_settings() -> Settings:
    """Lazily resolved settings shared by the worker process (one
    resolution per process; avoids import-time file I/O — AUD-001 L-5)."""
    return load_settings()


@setup_logging.connect
def _configure_worker_logging(**_kwargs: Any) -> None:
    """Route every worker log line through the platform JSON formatter
    (IP-001 §12; ADR-002 §5)."""
    settings = worker_settings()
    configure_logging(
        service_name=f"{settings.service_name}-worker",
        log_level=settings.log_level,
    )


def create_worker_app(settings: Settings) -> Celery:
    """Compose the platform Celery application from validated settings."""
    worker = Celery("atlas")
    worker.conf.update(
        broker_url=settings.worker_broker,
        result_backend=settings.worker_backend,
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
        task_default_queue="atlas.platform",
        broker_connection_retry_on_startup=True,
        worker_hijack_root_logger=False,
        task_track_started=True,
        result_expires=3600,
        beat_schedule={
            "platform-outbox-drain": {
                "task": "platform.outbox_drain",
                "schedule": float(settings.outbox_drain_interval_seconds),
                "options": {"queue": "atlas.platform"},
            },
        },
    )
    # Platform task modules; service task modules register here in their
    # governing Implementation Packs (IP-002 §17 onward).
    worker.conf.include = ["workers.tasks"]
    return worker


#: Module-level application consumed by ``celery -A workers.app``.
celery_app = create_worker_app(worker_settings())

#: Celery's default discovery attribute name.
app = celery_app
