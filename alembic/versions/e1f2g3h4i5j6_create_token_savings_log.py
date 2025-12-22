"""create token savings log

Revision ID: e1f2g3h4i5j6
Revises: d4e5f6a7b8c9
Create Date: 2025-12-21 23:30:00.000000

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e1f2g3h4i5j6'
down_revision = 'd4e5f6a7b8c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'token_savings_log',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('tenant_id', sa.String(255), nullable=False),
        sa.Column('project_id', sa.String(255), nullable=False),
        sa.Column('request_id', sa.String(255), nullable=True),
        sa.Column('predicted_tokens', sa.Integer(), nullable=False),
        sa.Column('real_tokens', sa.Integer(), nullable=False),
        sa.Column('saved_tokens', sa.Integer(), nullable=False),
        sa.Column('estimated_cost_saved_usd', sa.Float(), nullable=False),
        sa.Column('savings_type', sa.String(50), nullable=False),
        sa.Column('model', sa.String(100), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_token_savings_tenant_time', 'token_savings_log', ['tenant_id', 'timestamp'])
    op.create_index('idx_token_savings_project_time', 'token_savings_log', ['project_id', 'timestamp'])


def downgrade() -> None:
    op.drop_table('token_savings_log')
