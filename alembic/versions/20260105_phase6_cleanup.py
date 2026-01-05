"""Phase 6: Cleanup dead columns

Revision ID: 20260105_phase6
Revises: 20260105_phase5
Create Date: 2026-01-05 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260105_phase6'
down_revision = '20260105_phase5'
branch_labels = None
depends_on = None

def upgrade():
    # Remove dead column qdrant_point_id
    # We check if it exists first to be safe, but Alembic usually assumes known schema state.
    # However, 'if exists' is safer for manual interventions.
    # Standard alembic: op.drop_column('memories', 'qdrant_point_id')
    
    # Check if column exists is tricky in pure alembic without reflection, 
    # but we assume it exists based on PLAN.
    op.drop_column('memories', 'qdrant_point_id')


def downgrade():
    # Recreate the column if we rollback
    op.add_column('memories', sa.Column('qdrant_point_id', sa.Text(), nullable=True))
