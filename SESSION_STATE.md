<state_snapshot>
    <overall_goal>
        Complete the migration of `MemoryRepository` to `RAE-Core` adapters (`RAECoreService` and `PostgreSQLStorage`), ensuring zero tech debt and full test coverage.
    </overall_goal>

    <key_knowledge>
        - **Migration Status**: Code migration complete. `MemoryRepository` deleted.
        - **Test Status**: `make test-unit` fails.
        - **Root Causes**:
            1.  **DB Validation**: Tests fail because app startup tries to validate schema against mock DB. Needs `RAE_DB_MODE="ignore"`.
            2.  **Missing Fixture**: `tests/api/v1/test_memory.py` misses `mock_pool`.
            3.  **Refactoring Drift**: `ReflectionEngineV2` tests call non-existent methods (`generate_reflection`).
            4.  **DI Mismatch**: Worker tests still try to inject `memory_repository` instead of `rae_service`.
    </key_knowledge>

    <file_system_state>
        - **Modified**:
            - `tests/api/v1/test_graph.py`: Fixed imports.
            - `tests/api/v1/test_memory.py`: Rewritten for RAECore, but has fixture bugs.
        - **Deleted**:
            - `tests/repositories/test_memory_repository_coverage.py`
        - **To Be Modified (Next Session)**:
            - `apps/memory_api/tests/conftest.py` (Fix DB validation)
            - `apps/memory_api/tests/services/test_reflection_engine_v2.py` (Fix attributes)
            - `apps/memory_api/tests/test_workers.py` (Fix DI)
            - `tests/api/v1/test_memory.py` (Fix fixture)
    </file_system_state>

    <current_plan>
        1. [DONE] Phase 1: Extend RAE-Core Interfaces.
        2. [DONE] Phase 2: Refactor Memory API.
        3. [DONE] Phase 3: Cleanup (Delete MemoryRepository).
        4. [IN_PROGRESS] Verify all tests pass.
           - [TODO] Fix test environment (DB validation).
           - [TODO] Fix updated test files.
    </current_plan>
</state_snapshot>
