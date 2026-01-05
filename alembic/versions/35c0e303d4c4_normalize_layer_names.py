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
    # Added check for table existence to prevent failure during fresh installs
    op.execute("""
        DO $$ 
        BEGIN 
            IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'memories') THEN
                UPDATE memories SET layer = 'episodic' WHERE layer = 'em';
                UPDATE memories SET layer = 'working' WHERE layer = 'stm' OR layer = 'wm';
                UPDATE memories SET layer = 'semantic' WHERE layer = 'ltm' OR layer = 'sm';
                UPDATE memories SET layer = 'reflective' WHERE layer = 'rm';
            END IF;
        END $$;
    """)


def downgrade():
    # Optional: logic to revert to short names if needed
    pass