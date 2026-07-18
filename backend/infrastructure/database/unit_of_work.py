"""Unit of Work pattern.

Governing documents:
- RA-001 §10 — a Unit of Work represents one business transaction and is
  responsible for transaction management, change tracking (delegated to
  the SQLAlchemy session), commit, rollback, and event collection.
- RA-001 §13 — one business use case per transaction; integration events
  are published only after successful commit.
- RA-006 §10 — the transactional Outbox pattern supersedes the direct
  post-commit publisher when the Event Platform foundation lands
  (Sprint-001 S1.4 events package); the ``event_publisher`` seam below is
  where the outbox writer plugs in without changing call sites.
"""

from __future__ import annotations

from types import TracebackType
from typing import Any, Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from shared.logging import get_logger

_logger = get_logger("atlas.infrastructure.unit_of_work")

#: Publishes one collected event after a successful commit.
EventPublisher = Callable[[Any], Awaitable[None]]


class UnitOfWork:
    """Async context manager scoping one business transaction (RA-001 §10)."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        event_publisher: EventPublisher | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._event_publisher = event_publisher
        self._events: list[Any] = []
        self._session: AsyncSession | None = None

    @property
    def session(self) -> AsyncSession:
        """The transaction's session; valid only inside the context."""
        if self._session is None:
            raise RuntimeError("UnitOfWork used outside of its async context")
        return self._session

    def collect_event(self, event: Any) -> None:
        """Queue a domain event for publication after successful commit
        (RA-001 §10 event collection, §13 publish-after-commit)."""
        self._events.append(event)

    async def commit(self) -> None:
        """Commit the transaction, then publish collected events."""
        await self.session.commit()
        await self._publish_events()

    async def rollback(self) -> None:
        """Roll back the transaction and discard collected events."""
        await self.session.rollback()
        self._events.clear()

    async def _publish_events(self) -> None:
        if not self._event_publisher:
            self._events.clear()
            return
        events, self._events = self._events, []
        for event in events:
            try:
                await self._event_publisher(event)
            except Exception as exc:  # noqa: BLE001 — a publish failure must not
                # roll back the already-committed business transaction
                # (RA-001 §13); it is logged for the observability platform.
                _logger.error(
                    "Post-commit event publication failed",
                    exc_info=exc,
                    extra={"eventType": type(event).__name__},
                )

    async def __aenter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self.session.close()
            self._session = None
