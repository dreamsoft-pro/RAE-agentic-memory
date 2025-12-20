"""create_memories_table_initial

Revision ID: 000000000000
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""

import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY

from alembic import op

# revision identifiers, used by Alembic.
revision = "000000000000"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "memories",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("tenant_id", sa.String(), nullable=True), # Nullable based on some legacy, but contract says TEXT. Let's make it nullable to be safe initially or follow contract strictness? Contract doesn't specify nullable for tenant_id, usually it's required. Let's assume required but maybe check models.MemoryRecord says tenant_id: Optional[str] = None. So nullable=True.
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("importance", sa.Float(), nullable=True),
        sa.Column("layer", sa.String(), nullable=True),
        sa.Column("tags", ARRAY(sa.String()), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("project", sa.String(), nullable=True),
        sa.Column("metadata", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("last_accessed_at", sa.DateTime(), nullable=True),
        sa.Column("usage_count", sa.Integer(), default=0),
    )


def downgrade():
    op.drop_table("memories")
