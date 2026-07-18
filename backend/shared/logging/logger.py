"""Structured JSON logging framework.

Governing documents:
- IP-001 §12 — machine-readable structured logs; mandatory fields:
  Timestamp, Correlation ID, Request ID, Tenant ID, User ID, Service Name,
  Severity, Message, Exception (if applicable); levels TRACE through
  CRITICAL.
- ES-001 §12 / ARCH-007 §16 — structured JSON format; sensitive
  information shall never be logged.
"""

from __future__ import annotations

import json
import logging
import sys
import traceback
from datetime import datetime, timezone
from typing import Any

from shared.logging.context import get_request_context
from shared.security import REDACTED as _REDACTED_MARKER
from shared.security import is_sensitive_key

#: IP-001 §12 requires a TRACE level below DEBUG; stdlib logging lacks one.
TRACE_LEVEL = 5

#: Log-record attributes that belong to the stdlib record itself; anything
#: else passed via ``extra=`` is treated as a structured field.
_STANDARD_RECORD_ATTRS = frozenset(
    {
        "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
        "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
        "created", "msecs", "relativeCreated", "thread", "threadName",
        "processName", "process", "taskName", "message", "asctime",
    }
)

# Redaction is centralized in shared.security (S1.4 relocation; ES-004 §12).


class JsonLogFormatter(logging.Formatter):
    """Render every log record as a single JSON object per line."""

    def __init__(self, service_name: str) -> None:
        super().__init__()
        self._service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        context = get_request_context()
        entry: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "severity": record.levelname,
            "service": self._service_name,
            "logger": record.name,
            "message": record.getMessage(),
            "correlationId": context.correlation_id,
            "requestId": context.request_id,
            "tenantId": context.tenant_id,
            "userId": context.user_id,
        }

        for key, value in record.__dict__.items():
            if key in _STANDARD_RECORD_ATTRS or key.startswith("_"):
                continue
            entry[key] = _REDACTED_MARKER if is_sensitive_key(key) else value

        if record.exc_info and record.exc_info[0] is not None:
            entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "stackTrace": "".join(traceback.format_exception(*record.exc_info)),
            }

        return json.dumps(entry, default=str)


def configure_logging(service_name: str, log_level: str) -> None:
    """Install the structured JSON handler on the root logger.

    Idempotent: repeated calls replace the platform handler rather than
    stacking duplicates.
    """
    if logging.getLevelName(TRACE_LEVEL) != "TRACE":
        logging.addLevelName(TRACE_LEVEL, "TRACE")

    level = TRACE_LEVEL if log_level.upper() == "TRACE" else log_level.upper()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonLogFormatter(service_name))
    handler.set_name("atlas-json")

    root = logging.getLogger()
    root.handlers = [h for h in root.handlers if h.get_name() != "atlas-json"]
    root.addHandler(handler)
    root.setLevel(level)

    # Route uvicorn loggers through the structured root handler so every
    # emitted line is machine-readable JSON (IP-001 §12).
    for uvicorn_logger in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(uvicorn_logger).handlers = []
        logging.getLogger(uvicorn_logger).propagate = True


def get_logger(name: str) -> logging.Logger:
    """Return a named logger bound to the platform logging configuration."""
    return logging.getLogger(name)
