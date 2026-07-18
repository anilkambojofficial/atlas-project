"""Background worker foundation (IP-001 §6 — ``backend/workers/``).

Celery is the platform background-processing runtime (IP-001 §7).
This package provides the configured worker application only; business
jobs are registered by their owning services in later Implementation
Packs (IP-002 §17 onward). Workers must remain idempotent and
retry-safe (IP-002 §17 rule, applied platform-wide).
"""
