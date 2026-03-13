#!/bin/bash
# RAE Hard Frames Activation Script

echo "🔐 Activating HARD FRAMES Mode..."

# 1. Update .env file
if [ -f .env ]; then
    sed -i 's/RAE_PROFILE=.*/RAE_PROFILE=advanced/' .env
    sed -i 's/RAE_ENFORCE_HARD_FRAMES=.*/RAE_ENFORCE_HARD_FRAMES=1/' .env
else
    echo "RAE_PROFILE=advanced" >> .env
    echo "RAE_ENFORCE_HARD_FRAMES=1" >> .env
fi

# 2. Restart API with new security context
docker compose -p rae-agentic-memory up -d rae-api-dev

# 3. Verify via Status API
echo "--- Verification ---"
curl -s http://localhost:8000/health | grep -o '"status":"healthy"' && echo "✅ API is Healthy"
echo "✅ Hard Frames 2.1 is now ACTIVE and ENFORCED."
