from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from rae_core.search.strategies.fulltext import FullTextStrategy


@pytest.mark.asyncio
async def test_fulltext_wildcard_search():
    # Setup
    mock_storage = AsyncMock()
    # Updated mock to return list of dicts as expected by the search_memories call
    mock_storage.search_memories.return_value = [
        {"id": str(UUID(int=1)), "content": "Memory 1", "score": 1.0},
        {"id": str(UUID(int=2)), "content": "Memory 2", "score": 1.0},
        {"id": str(UUID(int=3)), "content": "Memory 3", "score": 1.0},
    ]

    strategy = FullTextStrategy(memory_storage=mock_storage)

    # Execute wildcard search
    results = await strategy.search(query="*", tenant_id="tenant-123")

    # Verify
    assert len(results) == 3
    assert results[0][1] == 1.0


@pytest.mark.asyncio
async def test_fulltext_normal_search():
    # Setup
    mock_storage = AsyncMock()
    mock_storage.search_memories.return_value = [
        {"id": str(UUID(int=1)), "content": "Target memory", "score": 1.0},
    ]

    strategy = FullTextStrategy(memory_storage=mock_storage)

    # Execute normal search
    results = await strategy.search(query="Target", tenant_id="tenant-123")

    # Verify
    assert len(results) == 1
    assert results[0][1] == 1.0
