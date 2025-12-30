# Session State Log

## Session: 2025-12-30 - RAE Slimming & Optimization

### Achievements
1.  **Architecture Optimization (Slimming):**
    *   Removed `ml-service` container entirely.
    *   Removed heavy ML dependencies (`sentence-transformers`, `torch`) from the main Docker image.
    *   Implemented "One Image Strategy": `rae-api`, `celery-worker`, and `celery-beat` now share a single, lighter `rae-memory:latest` image.
    *   Cleaned up `docker-compose.yml` (removed volumes for prod, dynamic container names).

2.  **Code Logic:**
    *   Refactored `EmbeddingService` to support **automatic fallback** to `LiteLLM` (API-based embeddings) when local libraries are missing. This enables RAE-Lite and GPU-less operation.
    *   Updated `requirements.txt` to exclude ML packages by default.

3.  **Quality Assurance (Zero Warning/Error Policy):**
    *   Fixed **11 failing unit tests** caused by the switch to async embedding generation (incorrect `MagicMock` usage in `test_hybrid_search.py`, `test_memory.py`, `test_agent.py`).
    *   Eliminated **torch/cuda warnings** in tests by mocking `SentenceTransformer` initialization in `test_distributed_integration.py`.
    *   Resolved **skipped tests** in `test_architecture.py` by allowlisting stateless services for Dependency Injection checks.
    *   **Lint Fixes:** Fixed import sorting, unused imports in `embedding.py` and unused variables in `test_distributed_integration.py` to ensure CI/CD compliance.
    *   **Result:** 100% Pass Rate (909 passed, 0 failed, 0 skipped, 0 warnings).

### Removed Services Explanation
*   **ml-service:** Previously handled local heavy ML tasks (embeddings, entity resolution via Spacy/Transformers).
    *   *Why removed:* It created a huge dependency footprint (GBs) and required complex GPU passthrough in Docker.
    *   *Replacement:* All ML tasks are now offloaded to External APIs (Ollama for local, OpenAI/Anthropic for cloud) via `LiteLLM`. This decouples logic from hardware.
*   **Reranker:** Was part of the ML stack.
    *   *Impact:* Removing local cross-encoders reduces reranking precision slightly for subtle semantic nuances.
    *   *Mitigation:* `SmartReranker` now falls back to a heuristic approach (keyword boosting). For higher precision, we should use an API-based reranker (e.g., Cohere) or Listwise Reranking via LLM in the future.

### Next Steps
*   Verify `RAE-Lite` deployment on Windows Server.
*   Check automated documentation generation (`scripts/docs_automator.py`).