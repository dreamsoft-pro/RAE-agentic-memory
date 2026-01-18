-- Migration 006: Enable Row-Level Security (RLS) for Multi-Tenant Isolation
-- ISO/IEC 42001 Compliance: RISK-001 (Data Leak), RISK-006 (Tenant Contamination)
--
-- This migration enables PostgreSQL Row-Level Security (RLS) to enforce tenant isolation
-- at the database level. Even if application code has a bug, the database will prevent
-- cross-tenant data access.
--
-- IMPORTANT: This is a critical security control. Test thoroughly before production deployment.

-- ============================================================================
-- 1. Enable RLS on core tables
-- ============================================================================

-- Memories table (primary data)
ALTER TABLE memories ENABLE ROW LEVEL SECURITY;

-- Semantic nodes (knowledge graph)
ALTER TABLE IF EXISTS semantic_nodes ENABLE ROW LEVEL SECURITY;

-- Graph triples (relationships)
ALTER TABLE IF EXISTS graph_triples ENABLE ROW LEVEL SECURITY;

-- Reflections (meta-learning)
ALTER TABLE IF EXISTS reflections ENABLE ROW LEVEL SECURITY;

-- Cost logs (financial tracking)
ALTER TABLE IF EXISTS cost_logs ENABLE ROW LEVEL SECURITY;

-- Audit logs (compliance)
ALTER TABLE IF EXISTS audit_logs ENABLE ROW LEVEL SECURITY;

-- Deletion audit (GDPR compliance)
ALTER TABLE IF EXISTS deletion_audit_log ENABLE ROW LEVEL SECURITY;


-- ============================================================================
-- 2. Create RLS policies for tenant isolation
-- ============================================================================

-- Policy: Users can only see their own tenant's memories
CREATE POLICY tenant_isolation_memories ON memories
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', true)::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true)::uuid);

-- Policy: Semantic nodes isolation
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'semantic_nodes') THEN
        EXECUTE 'CREATE POLICY tenant_isolation_semantic_nodes ON semantic_nodes
            FOR ALL
            USING (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)
            WITH CHECK (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)';
    END IF;
END $$;

-- Policy: Graph triples isolation
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'graph_triples') THEN
        EXECUTE 'CREATE POLICY tenant_isolation_graph_triples ON graph_triples
            FOR ALL
            USING (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)
            WITH CHECK (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)';
    END IF;
END $$;

-- Policy: Reflections isolation
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'reflections') THEN
        EXECUTE 'CREATE POLICY tenant_isolation_reflections ON reflections
            FOR ALL
            USING (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)
            WITH CHECK (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)';
    END IF;
END $$;

-- Policy: Cost logs isolation
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'cost_logs') THEN
        EXECUTE 'CREATE POLICY tenant_isolation_cost_logs ON cost_logs
            FOR ALL
            USING (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)
            WITH CHECK (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)';
    END IF;
END $$;

-- Policy: Audit logs isolation
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'audit_logs') THEN
        EXECUTE 'CREATE POLICY tenant_isolation_audit_logs ON audit_logs
            FOR ALL
            USING (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)
            WITH CHECK (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)';
    END IF;
END $$;

-- Policy: Deletion audit isolation
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'deletion_audit_log') THEN
        EXECUTE 'CREATE POLICY tenant_isolation_deletion_audit ON deletion_audit_log
            FOR ALL
            USING (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)
            WITH CHECK (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)';
    END IF;
END $$;


-- ============================================================================
-- 3. Create policy for superuser bypass (admin operations)
-- ============================================================================

-- Allow superusers to bypass RLS for admin operations
-- This is needed for maintenance, backups, and cross-tenant operations

CREATE POLICY superuser_bypass_memories ON memories
    FOR ALL
    TO postgres  -- Adjust to your superuser role
    USING (true)
    WITH CHECK (true);

-- Repeat for other tables if needed (conditional)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'semantic_nodes') THEN
        EXECUTE 'CREATE POLICY superuser_bypass_semantic_nodes ON semantic_nodes
            FOR ALL TO postgres USING (true) WITH CHECK (true)';
    END IF;
END $$;


-- ============================================================================
-- 4. Grant appropriate permissions
-- ============================================================================

-- Ensure application role has necessary permissions
-- Replace 'rae_app_user' with your actual application database role

DO $$
BEGIN
    -- Only grant if role exists
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'rae_app_user') THEN
        GRANT SELECT, INSERT, UPDATE, DELETE ON memories TO rae_app_user;

        IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'semantic_nodes') THEN
            GRANT SELECT, INSERT, UPDATE, DELETE ON semantic_nodes TO rae_app_user;
        END IF;

        IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'graph_triples') THEN
            GRANT SELECT, INSERT, UPDATE, DELETE ON graph_triples TO rae_app_user;
        END IF;

        IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'reflections') THEN
            GRANT SELECT, INSERT, UPDATE, DELETE ON reflections TO rae_app_user;
        END IF;

        IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'cost_logs') THEN
            GRANT SELECT, INSERT, UPDATE, DELETE ON cost_logs TO rae_app_user;
        END IF;
    END IF;
END $$;


-- ============================================================================
-- 5. Create helper functions for RLS
-- ============================================================================

-- Function to set tenant context (called by application middleware)
CREATE OR REPLACE FUNCTION set_current_tenant(tenant_uuid uuid)
RETURNS void AS $$
BEGIN
    PERFORM set_config('app.current_tenant_id', tenant_uuid::text, false);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get current tenant (for debugging)
CREATE OR REPLACE FUNCTION get_current_tenant()
RETURNS uuid AS $$
BEGIN
    RETURN current_setting('app.current_tenant_id', true)::uuid;
EXCEPTION
    WHEN OTHERS THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Function to clear tenant context (for cleanup)
CREATE OR REPLACE FUNCTION clear_current_tenant()
RETURNS void AS $$
BEGIN
    PERFORM set_config('app.current_tenant_id', '', false);
END;
$$ LANGUAGE plpgsql;


-- ============================================================================
-- 6. Verification queries (for testing)
-- ============================================================================

-- Query to check if RLS is enabled on a table
-- SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public' AND tablename = 'memories';

-- Query to list all RLS policies
-- SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
-- FROM pg_policies
-- WHERE schemaname = 'public'
-- ORDER BY tablename, policyname;

-- Test query (should only return current tenant's data)
-- SELECT set_current_tenant('00000000-0000-0000-0000-000000000001');
-- SELECT COUNT(*) FROM memories;  -- Should only see tenant 1 data
-- SELECT clear_current_tenant();


-- ============================================================================
-- 7. Migration notes and warnings
-- ============================================================================

-- IMPORTANT NOTES:
--
-- 1. Application Code Changes Required:
--    - Update middleware to call set_current_tenant() at start of each request
--    - Ensure tenant_id is set before ANY database query
--    - Handle cases where tenant_id is NULL (should reject request)
--
-- 2. Testing:
--    - Test cross-tenant access attempts (should be blocked)
--    - Test superuser bypass (should work)
--    - Test performance impact (RLS adds slight overhead)
--
-- 3. Rollback:
--    - To rollback, run: ALTER TABLE <table> DISABLE ROW LEVEL SECURITY;
--    - To drop policies: DROP POLICY <policy_name> ON <table>;
--
-- 4. Monitoring:
--    - Monitor for "permission denied" errors (may indicate RLS issues)
--    - Log all set_current_tenant() calls for audit trail
--
-- 5. Performance:
--    - RLS adds a WHERE clause to every query
--    - Ensure tenant_id columns are indexed
--    - Consider query plan analysis for critical queries

COMMENT ON FUNCTION set_current_tenant(uuid) IS
'Sets the current tenant context for RLS. Must be called at the start of each request.';

COMMENT ON FUNCTION get_current_tenant() IS
'Returns the current tenant UUID from session context. Used for debugging and verification.';

COMMENT ON FUNCTION clear_current_tenant() IS
'Clears the tenant context. Should be called at end of request for cleanup.';
