CREATE TABLE knowledge_graph_nodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id VARCHAR(255) NOT NULL,
  label VARCHAR(255) NOT NULL,
  properties JSONB
);

CREATE TABLE knowledge_graph_edges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id VARCHAR(255) NOT NULL,
  source_node_id UUID NOT NULL REFERENCES knowledge_graph_nodes(id),
  target_node_id UUID NOT NULL REFERENCES knowledge_graph_nodes(id),
  label VARCHAR(255) NOT NULL,
  properties JSONB
);

ALTER TABLE knowledge_graph_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_graph_edges ENABLE ROW LEVEL SECURITY;
