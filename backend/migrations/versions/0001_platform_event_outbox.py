"""platform_event_outbox (ADR-002 §1; RA-006 §10)

Revision ID: 0001
Revises:
Create Date: 2026-07-19
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "platform_event_outbox",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=200), nullable=False),
        sa.Column("organization_id", sa.String(length=36), nullable=True),
        sa.Column("envelope", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'pending'"),
        ),
        sa.Column(
            "attempts", sa.Integer(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_platform_event_outbox")),
        sa.UniqueConstraint(
            "event_id", name=op.f("uq_platform_event_outbox_event_id")
        ),
    )
    op.create_index(
        op.f("ix_platform_event_outbox_event_type"),
        "platform_event_outbox",
        ["event_type"],
    )
    op.create_index(
        op.f("ix_platform_event_outbox_organization_id"),
        "platform_event_outbox",
        ["organization_id"],
    )
    op.create_index(
        op.f("ix_platform_event_outbox_status"), "platform_event_outbox", ["status"]
    )
    op.create_index(
        op.f("ix_platform_event_outbox_next_attempt_at"),
        "platform_event_outbox",
        ["next_attempt_at"],
    )


def downgrade() -> None:
    op.drop_table("platform_event_outbox")
