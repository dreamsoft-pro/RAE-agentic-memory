# Multi-stage build for RAE Memory API with GPU Support
# Using 12.4.1-devel to ensure all libraries (cublas, cudnn) are present and keys are valid
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 AS base

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    git \
    gcc \
    g++ \
    postgresql-client \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    && rm -rf /var/lib/apt/lists/*

# Install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# Set python3 default
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.10 /usr/bin/python

# Set working directory
WORKDIR /app

# Copy SDK and install
COPY sdk/python/rae_memory_sdk /app/sdk/python/rae_memory_sdk
RUN pip install --no-cache-dir -e /app/sdk/python/rae_memory_sdk

# Copy RAE Core and install
COPY rae-core /app/rae-core
RUN pip install --no-cache-dir -e /app/rae-core

# Copy RAE Adapters and install
COPY rae_adapters /app/rae_adapters
RUN pip install --no-cache-dir -e /app/rae_adapters

# Copy requirements
COPY apps/memory_api/requirements-base.txt /app/requirements-base.txt
COPY apps/memory_api/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
COPY apps /app/apps
COPY models /app/models

# Create non-root user (with access to /app and video devices)
RUN useradd -m -u 1000 appuser && \
    usermod -aG video appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["/bin/bash", "-c", "alembic upgrade head && uvicorn apps.memory_api.main:app --host 0.0.0.0 --port 8000"]