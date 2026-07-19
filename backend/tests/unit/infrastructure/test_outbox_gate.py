"""ADR-002 gate tests: typed collection + outbox-in-transaction staging.

Deterministic and network-free (ES-007 §5): the session factory is faked;
no database or broker is touched.
"""

from __future__ import annotations

from datetime import timedelta

import pytest

from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.messaging.outbox_model import OutboxRecord
from shared.events import EventCategory, EventEnvelope
from workers.outbox import _next_attempt_delay


def _envelope() -> EventEnvelope:
    return EventEnvelope.create(
        event_type="identity.user.registered.v1",
        category=EventCategory.DOMAIN,
        producer="atlas-backend-test",
        organization_id="0198f5a0-0000-7000-8000-000000000001",
        payload={"userId": "u-1"},
    )


class FakeSession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def add(self, obj: object) -> None:
        self.added.append(obj)

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True

    async def close(self) -> None:
        self.closed = True


class FakeSessionFactory:
    def __init__(self) -> None:
        self.session = FakeSession()

    def __call__(self) -> FakeSession:
        return self.session


class TestTypedCollection:
    def test_non_envelope_rejected_before_commit(self) -> None:
        uow = UnitOfWork(FakeSessionFactory())  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="ADR-002"):
            uow.collect_event({"eventType": "identity.user.registered.v1"})  # type: ignore[arg-type]

    def test_envelope_accepted(self) -> None:
        uow = UnitOfWork(FakeSessionFactory())  # type: ignore[arg-type]
        uow.collect_event(_envelope())


class TestOutboxStaging:
    @pytest.mark.asyncio
    async def test_commit_stages_outbox_record_in_transaction(self) -> None:
        factory = FakeSessionFactory()
        envelope = _envelope()
        async with UnitOfWork(factory) as uow:  # type: ignore[arg-type]
            uow.collect_event(envelope)
        session = factory.session
        assert session.committed and session.closed
        records = [obj for obj in session.added if isinstance(obj, OutboxRecord)]
        assert len(records) == 1
        record = records[0]
        assert record.event_id == envelope.event_id
        assert record.event_type == "identity.user.registered.v1"
        assert record.organization_id == envelope.organization_id
        assert record.envelope["eventId"] == envelope.event_id

    @pytest.mark.asyncio
    async def test_rollback_discards_events(self) -> None:
        factory = FakeSessionFactory()
        with pytest.raises(RuntimeError, match="boom"):
            async with UnitOfWork(factory) as uow:  # type: ignore[arg-type]
                uow.collect_event(_envelope())
                raise RuntimeError("boom")
        session = factory.session
        assert session.rolled_back and not session.committed
        assert not [o for o in session.added if isinstance(o, OutboxRecord)]


class TestDrainBackoff:
    def test_backoff_grows_and_caps(self) -> None:
        assert _next_attempt_delay(1) == timedelta(seconds=4)
        assert _next_attempt_delay(3) == timedelta(seconds=16)
        assert _next_attempt_delay(30) == timedelta(seconds=300)
