"""
Additional coverage tests for reward.py to hit edge cases and helper functions.
"""

from unittest.mock import Mock

import pytest

from apps.memory_api.core.actions import SummarizeContextAction
from apps.memory_api.core.reward import RewardFunction
from apps.memory_api.core.state import RAEState


@pytest.fixture
def default_state():
    return RAEState(tenant_id="test", project_id="test")


@pytest.fixture
def reward_fn():
    return RewardFunction()


@pytest.mark.unit
def test_evaluate_quality_default_else_branch(reward_fn, default_state):
    # ActionType not in the explicit list (e.g. SUMMARIZE_CONTEXT)
    # Should hit the 'else: quality = 0.5' branch (Line 210 approx)
    action = SummarizeContextAction(parameters={})

    # Execution result irrelevant for default branch
    quality = reward_fn._evaluate_quality(default_state, action, default_state, None)
    assert quality == 0.5


@pytest.mark.unit
def test_evaluate_retrieval_quality_no_result(reward_fn):
    # Line 224: if not execution_result: return 0.5
    quality = reward_fn._evaluate_retrieval_quality(None)
    assert quality == 0.5


@pytest.mark.unit
def test_evaluate_reflection_quality_no_result(reward_fn):
    # Line 270: if not execution_result: return 0.5
    quality = reward_fn._evaluate_reflection_quality(None)
    assert quality == 0.5


@pytest.mark.unit
def test_evaluate_reflection_quality_empty_reflections(reward_fn):
    # Line 275: if not reflections: return 0.0
    quality = reward_fn._evaluate_reflection_quality({"reflections": []})
    assert quality == 0.0


@pytest.mark.unit
def test_evaluate_reflection_quality_with_scores(reward_fn):
    # Lines 284-288: scoring logic
    mock_reflection = Mock()
    mock_reflection.scoring = Mock()
    mock_reflection.scoring.composite_score = 0.8

    quality = reward_fn._evaluate_reflection_quality({"reflections": [mock_reflection]})
    assert quality == 0.8


@pytest.mark.unit
def test_evaluate_reflection_quality_no_scoring_obj(reward_fn):
    # Edge case where reflection object doesn't have scoring
    mock_reflection = Mock()
    del (
        mock_reflection.scoring
    )  # Ensure attribute error if accessed, or None if we set it
    mock_reflection.scoring = None

    quality = reward_fn._evaluate_reflection_quality({"reflections": [mock_reflection]})
    # Should skip appending to scores
    # if scores is empty, returns 0.6 (Line ~290)
    assert quality == 0.6


@pytest.mark.unit
def test_evaluate_pruning_quality_full_coverage(reward_fn, default_state):
    # Lines 298-317

    # 1. No result
    assert (
        reward_fn._evaluate_pruning_quality(default_state, default_state, None) == 0.5
    )

    # 2. Zero tokens saved
    assert (
        reward_fn._evaluate_pruning_quality(
            default_state, default_state, {"tokens_saved": 0}
        )
        == 0.0
    )

    # 3. Valid pruning
    state_before = RAEState(tenant_id="test", project_id="test")
    state_before.working_context.token_count = 1000

    # Saved 200 tokens = 20% compression
    quality = reward_fn._evaluate_pruning_quality(
        state_before, default_state, {"tokens_saved": 200}
    )
    # Expected: min(1.0, 0.2 * 2) = 0.4
    assert quality == 0.4


@pytest.mark.unit
def test_evaluate_graph_update_quality_branches(reward_fn, default_state):
    # Lines ~333, 338

    state_before = RAEState(tenant_id="test", project_id="test")
    state_before.graph_state.node_count = 10
    state_before.graph_state.edge_count = 10

    state_after = RAEState(tenant_id="test", project_id="test")
    state_after.graph_state.node_count = 10
    state_after.graph_state.edge_count = 10

    # 1. No change
    assert reward_fn._evaluate_graph_update_quality(state_before, state_after) == 0.5

    # 2. Increase nodes
    state_more_nodes = RAEState(tenant_id="test", project_id="test")
    state_more_nodes.graph_state.node_count = 11
    state_more_nodes.graph_state.edge_count = 10
    assert (
        reward_fn._evaluate_graph_update_quality(state_before, state_more_nodes) == 0.7
    )

    # 3. Pruning (decrease)
    state_fewer = RAEState(tenant_id="test", project_id="test")
    state_fewer.graph_state.node_count = 9
    assert reward_fn._evaluate_graph_update_quality(state_before, state_fewer) == 0.6


@pytest.mark.unit
def test_evaluate_llm_quality_edge_cases(reward_fn):
    # 1. No result (None) -> 0.5
    assert reward_fn._evaluate_llm_quality(None) == 0.5

    # 2. Empty dict (falsy) -> 0.5
    assert reward_fn._evaluate_llm_quality({}) == 0.5

    # 3. Non-empty dict without llm_result -> 0.0
    assert reward_fn._evaluate_llm_quality({"other": "data"}) == 0.0

    # 4. Short output
    mock_res = Mock()
    mock_res.text = "Short"
    assert reward_fn._evaluate_llm_quality({"llm_result": mock_res}) == 0.4

    # 5. Long output
    mock_res_long = Mock()
    mock_res_long.text = "A" * 2001
    assert reward_fn._evaluate_llm_quality({"llm_result": mock_res_long}) == 0.7

    # 6. Empty output
    mock_res_empty = Mock()
    mock_res_empty.text = ""
    assert reward_fn._evaluate_llm_quality({"llm_result": mock_res_empty}) == 0.0
