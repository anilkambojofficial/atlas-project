"""Celery worker application factory.

Governing documents:
- IP-001 §7 — Celery is part of the canonical backend stack; Redis is
  the platform's broker-capable store (worker broker/backend default to
  the configured Redis URL; overridable through the IP-001 §10
  configuration hierarchy).
- IP-001 §15 — UTC timezone, JSON serialization.
- IP-001 §12 — the worker does not hijack the root logger so structured
  platform logging remains in effect.

Run a worker from ``backend/``:

    uv run celery -A workers.app worker --pool=solo --loglevel=info
"""

from __future__ import annotations

from celery import Celery

from shared.config import Settings, load_settings


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
    )
    # Platform task modules; service task modules register here in their
    # governing Implementation Packs (IP-002 §17 onward).
    worker.conf.include = ["workers.tasks"]
    return worker


#: Module-level application consumed by ``celery -A workers.app``.
celery_app = create_worker_app(load_settings())

#: Celery's default discovery attribute name.
app = celery_app
