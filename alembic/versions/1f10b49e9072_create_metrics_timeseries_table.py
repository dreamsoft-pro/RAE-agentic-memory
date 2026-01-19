"""create metrics_timeseries table

Revision ID: 1f10b49e9072
Revises: 20260117_sbb2
Create Date: 2026-01-18 19:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1f10b49e9072'
down_revision: Union[str, None] = 'a8e446ca7f97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('metrics_timeseries',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('tenant_id', sa.String(length=255), nullable=False),
        sa.Column('project_id', sa.String(length=255), nullable=True),
        sa.Column('metric_name', sa.String(length=255), nullable=False),
        sa.Column('metric_value', sa.Float(), nullable=False),
        sa.Column('metric_type', sa.String(length=50), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), server_default='[]', nullable=True),
        sa.Column('dimensions', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=True),
        sa.Column('aggregation_period', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.CheckConstraint("metric_type IN ('gauge', 'counter', 'histogram')", name='metrics_timeseries_valid_type')
    )
    op.create_index('idx_metrics_ts_metric_tenant_time', 'metrics_timeseries', ['metric_name', 'tenant_id', sa.text('timestamp DESC')], unique=False)
    op.create_index('idx_metrics_ts_project_time', 'metrics_timeseries', ['tenant_id', 'project_id', sa.text('timestamp DESC')], unique=False)
    op.create_index('idx_metrics_ts_metric_time', 'metrics_timeseries', ['metric_name', sa.text('timestamp DESC')], unique=False)
    op.create_index('idx_metrics_ts_dashboard_query', 'metrics_timeseries', ['tenant_id', 'project_id', 'metric_name', sa.text('timestamp DESC')], unique=False)
    # GIN indexes for JSONB
    op.create_index('idx_metrics_ts_tags', 'metrics_timeseries', ['tags'], unique=False, postgresql_using='gin')
    op.create_index('idx_metrics_ts_dimensions', 'metrics_timeseries', ['dimensions'], unique=False, postgresql_using='gin')


def downgrade() -> None:
    op.drop_index('idx_metrics_ts_dimensions', table_name='metrics_timeseries', postgresql_using='gin')
    op.drop_index('idx_metrics_ts_tags', table_name='metrics_timeseries', postgresql_using='gin')
    op.drop_index('idx_metrics_ts_dashboard_query', table_name='metrics_timeseries')
    op.drop_index('idx_metrics_ts_metric_time', table_name='metrics_timeseries')
    op.drop_index('idx_metrics_ts_project_time', table_name='metrics_timeseries')
    op.drop_index('idx_metrics_ts_metric_tenant_time', table_name='metrics_timeseries')
    op.drop_table('metrics_timeseries')