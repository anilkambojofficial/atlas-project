"""Regression tests: security mutations commit despite rejected requests.

Defect found in S2-04 live verification: family revocation (token-reuse
theft response) and failed-login lockout counters were rolled back by the
Unit of Work's exception path. The services must commit security state
before raising (RA-011 §2 fail secure).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest

from apps.identity import security
from apps.identity.models import RefreshSession, User, UserStatus
from apps.identity.services import AuthenticationService
from shared.config import Settings
from shared.exceptions import AuthenticationError
from shared.utils import uuid7


class _Result:
    def __init__(self, rows: list) -> None:
        self._rows = rows

    def scalar_one_or_none(self):
        return self._rows[0] if self._rows else None

    def scalars(self):
        return self

    def all(self):
        return list(self._rows)


class FakeSession:
    """Programmable async-session fake: maps model class -> row list."""

    def __init__(self, rows_by_model: dict[type, list]) -> None:
        self._rows = rows_by_model
        self.added: list = []
        self.commits = 0
        self.rolled_back = False

    def add(self, obj) -> None:
        self.added.append(obj)

    async def execute(self, statement) -> _Result:
        model = statement.column_descriptions[0]["entity"]
        return _Result(self._rows.get(model, []))

    async def flush(self) -> None:  # pragma: no cover - not hit in these paths
        pass

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rolled_back = True

    async def close(self) -> None:
        pass


class FakeUow:
    def __init__(self, session: FakeSession) -> None:
        self.session = session
        self.events: list = []

    def collect_event(self, event) -> None:
        self.events.append(event)

    async def commit(self) -> None:
        await self.session.commit()


def _settings() -> Settings:
    return Settings(auth_max_failed_logins=2)


class TestReuseDetectionCommits:
    @pytest.mark.asyncio
    async def test_family_revocation_commits_before_rejection(self) -> None:
        family = uuid7()
        replayed = RefreshSession(
            id=uuid7(),
            user_id=uuid7(),
            family_id=family,
            refresh_token_hash=security.token_digest("stolen-token"),
            expires_at=datetime.now(timezone.utc) + timedelta(days=1),
            replaced_by=uuid7(),  # already rotated -> replay is theft
        )
        survivor = RefreshSession(
            id=uuid7(),
            user_id=replayed.user_id,
            family_id=family,
            refresh_token_hash="other-hash",
            expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        )
        session = FakeSession({RefreshSession: [replayed, survivor]})
        service = AuthenticationService(FakeUow(session), _settings())  # type: ignore[arg-type]

        with pytest.raises(AuthenticationError):
            await service.refresh("stolen-token")

        assert survivor.revoked_at is not None, "family member must be revoked"
        assert session.commits == 1, "revocation must be committed despite raise"


class TestLockoutCommits:
    @pytest.mark.asyncio
    async def test_failed_login_counter_commits_despite_rejection(self) -> None:
        user = User(
            id=uuid7(),
            email="locked@example.com",
            password_hash=security.hash_password("Correct-Passw0rd-123"),
            display_name="L",
            status=UserStatus.ACTIVE.value,
            failed_login_count=0,
        )
        session = FakeSession({User: [user]})
        service = AuthenticationService(FakeUow(session), _settings())  # type: ignore[arg-type]

        with pytest.raises(AuthenticationError):
            await service.login(email=user.email, password="Wrong-Passw0rd-123")

        assert user.failed_login_count == 1
        assert session.commits == 1, "counter must persist despite rejection"

    @pytest.mark.asyncio
    async def test_lock_engages_at_threshold_and_commits(self) -> None:
        user = User(
            id=uuid7(),
            email="locked@example.com",
            password_hash=security.hash_password("Correct-Passw0rd-123"),
            display_name="L",
            status=UserStatus.ACTIVE.value,
            failed_login_count=1,  # threshold is 2 in _settings()
        )
        session = FakeSession({User: [user]})
        uow = FakeUow(session)
        service = AuthenticationService(uow, _settings())  # type: ignore[arg-type]

        with pytest.raises(AuthenticationError):
            await service.login(email=user.email, password="Wrong-Passw0rd-123")

        assert user.locked_until is not None, "lock must engage at threshold"
        assert session.commits == 1
        assert any(e.event_type == "identity.user.locked.v1" for e in uow.events)
