"""Create budgets table

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2024-05-23 10:00:00.000000

"""

import uuid

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c3d4e5f6a7b8"
down_revision = "b2c3d4e5f6a7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "budgets",
        sa.Column("id", sa.UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("project_id", sa.String(), nullable=False),
        sa.Column("monthly_limit", sa.Float(), nullable=True),
        sa.Column("monthly_usage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("daily_limit", sa.Float(), nullable=True),
        sa.Column("daily_usage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("last_usage_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("tenant_id", "project_id", name="uq_tenant_project"),
    )


def downgrade():
    op.drop_table("budgets")
