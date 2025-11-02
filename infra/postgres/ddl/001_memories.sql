CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE memories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id VARCHAR(255) NOT NULL,
  agent_id  VARCHAR(255) NOT NULL,
  memory_type VARCHAR(50) NOT NULL,
  content   TEXT NOT NULL,
  saliency_score REAL DEFAULT 0.5,
  uncertainty_score REAL DEFAULT 1.0,
  source_id VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_accessed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE episodic_memories (
  memory_id UUID PRIMARY KEY REFERENCES memories(id) ON DELETE CASCADE,
  event_timestamp TIMESTAMPTZ NOT NULL,
  actors JSONB,
  location VARCHAR(255),
  emotional_valence REAL
);

CREATE TABLE semantic_memories (
  memory_id UUID PRIMARY KEY REFERENCES memories(id) ON DELETE CASCADE,
  subject_node_id UUID,
  predicate VARCHAR(255),
  object_node_id UUID,
  object_literal TEXT
);

CREATE TABLE procedural_memories (
  memory_id UUID PRIMARY KEY REFERENCES memories(id) ON DELETE CASCADE,
  trigger_condition TEXT,
  steps JSONB NOT NULL,
  expected_outcome TEXT
);
