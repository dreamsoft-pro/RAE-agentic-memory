#!/bin/bash
# Syncs code to Node 1 (Lumina) without overwriting secrets, config, or heavy assets.
# Usage: ./scripts/sync_to_node1.sh

echo "🚀 Syncing code to Node 1 (Lumina)..."
rsync -avz --exclude '.env' --exclude '.venv*' --exclude '__pycache__' --exclude '.git' --exclude 'models/' --exclude '*.log' --exclude 'bandit_state.json' --exclude 'docker-compose.override.yml' ./ operator@100.68.166.117:~/rae-node-agent/
echo "✅ Sync complete."
