"""
Tests for RAE Engine.
"""

import pytest

from rae_core import RAEEngine


@pytest.mark.asyncio
async def test_engine_initialization():
    """Test engine initialization."""
    engine = RAEEngine()

    assert engine.sensory is not None
    assert engine.working is not None
    assert engine.longterm is not None
    assert engine.reflective is not None


@pytest.mark.asyncio
async def test_store_and_query():
    """Test basic store and query operations."""
    engine = RAEEngine()

    # Store a memory
    memory_id = await engine.store_memory(
        content="Test memory about Python programming",
        source="test",
        importance=0.8,
        tags=["python", "programming"]
    )

    assert memory_id is not None
    assert memory_id.startswith("mem_")

    # Query the memory
    response = await engine.query_memory(
        query="Python programming",
        k=5
    )

    assert len(response.results) > 0
    assert response.results[0].content == "Test memory about Python programming"


@pytest.mark.asyncio
async def test_consolidation():
    """Test memory consolidation."""
    engine = RAEEngine(enable_auto_consolidation=False)

    # Store multiple memories
    for i in range(5):
        await engine.store_memory(
            content=f"Memory {i}",
            importance=0.7,
            layer="sensory"
        )

    # Manual consolidation
    results = await engine.consolidate_memories()

    assert "sensory_to_working" in results
    assert len(results["sensory_to_working"]) > 0


@pytest.mark.asyncio
async def test_statistics():
    """Test statistics gathering."""
    engine = RAEEngine()

    # Store some memories
    await engine.store_memory(content="Memory 1", layer="longterm")
    await engine.store_memory(content="Memory 2", layer="working")

    stats = await engine.get_statistics()

    assert "sensory" in stats
    assert "working" in stats
    assert "longterm" in stats
    assert "reflective" in stats
    assert stats["total_memories"] >= 2
