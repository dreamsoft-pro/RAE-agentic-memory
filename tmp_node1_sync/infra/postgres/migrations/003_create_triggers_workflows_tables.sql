-- Migration 003: Event Triggers and Workflows Tables
-- Creates database tables for storing trigger rules, workflows, and execution history

-- ============================================================================
-- Trigger Rules Table
-- ============================================================================

CREATE TABLE IF NOT EXISTS trigger_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    description TEXT,

    -- Event matching
    event_types TEXT[] NOT NULL, -- List of event types to match

    -- Conditions (stored as JSONB for flexibility)
    conditions JSONB NOT NULL DEFAULT '[]'::jsonb, -- Array of condition objects
    condition_operator TEXT NOT NULL DEFAULT 'AND', -- 'AND' or 'OR'

    -- Actions (stored as JSONB)
    actions JSONB NOT NULL DEFAULT '[]'::jsonb, -- Array of action objects

    -- Configuration
    priority INTEGER NOT NULL DEFAULT 0, -- Higher priority triggers fire first
    status TEXT NOT NULL DEFAULT 'active', -- 'active', 'inactive', 'paused', 'error'
    retry_config JSONB, -- Retry configuration (max_retries, backoff, etc.)

    -- Metadata
    created_by TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_executed_at TIMESTAMPTZ,
    execution_count INTEGER NOT NULL DEFAULT 0,
    error_count INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,

    -- Template metadata
    template_id TEXT, -- If created from template
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    metadata JSONB DEFAULT '{}'::jsonb,

    UNIQUE(tenant_id, project_id, rule_name)
);

-- Indexes for trigger rules
CREATE INDEX idx_trigger_rules_tenant_project ON trigger_rules(tenant_id, project_id);
CREATE INDEX idx_trigger_rules_status ON trigger_rules(status);
CREATE INDEX idx_trigger_rules_event_types ON trigger_rules USING GIN(event_types);
CREATE INDEX idx_trigger_rules_priority ON trigger_rules(priority DESC);
CREATE INDEX idx_trigger_rules_template ON trigger_rules(template_id) WHERE template_id IS NOT NULL;

COMMENT ON TABLE trigger_rules IS 'Event trigger rules that automatically execute actions when conditions are met';
COMMENT ON COLUMN trigger_rules.conditions IS 'Array of condition objects: [{field, operator, value}, ...]';
COMMENT ON COLUMN trigger_rules.actions IS 'Array of action objects: [{action_type, config}, ...]';
COMMENT ON COLUMN trigger_rules.retry_config IS 'Retry configuration for failed actions';

-- ============================================================================
-- Workflows Table
-- ============================================================================

CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,
    workflow_name TEXT NOT NULL,
    description TEXT,

    -- Workflow definition
    steps JSONB NOT NULL DEFAULT '[]'::jsonb, -- Array of step objects
    execution_mode TEXT NOT NULL DEFAULT 'sequential', -- 'sequential', 'parallel', 'dag'

    -- Configuration
    status TEXT NOT NULL DEFAULT 'active', -- 'active', 'inactive', 'draft'
    timeout_seconds INTEGER DEFAULT 3600, -- Workflow timeout (1 hour default)
    retry_policy JSONB, -- Retry policy for failed steps

    -- Metadata
    created_by TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_executed_at TIMESTAMPTZ,
    execution_count INTEGER NOT NULL DEFAULT 0,
    success_count INTEGER NOT NULL DEFAULT 0,
    failure_count INTEGER NOT NULL DEFAULT 0,

    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    metadata JSONB DEFAULT '{}'::jsonb,

    UNIQUE(tenant_id, project_id, workflow_name)
);

-- Indexes for workflows
CREATE INDEX idx_workflows_tenant_project ON workflows(tenant_id, project_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflows_created_at ON workflows(created_at DESC);

COMMENT ON TABLE workflows IS 'Multi-step workflows that chain multiple actions with dependency management';
COMMENT ON COLUMN workflows.steps IS 'Array of workflow steps with dependencies and actions';
COMMENT ON COLUMN workflows.execution_mode IS 'How steps are executed: sequential, parallel, or DAG';

-- ============================================================================
-- Trigger Executions Table (Audit Log)
-- ============================================================================

CREATE TABLE IF NOT EXISTS trigger_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trigger_id UUID NOT NULL REFERENCES trigger_rules(id) ON DELETE CASCADE,
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,

    -- Execution details
    event_id UUID, -- The event that triggered this execution
    event_type TEXT NOT NULL,
    event_payload JSONB, -- Event data

    -- Results
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'running', 'success', 'failed', 'cancelled'
    actions_executed INTEGER NOT NULL DEFAULT 0,
    actions_succeeded INTEGER NOT NULL DEFAULT 0,
    actions_failed INTEGER NOT NULL DEFAULT 0,

    -- Timing
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    duration_ms INTEGER, -- Execution duration in milliseconds

    -- Error handling
    error_message TEXT,
    error_details JSONB,
    retry_count INTEGER NOT NULL DEFAULT 0,

    -- Results
    action_results JSONB, -- Array of action execution results
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for trigger executions
CREATE INDEX idx_trigger_executions_trigger_id ON trigger_executions(trigger_id);
CREATE INDEX idx_trigger_executions_tenant_project ON trigger_executions(tenant_id, project_id);
CREATE INDEX idx_trigger_executions_status ON trigger_executions(status);
CREATE INDEX idx_trigger_executions_started_at ON trigger_executions(started_at DESC);
CREATE INDEX idx_trigger_executions_event_id ON trigger_executions(event_id) WHERE event_id IS NOT NULL;

COMMENT ON TABLE trigger_executions IS 'Audit log of trigger rule executions with results and timing';
COMMENT ON COLUMN trigger_executions.action_results IS 'Detailed results for each action executed';

-- ============================================================================
-- Workflow Executions Table
-- ============================================================================

CREATE TABLE IF NOT EXISTS workflow_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,

    -- Execution details
    trigger_source TEXT, -- What triggered this workflow (manual, scheduled, event, api)
    input_data JSONB, -- Input parameters for workflow

    -- Status
    status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'running', 'success', 'failed', 'cancelled', 'timeout'
    current_step INTEGER DEFAULT 0, -- Current step index
    steps_completed INTEGER NOT NULL DEFAULT 0,
    steps_failed INTEGER NOT NULL DEFAULT 0,

    -- Timing
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    duration_ms INTEGER,

    -- Results
    step_results JSONB, -- Array of step execution results
    final_output JSONB, -- Final workflow output

    -- Error handling
    error_message TEXT,
    error_step INTEGER, -- Step index where error occurred
    error_details JSONB,

    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for workflow executions
CREATE INDEX idx_workflow_executions_workflow_id ON workflow_executions(workflow_id);
CREATE INDEX idx_workflow_executions_tenant_project ON workflow_executions(tenant_id, project_id);
CREATE INDEX idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX idx_workflow_executions_started_at ON workflow_executions(started_at DESC);

COMMENT ON TABLE workflow_executions IS 'Execution history for workflows with step-by-step results';
COMMENT ON COLUMN workflow_executions.step_results IS 'Results for each executed step';

-- ============================================================================
-- Update Triggers
-- ============================================================================

-- Automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_trigger_rules_updated_at BEFORE UPDATE ON trigger_rules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON workflows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Execution Stats Update Trigger
-- ============================================================================

-- Update trigger_rules stats when execution completes
CREATE OR REPLACE FUNCTION update_trigger_execution_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'success' AND (OLD.status IS NULL OR OLD.status != 'success') THEN
        UPDATE trigger_rules
        SET execution_count = execution_count + 1,
            last_executed_at = NEW.completed_at
        WHERE id = NEW.trigger_id;
    ELSIF NEW.status = 'failed' AND (OLD.status IS NULL OR OLD.status != 'failed') THEN
        UPDATE trigger_rules
        SET execution_count = execution_count + 1,
            error_count = error_count + 1,
            last_executed_at = NEW.completed_at,
            last_error = NEW.error_message
        WHERE id = NEW.trigger_id;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_execution_stats_update
    AFTER UPDATE ON trigger_executions
    FOR EACH ROW
    WHEN (NEW.status IN ('success', 'failed') AND OLD.status NOT IN ('success', 'failed'))
    EXECUTE FUNCTION update_trigger_execution_stats();

-- Update workflow stats when execution completes
CREATE OR REPLACE FUNCTION update_workflow_execution_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'success' AND (OLD.status IS NULL OR OLD.status != 'success') THEN
        UPDATE workflows
        SET execution_count = execution_count + 1,
            success_count = success_count + 1,
            last_executed_at = NEW.completed_at
        WHERE id = NEW.workflow_id;
    ELSIF NEW.status = 'failed' AND (OLD.status IS NULL OR OLD.status != 'failed') THEN
        UPDATE workflows
        SET execution_count = execution_count + 1,
            failure_count = failure_count + 1,
            last_executed_at = NEW.completed_at
        WHERE id = NEW.workflow_id;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER workflow_execution_stats_update
    AFTER UPDATE ON workflow_executions
    FOR EACH ROW
    WHEN (NEW.status IN ('success', 'failed') AND OLD.status NOT IN ('success', 'failed'))
    EXECUTE FUNCTION update_workflow_execution_stats();

-- ============================================================================
-- Data Validation
-- ============================================================================

-- Validate trigger status
ALTER TABLE trigger_rules ADD CONSTRAINT trigger_status_check
    CHECK (status IN ('active', 'inactive', 'paused', 'error'));

-- Validate workflow status
ALTER TABLE workflows ADD CONSTRAINT workflow_status_check
    CHECK (status IN ('active', 'inactive', 'draft'));

-- Validate workflow execution mode
ALTER TABLE workflows ADD CONSTRAINT workflow_execution_mode_check
    CHECK (execution_mode IN ('sequential', 'parallel', 'dag'));

-- Validate trigger execution status
ALTER TABLE trigger_executions ADD CONSTRAINT trigger_execution_status_check
    CHECK (status IN ('pending', 'running', 'success', 'failed', 'cancelled'));

-- Validate workflow execution status
ALTER TABLE workflow_executions ADD CONSTRAINT workflow_execution_status_check
    CHECK (status IN ('pending', 'running', 'success', 'failed', 'cancelled', 'timeout'));

-- ============================================================================
-- Default Data
-- ============================================================================

-- Insert example trigger template metadata (optional)
-- This can be used by the API to validate template instantiation
-- The actual template definitions are in the application code

COMMENT ON COLUMN trigger_rules.template_id IS 'Template ID if created from predefined template (see DEFAULT_TEMPLATES in code)';

-- ============================================================================
-- Rollback Script
-- ============================================================================

-- To rollback this migration:
-- DROP TRIGGER IF EXISTS workflow_execution_stats_update ON workflow_executions;
-- DROP TRIGGER IF EXISTS trigger_execution_stats_update ON trigger_executions;
-- DROP TRIGGER IF EXISTS update_workflows_updated_at ON workflows;
-- DROP TRIGGER IF EXISTS update_trigger_rules_updated_at ON trigger_rules;
-- DROP FUNCTION IF EXISTS update_workflow_execution_stats();
-- DROP FUNCTION IF EXISTS update_trigger_execution_stats();
-- DROP FUNCTION IF EXISTS update_updated_at_column();
-- DROP TABLE IF EXISTS workflow_executions;
-- DROP TABLE IF EXISTS trigger_executions;
-- DROP TABLE IF EXISTS workflows;
-- DROP TABLE IF EXISTS trigger_rules;
