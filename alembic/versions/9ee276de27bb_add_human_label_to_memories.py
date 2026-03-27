"""add_human_label_to_memories

Revision ID: 9ee276de27bb
Revises: 20260225_ghost
Create Date: 2026-03-27 16:13:08.408442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ee276de27bb'
down_revision = '20260225_ghost'
branch_labels = None
depends_on = None


def upgrade():
    # Add human_label to memories table
    op.add_column("memories", sa.Column("human_label", sa.Text(), nullable=True))


def downgrade():
    # Remove human_label from memories table
    op.drop_column("memories", "human_label")
