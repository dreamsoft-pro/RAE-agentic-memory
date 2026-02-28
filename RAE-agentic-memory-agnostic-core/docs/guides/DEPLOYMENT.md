# RAE Deployment & Configuration Guide

This guide covers everything from local setup to high-availability production clusters.

---

## 1. Quick Start (Docker Profiles)

RAE uses Docker Compose Profiles to simplify deployment:

- **Dev Mode**: `docker compose --profile dev up -d` (Port 8001, Hot-reload enabled)
- **Lite Mode**: `docker compose --profile lite up -d` (Port 8010, No Celery/ML)
- **Full Mode**: `docker compose up -d` (Port 8000, Full stack)

---

## 2. Configuration (`.env`)

Key environment variables:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `RAE_EMBEDDING_BACKEND` | `onnx` | `onnx`, `ollama`, or `litellm` |
| `RAE_LLM_MODEL_DEFAULT` | `gpt-4o-mini` | Default model for reasoning |
| `RAE_DB_MODE` | `migrate` | `migrate` (auto-migrations) or `ignore` |
| `POSTGRES_HOST` | `postgres` | Database hostname |

---

## 3. Production Hardening

### Hard Frames (Agent Isolation)
To enable maximum security, run agents in a separate network bridge with NO internet access. Ensure they can only talk to the RAE API.

### Database Backups
Always backup both PostgreSQL (metadata) and Qdrant (vectors).
```bash
# Snapshotting Qdrant
curl -X POST http://localhost:6333/collections/memories/snapshots
```

### Resource Management
For large datasets (100k+), ensure the API container has at least 4GB RAM to handle the ONNX models and Semantic Resonance calculations.
