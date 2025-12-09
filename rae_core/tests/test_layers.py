"""
Tests for memory layers.
"""

import pytest
from datetime import datetime

from rae_core.layers import (
    SensoryLayer,
    WorkingMemoryLayer,
    LongTermMemoryLayer,
    ReflectiveMemoryLayer,
)
from rae_core.models.memory import MemoryRecord


@pytest.mark.asyncio
async def test_sensory_layer():
    """Test sensory layer operations."""
    layer = SensoryLayer(max_size=10, retention_seconds=60)

    memory = MemoryRecord(
        id="test_1",
        content="Test sensory memory",
        importance=0.5,
        timestamp=datetime.now()
    )

    # Store
    memory_id = await layer.store(memory)
    assert memory_id == "test_1"

    # Retrieve
    retrieved = await layer.get_by_id("test_1")
    assert retrieved is not None
    assert retrieved.content == "Test sensory memory"

    # Statistics
    stats = await layer.get_statistics()
    assert stats["count"] == 1


@pytest.mark.asyncio
async def test_working_memory():
    """Test working memory operations."""
    layer = WorkingMemoryLayer(max_size=20)

    memory = MemoryRecord(
        id="test_2",
        content="Test working memory",
        importance=0.7,
        timestamp=datetime.now()
    )

    # Store
    await layer.store(memory)

    # Query
    results = await layer.retrieve("working memory", k=5)
    assert len(results) > 0
    assert results[0].id == "test_2"


@pytest.mark.asyncio
async def test_longterm_memory():
    """Test long-term memory operations."""
    layer = LongTermMemoryLayer()

    memory = MemoryRecord(
        id="test_3",
        content="Important long-term knowledge",
        importance=0.9,
        timestamp=datetime.now(),
        tags=["important", "knowledge"]
    )

    # Store
    await layer.store(memory)

    # Query with filters
    results = await layer.retrieve(
        "knowledge",
        k=5,
        filters={"tags": ["important"]}
    )

    assert len(results) > 0
    assert results[0].tags is not None
    assert "important" in results[0].tags


@pytest.mark.asyncio
async def test_reflective_memory():
    """Test reflective memory operations."""
    layer = ReflectiveMemoryLayer()

    reflection = MemoryRecord(
        id="refl_1",
        content="Pattern: Users frequently ask about Python basics",
        importance=0.85,
        timestamp=datetime.now(),
        tags=["pattern", "python", "basics"]
    )

    # Store
    await layer.store(reflection)

    # Query
    results = await layer.retrieve("Python pattern", k=5)
    assert len(results) > 0

    # Get patterns
    patterns = await layer.get_patterns()
    assert "pattern" in patterns


@pytest.mark.asyncio
async def test_layer_consolidation():
    """Test consolidation between layers."""
    sensory = SensoryLayer()
    working = WorkingMemoryLayer()

    # Store high-importance memory in sensory
    memory = MemoryRecord(
        id="test_4",
        content="High importance memory",
        importance=0.9,
        timestamp=datetime.now()
    )
    await sensory.store(memory)

    # Consolidate
    consolidated = await sensory.consolidate(
        working,
        criteria={"importance_threshold": 0.7}
    )

    assert len(consolidated) > 0
    assert "test_4" in consolidated

    # Verify memory moved
    assert await sensory.get_by_id("test_4") is None
    assert await working.get_by_id("test_4") is not None
