# Next Session Plan

The immediate next task is to address the architectural refactoring of `rae_core` to ensure its agnosticism to infrastructure.

**Details for this refactoring are documented in TENANT_ID_REFACTOR_PLAN.md (section "Architectural Refactoring: Addressing `rae_core` Agnosticism").**

This involves:
1. Moving concrete adapter implementations from `rae-core/rae_core/adapters` to `apps/memory_api/adapters`.
2. Updating imports across the project.
3. Validating `RAEEngine` integration with interfaces.
4. Adjusting `apps/memory_api/services/rae_core_service.py` for correct adapter construction and injection.
