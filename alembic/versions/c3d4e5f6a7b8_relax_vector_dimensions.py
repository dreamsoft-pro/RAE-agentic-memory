"""relax vector dimensions

Revision ID: c3d4e5f6a7b8
Revises: 5b600ed8dfcb
Create Date: 2026-01-03 00:15:00.000000

"""
import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = 'c3d4e5f6a7b8'
down_revision = '5b600ed8dfcb'
branch_labels = None
depends_on = None


def upgrade():
    # Relax dimension constraint on memories table
    op.execute("ALTER TABLE memories ALTER COLUMN embedding TYPE vector")
    # Relax dimension constraint on memory_embeddings table
    op.execute("ALTER TABLE memory_embeddings ALTER COLUMN embedding TYPE vector")


def downgrade():
    # Note: Downgrading back to 384 might fail if 768-dim data exists
    op.execute("ALTER TABLE memories ALTER COLUMN embedding TYPE vector(384)")
    op.execute("ALTER TABLE memory_embeddings ALTER COLUMN embedding TYPE vector(384)")
