# 🚀 RAE Agentic Memory: Developer Quickstart

This guide explains how to set up the RAE Memory ecosystem for the first time.

## 🛠️ Initial Setup

1.  **Clone the repository**
2.  **Initialize Environment**:
    ```bash
    cp .env.example .env
    # Edit .env and add your API keys (OpenAI, Anthropic, etc.)
    ```
3.  **Build Images**:
    ```bash
    docker compose build
    ```

## 🎭 Running Different Profiles

RAE uses Docker Compose profiles to scale functionality based on your needs:

### 1. Lite Mode (Recommended for first-time users)
Minimalistic stack using local math-based logic and Ollama if available.
```bash
docker compose --profile lite up -d
```
*Port: 8001 (API), 8500 (Portal)*

### 2. Standard Stack
Full production-like environment with PostgreSQL, Redis, and Qdrant.
```bash
docker compose --profile standard up -d
```

### 3. Development / Hotreload
Starts the system with source code mounted from your host. Changes to `.py` files trigger automatic service restarts.
```bash
docker compose --profile dev up -d
```

## 🔍 Verification

Check if the API is alive:
```bash
curl http://localhost:8001/health
```

Access the Knowledge Graph UI:
`http://localhost:8500`

## 🛡️ Security Note
The **Hard Frames** architecture is enabled by default in `secure` profiles. For local development, use the `dev` or `standard` profiles to maintain full access to system tools.

---
*Silicon Oracle v3.2 - Developer Context Injected*
