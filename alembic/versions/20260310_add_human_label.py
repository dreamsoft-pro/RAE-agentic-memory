"""add human label column to memories

Revision ID: 20260310_human_label
Revises: 20260225_ghost
Create Date: 2026-03-10 13:10:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260310_human_label'
down_revision = '20260225_ghost'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Add human_label column
    op.add_column('memories', sa.Column('human_label', sa.String(length=255), nullable=True))
    
    # 2. Create B-Tree index for fast human searches
    op.create_index('idx_memories_human_label', 'memories', ['human_label'], unique=False)
    
    # 3. Backfill data from metadata JSONB to the new column
    # SQL query to extract human_label from metadata and put it into the new column
    op.execute(
        "UPDATE memories SET human_label = metadata->>'human_label' WHERE metadata ? 'human_label';"
    )


def downgrade():
    # Remove index and column
    op.drop_index('idx_memories_human_label', table_name='memories')
    op.drop_column('memories', 'human_label')
