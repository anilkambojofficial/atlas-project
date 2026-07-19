"""identity tables (Sprint-002; BP-003, ES-003)

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-19
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def _audit_columns() -> list[sa.Column]:
    return [
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
    ]


def _soft_delete_columns() -> list[sa.Column]:
    return [
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("delete_reason", sa.String(length=500), nullable=True),
    ]


def upgrade() -> None:
    op.create_table(
        "identity_users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=512), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default=sa.text("'pending_verification'"),
        ),
        sa.Column(
            "identity_class",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'human'"),
        ),
        sa.Column("email_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "failed_login_count",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
        *_audit_columns(),
        *_soft_delete_columns(),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_users")),
        sa.UniqueConstraint("email", name=op.f("uq_identity_users_email")),
    )

    op.create_table(
        "identity_organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default=sa.text("'active'"),
        ),
        *_audit_columns(),
        *_soft_delete_columns(),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_organizations")),
        sa.UniqueConstraint("slug", name=op.f("uq_identity_organizations_slug")),
    )

    op.create_table(
        "identity_roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column(
            "permissions",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "is_system", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_roles")),
        sa.UniqueConstraint(
            "organization_id", "name", name=op.f("uq_identity_roles_organization_id")
        ),
    )
    op.create_index(
        op.f("ix_identity_roles_organization_id"),
        "identity_roles",
        ["organization_id"],
    )

    op.create_table(
        "identity_memberships",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default=sa.text("'active'"),
        ),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_memberships")),
        sa.UniqueConstraint(
            "organization_id",
            "user_id",
            name=op.f("uq_identity_memberships_organization_id"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["identity_users.id"],
            name=op.f("fk_identity_memberships_user_id_identity_users"),
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["identity_roles.id"],
            name=op.f("fk_identity_memberships_role_id_identity_roles"),
        ),
    )
    op.create_index(
        op.f("ix_identity_memberships_organization_id"),
        "identity_memberships",
        ["organization_id"],
    )
    op.create_index(
        op.f("ix_identity_memberships_user_id"), "identity_memberships", ["user_id"]
    )

    op.create_table(
        "identity_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("family_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("refresh_token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("replaced_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user_agent", sa.String(length=400), nullable=True),
        sa.Column("client_ip", postgresql.INET(), nullable=True),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_sessions")),
        sa.UniqueConstraint(
            "refresh_token_hash",
            name=op.f("uq_identity_sessions_refresh_token_hash"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["identity_users.id"],
            name=op.f("fk_identity_sessions_user_id_identity_users"),
        ),
    )
    op.create_index(
        op.f("ix_identity_sessions_user_id"), "identity_sessions", ["user_id"]
    )
    op.create_index(
        op.f("ix_identity_sessions_organization_id"),
        "identity_sessions",
        ["organization_id"],
    )
    op.create_index(
        op.f("ix_identity_sessions_family_id"), "identity_sessions", ["family_id"]
    )

    op.create_table(
        "identity_verification_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("purpose", sa.String(length=40), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_verification_tokens")),
        sa.UniqueConstraint(
            "token_hash", name=op.f("uq_identity_verification_tokens_token_hash")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["identity_users.id"],
            name=op.f("fk_identity_verification_tokens_user_id_identity_users"),
        ),
    )
    op.create_index(
        op.f("ix_identity_verification_tokens_user_id"),
        "identity_verification_tokens",
        ["user_id"],
    )
    op.create_index(
        op.f("ix_identity_verification_tokens_purpose"),
        "identity_verification_tokens",
        ["purpose"],
    )

    op.create_table(
        "identity_audit_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("target", sa.String(length=200), nullable=True),
        sa.Column(
            "detail",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("correlation_id", sa.String(length=36), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_identity_audit_log")),
    )
    for column in ("occurred_at", "organization_id", "actor_user_id", "action"):
        op.create_index(
            op.f(f"ix_identity_audit_log_{column}"), "identity_audit_log", [column]
        )


def downgrade() -> None:
    for table in (
        "identity_audit_log",
        "identity_verification_tokens",
        "identity_sessions",
        "identity_memberships",
        "identity_roles",
        "identity_organizations",
        "identity_users",
    ):
        op.drop_table(table)
