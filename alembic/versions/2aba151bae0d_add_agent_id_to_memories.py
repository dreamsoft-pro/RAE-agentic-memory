"""add_agent_id_to_memories

Revision ID: 2aba151bae0d
Revises: 602c7e62b29d
Create Date: 2025-12-21 08:45:00.000000

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2aba151bae0d'
down_revision: Union[str, None] = '602c7e62b29d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add agent_id column (nullable initially)
    op.add_column('memories', sa.Column('agent_id', sa.Text(), nullable=True))

    # 2. Backfill agent_id with project value for existing records
    op.execute("UPDATE memories SET agent_id = project WHERE agent_id IS NULL")

    # 3. Handle cases where project might be null (set default 'default')
    op.execute("UPDATE memories SET agent_id = 'default' WHERE agent_id IS NULL")

    # 4. Make agent_id not null now that it's populated
    op.alter_column('memories', 'agent_id', nullable=False)

    # 5. Add index for performance (filtering by agent_id is common in RAE)
    op.create_index(op.f('idx_memories_agent_id'), 'memories', ['agent_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('idx_memories_agent_id'), table_name='memories')
    op.drop_column('memories', 'agent_id')
