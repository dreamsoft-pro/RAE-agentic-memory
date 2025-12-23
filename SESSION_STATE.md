<state_snapshot>
    <overall_goal>
        Complete Phase 3 of the Core Architecture refactor, migrating all components in `apps/memory_api` to use `RAECoreService` (Contract over Implementation).
    </overall_goal>

    <key_knowledge>
        - **Migration Status**: ~95% complete. Core services, workers, and tasks migrated.
        - **Test Stability**: 892 unit tests passing (100% green). Integration tests in progress.
        - **Mocking Strategy**: Standardized `DummyAsyncContextManager` for mocking `rae_service.postgres_pool`.
        - **Data Constraints**: `memories` table uses naive `TIMESTAMP`, requiring naive `datetime` in Python.
        - **Performance**: `test_hybrid_search.py` patched to bypass CUDA dependency in CPU-only test environments.
    </key_knowledge>

    <file_system_state>
        - **Modified**:
            - `apps/memory_api/services/`: Retention, EntityResolution, CommunityDetection, HybridSearch, ContextBuilder, ReflectionEngineV2.
            - `apps/memory_api/workers/`: `memory_maintenance.py` (Decay, Summarization, Dreaming).
            - `apps/memory_api/tasks/`: `background_tasks.py` (Celery integration).
            - `apps/memory_api/dependencies.py`: Added factories for all core services.
            - `apps/memory_api/tests/`: Extensive updates to unit tests.
            - `tests/integration/`: Migration to `rae_service`.
    </file_system_state>

    <current_plan>
        1. [DONE] Refactor Workers (`DecayWorker`, `SummarizationWorker`, `DreamingWorker`) to use `rae_service`.
        2. [DONE] Refactor Background Tasks and Celery `rae_context`.
        3. [DONE] Refactor remaining services: `RetentionService`, `EntityResolutionService`, `CommunityDetectionService`.
        4. [IN_PROGRESS] Fix remaining integration test failures (`test_decay_worker.py`, `test_dreaming_worker.py`).
        5. [TODO] Final audit for direct `pool` injections.
        6. [TODO] Performance verification with `make benchmark-lite`.
    </current_plan>
</state_snapshot>