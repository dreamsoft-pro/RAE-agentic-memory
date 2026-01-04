"""create knowledge graph tables

Revision ID: 37fcdedf6f6d
Revises: c3d4e5f6a7ba
Create Date: 2025-12-05 20:00:00.000000

"""

import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

from alembic import op

# revision identifiers, used by Alembic.
revision = "37fcdedf6f6d"
down_revision = "c3d4e5f6a7b8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "knowledge_graph_nodes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("tenant_id", sa.String(), nullable=False, index=True),
        sa.Column("project_id", sa.String(), nullable=False, index=True),
        sa.Column(
            "node_id", sa.String(), nullable=False, index=True
        ),  # The unique business ID of the node
        sa.Column("label", sa.String(), nullable=False),
        sa.Column("properties", JSONB, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "tenant_id", "project_id", "node_id", name="uq_tenant_project_node"
        ),
    )

    op.create_table(
        "knowledge_graph_edges",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("tenant_id", sa.String(), nullable=False, index=True),
        sa.Column("project_id", sa.String(), nullable=False, index=True),
        sa.Column(
            "source_node_id",
            UUID(as_uuid=True),
            sa.ForeignKey("knowledge_graph_nodes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "target_node_id",
            UUID(as_uuid=True),
            sa.ForeignKey("knowledge_graph_nodes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("relation", sa.String(), nullable=False, index=True),
        sa.Column("properties", JSONB, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("knowledge_graph_edges")
    op.drop_table("knowledge_graph_nodes")
