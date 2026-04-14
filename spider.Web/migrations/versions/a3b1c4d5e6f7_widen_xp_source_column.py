"""widen xp_events source column to VARCHAR(20)

Revision ID: a3b1c4d5e6f7
Revises: 2e70c002c7cc
Create Date: 2026-04-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3b1c4d5e6f7'
down_revision: Union[str, None] = '2e70c002c7cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Widen source column: String(10) → String(20)
    # Fixes existing truncation bug ("money_maker" = 11 chars was being truncated)
    # Also supports new source values: council, idle, improve, sandbox
    op.alter_column('xp_events', 'source',
                    existing_type=sa.String(10),
                    type_=sa.String(20),
                    existing_nullable=False)


def downgrade() -> None:
    op.alter_column('xp_events', 'source',
                    existing_type=sa.String(20),
                    type_=sa.String(10),
                    existing_nullable=False)
