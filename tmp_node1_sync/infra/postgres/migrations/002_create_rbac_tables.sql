-- Migration: Create RBAC (Role-Based Access Control) tables
-- Date: 2025-11-27
-- Description: Creates tables for user-tenant-role assignments and access control

-- Create user_tenant_roles table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'user_tenant_roles'
    ) THEN
        CREATE TABLE user_tenant_roles (
            id UUID PRIMARY KEY,
            user_id TEXT NOT NULL,
            tenant_id UUID NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('owner', 'admin', 'developer', 'analyst', 'viewer')),

            -- Scope restrictions (optional)
            project_ids TEXT[], -- Empty array means access to all projects

            -- Metadata
            assigned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            assigned_by TEXT,
            expires_at TIMESTAMPTZ,

            -- Constraints
            CONSTRAINT user_tenant_roles_unique UNIQUE (user_id, tenant_id)
        );

        -- Create indexes for common queries
        CREATE INDEX idx_user_tenant_roles_user_id ON user_tenant_roles(user_id);
        CREATE INDEX idx_user_tenant_roles_tenant_id ON user_tenant_roles(tenant_id);
        CREATE INDEX idx_user_tenant_roles_role ON user_tenant_roles(role);
        CREATE INDEX idx_user_tenant_roles_expires_at ON user_tenant_roles(expires_at) WHERE expires_at IS NOT NULL;

        RAISE NOTICE 'Created table user_tenant_roles';
    ELSE
        RAISE NOTICE 'Table user_tenant_roles already exists, skipping';
    END IF;
END $$;

-- Create access_logs table for audit logging
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'access_logs'
    ) THEN
        CREATE TABLE access_logs (
            id UUID PRIMARY KEY,
            tenant_id UUID NOT NULL,
            user_id TEXT NOT NULL,
            action TEXT NOT NULL,
            resource TEXT NOT NULL,
            resource_id TEXT,

            -- Result
            allowed BOOLEAN NOT NULL,
            denial_reason TEXT,

            -- Context
            ip_address TEXT,
            user_agent TEXT,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

            -- Metadata (JSONB for flexible structure)
            metadata JSONB DEFAULT '{}'::jsonb
        );

        -- Create indexes for audit queries
        CREATE INDEX idx_access_logs_tenant_id ON access_logs(tenant_id);
        CREATE INDEX idx_access_logs_user_id ON access_logs(user_id);
        CREATE INDEX idx_access_logs_timestamp ON access_logs(timestamp DESC);
        CREATE INDEX idx_access_logs_allowed ON access_logs(allowed);
        CREATE INDEX idx_access_logs_action ON access_logs(action);
        CREATE INDEX idx_access_logs_resource ON access_logs(resource);

        RAISE NOTICE 'Created table access_logs';
    ELSE
        RAISE NOTICE 'Table access_logs already exists, skipping';
    END IF;
END $$;

-- Create function to check expired roles
CREATE OR REPLACE FUNCTION check_role_expiration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.expires_at IS NOT NULL AND NEW.expires_at <= NOW() THEN
        RAISE EXCEPTION 'Cannot assign expired role (expires_at: %)', NEW.expires_at;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to validate role expiration on insert/update
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'trigger_check_role_expiration'
    ) THEN
        CREATE TRIGGER trigger_check_role_expiration
        BEFORE INSERT OR UPDATE ON user_tenant_roles
        FOR EACH ROW
        EXECUTE FUNCTION check_role_expiration();

        RAISE NOTICE 'Created trigger trigger_check_role_expiration';
    END IF;
END $$;

-- Insert comment documentation
COMMENT ON TABLE user_tenant_roles IS 'Maps users to tenants with specific roles and optional project-level access restrictions';
COMMENT ON COLUMN user_tenant_roles.role IS 'User role: owner (full access), admin (manage users/settings), developer (API access), analyst (read analytics), viewer (read-only)';
COMMENT ON COLUMN user_tenant_roles.project_ids IS 'Optional project restrictions. Empty array = access to all projects';
COMMENT ON COLUMN user_tenant_roles.expires_at IS 'Optional role expiration timestamp. NULL = never expires';

COMMENT ON TABLE access_logs IS 'Audit log for all access control decisions';
COMMENT ON COLUMN access_logs.allowed IS 'Whether access was granted (true) or denied (false)';
COMMENT ON COLUMN access_logs.metadata IS 'Additional context in JSON format';
