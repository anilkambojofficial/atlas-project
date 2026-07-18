"""Redis connection management.

Governing documents:
- IP-001 §7 — Redis is the platform cache technology.
- IP-001 §14 — health checks validate the Redis dependency.
- RA-005 §9 / ARCH-004 §11 — the cache is an optimization layer and
  never the system of record; explicit expiration and tenant-scoped
  keys are enforced by the consuming services (IP-002 §16 onward).
"""

from __future__ import annotations

from redis.asyncio import Redis

from shared.config import Settings
from shared.logging import get_logger

_logger = get_logger("atlas.infrastructure.redis")


class RedisManager:
    """Owns the application-scoped async Redis client."""

    def __init__(self, settings: Settings) -> None:
        self._client: Redis = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=settings.redis_timeout_seconds,
            socket_timeout=settings.redis_timeout_seconds,
        )

    @property
    def client(self) -> Redis:
        """The shared async Redis client (injected, never re-created)."""
        return self._client

    async def ping(self) -> None:
        """Round-trip PING; raises on connectivity failure."""
        await self._client.ping()

    async def health_check(self) -> tuple[bool, str]:
        """Redis health check (IP-001 §14)."""
        try:
            await self.ping()
        except Exception as exc:  # noqa: BLE001 — probe converts failures to status
            return False, f"connection failed: {type(exc).__name__}"
        return True, "connected"

    async def close(self) -> None:
        """Close the client and its connection pool (application shutdown)."""
        await self._client.aclose()
        _logger.info("Redis client closed")
