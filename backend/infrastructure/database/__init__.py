"""PostgreSQL persistence foundation (IP-001 §7 — SQLAlchemy 2.x, Alembic).

Provides the declarative base with the ES-003 mandatory column mixins,
async engine/session management, and the Unit of Work pattern (RA-001 §10).
"""

from infrastructure.database.base import (
    AtlasBase,
    AuditColumnsMixin,
    OrganizationScopedMixin,
    SoftDeleteMixin,
    UUIDPrimaryKeyMixin,
)
from infrastructure.database.engine import DatabaseManager
from infrastructure.database.session import get_db_session
from infrastructure.database.unit_of_work import UnitOfWork

__all__ = [
    "AtlasBase",
    "AuditColumnsMixin",
    "DatabaseManager",
    "OrganizationScopedMixin",
    "SoftDeleteMixin",
    "UUIDPrimaryKeyMixin",
    "UnitOfWork",
    "get_db_session",
]
