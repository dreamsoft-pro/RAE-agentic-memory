"""Phase 5: Performance Indexes

Revision ID: 20260105_phase5
Revises: 20260105_phase4
Create Date: 2026-01-05 20:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260105_phase5'
down_revision = '20260105_phase4'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Index on project (High cardinality, frequent filtering in Dashboard)
    op.create_index(
        'idx_memories_project',
        'memories',
        ['project'],
        unique=False,
        postgresql_using='btree'
    )

    # 2. Index on session_id (Medium cardinality, used for conversation history)
    op.create_index(
        'idx_memories_session_id',
        'memories',
        ['session_id'],
        unique=False,
        postgresql_using='btree'
    )

    # 3. Index on source (Low-Medium cardinality, ISO 42001 audit trails)
    op.create_index(
        'idx_memories_source',
        'memories',
        ['source'],
        unique=False,
        postgresql_using='btree'
    )
    
    # 4. Composite Index for Dashboard Time-Range queries by Project
    # Helps with: "Show me project X activity sorted by date"
    op.create_index(
        'idx_memories_project_created_at',
        'memories',
        ['project', 'created_at'],
        unique=False,
        postgresql_using='btree'
    )

def downgrade():
    op.drop_index('idx_memories_project_created_at', table_name='memories')
    op.drop_index('idx_memories_source', table_name='memories')
    op.drop_index('idx_memories_session_id', table_name='memories')
    op.drop_index('idx_memories_project', table_name='memories')
