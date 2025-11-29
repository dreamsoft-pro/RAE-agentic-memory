# RAE Agentic Memory - Missing/Incomplete Functionalities

This document lists functionalities described in `docs/all.md` that are either entirely missing from the codebase or are only partially implemented, requiring further development.

## 1. RAE–Reflective Memory v1 Iteration Fix and Polish Plan

### 1.4. Maintenance Workers (Decay, Summarization, Dreaming)
*   **Implement `SummarizationWorker.summarize_long_sessions`:** The current implementation in `apps/memory_api/workers/memory_maintenance.py` has a `TODO` comment indicating it needs to be fully implemented beyond just returning an empty list.
*   **Upgrade `SummarizationWorker._create_summary_text` to use an LLM:** Currently, this function performs simple text aggregation, but `memory_maintenance.py` notes that it should use an LLM in production.
*   **Confirm `ImportanceScoringService.decay_importance` details:** Further investigation is needed to ensure decay mechanisms explicitly prevent negative importance scores and prioritize fresh memories as per documentation.
### 1.5. Actor–Evaluator–Reflector Contract
*   **Implement LLM-based evaluator:** The `apps/memory_api/services/evaluator.py` module defines an `LLM` evaluator type but explicitly raises `NotImplementedError`.
*   **Clarify `EvaluationResult` model consolidation:** Investigate if the `EvaluationResult` models in `apps/memory_api/models/reflection_v2_models.py` and `apps/memory_api/models/evaluation_models.py` should be consolidated or if their distinction is intentional.
### 1.6. Tests, Metrics, DX
*   **Implement integration tests for Decay Worker:** As per `TESTING_STATUS.md`, these tests are planned but not yet implemented.
*   **Implement integration tests for Summarization Worker:** As per `TESTING_STATUS.md`, these tests are planned but not yet implemented.
*   **Implement integration tests for Dreaming Worker:** As per `TESTING_STATUS.md`, these tests are planned but not yet implemented.

## 2. RAE Agentic Memory API Reference

### 2.1. Event Triggers (`/v1/triggers/*`)
*   **Implement database storage and retrieval for trigger rules:** The API endpoints (`create_trigger`, `get_trigger`, `update_trigger`, `delete_trigger`, `list_triggers`) in `apps/memory_api/routes/event_triggers.py` are largely placeholders with "database storage not yet implemented" comments.
*   **Implement database storage and retrieval for workflows:** Similarly, workflow endpoints (`create_workflow`, `get_workflow`, `list_workflows`) in `apps/memory_api/routes/event_triggers.py` lack full database integration.
### 2.4. Evaluation (`/v1/evaluation/*`)
*   **Implement database storage and retrieval for A/B tests:** The A/B test endpoints (`create_ab_test`, `compare_ab_test_variants`) in `apps/memory_api/routes/evaluation.py` require database integration for persisting test definitions and results.
*   **Implement database storage and retrieval for benchmark suites and their execution results:** The benchmarking endpoints (`run_benchmark_suite`) in `apps/memory_api/routes/evaluation.py` require full database integration for managing benchmark suites and their results.
### 2.5. Dashboard (`/v1/dashboard/*`)
*   **Implement time series data retrieval for `/v1/dashboard/metrics/timeseries/{metric_name}`:** This endpoint in `apps/memory_api/routes/dashboard.py` currently uses a placeholder and returns an empty list, indicating a need for a backend metrics table and data retrieval logic.

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
