#!/bin/bash
# scripts/start_rae.sh
# Universal Startup Script for RAE
# Automatically detects GPU availability and configures Docker Compose.

echo "🚀 RAE Universal Launcher"
echo "========================="

# 1. Detect GPU on Host
HAS_GPU=false
if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi &> /dev/null; then
        echo "✅ NVIDIA GPU Detected on Host."
        HAS_GPU=true
    else
        echo "⚠️  nvidia-smi found but failed. Assuming no GPU."
    fi
else
    echo "ℹ️  No NVIDIA GPU detected (nvidia-smi missing)."
fi

# 2. Detect Docker Runtime
HAS_NVIDIA_DOCKER=false
if docker info 2>/dev/null | grep -i "runtimes" | grep -q "nvidia"; then
    echo "✅ Docker NVIDIA Runtime Detected."
    HAS_NVIDIA_DOCKER=true
else
    echo "ℹ️  Docker NVIDIA Runtime NOT detected. (Check 'docker info')"
fi

# 3. Set Default Profile
if [ -z "$COMPOSE_PROFILES" ]; then
    echo "ℹ️  COMPOSE_PROFILES not set. Defaulting to 'dev'."
    export COMPOSE_PROFILES=dev
else
    echo "ℹ️  COMPOSE_PROFILES set to '$COMPOSE_PROFILES'."
fi

# 4. Construct Command
COMPOSE_FILES="-f docker-compose.yml"

if [ "$HAS_GPU" = true ] && [ "$HAS_NVIDIA_DOCKER" = true ]; then
    echo "⚙️  Mode: GPU ACCELERATED (Cuda)"
    COMPOSE_FILES="$COMPOSE_FILES -f docker-compose.gpu.yml"
else
    echo "⚙️  Mode: CPU ONLY (Standard)"
    if [ "$HAS_GPU" = true ]; then
        echo "   (GPU exists but Docker runtime is missing. Install nvidia-container-toolkit to enable acceleration.)"
    fi
fi

# Check for override
if [ -f "docker-compose.override.yml" ]; then
    echo "   + Loading docker-compose.override.yml"
    COMPOSE_FILES="$COMPOSE_FILES -f docker-compose.override.yml"
fi

echo "---------------------------------------------------------------"
CMD="docker compose $COMPOSE_FILES $@"
echo "Running: $CMD"
eval $CMD
