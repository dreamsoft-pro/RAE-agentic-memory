"""Add vector support to memories table

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2024-05-21 12:00:00.000000

"""

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

from alembic import op

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column("memories", sa.Column("embedding", Vector(384)))


def downgrade():
    op.drop_column("memories", "embedding")
    op.execute("DROP EXTENSION vector")
