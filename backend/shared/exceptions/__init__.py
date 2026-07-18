"""Shared platform exception taxonomy (IP-001 §9 — exceptions package)."""

from shared.exceptions.errors import (
    AIError,
    AtlasError,
    AuthenticationError,
    AuthorizationError,
    BusinessError,
    ExternalServiceError,
    InfrastructureError,
    NotFoundError,
    ValidationError,
)

__all__ = [
    "AIError",
    "AtlasError",
    "AuthenticationError",
    "AuthorizationError",
    "BusinessError",
    "ExternalServiceError",
    "InfrastructureError",
    "NotFoundError",
    "ValidationError",
]
