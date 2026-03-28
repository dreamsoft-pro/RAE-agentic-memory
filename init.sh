#!/bin/bash
# RAE System Initialization Script
# Ensures .env exists and basic structure is ready

if [ ! -f .env ]; then
    echo "📄 Creating .env from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env created. Please review secrets in .env"
    else
        echo "⚠️  .env.example not found! Creating a basic .env..."
        cat << 'EOF' > .env
# Docker Settings
COMPOSE_BAKE=false

# RAE Environment Configuration
RAE_PROFILE=standard
RAE_DB_MODE=migrate
POSTGRES_USER=rae
POSTGRES_PASSWORD=rae_password
POSTGRES_DB=rae
QDRANT_HOST=rae-qdrant
REDIS_HOST=rae-redis
OLLAMA_API_URL=http://host.docker.internal:11434
EOF
        echo "✅ Basic .env generated."
    fi
fi

# Ensure work_dir and data volumes exist
mkdir -p work_dir data/postgres data/qdrant data/lite

echo "🚀 Initialization complete."
echo "--------------------------------------------------"
echo "Standard (CPU):             docker compose up -d"
echo "GPU Acceleration (NVIDIA):  docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d"
echo "Lite:                       docker compose -f docker-compose.lite.yml up -d"
echo "Dev:                        docker compose -f docker-compose.dev.yml up -d"
echo "--------------------------------------------------"
echo "🛡️  HARD FRAMES (Isolation Mode) - append overlay:"
echo "Example: docker compose -f docker-compose.yml -f docker-compose.hard-frames.yml up -d"
echo "--------------------------------------------------"
