"""silicon oracle deduplication

Revision ID: 20260211_oracle_dedup
Revises: d1e01c396ec2
Create Date: 2026-02-11 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import hashlib

# revision identifiers, used by Alembic.
revision = '20260211_oracle_dedup'
down_revision = 'd1e01c396ec2'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Add content_hash column
    op.add_column('memories', sa.Column('content_hash', sa.String(length=64), nullable=True))
    
    # 2. Add unique constraint on (tenant_id, content_hash)
    op.create_index('idx_memories_tenant_content_hash', 'memories', ['tenant_id', 'content_hash'], unique=True)
    
    # 3. Add trigger/index for faster lookup if needed, but for now unique index is enough

def downgrade():
    op.drop_index('idx_memories_tenant_content_hash', table_name='memories')
    op.drop_column('memories', 'content_hash')
