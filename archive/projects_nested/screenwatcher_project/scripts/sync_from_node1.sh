#!/bin/bash
# Syncs code FROM Node 1 (Lumina) back to local machine.
# Usage: ./scripts/sync_from_node1.sh

echo "📥 Syncing code FROM Node 1 (Lumina) back to local..."
rsync -avz --exclude '.env' --exclude '.venv*' --exclude '__pycache__' --exclude '.git' --exclude 'models/' --exclude '*.log' --exclude 'bandit_state.json' operator@100.68.166.117:~/rae-node-agent/ ./
echo "✅ Sync complete."
