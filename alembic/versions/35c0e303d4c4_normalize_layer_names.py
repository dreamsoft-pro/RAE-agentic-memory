"""normalize_layer_names

Revision ID: 35c0e303d4c4
Revises: 000000000000
Create Date: 2026-01-04 12:59:09.422910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35c0e303d4c4'
down_revision = '000000000000'
branch_labels = None
depends_on = None


def upgrade():
    # Normalize legacy short layer codes to full standard names
    op.execute("UPDATE memories SET layer = 'episodic' WHERE layer = 'em'")
    op.execute("UPDATE memories SET layer = 'working' WHERE layer = 'stm' OR layer = 'wm'")
    op.execute("UPDATE memories SET layer = 'semantic' WHERE layer = 'ltm' OR layer = 'sm'")
    op.execute("UPDATE memories SET layer = 'reflective' WHERE layer = 'rm'")


def downgrade():
    # Optional: logic to revert to short names if needed, but we want to stick to the new standard
    pass
