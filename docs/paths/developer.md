# RAE for Developers: Advanced Integration & Core Development

This guide is designed for Senior Developers working on or integrating with the RAE (Reflective Agentic Engine) ecosystem. It covers architecture, internal standards, and advanced operational workflows.

---

## 🏗️ System Architecture

RAE follows a strict **3-Layer Modular Architecture** to ensure maintainability, testability, and portability.

### 1. Route Layer (FastAPI)
- **Location:** `apps/memory_api/api/v2/`
- **Role:** Handles HTTP requests, Pydantic validation, and response serialization. No business logic should reside here.
- **Contract:** All endpoints must enforce multi-tenancy via `X-Tenant-Id`.

### 2. Service Layer (The Engine)
- **Location:** `apps/memory_api/services/`
- **Role:** Orchestrates complex workflows (Scoring, Reflection, Ingestion). This is the "brain" of the module.
- **Pattern:** Uses dependency injection to interact with repositories.

### 3. Repository/Adapter Layer
- **Location:** `rae_adapters/`
- **Role:** Low-level interaction with PostgreSQL, Qdrant, Redis, and LLM Providers.
- **Contract:** Must implement abstract interfaces defined in `rae-core`.

---

## 🛡️ Senior Developer Mandates

To maintain the integrity of the Silicon Oracle, all code must adhere to these mandates:

### 1. Zero Hardcoding Policy
Hardcoded absolute paths (e.g., `/home/...`, `/app/...`) are strictly forbidden. Use the `RAEPathManager` contract:
```python
from rae_core.utils.paths import RAEPathManager

# Correct way to resolve a project asset
config_path = RAEPathManager.resolve_path("config/settings.yaml")
```

### 2. Failure-First Testing
We use a **"Fail Fast"** strategy. If a critical component (Database, Vector Store) is unavailable, the system must terminate immediately with a clear `ContractViolationError` rather than continuing in a degraded state.

### 3. Asynchronous by Default
All I/O bound operations (API calls, DB queries) **MUST** be `async/await`. Blocking calls are prohibited in the Route and Service layers to prevent event loop exhaustion.

---

## 🛡️ Security & Compliance (ISO 42001)

RAE is designed for high-compliance environments.

### Hard Frames (Isolation)
When running in `Hard Frames` mode, the agent is physically isolated:
- **Network:** Outbound internet is blocked at the network level.
- **Filesystem:** Root FS is read-only; writes are allowed ONLY to `/workspace`.
- **Audit:** Every request is logged with full decision provenance.

### PII Scrubber
All ingested data automatically passes through the **PII Scrubber** middleware, which anonymizes sensitive information (Emails, SSNs, Keys) before they reach the vector store.

---

## 🛠️ Advanced Development Workflows

### Hot-Reload & Debugging
Use the **Dev Profile** for active development:
```bash
docker compose -f docker-compose.dev.yml up -d
```
- **Hot-Reload:** Code changes in `rae-core/` or `apps/` are reflected instantly.
- **Logs:** `docker logs -f rae-api-dev`
- **Interactive Debugging:** Use `breakpoint()` – the dev container supports remote debugging attachments.

### Extending RAE (New Adapters)
To add a new storage backend:
1. Define the interface in `rae-core/rae_core/interfaces/storage.py`.
2. Implement the adapter in `rae_adapters/my_new_db.py`.
3. Register the provider in `rae_adapters/infra_factory.py`.

---

## 📊 Performance & Benchmarking

Developers are responsible for maintaining the **Silicon Oracle** performance baseline (MRR 1.0 at 10k scale).
- **Run Benchmarks:** `python3 scripts/run_benchmark.py --set industrial_large`
- **Verify Fluidity:** `python3 scripts/test_rae_fluidity.py`

---

## 🔗 Internal Resources
- 📜 **[API Documentation](../API_DOCUMENTATION.md)** – Detailed endpoint specs.
- 🧪 **[Testing Policy](../testing/README.md)** – Standards for unit and integration tests.
- 🛤️ **[Modernization Roadmap](../modernization/OPERACJA_LUSTRO_ROADMAP.md)** – Current project focus.

*RAE is an advanced cognitive OS. Code with precision. Fail fast. Maintain alignment.*
