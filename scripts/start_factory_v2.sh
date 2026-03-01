#!/bin/bash
set -e

echo "🚀 STARTING RAE-FENIKS POWERED FACTORY V2.2 (Oracle V2.0 Protocol)..."

# 📍 Path Definitions
FENIKS_ROOT="/mnt/extra_storage/factory/RAE-Feniks"
PROJECT_ROOT="/mnt/extra_storage/RAE-agentic-memory-agnostic-core"
CONFIG_PATH="$PROJECT_ROOT/config/agentic_board.yaml"
STRATEGY_PATH="$PROJECT_ROOT/docs/modernization/STRATEGIC_ORACLE_PLAN_V2.md"

# 1. Verify Configuration and Strategy
if [ ! -f "$CONFIG_PATH" ]; then
    echo "❌ ERROR: agentic_board.yaml not found!"
    exit 1
fi
echo "✅ Configuration found: $CONFIG_PATH"

if [ ! -f "$STRATEGY_PATH" ]; then
    echo "⚠️  Warning: Strategic Plan V2.0 not found locally. Searching in RAE..."
fi

# 2. Start RAE Kernel (Hard Frames Mode)
echo "🛡️  Booting RAE Kernel & Telemetry (Jaeger)..."
cd $PROJECT_ROOT
docker compose -f docker-compose.telemetry.yml up -d
docker compose -f docker-compose.yml up -d rae-api-dev postgres redis qdrant

# 3. Wait for Kernel Health
echo "⏳ Waiting for RAE API..."
until curl -s http://localhost:8001/health > /dev/null; do
    sleep 2
    echo -n "."
done
echo "✅ RAE Kernel ONLINE."

# Enable OTel in container
docker exec rae-api-dev bash -c 'export OTEL_TRACES_ENABLED=true'

# 4. Initalize RAE-Feniks (Build System Model)
echo "🧠 Feniks: Synchronizing with RAE and building System Model..."
export PYTHONPATH=$FENIKS_ROOT
# Running Feniks analysis using the created venv
$FENIKS_ROOT/venv/bin/python3 -m feniks.apps.cli.main analyze --project-id dreamsoft-pro --collection code_chunks --rae-enabled true

# 5. Deploy Modernized Agent Scripts to Hard Frame
echo "📦 Deploying AI-Powered Agents (Verifying Version 4.2)..."
docker exec rae-api-dev mkdir -p /app/config

# CRITICAL: Always use scripts from physical disk (Source of Truth)
# If local files in /mnt are missing, the factory STOPS instead of using old /tmp fallbacks.
for script in "hive_engine_v55.py" "hive_auditor_v1.py" "supervisor_mcp.py"; do
    if [ -f "$PROJECT_ROOT/agent_hive/$script" ]; then
        echo "   -> Copying $script from Source of Truth..."
        docker cp "$PROJECT_ROOT/agent_hive/$script" rae-api-dev:/app/$script
    else
        echo "❌ FATAL ERROR: $script missing from $PROJECT_ROOT/agent_hive/!"
        echo "   Preventing agentic overwrite. Factory startup ABORTED."
        exit 1
    fi
done
docker cp "$CONFIG_PATH" rae-api-dev:/app/config/agentic_board.yaml

# 6. Launch Autonomic Daemons
echo "🤖 Launching Hive Daemons (14B/16B Stack)..."
docker exec -d rae-api-dev python3 -u /app/hive_engine_v55.py
docker exec -d rae-api-dev bash -c 'python3 -u /app/hive_auditor_v1.py > /app/auditor.log 2>&1'
docker exec -d rae-api-dev bash -c 'python3 -u /app/supervisor_mcp.py > /app/supervisor.log 2>&1'

echo "🎉 FACTORY V2.2 (ORACLE) IS ACTIVE."
echo "   - Orchestrator: RAE-Feniks (AST Awareness)"
echo "   - Governance: 3-Tier Hybrid Council"
echo "   - Security: Hard Frames Isolation"
echo "   - Log: docker exec -it rae-api-dev tail -f /app/supervisor.log"
