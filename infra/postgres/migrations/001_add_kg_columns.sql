-- Migration: Add missing columns to knowledge_graph tables
-- Date: 2025-11-20
-- Description: Adds project_id, node_id, created_at columns to support PageRank filtering

-- Add columns to knowledge_graph_nodes if they don't exist
DO $$
BEGIN
    -- Add project_id column
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'knowledge_graph_nodes' AND column_name = 'project_id'
    ) THEN
        ALTER TABLE knowledge_graph_nodes ADD COLUMN project_id VARCHAR(255);
        -- Set default value for existing rows
        UPDATE knowledge_graph_nodes SET project_id = 'default' WHERE project_id IS NULL;
        -- Make it NOT NULL after setting defaults
        ALTER TABLE knowledge_graph_nodes ALTER COLUMN project_id SET NOT NULL;
    END IF;

    -- Add node_id column
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'knowledge_graph_nodes' AND column_name = 'node_id'
    ) THEN
        ALTER TABLE knowledge_graph_nodes ADD COLUMN node_id VARCHAR(255);
        -- Set default value for existing rows (use label as fallback)
        UPDATE knowledge_graph_nodes SET node_id = label || '_' || id::text WHERE node_id IS NULL;
        -- Make it NOT NULL after setting defaults
        ALTER TABLE knowledge_graph_nodes ALTER COLUMN node_id SET NOT NULL;
    END IF;

    -- Add created_at column
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'knowledge_graph_nodes' AND column_name = 'created_at'
    ) THEN
        ALTER TABLE knowledge_graph_nodes ADD COLUMN created_at TIMESTAMPTZ DEFAULT NOW();
    END IF;

    -- Add unique constraint if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'knowledge_graph_nodes_tenant_id_project_id_node_id_key'
    ) THEN
        ALTER TABLE knowledge_graph_nodes
        ADD CONSTRAINT knowledge_graph_nodes_tenant_id_project_id_node_id_key
        UNIQUE (tenant_id, project_id, node_id);
    END IF;
END $$;

-- Add columns to knowledge_graph_edges if they don't exist
DO $$
BEGIN
    -- Add project_id column
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'knowledge_graph_edges' AND column_name = 'project_id'
    ) THEN
        ALTER TABLE knowledge_graph_edges ADD COLUMN project_id VARCHAR(255);
        -- Set default value for existing rows
        UPDATE knowledge_graph_edges SET project_id = 'default' WHERE project_id IS NULL;
        -- Make it NOT NULL after setting defaults
        ALTER TABLE knowledge_graph_edges ALTER COLUMN project_id SET NOT NULL;
    END IF;

    -- Rename label to relation if needed
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'knowledge_graph_edges' AND column_name = 'label'
    ) AND NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'knowledge_graph_edges' AND column_name = 'relation'
    ) THEN
        ALTER TABLE knowledge_graph_edges RENAME COLUMN label TO relation;
    END IF;

    -- Add created_at column
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'knowledge_graph_edges' AND column_name = 'created_at'
    ) THEN
        ALTER TABLE knowledge_graph_edges ADD COLUMN created_at TIMESTAMPTZ DEFAULT NOW();
    END IF;
END $$;

-- Create indexes for common queries (if they don't exist)
CREATE INDEX IF NOT EXISTS idx_kg_nodes_tenant_project ON knowledge_graph_nodes(tenant_id, project_id);
CREATE INDEX IF NOT EXISTS idx_kg_nodes_node_id ON knowledge_graph_nodes(node_id);
CREATE INDEX IF NOT EXISTS idx_kg_edges_tenant_project ON knowledge_graph_edges(tenant_id, project_id);
CREATE INDEX IF NOT EXISTS idx_kg_edges_source ON knowledge_graph_edges(source_node_id);
CREATE INDEX IF NOT EXISTS idx_kg_edges_target ON knowledge_graph_edges(target_node_id);
CREATE INDEX IF NOT EXISTS idx_kg_edges_relation ON knowledge_graph_edges(relation);
