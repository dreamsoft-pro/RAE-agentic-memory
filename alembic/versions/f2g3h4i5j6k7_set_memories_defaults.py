"""set memories defaults for benchmark compatibility

Revision ID: f2g3h4i5j6k7
Revises: 833152c0b02f
Create Date: 2025-12-21 23:55:00.000000

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'f2g3h4i5j6k7'
down_revision = '833152c0b02f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure uuid-ossp extension exists
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Set defaults for memories table
    op.alter_column('memories', 'id', server_default=sa.text('uuid_generate_v4()'))
    op.alter_column('memories', 'memory_type', server_default='episodic')
    op.alter_column('memories', 'agent_id', server_default='default_agent')


def downgrade() -> None:
    op.alter_column('memories', 'agent_id', server_default=None)
    op.alter_column('memories', 'memory_type', server_default=None)
    op.alter_column('memories', 'id', server_default=None)
