"""Add 3-Layer Reflection Audits and IdeaField edge storage.

Revision ID: 20260224_refl_v3
Revises: 20260211_oracle_dedup
Create Date: 2026-02-24 08:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision = '20260224_refl_v3'
down_revision = '20260211_oracle_dedup'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Table for Reflection Audits (L1, L2, L3 results)
    op.create_table(
        'reflection_audits',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('query_id', sa.String(), nullable=False, index=True),
        sa.Column('tenant_id', sa.String(), nullable=False, index=True),
        sa.Column('agent_id', sa.String(), nullable=True, index=True),
        sa.Column('fsi_score', sa.Float(), nullable=False),
        sa.Column('final_decision', sa.String(), nullable=False), # 'pass', 'blocked'
        sa.Column('l1_report', JSONB, nullable=True),
        sa.Column('l2_report', JSONB, nullable=True),
        sa.Column('l3_report', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('metadata', JSONB, nullable=True)
    )

    # 2. Table for IdeaField Edge Storage (Sparse graph for L3)
    op.create_table(
        'idea_field_edges',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('source_concept', sa.String(), nullable=False, index=True),
        sa.Column('target_concept', sa.String(), nullable=False, index=True),
        sa.Column('weight', sa.Float(), default=1.0),
        sa.Column('domain', sa.String(), nullable=True, index=True),
        sa.Column('tenant_id', sa.String(), nullable=False, index=True),
        sa.Column('last_seen', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('source_concept', 'target_concept', 'domain', 'tenant_id', name='uq_concept_edge')
    )

def downgrade():
    op.drop_table('idea_field_edges')
    op.drop_table('reflection_audits')
