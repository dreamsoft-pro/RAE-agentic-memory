"""Ghost Cleanup - Adding missing tables for Reflections and Cluster Infrastructure.

Revision ID: 20260225_ghost
Revises: 20260224_refl_v3
Create Date: 2026-02-25 15:30:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260225_ghost'
down_revision = '20260224_refl_v3'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Full Reflection Table (Matched with reflection_repository.py)
    op.create_table(
        'reflections',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('priority', sa.Integer(), server_default='3'),
        sa.Column('score', sa.Float(), server_default='0.5'),
        sa.Column('novelty_score', sa.Float(), server_default='0.5'),
        sa.Column('importance_score', sa.Float(), server_default='0.5'),
        sa.Column('utility_score', sa.Float(), server_default='0.5'),
        sa.Column('confidence_score', sa.Float(), server_default='0.5'),
        sa.Column('parent_reflection_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('reflections.id', ondelete='CASCADE'), nullable=True),
        sa.Column('depth_level', sa.Integer(), server_default='0'),
        sa.Column('source_memory_ids', postgresql.ARRAY(postgresql.UUID(as_uuid=True)), server_default='{}'),
        sa.Column('source_reflection_ids', postgresql.ARRAY(postgresql.UUID(as_uuid=True)), server_default='{}'),
        sa.Column('embedding', postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column('cluster_id', sa.String(), nullable=True),
        sa.Column('cluster_centroid', postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column('cache_key', sa.String(), nullable=True),
        sa.Column('reuse_count', sa.Integer(), server_default='0'),
        sa.Column('tags', postgresql.ARRAY(sa.String()), server_default='{}'),
        sa.Column('metadata', postgresql.JSONB, server_default='{}'),
        sa.Column('generation_model', sa.String(), nullable=True),
        sa.Column('generation_duration_ms', sa.Float(), nullable=True),
        sa.Column('generation_tokens_used', sa.Integer(), nullable=True),
        sa.Column('generation_cost_usd', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_accessed_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('accessed_count', sa.Integer(), server_default='0')
    )
    
    # 2. Reflection Relationships (Full Schema)
    op.create_table(
        'reflection_relationships',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('source_reflection_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('reflections.id', ondelete='CASCADE')),
        sa.Column('target_reflection_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('reflections.id', ondelete='CASCADE')),
        sa.Column('relation_type', sa.String(), nullable=False),
        sa.Column('strength', sa.Float(), server_default='1.0'),
        sa.Column('confidence', sa.Float(), server_default='1.0'),
        sa.Column('supporting_evidence', postgresql.ARRAY(sa.Text()), server_default='{}'),
        sa.Column('metadata', postgresql.JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    # 3. Reflection Usage Log
    op.create_table(
        'reflection_usage_log',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('reflection_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('reflections.id', ondelete='CASCADE')),
        sa.Column('usage_type', sa.String(), nullable=False),
        sa.Column('query_text', sa.Text(), nullable=True),
        sa.Column('relevance_score', sa.Float(), nullable=True),
        sa.Column('rank_position', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('session_id', sa.String(), nullable=True),
        sa.Column('metadata', postgresql.JSONB, server_default='{}'),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    # 4. Compute Nodes & Tasks (Cluster)
    op.create_table(
        'compute_nodes',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('hostname', sa.String(), nullable=False),
        sa.Column('status', sa.String(), server_default='offline'),
        sa.Column('capabilities', postgresql.JSONB, server_default='{}'),
        sa.Column('last_seen', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    op.create_table(
        'delegated_tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', sa.String(), sa.ForeignKey('compute_nodes.id')),
        sa.Column('payload', postgresql.JSONB, nullable=False),
        sa.Column('status', sa.String(), server_default='pending'),
        sa.Column('result', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('delegated_tasks')
    op.drop_table('compute_nodes')
    op.drop_table('reflection_usage_log')
    op.drop_table('reflection_relationships')
    op.drop_table('reflections')
