"""Shared structured logging package (IP-001 §9 — logging package)."""

from shared.logging.context import (
    RequestContext,
    bind_request_context,
    clear_request_context,
    get_correlation_id,
    get_request_context,
)
from shared.logging.logger import TRACE_LEVEL, configure_logging, get_logger

__all__ = [
    "TRACE_LEVEL",
    "RequestContext",
    "bind_request_context",
    "clear_request_context",
    "configure_logging",
    "get_correlation_id",
    "get_logger",
    "get_request_context",
]
