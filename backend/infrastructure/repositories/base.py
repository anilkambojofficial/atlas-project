"""Generic repository base class.

Governing documents:
- RA-001 §9 — repositories abstract persistence from the domain layer:
  aggregate retrieval, aggregate persistence, query execution,
  transaction participation. Repositories expose business-oriented
  operations and contain no business rules (IP-002 §10 rule, applied
  platform-wide).
- ES-003 §12 — parameterized queries only, pagination for large result
  sets, no ``SELECT *`` semantics beyond mapped columns.
- ES-003 §15 — soft delete by default; soft-deleted rows are excluded
  from normal queries; hard deletes are not exposed by the platform.

Concrete business repositories (UserRepository, TenantRepository, …) are
delivered by their owning Implementation Packs (IP-002 onward) by
subclassing this base and adding business-oriented queries.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.base import AtlasBase, SoftDeleteMixin
from shared.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

ModelT = TypeVar("ModelT", bound=AtlasBase)


class SqlAlchemyRepository(Generic[ModelT]):
    """Persistence primitives shared by every concrete repository.

    Subclasses declare the mapped ``model`` and add business-oriented
    query methods; they never bypass the session or embed business rules.
    """

    model: type[ModelT]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "model"):
            raise TypeError(
                f"{cls.__name__} must declare its mapped 'model' class attribute"
            )

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """The unit-of-work session this repository participates in."""
        return self._session

    def _base_statement(self) -> Select[tuple[ModelT]]:
        """Base SELECT excluding soft-deleted rows (ES-003 §15)."""
        statement = select(self.model)
        if issubclass(self.model, SoftDeleteMixin):
            statement = statement.where(self.model.deleted_at.is_(None))
        return statement

    async def get_by_id(self, entity_id: uuid.UUID) -> ModelT | None:
        """Fetch one aggregate by primary key; soft-deleted rows excluded."""
        statement = self._base_statement().where(self.model.id == entity_id)  # type: ignore[attr-defined]
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def list(
        self, *, limit: int = DEFAULT_PAGE_SIZE, offset: int = 0
    ) -> Sequence[ModelT]:
        """Paginated listing (ES-003 §12; ADR-005): deterministic primary-key
        ordering — UUID v7 keys are time-ordered, so this is stable
        creation-time order at index cost. ``limit`` is capped at
        ``MAX_PAGE_SIZE``; OFFSET mode is a bounded convenience — unbounded
        collections use :meth:`list_after` (keyset)."""
        bounded_limit = max(1, min(limit, MAX_PAGE_SIZE))
        statement = (
            self._base_statement()
            .order_by(self.model.id)  # type: ignore[attr-defined]
            .limit(bounded_limit)
            .offset(max(0, offset))
        )
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def list_after(
        self, *, cursor: uuid.UUID | None = None, limit: int = DEFAULT_PAGE_SIZE
    ) -> Sequence[ModelT]:
        """Keyset pagination (ADR-005 — the platform standard for unbounded
        collections): O(page) at any depth. ``cursor`` is the last ``id`` of
        the previous page; ``None`` starts from the beginning."""
        bounded_limit = max(1, min(limit, MAX_PAGE_SIZE))
        statement = self._base_statement().order_by(self.model.id)  # type: ignore[attr-defined]
        if cursor is not None:
            statement = statement.where(self.model.id > cursor)  # type: ignore[attr-defined]
        statement = statement.limit(bounded_limit)
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def count(self) -> int:
        """Count non-deleted aggregates."""
        statement = select(func.count()).select_from(self._base_statement().subquery())
        result = await self._session.execute(statement)
        return int(result.scalar_one())

    def add(self, entity: ModelT) -> ModelT:
        """Register a new aggregate with the current transaction."""
        self._session.add(entity)
        return entity

    def add_many(self, entities: Sequence[ModelT]) -> Sequence[ModelT]:
        """Register several aggregates with the current transaction."""
        self._session.add_all(entities)
        return entities

    async def flush(self) -> None:
        """Flush pending changes so database defaults (ids, timestamps)
        become visible inside the still-open transaction."""
        await self._session.flush()

    def soft_delete(
        self,
        entity: ModelT,
        *,
        deleted_by: uuid.UUID | None = None,
        reason: str | None = None,
    ) -> ModelT:
        """Soft-delete an aggregate (ES-003 §15).

        Hard deletion is intentionally not provided by the platform base:
        it requires explicit architectural approval per ES-003 §15 and
        would then be implemented by the approving service itself.
        """
        if not isinstance(entity, SoftDeleteMixin):
            raise TypeError(
                f"{type(entity).__name__} does not support soft delete; "
                "hard deletes require architectural approval (ES-003 §15)"
            )
        entity.deleted_at = datetime.now(timezone.utc)
        entity.deleted_by = deleted_by
        entity.delete_reason = reason
        return entity
