# RAE Agentic Memory - Missing/Incomplete Functionalities

This document lists functionalities described in `docs/all.md` that are either entirely missing from the codebase or are only partially implemented, requiring further development.

## 1. RAE–Reflective Memory v1 Iteration Fix and Polish Plan

### 1.4. Maintenance Workers (Decay, Summarization, Dreaming) ✅ COMPLETED

*   **✅ Implement `SummarizationWorker.summarize_long_sessions`:** COMPLETED - The implementation in `apps/memory_api/workers/memory_maintenance.py` lines 305-378 now includes full database query logic to find and summarize long sessions with SQL-based aggregation and optional LLM fallback.
*   **✅ Upgrade `SummarizationWorker._create_summary_text` to use an LLM:** COMPLETED - Lines 351-378 now use LLM with SessionSummaryResponse model and structured output, with fallback to string aggregation.
*   **✅ Confirm `ImportanceScoringService.decay_importance` details:** VERIFIED - Implementation in `apps/memory_api/services/importance_scoring.py` lines 366-465 includes importance floor (GREATEST(0.01, ...)), accelerated decay for stale memories (>30 days), and protected decay for recent memories (<7 days).

### 1.5. Actor–Evaluator–Reflector Contract ✅ COMPLETED

*   **✅ Implement LLM-based evaluator:** COMPLETED - The `LLMEvaluator` class in `apps/memory_api/services/evaluator.py` lines 273-352 is fully implemented with LLM integration using LLMEvaluationResponse model and fallback to DeterministicEvaluator on error.
*   **✅ Clarify `EvaluationResult` model consolidation:** INVESTIGATED - The two `EvaluationResult` models serve different purposes and should remain separate:
    *   `reflection_v2_models.py` line 231: Dataclass for reflection evaluation (internal use)
    *   `evaluation_models.py` line 126: Pydantic model for search quality evaluation (API responses)

### 1.6. Tests, Metrics, DX ✅ COMPLETED

*   **✅ Implement integration tests for Decay Worker:** COMPLETED - Created `tests/integration/test_decay_worker.py` with 9 comprehensive tests covering basic decay, access stats, multi-tenant, importance floor, error handling, and metadata preservation (372 lines).
*   **✅ Implement integration tests for Dreaming Worker:** COMPLETED - Created `tests/integration/test_dreaming_worker.py` with 9 comprehensive tests covering basic cycle, config flags, lookback windows, importance filtering, max samples, and error handling (383 lines).
*   **Note:** Summarization Worker integration tests were not created as the worker is already well-tested through unit tests and the implementation was verified to be complete.

## 2. RAE Agentic Memory API Reference

### 2.1. Event Triggers (`/v1/triggers/*`) ✅ COMPLETED

*   **✅ Implement database storage and retrieval for trigger rules:** COMPLETED - Created `infra/postgres/migrations/003_create_triggers_workflows_tables.sql` with trigger_rules table and `apps/memory_api/repositories/trigger_repository.py` (486 lines) with full CRUD operations. All 10 endpoints in `apps/memory_api/routes/event_triggers.py` now use database storage.
*   **✅ Implement database storage and retrieval for workflows:** COMPLETED - Migration 003 includes workflows table, and WorkflowRepository in `trigger_repository.py` provides full CRUD operations. All workflow endpoints now use database storage.

### 2.4. Evaluation (`/v1/evaluation/*`) ✅ COMPLETED

*   **✅ Implement database storage and retrieval for A/B tests:** COMPLETED - Created `infra/postgres/migrations/005_create_evaluation_tables.sql` with ab_tests and ab_test_results tables, and `apps/memory_api/repositories/evaluation_repository.py` with ABTestRepository class (full CRUD + statistics). Updated `create_ab_test` and `compare_ab_test_variants` endpoints in `apps/memory_api/routes/evaluation.py` to use database storage.
*   **✅ Implement database storage and retrieval for benchmark suites and their execution results:** COMPLETED - Migration 005 includes benchmark_suites and benchmark_executions tables. BenchmarkRepository in `evaluation_repository.py` provides full CRUD operations. Updated `run_benchmark_suite` and `list_benchmark_suites` endpoints to use database storage.

### 2.5. Dashboard (`/v1/dashboard/*`) ✅ COMPLETED

*   **✅ Implement time series data retrieval for `/v1/dashboard/metrics/timeseries/{metric_name}`:** COMPLETED - Created `infra/postgres/migrations/004_create_metrics_timeseries_table.sql` with metrics_timeseries table and helper functions, and `apps/memory_api/repositories/metrics_repository.py` (346 lines) for time series operations. Updated `/v1/dashboard/metrics/timeseries/{metric_name}` endpoint in `apps/memory_api/routes/dashboard.py` to retrieve real data with automatic aggregation intervals.

## 6. Go SDK (rae_memory_sdk)
*   **Implement the Go SDK:** The `docs/sdk_go_design.md` describes a Go SDK, but the actual implementation is missing from the `sdk/go` directory.

## 7. Node.js SDK (rae-memory-sdk)
*   **Implement the Node.js SDK:** The `docs/sdk_nodejs_design.md` describes a Node.js SDK, but the actual implementation is missing from the `sdk/nodejs` directory.

## 9. RAE Memory Replay Tool - Design Document
*   **Implement the RAE Memory Replay Tool:** This functionality is entirely missing. This includes:
    *   Creating the `agent_sessions` database table.
    *   Integrating session recording into the `apps/memory_api/routers/agent.py` `execute` endpoint.
    *   Implementing core replay functionalities (record, list, replay, visualize, inspect, filter, search).
    *   Developing CLI/Web UI for the tool.
