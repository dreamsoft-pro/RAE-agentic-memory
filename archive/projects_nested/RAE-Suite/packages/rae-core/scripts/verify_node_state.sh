#!/bin/bash
# Verify the state of RAE containers on a node
# Usage: ./scripts/verify_node_state.sh

echo "🔍 Verifying RAE Node State..."

# Check RAE Dev
if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ RAE Dev API (8001): Online"
else
    echo "❌ RAE Dev API (8001): Offline or Unhealthy"
fi

# Check RAE Lite
if curl -s http://localhost:8008/health > /dev/null; then
    echo "✅ RAE Lite API (8008): Online"
else
    echo "❌ RAE Lite API (8008): Offline or Unhealthy"
fi

# Check Docker Containers
echo -e "\n🐳 Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep "rae"
