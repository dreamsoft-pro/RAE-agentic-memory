# RAE Project Refinement Plan (claude-todo.md)

**Context:** The project has achieved high unit test coverage (Green Tests) for core modules (`pgvector`, `pii_scrubber`, `graph_extraction`). We are now transitioning from "Code Complete" to "Production Ready".
**Primary Goal:** Address architectural gaps, verify End-to-End (E2E) stability, optimize costs, and improve Developer Experience (DX).

---

## Phase 1: Critical Stability & E2E Verification 🚨
*Focus: Moving beyond mocked unit tests to verify the system actually works with real database containers.*

- [ ] **Create E2E Smoke Test Script** (`scripts/smoke_test.py`)
    - **Goal:** A standalone Python script (using `requests`, not `pytest`) that verifies the full pipeline against a running Docker stack.
    - **Steps:**
        1. Wait for API health check (200 OK).
        2. Send `POST /memory/store` with complex data (e.g., "Adam works at Google as a Senior Engineer").
        3. Sleep/Wait for async processing (Celery worker).
        4. Send `POST /memory/search` query ("Where does Adam work?").
        5. Verify response contains "Google" (proving Vector + SQL sync worked).
    - **Constraint:** Must run against `localhost:8000` (real HTTP stack).

- [ ] **Implement Transaction Consistency Check**
    - **Context:** `hybrid_search.py` queries both Postgres (Graph) and Qdrant (Vector).
    - **Task:** Ensure `GraphExtractionService` and `EmbeddingService` handle failures gracefully. If Qdrant fails, the Postgres transaction should ideally be marked or retried (implement basic "Outbox Pattern" or robust Retry logic in Celery).

---

## Phase 2: Cost Optimization & Performance 💰
*Focus: Preventing "Token Bankruptcy" and 429 Rate Limit errors during heavy imports.*

- [ ] **Implement Rate Limiting for Extraction**
    - **File:** `apps/memory_api/tasks/background_tasks.py`
    - **Task:** Add a semaphore or delay mechanism to the graph extraction worker.
    - **Logic:** Ensure we don't fire 500 parallel requests to the LLM provider when importing 500 log lines.
    - **Implementation:** Use `tenacity.retry` with exponential backoff specifically handling `429 Too Many Requests`.

- [ ] **Optimize Dependency Weight**
    - **Task:** Split `requirements.txt` into:
        - `requirements-core.txt` (FastAPI, Pydantic, PG driver - light).
        - `requirements-worker.txt` (Torch, Sentence-transformers, Spacy - heavy).
    - **Goal:** The API container should start in <5s. The Worker container handles the heavy ML lifting.

---

## Phase 3: Security & Privacy Strategy 🛡️
*Focus: Correct implementation of PII Scrubbing.*

- [ ] **Verify "Scrub-Before-Embed"**
    - **Context:** We have 100% coverage on the scrubber, but we need to ensure it's called at the right moment.
    - **Task:** Audit `EmbeddingService`. Ensure text is passed through `PIIScrubber` *before* being sent to the embedding model.
    - **Why:** If raw data is embedded, PII can be mathematically reconstructed from the vector.

- [ ] **Secure MCP Logs**
    - **File:** `integrations/mcp-server/src/rae_mcp_server/server.py`
    - **Task:** Review logging middleware. Ensure `save_memory` arguments (content) are not logged in plain text if they contain PII. Apply scrubber to logs or truncate content.

---

## Phase 4: Developer Experience (DX) & Open Source Prep 🚀
*Focus: Making the project usable for others immediately after cloning.*

- [ ] **Create "One-Click" Dev Environment**
    - **Task:** Refine `docker-compose.dev.yml`.
    - **Requirement:** It must spin up: Postgres (with pgvector), Redis, Qdrant, and the API.
    - **Add:** A `healthcheck` service or script that waits for all DBs to be ready.

- [ ] **Create Seed Data Script** (`scripts/seed_demo_data.py`)
    - **Task:** A script that populates the memory with a demo scenario (e.g., RAE's own documentation or a fake project "Project Omega").
    - **Goal:** Ensure the Dashboard (`Knowledge Graph`) is not empty for a new user.

- [ ] **License Consistency Check**
    - **Task:** Verify `Apache-2.0` is reflected in:
        - `LICENSE` file.
        - `pyproject.toml` (all packages).
        - `README.md`.
    - **Note:** Ensure private modules (like the "CLI Farm") are strictly excluded via `.gitignore`.

---

## Phase 5: Code Quality & Architecture 🏗️

- [ ] **Refine LLM Provider Abstraction**
    - **Context:** `graph_extraction.py` currently has hardcoded checks like `if provider == "openai"`.
    - **Task:** Refactor to fully use the `LLMProvider` interface. The service should call `llm.generate_structured(..., schema=Triple)` regardless of the backend.

- [ ] **Entity Normalization (Graph Quality)**
    - **Task:** In `GraphExtractionService`, before saving nodes:
        - Convert to lowercase (optional, configurable).
        - Trim whitespace.
    - **Goal:** Avoid duplicate nodes like "AuthService" and "auth-service".