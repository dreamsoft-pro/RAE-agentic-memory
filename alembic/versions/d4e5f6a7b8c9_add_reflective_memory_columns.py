"""Add reflective memory columns (memory_type, session_id, qdrant_point_id)

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2025-11-28 14:00:00.000000

"""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision = "d4e5f6a7b8c9"
down_revision = "c3d4e5f6a7b8"
branch_labels = None
depends_on = None


def upgrade():
    # Add memory_type column with default based on existing layer
    # memory_type options: sensory, episodic, semantic, profile, reflection, strategy
    op.add_column("memories", sa.Column("memory_type", sa.Text(), nullable=True))

    # Set initial values based on existing layer column
    # em -> episodic, sm -> semantic, rm -> reflection
    op.execute(
        """
        UPDATE memories SET memory_type = CASE
            WHEN layer = 'em' THEN 'episodic'
            WHEN layer = 'sm' THEN 'semantic'
            WHEN layer = 'rm' THEN 'reflection'
            WHEN layer = 'stm' THEN 'sensory'
            WHEN layer = 'ltm' THEN 'semantic'
            ELSE 'semantic'
        END
        WHERE memory_type IS NULL
    """
    )

    # Make memory_type NOT NULL after setting initial values
    op.alter_column("memories", "memory_type", nullable=False)

    # Add session_id for episodic and reflective memories
    op.add_column(
        "memories", sa.Column("session_id", UUID(as_uuid=True), nullable=True)
    )

    # Add qdrant_point_id for vector store integration
    op.add_column("memories", sa.Column("qdrant_point_id", sa.Text(), nullable=True))

    # Add index on memory_type for faster filtering
    op.create_index("idx_memories_memory_type", "memories", ["memory_type"])

    # Add index on session_id for session-based queries
    op.create_index("idx_memories_session_id", "memories", ["session_id"])

    # Add composite index for common queries
    op.create_index(
        "idx_memories_tenant_project_type",
        "memories",
        ["tenant_id", "project", "memory_type"],
    )


def downgrade():
    op.drop_index("idx_memories_tenant_project_type", table_name="memories")
    op.drop_index("idx_memories_session_id", table_name="memories")
    op.drop_index("idx_memories_memory_type", table_name="memories")
    op.drop_column("memories", "qdrant_point_id")
    op.drop_column("memories", "session_id")
    op.drop_column("memories", "memory_type")
