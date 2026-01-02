"""create_access_logs_table

Revision ID: b2c3d4e5f6a8
Revises: a1b2c3d4e5f7
Create Date: 2026-01-02 23:58:00.000000

"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b2c3d4e5f6a8'
down_revision = 'a1b2c3d4e5f7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'access_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource', sa.String(100), nullable=False),
        sa.Column('resource_id', sa.String(255), nullable=True),
        sa.Column('allowed', sa.Boolean(), nullable=False),
        sa.Column('denial_reason', sa.Text(), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('metadata', JSONB, server_default='{}'),
    )

    op.create_index('ix_access_logs_tenant_id', 'access_logs', ['tenant_id'])
    op.create_index('ix_access_logs_user_id', 'access_logs', ['user_id'])
    op.create_index('ix_access_logs_timestamp', 'access_logs', ['timestamp'])


def downgrade():
    op.drop_table('access_logs')
