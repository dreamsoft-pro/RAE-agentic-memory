#!/bin/bash
# RESTORE INFRASTRUCTURE SCRIPT
# Generated automatically to save RAM while preserving configuration state.

echo "🔄 Restoring RAE Infrastructure..."

# 1. RAE Standard (Dev/Hotreload)
# Ports: 
# - API: 8001 (mapped to internal 8000)
# - Dashboard: 8501
# - Qdrant: 6333
# - Postgres: 5432
# - Redis: 6379
# - ML Service: 8002
# - Reranker: 8004
echo "   🚀 Starting RAE Standard (Hotreload)..."
docker compose up -d rae-api-dev rae-postgres rae-redis rae-qdrant rae-dashboard rae-celery-worker rae-celery-beat

# 2. RAE Lite (Sandbox/Test)
# Ports:
# - API: 8008
# - Postgres: 5433
# - Redis: 6380
# - Qdrant: 6335, 6336
echo "   🚀 Starting RAE Lite (Sandbox)..."
docker compose -f docker-compose.test-sandbox.yml up -d

# 3. ScreenWatcher Project
# Ports:
# - Web: 9000
# - MCP: 9001
# - Grafana: 3000
# - MariaDB: 3306
echo "   🚀 Starting ScreenWatcher..."
# Assuming ScreenWatcher is in a sibling directory or managed via main compose
# Based on container names, it seems to be in a separate project context, 
# but for safety we list the containers if they are in the current context.
# If they fail to start here, go to ../screenwatcher_project and run docker compose up -d
docker start screenwatcher_project-web-1 screenwatcher-grafana screenwatcher_project-db-1 screenwatcher_project-redis-1 screenwatcher_project-celery-1 screenwatcher_project-mcp-1 || echo "⚠️  Could not start ScreenWatcher containers directly. Navigate to project folder."

echo "✅ Infrastructure restored."
echo "   - RAE Standard: http://localhost:8001"
echo "   - RAE Dashboard: http://localhost:8501"
echo "   - RAE Lite: http://localhost:8008"
echo "   - ScreenWatcher: http://localhost:9000"
