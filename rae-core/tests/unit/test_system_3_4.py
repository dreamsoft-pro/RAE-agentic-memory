from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from rae_core.adapters.qdrant import QdrantVectorStore
from rae_core.embedding.native import NativeEmbeddingProvider
from rae_core.math.bandit.arm import Arm
from rae_core.math.bandit.bandit import BanditConfig, MultiArmedBandit
from rae_core.math.types import MathLevel

# --- Test Sliding Window Arm ---


def test_arm_sliding_window():
    """Test that Arm uses sliding window for mean calculation."""
    arm = Arm(level=MathLevel.L1, strategy="test", window_size=5)

    # Fill window
    rewards = [1.0, 1.0, 1.0, 1.0, 1.0]
    for r in rewards:
        arm.update(r)

    assert arm.mean_reward() == 1.0
    assert len(arm.history) == 5

    # Push new values (0.0) - should slide out old 1.0s
    for _ in range(5):
        arm.update(0.0)

    assert arm.mean_reward() == 0.0  # Window should only contain 0.0s now
    assert len(arm.history) == 5

    # Partial update
    arm.update(0.5)
    # History: [0.0, 0.0, 0.0, 0.0, 0.5] -> Sum 0.5 / 5 = 0.1
    assert arm.mean_reward() == 0.1


def test_arm_reset():
    """Test that reset_window clears history."""
    arm = Arm(level=MathLevel.L1, strategy="test")
    arm.update(1.0)
    assert len(arm.history) == 1

    arm.reset_window()
    assert len(arm.history) == 0
    assert arm.mean_reward() == 0.0


# --- Test Bandit Drift Detection ---


def test_bandit_drift_detection_and_reset():
    """Test that degradation triggers a global reset."""
    config = BanditConfig(degradation_threshold=0.5)  # 50% drop triggers reset
    bandit = MultiArmedBandit(config=config)

    # 1. Establish high baseline
    bandit.baseline_mean_reward = 1.0
    bandit.total_pulls = 100  # Simulate mature state

    # 2. Simulate recent rewards dropping to 0.0
    # We need to fill last_100_rewards with 0.0
    bandit.last_100_rewards = [0.0] * 20  # Minimum 20 samples to check

    # 3. Simulate arms having history
    for arm in bandit.arms:
        arm.update(1.0)  # Assume they were good

    assert bandit.arms[0].history != []

    # 4. Check degradation
    is_degraded, drop = bandit.check_degradation()

    assert is_degraded is True
    assert drop > 0.5

    # 5. Verify RESET happened
    assert bandit.baseline_mean_reward == 0.0
    assert bandit.last_100_rewards == []
    for arm in bandit.arms:
        assert arm.history == []  # Window cleared


# --- Test Native Embedding Provider Prefixes ---


@patch("rae_core.embedding.native.ort")
@patch("rae_core.embedding.native.Tokenizer")
def test_nomic_prefixes(mock_tokenizer, mock_ort):
    """Test that Nomic models get correct prefixes."""
    # Setup mocks
    mock_ort.get_available_providers.return_value = ["CPUExecutionProvider"]
    session_mock = MagicMock()
    # Mock get_inputs/outputs for init
    input_mock = MagicMock()
    input_mock.name = "input_ids"
    output_mock = MagicMock()
    output_mock.name = "last_hidden_state"
    session_mock.get_inputs.return_value = [input_mock]
    session_mock.get_outputs.return_value = [output_mock]

    # Mock run return value (batch, seq, dim=10)
    import numpy as np

    session_mock.run.return_value = [np.zeros((1, 1, 10))]

    mock_ort.InferenceSession.return_value = session_mock

    mock_enc = MagicMock()
    mock_enc.ids = [1]
    mock_enc.attention_mask = [1]
    mock_tokenizer.from_file.return_value.encode_batch.return_value = [mock_enc]

    # Initialize Provider with Nomic name
    provider = NativeEmbeddingProvider(
        model_path="dummy_nomic.onnx",
        tokenizer_path="dummy.json",
        model_name="nomic-embed-text-v1.5",
    )

    # Test Embed Batch
    import asyncio

    async def run_test():
        # Call with search_query
        await provider.embed_batch(["test query"], task_type="search_query")

        # Check Tokenizer call - verify prefix was added
        call_args = mock_tokenizer.from_file.return_value.encode_batch.call_args
        texts_passed = call_args[0][0]
        assert texts_passed[0] == "search_query: test query"

        # Call with search_document
        await provider.embed_batch(["test doc"], task_type="search_document")
        call_args = mock_tokenizer.from_file.return_value.encode_batch.call_args
        texts_passed = call_args[0][0]
        assert texts_passed[0] == "search_document: test doc"

        # Call with prefix already present
        await provider.embed_batch(["search_query: existing"], task_type="search_query")
        call_args = mock_tokenizer.from_file.return_value.encode_batch.call_args
        texts_passed = call_args[0][0]
        assert texts_passed[0] == "search_query: existing"  # No double prefix

    asyncio.run(run_test())


# --- Test Qdrant Multi-Vector ---


@pytest.mark.asyncio
async def test_qdrant_multi_vector_search():
    """Test that search passes vector_name to client."""
    mock_client = AsyncMock()
    store = QdrantVectorStore(client=mock_client)

    # Setup mocks
    mock_client.search = AsyncMock(return_value=[])
    mock_client.get_collections = AsyncMock()
    mock_client.get_collections.return_value.collections = []  # force create
    mock_client.create_collection = AsyncMock()

    # Call search with vector_name
    await store.search_similar(
        query_embedding=[0.1] * 384, tenant_id="t1", vector_name="custom_vector_space"
    )

    # Verify client.search was called with named vector
    call_kwargs = mock_client.search.call_args.kwargs
    query_vector = call_kwargs["query_vector"]

    assert query_vector.name == "custom_vector_space"
    assert query_vector.vector == [0.1] * 384
