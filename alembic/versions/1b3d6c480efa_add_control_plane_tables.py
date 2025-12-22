"""add_control_plane_tables

Revision ID: 1b3d6c480efa
Revises: f2g3h4i5j6k7
Create Date: 2025-12-22 11:18:22.988154

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = '1b3d6c480efa'
down_revision = 'f2g3h4i5j6k7'
branch_labels = None
depends_on = None


def upgrade():
    # Create compute_nodes table
    op.create_table(
        'compute_nodes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('node_id', sa.String(), nullable=False),
        sa.Column('api_key_hash', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='OFFLINE'),
        sa.Column('last_heartbeat', sa.DateTime(timezone=True), nullable=True),
        sa.Column('capabilities', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=False),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('node_id')
    )

    # Create delegated_tasks table
    op.create_table(
        'delegated_tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='PENDING'),
        sa.Column('priority', sa.Integer(), server_default='0', nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=False),
        sa.Column('result', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('assigned_node_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('compute_nodes.id'), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index for task polling
    op.create_index('ix_delegated_tasks_status_priority', 'delegated_tasks', ['status', 'priority'])


def downgrade():
    op.drop_index('ix_delegated_tasks_status_priority', table_name='delegated_tasks')
    op.drop_table('delegated_tasks')
    op.drop_table('compute_nodes')
