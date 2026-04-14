"""Add RBAC tables — roles and user_roles.

Revision ID: b4c2d5e6f7a8
Revises: a3b1c4d5e6f7
Create Date: 2026-04-11
"""
from alembic import op
import sqlalchemy as sa


revision = "b4c2d5e6f7a8"
down_revision = "a3b1c4d5e6f7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(50), unique=True, nullable=False),
        sa.Column("description", sa.String(200), server_default=""),
        sa.Column("permissions", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "user_roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("granted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )


def downgrade() -> None:
    op.drop_table("user_roles")
    op.drop_table("roles")
