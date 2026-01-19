-- Migration 007: ISO/IEC 42001 Compliance Tracking
-- Created: 2025-12-01
-- Purpose: Create tables for tracking ISO 42001 compliance metrics, audit trail, and risk register
--
-- This migration supports:
-- - Compliance requirement tracking
-- - Risk register database storage
-- - Comprehensive audit trail
-- - Data retention monitoring
-- - RLS context tracking
--
-- ISO/IEC 42001 alignment:
-- - Section 6: Risk management (risk_register table)
-- - Section 8: Information security (audit_trail_log table)
-- - Section 10: Monitoring and measurement (compliance_metrics table)

-- ==================================================================
-- ISO 42001 Compliance Metrics Table
-- ==================================================================

CREATE TABLE IF NOT EXISTS iso42001_compliance_metrics (
    id BIGSERIAL PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,

    -- Requirement identification
    requirement_id TEXT NOT NULL,
    requirement_name TEXT NOT NULL,
    requirement_description TEXT,
    compliance_area TEXT NOT NULL, -- governance, risk_management, data_management, etc.

    -- Compliance status
    status TEXT NOT NULL, -- compliant, non_compliant, partially_compliant, not_applicable
    current_value DECIMAL(5,2) NOT NULL, -- 0-100 percentage
    threshold DECIMAL(5,2) NOT NULL DEFAULT 100.0,

    -- Evidence and findings
    evidence_ids TEXT[], -- References to evidence documents/files
    findings TEXT[],
    recommendations TEXT[],

    -- Timestamps
    checked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_compliant_at TIMESTAMPTZ,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Indexes
    CONSTRAINT iso42001_compliance_metrics_tenant_id_fk
        CHECK (tenant_id IS NOT NULL AND length(tenant_id) > 0)
);

-- Indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_iso42001_metrics_tenant_id
    ON iso42001_compliance_metrics(tenant_id);
CREATE INDEX IF NOT EXISTS idx_iso42001_metrics_tenant_project
    ON iso42001_compliance_metrics(tenant_id, project_id);
CREATE INDEX IF NOT EXISTS idx_iso42001_metrics_requirement
    ON iso42001_compliance_metrics(requirement_id);
CREATE INDEX IF NOT EXISTS idx_iso42001_metrics_area
    ON iso42001_compliance_metrics(compliance_area);
CREATE INDEX IF NOT EXISTS idx_iso42001_metrics_status
    ON iso42001_compliance_metrics(status);
CREATE INDEX IF NOT EXISTS idx_iso42001_metrics_checked_at
    ON iso42001_compliance_metrics(checked_at DESC);

-- ==================================================================
-- Audit Trail Log Table
-- ==================================================================

CREATE TABLE IF NOT EXISTS audit_trail_log (
    id BIGSERIAL PRIMARY KEY,
    entry_id UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    tenant_id TEXT NOT NULL,
    project_id TEXT,

    -- Event classification
    event_type TEXT NOT NULL, -- data_access, model_decision, config_change, etc.
    event_category TEXT NOT NULL, -- data_operation, ai_decision, user_action, system_event
    event_description TEXT,

    -- Actor information
    actor_type TEXT NOT NULL, -- user, system, api, external, admin
    actor_id TEXT NOT NULL,
    actor_name TEXT,

    -- Resource information
    resource_type TEXT NOT NULL, -- memory, model, data, configuration
    resource_id TEXT NOT NULL,
    resource_name TEXT,

    -- Action details
    action TEXT NOT NULL, -- create, read, update, delete, execute, approve, reject
    action_description TEXT NOT NULL,

    -- Result
    result TEXT NOT NULL, -- success, failure, partial, pending
    result_details TEXT,
    error_message TEXT,

    -- Context
    request_id TEXT,
    session_id TEXT,
    ip_address INET,
    user_agent TEXT,

    -- Before/after state (for change tracking)
    state_before JSONB,
    state_after JSONB,

    -- Compliance tags
    compliance_relevant BOOLEAN DEFAULT TRUE,
    retention_period_days INTEGER DEFAULT 2555, -- 7 years for compliance

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Timestamp
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Constraints
    CONSTRAINT audit_trail_log_tenant_id_check
        CHECK (tenant_id IS NOT NULL AND length(tenant_id) > 0)
);

-- Indexes for audit trail queries
CREATE INDEX IF NOT EXISTS idx_audit_trail_tenant_id
    ON audit_trail_log(tenant_id);
CREATE INDEX IF NOT EXISTS idx_audit_trail_tenant_project
    ON audit_trail_log(tenant_id, project_id);
CREATE INDEX IF NOT EXISTS idx_audit_trail_timestamp
    ON audit_trail_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_trail_event_type
    ON audit_trail_log(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_trail_actor
    ON audit_trail_log(actor_type, actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_trail_resource
    ON audit_trail_log(resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_audit_trail_compliance
    ON audit_trail_log(compliance_relevant) WHERE compliance_relevant = TRUE;
CREATE INDEX IF NOT EXISTS idx_audit_trail_entry_id
    ON audit_trail_log(entry_id);

-- GIN index for metadata JSON queries
CREATE INDEX IF NOT EXISTS idx_audit_trail_metadata_gin
    ON audit_trail_log USING gin(metadata);

-- ==================================================================
-- Risk Register Table
-- ==================================================================

CREATE TABLE IF NOT EXISTS risk_register (
    id BIGSERIAL PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    project_id TEXT,

    -- Risk identification
    risk_id TEXT NOT NULL UNIQUE, -- RISK-001, RISK-002, etc.
    risk_title TEXT NOT NULL,
    risk_description TEXT NOT NULL,
    category TEXT NOT NULL, -- security, compliance, operational, technical, etc.

    -- Risk assessment
    probability DECIMAL(3,2) NOT NULL CHECK (probability >= 0.0 AND probability <= 1.0),
    impact DECIMAL(3,2) NOT NULL CHECK (impact >= 0.0 AND impact <= 1.0),
    risk_score DECIMAL(5,2) NOT NULL, -- Calculated: probability * impact
    risk_level TEXT NOT NULL, -- critical, high, medium, low, negligible

    -- Current status
    status TEXT NOT NULL DEFAULT 'open', -- open, mitigated, accepted, closed
    mitigation_status TEXT, -- FULLY MITIGATED, PARTIALLY MITIGATED, etc.

    -- Controls and mitigation
    mitigation_controls TEXT[] NOT NULL DEFAULT '{}',
    control_descriptions JSONB DEFAULT '{}'::jsonb,
    effectiveness_score DECIMAL(3,2) CHECK (effectiveness_score >= 0.0 AND effectiveness_score <= 1.0),

    -- Ownership
    owner TEXT,
    responsible_party TEXT,
    accountable_party TEXT,

    -- ISO 42001 mapping
    iso42001_requirements TEXT[], -- Which ISO requirements this risk relates to
    compliance_impact TEXT,

    -- Review and monitoring
    identified_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_reviewed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    next_review_due TIMESTAMPTZ,
    review_frequency_days INTEGER DEFAULT 90,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    notes TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Constraints
    CONSTRAINT risk_register_tenant_id_check
        CHECK (tenant_id IS NOT NULL AND length(tenant_id) > 0)
);

-- Indexes for risk register queries
CREATE INDEX IF NOT EXISTS idx_risk_register_tenant_id
    ON risk_register(tenant_id);
CREATE INDEX IF NOT EXISTS idx_risk_register_tenant_project
    ON risk_register(tenant_id, project_id);
CREATE INDEX IF NOT EXISTS idx_risk_register_risk_id
    ON risk_register(risk_id);
CREATE INDEX IF NOT EXISTS idx_risk_register_risk_level
    ON risk_register(risk_level);
CREATE INDEX IF NOT EXISTS idx_risk_register_status
    ON risk_register(status);
CREATE INDEX IF NOT EXISTS idx_risk_register_category
    ON risk_register(category);
CREATE INDEX IF NOT EXISTS idx_risk_register_review_due
    ON risk_register(next_review_due) WHERE status != 'closed';

-- GIN index for ISO requirements array
CREATE INDEX IF NOT EXISTS idx_risk_register_iso_requirements
    ON risk_register USING gin(iso42001_requirements);

-- ==================================================================
-- Data Retention Tracking Table
-- ==================================================================

CREATE TABLE IF NOT EXISTS data_retention_tracking (
    id BIGSERIAL PRIMARY KEY,
    tenant_id TEXT NOT NULL,

    -- Data classification
    data_class TEXT NOT NULL, -- episodic_memory, long_term_memory, audit_logs, etc.
    table_name TEXT NOT NULL,

    -- Retention policy
    retention_policy_days INTEGER NOT NULL, -- -1 for permanent
    policy_name TEXT NOT NULL,
    policy_description TEXT,

    -- Current status
    total_records BIGINT NOT NULL DEFAULT 0,
    expired_records BIGINT NOT NULL DEFAULT 0,
    deleted_records_last_30d BIGINT NOT NULL DEFAULT 0,

    -- Compliance
    compliance_percentage DECIMAL(5,2) NOT NULL DEFAULT 100.0,
    overdue_deletions BIGINT NOT NULL DEFAULT 0,

    -- Last cleanup
    last_cleanup_at TIMESTAMPTZ,
    next_cleanup_scheduled TIMESTAMPTZ,

    -- Timestamps
    checked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    CONSTRAINT data_retention_tracking_tenant_id_check
        CHECK (tenant_id IS NOT NULL AND length(tenant_id) > 0)
);

-- Indexes for retention tracking
CREATE INDEX IF NOT EXISTS idx_retention_tracking_tenant_id
    ON data_retention_tracking(tenant_id);
CREATE INDEX IF NOT EXISTS idx_retention_tracking_data_class
    ON data_retention_tracking(data_class);
CREATE INDEX IF NOT EXISTS idx_retention_tracking_compliance
    ON data_retention_tracking(compliance_percentage) WHERE compliance_percentage < 100.0;

-- ==================================================================
-- RLS Context Tracking Table
-- ==================================================================

CREATE TABLE IF NOT EXISTS rls_context_tracking (
    id BIGSERIAL PRIMARY KEY,
    tenant_id TEXT NOT NULL,

    -- Context type
    context_type TEXT NOT NULL, -- http_request, background_task, manual

    -- Success/failure
    status TEXT NOT NULL, -- success, failure
    failure_reason TEXT,

    -- Context details
    set_by TEXT, -- middleware, worker, admin
    session_id TEXT,
    request_id TEXT,

    -- Timestamp
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for RLS tracking (partition by time for performance)
CREATE INDEX IF NOT EXISTS idx_rls_tracking_tenant_id
    ON rls_context_tracking(tenant_id);
CREATE INDEX IF NOT EXISTS idx_rls_tracking_timestamp
    ON rls_context_tracking(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_rls_tracking_status
    ON rls_context_tracking(status) WHERE status = 'failure';

-- ==================================================================
-- RLS Policies (Enable on new tables)
-- ==================================================================

-- Enable RLS on compliance tables
ALTER TABLE iso42001_compliance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_trail_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE risk_register ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_retention_tracking ENABLE ROW LEVEL SECURITY;
-- rls_context_tracking is system-wide, no RLS needed

-- Create RLS policies for tenant isolation
CREATE POLICY tenant_isolation_iso42001_metrics ON iso42001_compliance_metrics
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', true)::text)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true)::text);

CREATE POLICY tenant_isolation_audit_trail ON audit_trail_log
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', true)::text)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true)::text);

CREATE POLICY tenant_isolation_risk_register ON risk_register
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', true)::text)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true)::text);

CREATE POLICY tenant_isolation_retention_tracking ON data_retention_tracking
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', true)::text)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true)::text);

-- Superuser bypass policies (for admins and maintenance)
CREATE POLICY superuser_bypass_iso42001_metrics ON iso42001_compliance_metrics
    FOR ALL
    TO postgres
    USING (true)
    WITH CHECK (true);

CREATE POLICY superuser_bypass_audit_trail ON audit_trail_log
    FOR ALL
    TO postgres
    USING (true)
    WITH CHECK (true);

CREATE POLICY superuser_bypass_risk_register ON risk_register
    FOR ALL
    TO postgres
    USING (true)
    WITH CHECK (true);

CREATE POLICY superuser_bypass_retention_tracking ON data_retention_tracking
    FOR ALL
    TO postgres
    USING (true)
    WITH CHECK (true);

-- ==================================================================
-- Helper Functions
-- ==================================================================

-- Function to calculate risk score
CREATE OR REPLACE FUNCTION calculate_risk_score(prob DECIMAL, imp DECIMAL)
RETURNS DECIMAL AS $$
BEGIN
    RETURN ROUND((prob * imp)::numeric, 2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to determine risk level from score
CREATE OR REPLACE FUNCTION get_risk_level(risk_score DECIMAL)
RETURNS TEXT AS $$
BEGIN
    IF risk_score >= 0.7 THEN
        RETURN 'critical';
    ELSIF risk_score >= 0.4 THEN
        RETURN 'high';
    ELSIF risk_score >= 0.2 THEN
        RETURN 'medium';
    ELSIF risk_score >= 0.05 THEN
        RETURN 'low';
    ELSE
        RETURN 'negligible';
    END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Trigger to automatically update risk_score and risk_level
CREATE OR REPLACE FUNCTION update_risk_score_trigger()
RETURNS TRIGGER AS $$
BEGIN
    NEW.risk_score := calculate_risk_score(NEW.probability, NEW.impact);
    NEW.risk_level := get_risk_level(NEW.risk_score);
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER risk_register_update_score
    BEFORE INSERT OR UPDATE OF probability, impact
    ON risk_register
    FOR EACH ROW
    EXECUTE FUNCTION update_risk_score_trigger();

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER risk_register_update_timestamp
    BEFORE UPDATE ON risk_register
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER retention_tracking_update_timestamp
    BEFORE UPDATE ON data_retention_tracking
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ==================================================================
-- Initial Data: Seed Risk Register from Documentation
-- ==================================================================

-- Insert known risks from RAE-Risk-Register.md
INSERT INTO risk_register (
    tenant_id, risk_id, risk_title, risk_description, category,
    probability, impact, risk_score, risk_level, status, mitigation_status,
    mitigation_controls, owner, iso42001_requirements
) VALUES
    -- RISK-001: Data Leak
    ('default', 'RISK-001', 'Wyciek danych wrażliwych',
     'Cross-tenant data contamination due to insufficient isolation', 'Security',
     0.3, 0.9, 0.27, 'high', 'mitigated', 'FULLY MITIGATED',
     ARRAY['PostgreSQL RLS', 'Tenant context middleware', 'Database-level isolation'],
     'Security Contact', ARRAY['10.1', '10.2']),

    -- RISK-002: Data Retention
    ('default', 'RISK-002', 'Nieprawidłowe przechowywanie danych',
     'GDPR non-compliance due to inadequate data retention policies', 'Compliance',
     0.4, 0.8, 0.32, 'high', 'mitigated', 'FULLY MITIGATED',
     ARRAY['RetentionService', 'Automated cleanup', 'Per-tenant policies'],
     'Data Steward', ARRAY['7.3', '10.2']),

    -- RISK-003: AI Hallucinations
    ('default', 'RISK-003', 'Halucynacje AI',
     'AI system generates false or unreliable information', 'Technical',
     0.6, 0.6, 0.36, 'high', 'mitigated', 'MITIGATED',
     ARRAY['Source trust scoring', 'Human verification', 'Confidence thresholds'],
     'ML Specialist', ARRAY['7.2', '8.1', '9.1']),

    -- RISK-006: Tenant Contamination
    ('default', 'RISK-006', 'Mieszanie wiedzy z wielu tenantów',
     'Knowledge contamination between tenants in shared AI context', 'Security',
     0.4, 0.9, 0.36, 'high', 'mitigated', 'FULLY MITIGATED',
     ARRAY['Database RLS', 'Context isolation', 'Separate vector stores'],
     'Security Contact', ARRAY['10.1', '7.3'])
ON CONFLICT (risk_id) DO NOTHING;

-- ==================================================================
-- Comments for Documentation
-- ==================================================================

COMMENT ON TABLE iso42001_compliance_metrics IS
    'Tracks compliance status for ISO/IEC 42001 requirements';
COMMENT ON TABLE audit_trail_log IS
    'Comprehensive audit trail for all system actions (ISO 42001 Section 8)';
COMMENT ON TABLE risk_register IS
    'Risk register for AI system risk management (ISO 42001 Section 6)';
COMMENT ON TABLE data_retention_tracking IS
    'Monitors data retention policy compliance (GDPR Article 5)';
COMMENT ON TABLE rls_context_tracking IS
    'Tracks RLS context setting success/failure for security monitoring';

-- ==================================================================
-- Grants (adjust based on your user model)
-- ==================================================================

-- Grant access to application user (adjust username as needed)
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO rae_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO rae_app_user;

-- ==================================================================
-- Migration Complete
-- ==================================================================

-- Verify tables were created
DO $$
BEGIN
    RAISE NOTICE 'ISO/IEC 42001 Compliance Tracking Migration Complete';
    RAISE NOTICE 'Created tables: iso42001_compliance_metrics, audit_trail_log, risk_register, data_retention_tracking, rls_context_tracking';
    RAISE NOTICE 'Enabled RLS on compliance tables with tenant isolation policies';
    RAISE NOTICE 'Seeded risk register with known risks from documentation';
END $$;
