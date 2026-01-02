"""create_memory_embeddings_table

Revision ID: 5b600ed8dfcb
Revises: 1b3d6c480efa
Create Date: 2026-01-01 07:38:26.499383

"""
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB, UUID

from alembic import op

# revision identifiers, used by Alembic.
revision = '5b600ed8dfcb'
down_revision = '1b3d6c480efa'
branch_labels = None
depends_on = None


def upgrade():
    # Create memory_embeddings table
    op.create_table(
        'memory_embeddings',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('memory_id', UUID(as_uuid=True), sa.ForeignKey('memories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('model_name', sa.String(255), nullable=False),
        sa.Column('embedding', Vector(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('metadata', JSONB, server_default='{}'),
    )

    # Create index on memory_id
    op.create_index('ix_memory_embeddings_memory_id', 'memory_embeddings', ['memory_id'])

    # Composite index for memory_id + model_name (unique constraint)
    op.create_unique_constraint('uq_memory_embeddings_memory_model', 'memory_embeddings', ['memory_id', 'model_name'])

    # Migrate data from memories table
    # We select only rows where embedding is not null.
    # We use 'default' as model_name for existing embeddings.
    op.execute("""
        INSERT INTO memory_embeddings (memory_id, model_name, embedding, created_at)
        SELECT id, 'default', embedding, COALESCE(created_at, NOW())
        FROM memories
        WHERE embedding IS NOT NULL
    """)


def downgrade():
    op.drop_table('memory_embeddings')
