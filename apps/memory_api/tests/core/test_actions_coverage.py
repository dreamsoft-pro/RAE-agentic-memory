"""
Additional coverage tests for actions.py to hit edge cases and invalid states.
"""

import pytest

from apps.memory_api.core.actions import (
    CallLLMAction,
    ConsolidateEpisodicToWorkingAction,
    GenerateReflectionAction,
    RetrieveLTMAction,
    RetrieveReflectiveAction,
    RetrieveSemanticAction,
    RetrieveWorkingAction,
    SummarizeContextAction,
    UpdateGraphAction,
)
from apps.memory_api.core.state import RAEState


@pytest.fixture
def exhausted_budget_state():
    state = RAEState(tenant_id="test", project_id="test")
    state.budget_state.remaining_tokens = 0  # Exhausted
    return state


@pytest.fixture
def empty_memory_state():
    state = RAEState(tenant_id="test", project_id="test")
    # Ensure all counts are 0 (default)
    return state


@pytest.mark.unit
def test_retrieve_working_invalid_states(exhausted_budget_state, empty_memory_state):
    action = RetrieveWorkingAction(parameters={})

    # Budget exhausted
    assert not action.is_valid_for_state(exhausted_budget_state)

    # Empty working memory
    assert not action.is_valid_for_state(empty_memory_state)


@pytest.mark.unit
def test_retrieve_semantic_invalid_states(exhausted_budget_state, empty_memory_state):
    action = RetrieveSemanticAction(parameters={})

    # Budget exhausted
    assert not action.is_valid_for_state(exhausted_budget_state)

    # Empty semantic memory
    assert not action.is_valid_for_state(empty_memory_state)

    # Use graph but no graph nodes
    action_graph = RetrieveSemanticAction(parameters={"use_graph": True})
    state_no_graph = RAEState(tenant_id="test", project_id="test")
    state_no_graph.memory_state.semantic.count = 10  # Valid memory
    state_no_graph.graph_state.node_count = 0  # Invalid graph

    assert not action_graph.is_valid_for_state(state_no_graph)


@pytest.mark.unit
def test_retrieve_ltm_invalid_states(exhausted_budget_state, empty_memory_state):
    action = RetrieveLTMAction(parameters={})

    # Budget exhausted
    assert not action.is_valid_for_state(exhausted_budget_state)

    # Empty LTM
    assert not action.is_valid_for_state(empty_memory_state)


@pytest.mark.unit
def test_retrieve_reflective_invalid_states(exhausted_budget_state, empty_memory_state):
    action = RetrieveReflectiveAction(parameters={})

    # Budget exhausted
    assert not action.is_valid_for_state(exhausted_budget_state)

    # Empty reflective
    assert not action.is_valid_for_state(empty_memory_state)


@pytest.mark.unit
def test_call_llm_invalid_states(exhausted_budget_state):
    action = CallLLMAction(parameters={"model": "gpt-4o", "max_tokens": 100})

    # Budget exhausted (tokens)
    assert not action.is_valid_for_state(exhausted_budget_state)

    # No context
    state_no_context = RAEState(tenant_id="test", project_id="test")
    state_no_context.working_context.token_count = 0
    assert not action.is_valid_for_state(state_no_context)

    # Cost exceeds budget (USD)
    state_poor = RAEState(tenant_id="test", project_id="test")
    state_poor.budget_state.remaining_cost_usd = 0.000001  # Very low
    state_poor.working_context.token_count = 1000
    # Estimate will be > 0.000001
    assert not action.is_valid_for_state(state_poor)

    # Tokens exceed budget
    state_low_tokens = RAEState(tenant_id="test", project_id="test")
    state_low_tokens.budget_state.remaining_tokens = 10  # Low
    state_low_tokens.working_context.token_count = 1000  # Needs input + output
    assert not action.is_valid_for_state(state_low_tokens)


@pytest.mark.unit
def test_generate_reflection_invalid_states(exhausted_budget_state):
    action = GenerateReflectionAction(parameters={"min_cluster_size": 5})

    # Budget exhausted
    assert not action.is_valid_for_state(exhausted_budget_state)

    # Insufficient memories
    state_few_memories = RAEState(tenant_id="test", project_id="test")
    state_few_memories.memory_state.episodic.count = 2
    state_few_memories.memory_state.semantic.count = 2
    # Total 4 < 10 (2 * min_cluster_size)
    assert not action.is_valid_for_state(state_few_memories)


@pytest.mark.unit
def test_summarize_context_invalid_states(exhausted_budget_state):
    action = SummarizeContextAction(parameters={})

    # Budget exhausted
    assert not action.is_valid_for_state(exhausted_budget_state)

    # Empty context
    state_no_context = RAEState(tenant_id="test", project_id="test")
    state_no_context.working_context.token_count = 0
    assert not action.is_valid_for_state(state_no_context)


@pytest.mark.unit
def test_consolidate_episodic_invalid_states():
    action = ConsolidateEpisodicToWorkingAction(parameters={})

    # No episodic memories
    state_empty = RAEState(tenant_id="test", project_id="test")
    assert not action.is_valid_for_state(state_empty)

    # Working memory full
    state_full = RAEState(tenant_id="test", project_id="test")
    state_full.memory_state.episodic.count = 10
    state_full.memory_state.working.count = 101  # > 100
    assert not action.is_valid_for_state(state_full)


@pytest.mark.unit
def test_update_graph_costs():
    # Coverage for different operations in estimate_cost
    state = RAEState(tenant_id="test", project_id="test")

    action_merge = UpdateGraphAction(parameters={"operation": "merge_nodes"})
    cost_merge = action_merge.estimate_cost(state)
    assert cost_merge["latency_ms"] == 100

    action_prune = UpdateGraphAction(parameters={"operation": "prune"})
    cost_prune = action_prune.estimate_cost(state)
    assert cost_prune["latency_ms"] == 200

    action_default = UpdateGraphAction(parameters={"operation": "add_node"})
    cost_default = action_default.estimate_cost(state)
    assert cost_default["latency_ms"] == 20


@pytest.mark.unit
def test_summarize_context_abstractive_cost():
    # Coverage for abstractive summarization cost path
    state = RAEState(tenant_id="test", project_id="test")
    state.working_context.token_count = 1000

    action = SummarizeContextAction(parameters={"method": "abstractive"})
    cost = action.estimate_cost(state)

    assert cost["tokens"] > 0
    assert cost["cost_usd"] > 0
