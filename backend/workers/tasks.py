"""Platform operational tasks.

Governing documents:
- IP-001 §14 — operational verification surface for the worker runtime;
  ``platform.ping`` proves broker round-trip, task execution, and result
  backend without touching any business capability.
- Business tasks are prohibited here; they belong to their owning
  services' ``workers/`` modules (IP-002 §17 onward).
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from workers.app import celery_app, worker_settings


@celery_app.task(name="platform.ping")
def ping() -> dict[str, Any]:
    """Operational round-trip task used by deployment and health tooling."""
    return {
        "status": "pong",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@celery_app.task(name="platform.outbox_drain")
def outbox_drain() -> dict[str, int]:
    """Drain one batch of the transactional outbox (ADR-002 §2).

    Scheduled by Celery beat at ``outbox_drain_interval_seconds``; may
    also be invoked ad hoc by operational tooling.
    """
    from workers.outbox import drain_outbox_once

    return asyncio.run(drain_outbox_once(worker_settings()))
