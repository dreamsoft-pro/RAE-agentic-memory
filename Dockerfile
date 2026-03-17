# STAGE 1: Builder
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    software-properties-common curl git gcc g++ \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.14 python3.14-dev python3.14-venv \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.14
RUN ln -sf /usr/bin/python3.14 /usr/bin/python3

WORKDIR /app

# Install dependencies in a virtualenv
RUN python3.14 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY sdk/python/rae_memory_sdk /app/sdk/python/rae_memory_sdk
RUN pip install --no-cache-dir /app/sdk/python/rae_memory_sdk

COPY rae-core /app/rae-core
RUN pip install --no-cache-dir /app/rae-core

COPY rae_adapters /app/rae_adapters
RUN pip install --no-cache-dir /app/rae_adapters

COPY apps/memory_api/requirements-base.txt /app/requirements-base.txt
COPY apps/memory_api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# STAGE 2: Final Runtime
FROM nvidia/cuda:12.4.1-base-ubuntu22.04 AS runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Only essential system libraries
RUN apt-get update && apt-get install -y \
    software-properties-common curl \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y python3.14 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtualenv from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
COPY apps /app/apps
COPY models /app/models

# Non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["/bin/bash", "-c", "alembic upgrade head && uvicorn apps.memory_api.main:app --host 0.0.0.0 --port 8000"]
