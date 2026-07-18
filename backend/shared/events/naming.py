"""Event naming and topic conventions.

Governing documents:
- BP-004 §11 — the concrete versioned event-name pattern used by the
  approved Build Packs: ``<domain>.<event>.v<n>`` (with optional
  underscore-separated event words), e.g. ``organization.activated.v1``,
  ``subscription.plan_changed.v1``, ``tenant.isolation_violation_detected.v1``.
- RA-006 §19 — naming standards are centrally governed; §21 — every
  event is registered in the Enterprise Event Catalog (the catalog
  service itself arrives with the Event Platform stages; the naming rule
  is enforceable now).
- ``shared.constants.EVENT_TOPIC_PREFIX`` — topics are namespaced
  ``atlas.<domain>`` so per-domain ordering by key remains possible
  (RA-006 §13 aggregate/partition ordering).
"""

from __future__ import annotations

import re

from shared.constants import EVENT_TOPIC_PREFIX
from shared.exceptions import ValidationError

#: ``<domain>.<event>.v<n>`` — lowercase segments, underscores within words.
_EVENT_TYPE_PATTERN = re.compile(
    r"^[a-z][a-z0-9]*(_[a-z0-9]+)*"  # domain
    r"(\.[a-z][a-z0-9]*(_[a-z0-9]+)*)+"  # one or more event segments
    r"\.v[1-9][0-9]*$"  # version suffix
)


def validate_event_type(event_type: str) -> None:
    """Validate the BP-004 §11 event-type pattern; raise on violation."""
    if not isinstance(event_type, str) or not _EVENT_TYPE_PATTERN.match(event_type):
        raise ValidationError(
            "Invalid event type.",
            details=[
                {
                    "field": "eventType",
                    "issue": "must match '<domain>.<event>.v<n>' (BP-004 §11)",
                }
            ],
        )


def topic_for(event_type: str) -> str:
    """Resolve the Kafka topic for an event type: ``atlas.<domain>``."""
    validate_event_type(event_type)
    domain = event_type.split(".", 1)[0]
    return f"{EVENT_TOPIC_PREFIX}.{domain}"
