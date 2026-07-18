"""Async PostgreSQL engine and connection management.

Governing documents:
- IP-001 §7/§15 — PostgreSQL with SQLAlchemy 2.x.
- IP-001 §14 — health checks validate the database dependency.
- ES-003 §1 — data integrity and consistency take precedence; pooled,
  pre-pinged connections keep failures observable rather than silent.
- RA-001 §5 — persistence concerns are isolated in the infrastructure
  layer.
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shared.config import Settings
from shared.logging import get_logger

_logger = get_logger("atlas.infrastructure.database")


class DatabaseManager:
    """Owns the async engine and session factory for one application."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine: AsyncEngine = create_async_engine(
            settings.database_url,
            echo=settings.database_echo,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            pool_pre_ping=True,
            connect_args={"timeout": settings.database_connect_timeout_seconds},
        )
        self._session_factory = async_sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )

    @property
    def engine(self) -> AsyncEngine:
        """The application-scoped async engine."""
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Factory producing request/unit-of-work scoped sessions."""
        return self._session_factory

    async def ping(self) -> None:
        """Execute ``SELECT 1``; raises on connectivity failure."""
        async with self._engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

    async def health_check(self) -> tuple[bool, str]:
        """Database health check (IP-001 §14)."""
        try:
            await self.ping()
        except Exception as exc:  # noqa: BLE001 — probe converts failures to status
            return False, f"connection failed: {type(exc).__name__}"
        return True, "connected"

    async def dispose(self) -> None:
        """Release every pooled connection (application shutdown)."""
        await self._engine.dispose()
        _logger.info("Database engine disposed")
