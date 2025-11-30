-- Migration 004: Dashboard Metrics Time Series Table
-- Creates table for storing time series metrics data for dashboard visualizations

-- ============================================================================
-- Metrics Time Series Table
-- ============================================================================

CREATE TABLE IF NOT EXISTS metrics_timeseries (
    id BIGSERIAL PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    project_id TEXT NOT NULL,

    -- Metric identification
    metric_name TEXT NOT NULL, -- e.g., 'memory_count', 'reflection_count', 'search_quality_mrr'
    metric_type TEXT NOT NULL DEFAULT 'gauge', -- 'gauge', 'counter', 'histogram'

    -- Metric value
    value DOUBLE PRECISION NOT NULL,
    value_unit TEXT, -- Optional unit (e.g., 'count', 'percentage', 'milliseconds')

    -- Time dimension
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    aggregation_period TEXT, -- 'minute', 'hour', 'day' - indicates aggregation level

    -- Additional dimensions (for filtering and grouping)
    dimensions JSONB DEFAULT '{}'::jsonb, -- e.g., {"layer": "em", "status": "active"}
    tags TEXT[] DEFAULT ARRAY[]::TEXT[], -- For quick filtering

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb, -- Additional metadata about this data point

    -- Index for efficient queries
    CONSTRAINT metrics_timeseries_valid_type CHECK (metric_type IN ('gauge', 'counter', 'histogram'))
);

-- ============================================================================
-- Indexes for Time Series Queries
-- ============================================================================

-- Primary query pattern: metric_name + tenant + time range
CREATE INDEX idx_metrics_ts_metric_tenant_time ON metrics_timeseries(metric_name, tenant_id, timestamp DESC);

-- Query by project
CREATE INDEX idx_metrics_ts_project_time ON metrics_timeseries(tenant_id, project_id, timestamp DESC);

-- Query specific metric for tenant
CREATE INDEX idx_metrics_ts_metric_time ON metrics_timeseries(metric_name, timestamp DESC);

-- Fast lookups by tags
CREATE INDEX idx_metrics_ts_tags ON metrics_timeseries USING GIN(tags);

-- Dimensions filtering
CREATE INDEX idx_metrics_ts_dimensions ON metrics_timeseries USING GIN(dimensions);

-- Composite index for common dashboard queries
CREATE INDEX idx_metrics_ts_dashboard_query ON metrics_timeseries(tenant_id, project_id, metric_name, timestamp DESC);

COMMENT ON TABLE metrics_timeseries IS 'Time series metrics data for dashboard visualizations and monitoring';
COMMENT ON COLUMN metrics_timeseries.metric_name IS 'Metric identifier (e.g., memory_count, avg_importance, search_quality_mrr)';
COMMENT ON COLUMN metrics_timeseries.metric_type IS 'Type of metric: gauge (point-in-time value), counter (cumulative), histogram (distribution)';
COMMENT ON COLUMN metrics_timeseries.dimensions IS 'Additional dimensions for filtering (e.g., {"layer": "em", "importance_range": "high"})';
COMMENT ON COLUMN metrics_timeseries.aggregation_period IS 'Time granularity of this data point (minute/hour/day for pre-aggregated data)';

-- ============================================================================
-- Hypertable Configuration (TimescaleDB) - Optional
-- ============================================================================

-- If TimescaleDB extension is available, convert to hypertable for better performance
-- This is optional and will fail gracefully if TimescaleDB is not installed

DO $$
BEGIN
    -- Check if TimescaleDB extension exists
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        -- Convert to hypertable with 7-day chunks
        PERFORM create_hypertable(
            'metrics_timeseries',
            'timestamp',
            chunk_time_interval => INTERVAL '7 days',
            if_not_exists => TRUE
        );

        -- Add compression policy (compress data older than 30 days)
        PERFORM add_compression_policy(
            'metrics_timeseries',
            INTERVAL '30 days',
            if_not_exists => TRUE
        );

        -- Add retention policy (keep data for 1 year)
        PERFORM add_retention_policy(
            'metrics_timeseries',
            INTERVAL '365 days',
            if_not_exists => TRUE
        );

        RAISE NOTICE 'TimescaleDB hypertable created for metrics_timeseries';
    ELSE
        RAISE NOTICE 'TimescaleDB not available, using regular PostgreSQL table';
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'TimescaleDB configuration skipped: %', SQLERRM;
END;
$$;

-- ============================================================================
-- Metric Definitions Reference Table (Optional)
-- ============================================================================

CREATE TABLE IF NOT EXISTS metric_definitions (
    metric_name TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    description TEXT,
    metric_type TEXT NOT NULL,
    value_unit TEXT,
    aggregation_method TEXT, -- 'avg', 'sum', 'count', 'max', 'min', 'last'
    collection_interval_seconds INTEGER, -- How often this metric is collected
    retention_days INTEGER DEFAULT 365, -- How long to keep this metric
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for metric definitions
CREATE INDEX idx_metric_definitions_active ON metric_definitions(is_active) WHERE is_active = TRUE;

COMMENT ON TABLE metric_definitions IS 'Definitions and metadata for available metrics';

-- ============================================================================
-- Insert Default Metric Definitions
-- ============================================================================

INSERT INTO metric_definitions (metric_name, display_name, description, metric_type, value_unit, aggregation_method, collection_interval_seconds)
VALUES
    ('memory_count', 'Memory Count', 'Total number of memories in the system', 'gauge', 'count', 'sum', 300),
    ('reflection_count', 'Reflection Count', 'Total number of reflections generated', 'gauge', 'count', 'sum', 300),
    ('semantic_nodes_count', 'Semantic Nodes', 'Total number of semantic nodes in knowledge graph', 'gauge', 'count', 'sum', 300),
    ('degraded_nodes_count', 'Degraded Nodes', 'Number of degraded semantic nodes', 'gauge', 'count', 'sum', 300),
    ('search_quality_mrr', 'Search Quality (MRR)', 'Mean Reciprocal Rank for search results', 'gauge', 'score', 'avg', 600),
    ('avg_importance', 'Average Importance', 'Average importance score across all memories', 'gauge', 'score', 'avg', 300),
    ('api_requests_total', 'API Requests', 'Total number of API requests', 'counter', 'count', 'sum', 60),
    ('api_latency_ms', 'API Latency', 'Average API response time', 'histogram', 'milliseconds', 'avg', 60),
    ('storage_size_bytes', 'Storage Size', 'Total storage size used', 'gauge', 'bytes', 'sum', 3600),
    ('active_triggers', 'Active Triggers', 'Number of active trigger rules', 'gauge', 'count', 'sum', 600)
ON CONFLICT (metric_name) DO NOTHING;

-- ============================================================================
-- Helper Functions
-- ============================================================================

-- Function to record a metric data point
CREATE OR REPLACE FUNCTION record_metric(
    p_tenant_id TEXT,
    p_project_id TEXT,
    p_metric_name TEXT,
    p_value DOUBLE PRECISION,
    p_dimensions JSONB DEFAULT '{}'::jsonb,
    p_tags TEXT[] DEFAULT ARRAY[]::TEXT[]
) RETURNS BIGINT AS $$
DECLARE
    metric_id BIGINT;
    metric_type_value TEXT;
BEGIN
    -- Get metric type from definitions
    SELECT metric_type INTO metric_type_value
    FROM metric_definitions
    WHERE metric_name = p_metric_name;

    -- Default to 'gauge' if not found
    IF metric_type_value IS NULL THEN
        metric_type_value := 'gauge';
    END IF;

    -- Insert metric data point
    INSERT INTO metrics_timeseries (
        tenant_id, project_id, metric_name, metric_type,
        value, dimensions, tags, timestamp
    )
    VALUES (
        p_tenant_id, p_project_id, p_metric_name, metric_type_value,
        p_value, p_dimensions, p_tags, NOW()
    )
    RETURNING id INTO metric_id;

    RETURN metric_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION record_metric IS 'Helper function to record a single metric data point';

-- Function to get time series data for a metric
CREATE OR REPLACE FUNCTION get_metric_timeseries(
    p_tenant_id TEXT,
    p_project_id TEXT,
    p_metric_name TEXT,
    p_start_time TIMESTAMPTZ,
    p_end_time TIMESTAMPTZ,
    p_aggregation_interval INTERVAL DEFAULT INTERVAL '1 hour'
) RETURNS TABLE (
    bucket_timestamp TIMESTAMPTZ,
    metric_value DOUBLE PRECISION,
    data_points INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        time_bucket(p_aggregation_interval, timestamp) AS bucket_timestamp,
        AVG(value) AS metric_value,
        COUNT(*)::INTEGER AS data_points
    FROM metrics_timeseries
    WHERE tenant_id = p_tenant_id
      AND project_id = p_project_id
      AND metric_name = p_metric_name
      AND timestamp BETWEEN p_start_time AND p_end_time
    GROUP BY bucket_timestamp
    ORDER BY bucket_timestamp ASC;
EXCEPTION
    WHEN undefined_function THEN
        -- Fallback if time_bucket (TimescaleDB) is not available
        RETURN QUERY
        SELECT
            date_trunc('hour', timestamp)::TIMESTAMPTZ AS bucket_timestamp,
            AVG(value) AS metric_value,
            COUNT(*)::INTEGER AS data_points
        FROM metrics_timeseries
        WHERE tenant_id = p_tenant_id
          AND project_id = p_project_id
          AND metric_name = p_metric_name
          AND timestamp BETWEEN p_start_time AND p_end_time
        GROUP BY date_trunc('hour', timestamp)
        ORDER BY date_trunc('hour', timestamp) ASC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_metric_timeseries IS 'Get aggregated time series data for a metric over a time range';

-- ============================================================================
-- Cleanup Old Data (Partitioning Alternative)
-- ============================================================================

-- Function to clean up old metrics data
CREATE OR REPLACE FUNCTION cleanup_old_metrics(retention_days INTEGER DEFAULT 365)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM metrics_timeseries
    WHERE timestamp < NOW() - (retention_days || ' days')::INTERVAL;

    GET DIAGNOSTICS deleted_count = ROW_COUNT;

    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION cleanup_old_metrics IS 'Delete metrics data older than specified retention period';

-- ============================================================================
-- Rollback Script
-- ============================================================================

-- To rollback this migration:
-- DROP FUNCTION IF EXISTS cleanup_old_metrics(INTEGER);
-- DROP FUNCTION IF EXISTS get_metric_timeseries(TEXT, TEXT, TEXT, TIMESTAMPTZ, TIMESTAMPTZ, INTERVAL);
-- DROP FUNCTION IF EXISTS record_metric(TEXT, TEXT, TEXT, DOUBLE PRECISION, JSONB, TEXT[]);
-- DROP TABLE IF EXISTS metric_definitions;
-- DROP TABLE IF EXISTS metrics_timeseries;
