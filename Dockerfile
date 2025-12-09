# Multi-stage build for RAE Memory API
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy SDK first
COPY sdk/python/rae_memory_sdk /app/sdk/python/rae_memory_sdk

# Install SDK
RUN pip install --no-cache-dir -e /app/sdk/python/rae_memory_sdk

# Copy rae_core
COPY rae_core /app/rae_core

# Install rae_core
RUN pip install --no-cache-dir -e /app/rae_core

# Copy requirements files
COPY apps/memory_api/requirements-base.txt /app/requirements-base.txt
COPY apps/memory_api/requirements-ml.txt /app/requirements-ml.txt
COPY apps/memory_api/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements-base.txt && \
    pip install --no-cache-dir -r /app/requirements-ml.txt && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
COPY apps /app/apps

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "apps.memory_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
