"""Unit of Work pattern.

Governing documents:
- RA-001 §10 — a Unit of Work represents one business transaction and is
  responsible for transaction management, change tracking (delegated to
  the SQLAlchemy session), commit, rollback, and event collection.
- RA-001 §13 — one business use case per transaction.
- RA-006 §10 / ADR-002 — transactional Outbox: collected envelopes are
  persisted as outbox records inside the same transaction as the business
  state change; the drain worker (``workers.outbox``) publishes them with
  retry. Direct post-commit publishing is retired for transactional
  events (AUD-001 C-1 closed).
- ADR-002 §3 — ``collect_event`` is typed and fail-fast: a non-envelope
  event fails the use case loudly before commit (AUD-001 H-6 closed).
"""

from __future__ import annotations

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infrastructure.messaging.outbox_model import OutboxRecord
from shared.events import EventEnvelope
from shared.logging import get_logger

_logger = get_logger("atlas.infrastructure.unit_of_work")


class UnitOfWork:
    """Async context manager scoping one business transaction (RA-001 §10)."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session_factory = session_factory
        self._events: list[EventEnvelope] = []
        self._session: AsyncSession | None = None

    @property
    def session(self) -> AsyncSession:
        """The transaction's session; valid only inside the context."""
        if self._session is None:
            raise RuntimeError("UnitOfWork used outside of its async context")
        return self._session

    def collect_event(self, event: EventEnvelope) -> None:
        """Queue a governed envelope for outbox persistence at commit
        (RA-001 §10 event collection; ADR-002 §1/§3)."""
        if not isinstance(event, EventEnvelope):
            raise TypeError(
                "collect_event accepts shared.events.EventEnvelope only "
                f"(ADR-002 §3); got {type(event).__name__}"
            )
        self._events.append(event)

    async def commit(self) -> None:
        """Persist collected envelopes to the outbox, then commit — one
        atomic transaction (RA-006 §10; ADR-002 §1)."""
        self._stage_outbox_records()
        await self.session.commit()

    async def rollback(self) -> None:
        """Roll back the transaction and discard collected events."""
        await self.session.rollback()
        self._events.clear()

    def _stage_outbox_records(self) -> None:
        events, self._events = self._events, []
        for envelope in events:
            self.session.add(
                OutboxRecord(
                    event_id=envelope.event_id,
                    event_type=envelope.event_type,
                    organization_id=envelope.organization_id,
                    envelope=envelope.to_wire(),
                )
            )
        if events:
            _logger.debug(
                "Staged outbox records",
                extra={"count": len(events)},
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
