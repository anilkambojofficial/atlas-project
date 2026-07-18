"""Alembic migration environment.

Governing documents:
- IP-001 §7 — Alembic with SQLAlchemy 2.x async engine.
- ES-003 §16 — every schema change is a versioned, reviewed migration;
  migration history is permanently retained.
- IP-001 §10 — the database URL resolves through the configuration
  hierarchy (never hard-coded).

``target_metadata`` is the platform declarative base metadata; service
models registered against ``AtlasBase`` (IP-002 onward) are picked up by
autogenerate automatically once their modules are imported here.
"""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from infrastructure.database.base import AtlasBase
from shared.config import load_settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Resolve the URL through the IP-001 §10 hierarchy (env vars, config files).
config.set_main_option("sqlalchemy.url", load_settings().database_url)

target_metadata = AtlasBase.metadata


def run_migrations_offline() -> None:
    """Emit migration SQL without a live database connection."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def _run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def _run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    """Apply migrations through the async engine."""
    asyncio.run(_run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
