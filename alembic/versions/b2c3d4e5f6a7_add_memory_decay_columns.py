"""Add strength, ttl, and expires_at to memories table

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2024-05-22 10:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "b2c3d4e5f6a7"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "memories",
        sa.Column("strength", sa.Float(), nullable=False, server_default="1.0"),
    )
    op.add_column("memories", sa.Column("ttl", sa.Integer(), nullable=True))
    op.add_column("memories", sa.Column("expires_at", sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column("memories", "expires_at")
    op.drop_column("memories", "ttl")
    op.drop_column("memories", "strength")
