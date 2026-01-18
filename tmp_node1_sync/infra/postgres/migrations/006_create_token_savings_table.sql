-- Migration: Create token_savings_log table
-- Description: Tracks token savings from optimizations (cache, RAG, etc.)

CREATE TABLE IF NOT EXISTS token_savings_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id VARCHAR(255) NOT NULL,
    project_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    request_id VARCHAR(255),
    
    -- Token metrics
    predicted_tokens INTEGER NOT NULL DEFAULT 0,
    real_tokens INTEGER NOT NULL DEFAULT 0,
    saved_tokens INTEGER GENERATED ALWAYS AS (predicted_tokens - real_tokens) STORED,
    
    -- Financial metrics
    estimated_cost_saved_usd DECIMAL(10, 6) DEFAULT 0.0,
    
    -- Metadata
    savings_type VARCHAR(50) NOT NULL, -- 'cache', 'rag', 'rerank', 'compression'
    model VARCHAR(100),
    
    -- Constraints
    CONSTRAINT check_positive_savings CHECK (saved_tokens >= 0)
);

-- Indexes for analytics
CREATE INDEX IF NOT EXISTS idx_token_savings_tenant_time ON token_savings_log(tenant_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_token_savings_project_time ON token_savings_log(project_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_token_savings_type ON token_savings_log(savings_type);

-- RLS Policies (Multi-tenancy)
ALTER TABLE token_savings_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON token_savings_log
    USING (tenant_id = current_setting('app.current_tenant', true));
