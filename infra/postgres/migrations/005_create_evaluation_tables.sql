-- Migration 005: Evaluation System Tables (A/B Tests, Benchmarks, Results)
-- Creates database tables for evaluation, A/B testing, and benchmark management

-- ============================================================================
-- A/B Test Definitions Table
-- ============================================================================

CREATE TABLE IF NOT EXISTS ab_tests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,

    -- Test identification
    test_name TEXT NOT NULL,
    description TEXT,
    hypothesis TEXT, -- What we're testing

    -- Variants
    variant_a_name TEXT NOT NULL DEFAULT 'control',
    variant_a_config JSONB NOT NULL, -- Configuration for variant A
    variant_b_name TEXT NOT NULL DEFAULT 'treatment',
    variant_b_config JSONB NOT NULL, -- Configuration for variant B

    -- Test parameters
    traffic_split FLOAT NOT NULL DEFAULT 0.5, -- 0.0-1.0, % traffic to variant B
    min_sample_size INTEGER NOT NULL DEFAULT 100, -- Minimum samples per variant
    confidence_level FLOAT NOT NULL DEFAULT 0.95, -- Statistical confidence (0.95 = 95%)

    -- Metrics to track
    primary_metric TEXT NOT NULL, -- e.g., 'mrr', 'ndcg', 'precision'
    secondary_metrics TEXT[] DEFAULT ARRAY[]::TEXT[],

    -- Status and lifecycle
    status TEXT NOT NULL DEFAULT 'draft', -- draft, running, completed, archived
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,

    -- Results summary (populated when completed)
    winner TEXT, -- 'variant_a', 'variant_b', 'no_difference'
    confidence_score FLOAT, -- Statistical confidence in winner
    effect_size FLOAT, -- Measured effect size
    results_summary JSONB, -- Detailed statistical results

    -- Metadata
    created_by TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    metadata JSONB DEFAULT '{}'::jsonb,

    UNIQUE(tenant_id, project_id, test_name)
);

-- Indexes for A/B tests
CREATE INDEX idx_ab_tests_tenant_project ON ab_tests(tenant_id, project_id);
CREATE INDEX idx_ab_tests_status ON ab_tests(status);
CREATE INDEX idx_ab_tests_started_at ON ab_tests(started_at DESC) WHERE started_at IS NOT NULL;
CREATE INDEX idx_ab_tests_primary_metric ON ab_tests(primary_metric);

COMMENT ON TABLE ab_tests IS 'A/B test definitions for comparing search/retrieval variants';
COMMENT ON COLUMN ab_tests.traffic_split IS 'Percentage of traffic sent to variant B (0.5 = 50/50 split)';
COMMENT ON COLUMN ab_tests.results_summary IS 'Statistical analysis results including p-values, effect sizes, and confidence intervals';

-- ============================================================================
-- A/B Test Results Table (Individual Observations)
-- ============================================================================

CREATE TABLE IF NOT EXISTS ab_test_results (
    id BIGSERIAL PRIMARY KEY,
    test_id UUID NOT NULL REFERENCES ab_tests(id) ON DELETE CASCADE,
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,

    -- Variant assignment
    variant TEXT NOT NULL, -- 'variant_a' or 'variant_b'

    -- Query/request info
    query_id UUID, -- Optional query identifier
    query_text TEXT,
    session_id TEXT,

    -- Metric values
    metric_values JSONB NOT NULL, -- {"mrr": 0.85, "ndcg": 0.75, "latency_ms": 120}

    -- Results
    retrieved_count INTEGER,
    relevance_labels INTEGER[], -- Relevance scores for retrieved docs

    -- Timing
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    execution_time_ms INTEGER,

    -- Metadata
    user_feedback TEXT, -- Optional: 'thumbs_up', 'thumbs_down', 'neutral'
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for A/B test results
CREATE INDEX idx_ab_test_results_test_id ON ab_test_results(test_id);
CREATE INDEX idx_ab_test_results_variant ON ab_test_results(test_id, variant);
CREATE INDEX idx_ab_test_results_recorded_at ON ab_test_results(recorded_at DESC);
CREATE INDEX idx_ab_test_results_query_id ON ab_test_results(query_id) WHERE query_id IS NOT NULL;

COMMENT ON TABLE ab_test_results IS 'Individual observations from A/B tests for statistical analysis';
COMMENT ON COLUMN ab_test_results.metric_values IS 'JSON object with all metric measurements for this observation';

-- ============================================================================
-- Benchmark Suites Table
-- ============================================================================

CREATE TABLE IF NOT EXISTS benchmark_suites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,

    -- Suite identification
    suite_name TEXT NOT NULL,
    description TEXT,
    version TEXT DEFAULT '1.0',

    -- Configuration
    test_queries JSONB NOT NULL, -- Array of test query objects
    evaluation_criteria JSONB NOT NULL, -- Metrics and thresholds
    expected_results JSONB, -- Optional: ground truth for comparison

    -- Execution settings
    timeout_seconds INTEGER DEFAULT 300,
    parallel_execution BOOLEAN DEFAULT FALSE,
    retry_on_failure BOOLEAN DEFAULT TRUE,

    -- Status
    status TEXT NOT NULL DEFAULT 'active', -- active, archived, deprecated
    is_baseline BOOLEAN DEFAULT FALSE, -- Is this the baseline for comparison?

    -- Statistics
    total_queries INTEGER NOT NULL DEFAULT 0,
    last_execution_id UUID, -- Reference to last run
    last_executed_at TIMESTAMPTZ,
    execution_count INTEGER NOT NULL DEFAULT 0,

    -- Metadata
    created_by TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    metadata JSONB DEFAULT '{}'::jsonb,

    UNIQUE(tenant_id, project_id, suite_name, version)
);

-- Indexes for benchmark suites
CREATE INDEX idx_benchmark_suites_tenant_project ON benchmark_suites(tenant_id, project_id);
CREATE INDEX idx_benchmark_suites_status ON benchmark_suites(status);
CREATE INDEX idx_benchmark_suites_baseline ON benchmark_suites(is_baseline) WHERE is_baseline = TRUE;

COMMENT ON TABLE benchmark_suites IS 'Reusable benchmark test suites for evaluating search quality';
COMMENT ON COLUMN benchmark_suites.test_queries IS 'Array of test query objects with expected results';
COMMENT ON COLUMN benchmark_suites.evaluation_criteria IS 'Metrics, thresholds, and pass/fail criteria';

-- ============================================================================
-- Benchmark Executions Table
-- ============================================================================

CREATE TABLE IF NOT EXISTS benchmark_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    suite_id UUID NOT NULL REFERENCES benchmark_suites(id) ON DELETE CASCADE,
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,

    -- Execution metadata
    execution_label TEXT, -- Optional: 'before-refactor', 'after-optimization', etc.
    triggered_by TEXT, -- 'manual', 'ci/cd', 'scheduled', 'api'
    git_commit_hash TEXT, -- Optional: for tracking code version

    -- Configuration used
    config_snapshot JSONB, -- Snapshot of config at execution time

    -- Results
    status TEXT NOT NULL DEFAULT 'pending', -- pending, running, completed, failed
    queries_executed INTEGER DEFAULT 0,
    queries_passed INTEGER DEFAULT 0,
    queries_failed INTEGER DEFAULT 0,

    -- Metrics
    overall_score FLOAT, -- 0.0-1.0
    metric_scores JSONB, -- Individual metric scores
    passed_criteria BOOLEAN DEFAULT FALSE, -- Did it meet all threshold criteria?

    -- Performance
    total_execution_time_ms INTEGER,
    avg_query_time_ms FLOAT,

    -- Comparison with baseline
    baseline_execution_id UUID, -- Reference to baseline for comparison
    improvement_vs_baseline FLOAT, -- % improvement (positive) or regression (negative)

    -- Timing
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,

    -- Error handling
    error_message TEXT,
    error_details JSONB,

    -- Detailed results
    query_results JSONB, -- Array of individual query results

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for benchmark executions
CREATE INDEX idx_benchmark_executions_suite_id ON benchmark_executions(suite_id);
CREATE INDEX idx_benchmark_executions_status ON benchmark_executions(status);
CREATE INDEX idx_benchmark_executions_started_at ON benchmark_executions(started_at DESC);
CREATE INDEX idx_benchmark_executions_baseline ON benchmark_executions(baseline_execution_id) WHERE baseline_execution_id IS NOT NULL;
CREATE INDEX idx_benchmark_executions_git_commit ON benchmark_executions(git_commit_hash) WHERE git_commit_hash IS NOT NULL;

COMMENT ON TABLE benchmark_executions IS 'Historical record of benchmark suite executions';
COMMENT ON COLUMN benchmark_executions.improvement_vs_baseline IS 'Percentage improvement compared to baseline (positive=better, negative=worse)';

-- ============================================================================
-- Update Triggers
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_ab_tests_updated_at BEFORE UPDATE ON ab_tests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_benchmark_suites_updated_at BEFORE UPDATE ON benchmark_suites
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Statistics Update Triggers
-- ============================================================================

-- Update A/B test summary when results are added
CREATE OR REPLACE FUNCTION update_ab_test_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- Update result counts in ab_tests table
    UPDATE ab_tests
    SET updated_at = NOW()
    WHERE id = NEW.test_id;

    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER ab_test_results_stats_update
    AFTER INSERT ON ab_test_results
    FOR EACH ROW
    EXECUTE FUNCTION update_ab_test_stats();

-- Update benchmark suite execution stats
CREATE OR REPLACE FUNCTION update_benchmark_suite_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' AND (OLD.status IS NULL OR OLD.status != 'completed') THEN
        UPDATE benchmark_suites
        SET
            last_execution_id = NEW.id,
            last_executed_at = NEW.completed_at,
            execution_count = execution_count + 1,
            updated_at = NOW()
        WHERE id = NEW.suite_id;
    END IF;

    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER benchmark_execution_stats_update
    AFTER UPDATE ON benchmark_executions
    FOR EACH ROW
    WHEN (NEW.status = 'completed')
    EXECUTE FUNCTION update_benchmark_suite_stats();

-- ============================================================================
-- Data Validation
-- ============================================================================

-- Validate A/B test status
ALTER TABLE ab_tests ADD CONSTRAINT ab_test_status_check
    CHECK (status IN ('draft', 'running', 'completed', 'archived'));

-- Validate variant selection
ALTER TABLE ab_test_results ADD CONSTRAINT ab_test_variant_check
    CHECK (variant IN ('variant_a', 'variant_b'));

-- Validate benchmark suite status
ALTER TABLE benchmark_suites ADD CONSTRAINT benchmark_suite_status_check
    CHECK (status IN ('active', 'archived', 'deprecated'));

-- Validate benchmark execution status
ALTER TABLE benchmark_executions ADD CONSTRAINT benchmark_execution_status_check
    CHECK (status IN ('pending', 'running', 'completed', 'failed'));

-- Validate traffic split
ALTER TABLE ab_tests ADD CONSTRAINT traffic_split_check
    CHECK (traffic_split >= 0.0 AND traffic_split <= 1.0);

-- Validate confidence level
ALTER TABLE ab_tests ADD CONSTRAINT confidence_level_check
    CHECK (confidence_level >= 0.0 AND confidence_level <= 1.0);

-- ============================================================================
-- Helper Functions
-- ============================================================================

-- Function to calculate A/B test statistics
CREATE OR REPLACE FUNCTION calculate_ab_test_statistics(p_test_id UUID)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    -- This would contain statistical calculations (t-test, effect size, etc.)
    -- Placeholder for now - implement full statistical analysis in application code

    SELECT jsonb_build_object(
        'variant_a_count', COUNT(*) FILTER (WHERE variant = 'variant_a'),
        'variant_b_count', COUNT(*) FILTER (WHERE variant = 'variant_b'),
        'variant_a_avg', AVG((metric_values->>'mrr')::float) FILTER (WHERE variant = 'variant_a'),
        'variant_b_avg', AVG((metric_values->>'mrr')::float) FILTER (WHERE variant = 'variant_b')
    )
    INTO result
    FROM ab_test_results
    WHERE test_id = p_test_id;

    RETURN result;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION calculate_ab_test_statistics IS 'Calculate basic statistics for A/B test (extend with full statistical tests)';

-- ============================================================================
-- Rollback Script
-- ============================================================================

-- To rollback this migration:
-- DROP TRIGGER IF EXISTS benchmark_execution_stats_update ON benchmark_executions;
-- DROP TRIGGER IF EXISTS ab_test_results_stats_update ON ab_test_results;
-- DROP TRIGGER IF EXISTS update_benchmark_suites_updated_at ON benchmark_suites;
-- DROP TRIGGER IF EXISTS update_ab_tests_updated_at ON ab_tests;
-- DROP FUNCTION IF EXISTS calculate_ab_test_statistics(UUID);
-- DROP FUNCTION IF EXISTS update_benchmark_suite_stats();
-- DROP FUNCTION IF EXISTS update_ab_test_stats();
-- DROP TABLE IF EXISTS benchmark_executions;
-- DROP TABLE IF EXISTS benchmark_suites;
-- DROP TABLE IF EXISTS ab_test_results;
-- DROP TABLE IF EXISTS ab_tests;
