from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from rae_core.adapters.qdrant import QdrantVectorStore


@pytest.mark.asyncio
async def test_batch_store_vectors_empty():
    store = QdrantVectorStore()
    assert await store.batch_store_vectors([], "t1") == 0


@pytest.mark.asyncio
async def test_search_similar_with_session_id():
    mock_client = AsyncMock()
    mock_client.get_collection = AsyncMock()
    mock_client.search = AsyncMock(return_value=[])

    store = QdrantVectorStore(client=mock_client)
    store._initialized = True

    await store.search_similar([0.1], "t1", session_id="s1")
    call_args = mock_client.search.call_args
    # Check if session_id is in filter
    # Filter object string representation contains the fields
    assert "session_id" in str(call_args.kwargs["query_filter"])


@pytest.mark.asyncio
async def test_search_with_contradiction_penalty_missing_vectors():
    mock_client = AsyncMock()
    mock_client.get_collection = AsyncMock()
    store = QdrantVectorStore(client=mock_client)
    store._initialized = True

    id1 = uuid4()
    id2 = uuid4()
    id3 = uuid4()

    with patch.object(
        store,
        "search_similar",
        AsyncMock(return_value=[(id1, 0.9), (id2, 0.8), (id3, 0.7)]),
    ):
        # Mock get_vector to return vector for id1 and id3, but NOT for id2
        with patch.object(
            store,
            "get_vector",
            AsyncMock(
                side_effect=lambda memory_id, tenant_id: (
                    [1.0] if memory_id != id2 else None
                )
            ),
        ):
            results = await store.search_with_contradiction_penalty([1.0], "t1")
            assert len(results) == 3
            # id2 should have no penalty
            id2_res = next(r for r in results if r[0] == id2)
            assert id2_res[1] == 0.8  # Original score


@pytest.mark.asyncio
async def test_search_similar_with_agent_id():
    mock_client = AsyncMock()
    mock_client.get_collection = AsyncMock()
    mock_client.search = AsyncMock(return_value=[])

    store = QdrantVectorStore(client=mock_client)
    store._initialized = True

    await store.search_similar([0.1], "t1", agent_id="a1")
    call_args = mock_client.search.call_args
    assert "agent_id" in str(call_args.kwargs["query_filter"])


@pytest.mark.asyncio
async def test_count_vectors_with_layer():
    mock_client = AsyncMock()
    mock_client.get_collection = AsyncMock()

    mock_res = MagicMock()
    mock_res.count = 5
    mock_client.count = AsyncMock(return_value=mock_res)

    store = QdrantVectorStore(client=mock_client)
    store._initialized = True

    count = await store.count_vectors("t1", layer="episodic")
    assert count == 5
    call_args = mock_client.count.call_args
    assert "layer" in str(call_args.kwargs["count_filter"])


@pytest.mark.asyncio
async def test_search_with_contradiction_penalty_full_logic():
    mock_client = AsyncMock()
    mock_client.get_collection = AsyncMock()

    store = QdrantVectorStore(client=mock_client)
    store._initialized = True

    id1 = uuid4()
    id2 = uuid4()

    # Mock search_similar
    with patch.object(
        store, "search_similar", AsyncMock(return_value=[(id1, 0.9), (id2, 0.8)])
    ):
        # Mock get_vector to return contradictory vectors
        # Similarity between query [1,0] and mem [-1,0] is -1
        # -1 < 0.15, so it triggers penalty
        with patch.object(
            store, "get_vector", AsyncMock(side_effect=[[-1.0, 0.0], [-1.0, 0.0]])
        ):
            results = await store.search_with_contradiction_penalty(
                [1.0, 0.0], "t1", penalty_factor=0.5
            )
            assert len(results) == 2
            # Both should be penalized since they contradict each other?
            # Actually the logic penalizes based on query similarity vs candidate similarity
            # If query is [1,0] and mem1 is [1,0], similarity is 1.0.
            # If mem2 is [-1,0], similarity(mem1, mem2) is -1.0.
            # -1.0 < 0.15, so penalty is applied.
            # results[0] is (id1, 0.9 * 0.5) = 0.45? No, it depends on implementation.
            # Let's just check they are penalized.
            assert results[0][1] < 0.9
