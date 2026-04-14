"""Add entity memory tables — knowledge graph.

Revision ID: c5d3e7f8a9b0
Revises: b4c2d5e6f7a8
Create Date: 2026-04-11
"""
from alembic import op
import sqlalchemy as sa


revision = "c5d3e7f8a9b0"
down_revision = "b4c2d5e6f7a8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "entities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("entity_type", sa.String(50), nullable=False),
        sa.Column("description", sa.Text(), server_default=""),
        sa.Column("mention_count", sa.Integer(), server_default="1"),
        sa.Column("first_seen", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("last_seen", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("name", "entity_type", name="uq_entity_name_type"),
    )
    op.create_table(
        "entity_relations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_id", sa.Integer(), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relation_type", sa.String(50), nullable=False),
        sa.Column("confidence", sa.Float(), server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("source_id", "target_id", "relation_type", name="uq_entity_relation"),
    )
    op.create_table(
        "entity_mentions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entity_id", sa.Integer(), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("conversation_id", sa.String(64), server_default=""),
        sa.Column("context_snippet", sa.Text(), server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("entity_mentions")
    op.drop_table("entity_relations")
    op.drop_table("entities")
