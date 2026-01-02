"""create_tenants_and_rbac_tables

Revision ID: a1b2c3d4e5f7
Revises: 5b600ed8dfcb
Create Date: 2026-01-02 23:55:00.000000

"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f7'
down_revision = '5b600ed8dfcb'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Create tenants table
    op.create_table(
        'tenants',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('tier', sa.String(50), nullable=False),
        sa.Column('config', JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('status', sa.String(50), server_default='active'),
        sa.Column('contact_email', sa.String(255), nullable=True),
        sa.Column('company_name', sa.String(255), nullable=True),
        sa.Column('current_memory_count', sa.Integer(), server_default='0'),
        sa.Column('current_project_count', sa.Integer(), server_default='0'),
        sa.Column('api_calls_today', sa.Integer(), server_default='0'),
        sa.Column('subscription_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('subscription_end', sa.DateTime(timezone=True), nullable=True),
    )

    # 2. Create user_tenant_roles table (RBAC)
    op.create_table(
        'user_tenant_roles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('project_ids', ARRAY(sa.String()), server_default='{}'),
        sa.Column('assigned_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('assigned_by', sa.String(255), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Indexes for RBAC
    op.create_index('ix_user_tenant_roles_user_id', 'user_tenant_roles', ['user_id'])
    op.create_index('ix_user_tenant_roles_tenant_id', 'user_tenant_roles', ['tenant_id'])
    op.create_unique_constraint('uq_user_tenant_role', 'user_tenant_roles', ['user_id', 'tenant_id'])


def downgrade():
    op.drop_table('user_tenant_roles')
    op.drop_table('tenants')
