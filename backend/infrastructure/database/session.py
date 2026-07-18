"""Request-scoped database session management.

Governing documents:
- IP-001 §11 — dependencies (Database category) are injected, never
  constructed by handlers.
- RA-001 §13 — transaction boundaries belong to application services;
  the request-scoped session therefore does not auto-commit. Application
  services own commits explicitly through the Unit of Work
  (``infrastructure.database.unit_of_work``).
"""

from __future__ import annotations

from typing import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session(request: Request) -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding one session per request.

    The session is rolled back on unhandled failure and always closed;
    committing is the explicit responsibility of the application-service
    transaction boundary (RA-001 §7, §13).
    """
    factory = request.app.state.container.database.session_factory
    async with factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
