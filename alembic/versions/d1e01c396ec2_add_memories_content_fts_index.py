"""add_memories_content_fts_index

Revision ID: d1e01c396ec2
Revises: 1f10b49e9072
Create Date: 2026-02-07 14:14:31.158263

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = 'd1e01c396ec2'
down_revision = '1f10b49e9072'
branch_labels = None
depends_on = None


def upgrade():
    # 1. GIN index for full-text search on content
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE c.relname = 'idx_memories_content_fts' AND n.nspname = 'public') THEN
                CREATE INDEX idx_memories_content_fts ON memories USING gin(to_tsvector('english', coalesce(content, '')));
            END IF;
        END $$;
    """
    )

    # 2. Index on session_id (was missing despite migration)
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE c.relname = 'idx_memories_session_id' AND n.nspname = 'public') THEN
                CREATE INDEX idx_memories_session_id ON memories (session_id);
            END IF;
        END $$;
    """
    )

    # 3. Index on source (was missing despite migration)
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE c.relname = 'idx_memories_source' AND n.nspname = 'public') THEN
                CREATE INDEX idx_memories_source ON memories (source);
            END IF;
        END $$;
    """
    )

    # 4. Composite Index for Dashboard Time-Range queries by Project
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE c.relname = 'idx_memories_project_created_at' AND n.nspname = 'public') THEN
                CREATE INDEX idx_memories_project_created_at ON memories (project, created_at);
            END IF;
        END $$;
    """
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_memories_project_created_at")
    op.execute("DROP INDEX IF EXISTS idx_memories_source")
    op.execute("DROP INDEX IF EXISTS idx_memories_session_id")
    op.execute("DROP INDEX IF EXISTS idx_memories_content_fts")
