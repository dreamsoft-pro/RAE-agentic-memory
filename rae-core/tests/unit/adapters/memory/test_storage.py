"""Unit tests for InMemoryStorage adapter."""

from uuid import uuid4

import pytest

from rae_core.adapters.memory.storage import InMemoryStorage


class TestInMemoryStorage:
    """Test suite for InMemoryStorage."""

    @pytest.fixture
    async def storage(self):
        """Create storage instance for testing."""
        return InMemoryStorage()

    @pytest.mark.asyncio
    async def test_store_memory_basic(self, storage):
        """Test basic memory storage."""
        memory_id = await storage.store_memory(
            content="Test memory",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
        )

        assert memory_id is not None
        assert isinstance(memory_id, type(uuid4()))

    @pytest.mark.asyncio
    async def test_store_and_retrieve_memory(self, storage):
        """Test storing and retrieving memory."""
        memory_id = await storage.store_memory(
            content="Test content",
            layer="episodic",
            tenant_id="tenant1",
            agent_id="agent1",
            tags=["test", "sample"],
            metadata={"source": "test"},
            importance=0.8,
        )

        memory = await storage.get_memory(memory_id, "tenant1")

        assert memory is not None
        assert memory["content"] == "Test content"
        assert memory["layer"] == "episodic"
        assert memory["tenant_id"] == "tenant1"
        assert memory["agent_id"] == "agent1"
        assert "test" in memory["tags"]
        assert memory["metadata"]["source"] == "test"
        assert memory["importance"] == 0.8

    @pytest.mark.asyncio
    async def test_get_nonexistent_memory(self, storage):
        """Test retrieving non-existent memory."""
        memory = await storage.get_memory(uuid4(), "tenant1")
        assert memory is None

    @pytest.mark.asyncio
    async def test_get_memory_wrong_tenant(self, storage):
        """Test tenant isolation."""
        memory_id = await storage.store_memory(
            content="Test",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
        )

        # Try to get with wrong tenant
        memory = await storage.get_memory(memory_id, "tenant2")
        assert memory is None

    @pytest.mark.asyncio
    async def test_update_memory_content(self, storage):
        """Test updating memory content."""
        memory_id = await storage.store_memory(
            content="Original",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
        )

        success = await storage.update_memory(
            memory_id, "tenant1", {"content": "Updated"}
        )
        assert success is True

        memory = await storage.get_memory(memory_id, "tenant1")
        assert memory["content"] == "Updated"
        assert memory["version"] == 2

    @pytest.mark.asyncio
    async def test_update_memory_tags(self, storage):
        """Test updating memory tags."""
        memory_id = await storage.store_memory(
            content="Test",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
            tags=["tag1", "tag2"],
        )

        success = await storage.update_memory(
            memory_id, "tenant1", {"tags": ["tag2", "tag3"]}
        )
        assert success is True

        memory = await storage.get_memory(memory_id, "tenant1")
        assert set(memory["tags"]) == {"tag2", "tag3"}

    @pytest.mark.asyncio
    async def test_update_memory_layer(self, storage):
        """Test updating memory layer."""
        memory_id = await storage.store_memory(
            content="Test",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
        )

        success = await storage.update_memory(
            memory_id, "tenant1", {"layer": "episodic"}
        )
        assert success is True

        memory = await storage.get_memory(memory_id, "tenant1")
        assert memory["layer"] == "episodic"

    @pytest.mark.asyncio
    async def test_update_nonexistent_memory(self, storage):
        """Test updating non-existent memory."""
        success = await storage.update_memory(
            uuid4(), "tenant1", {"content": "Updated"}
        )
        assert success is False

    @pytest.mark.asyncio
    async def test_delete_memory(self, storage):
        """Test deleting memory."""
        memory_id = await storage.store_memory(
            content="Test",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
        )

        success = await storage.delete_memory(memory_id, "tenant1")
        assert success is True

        memory = await storage.get_memory(memory_id, "tenant1")
        assert memory is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_memory(self, storage):
        """Test deleting non-existent memory."""
        success = await storage.delete_memory(uuid4(), "tenant1")
        assert success is False

    @pytest.mark.asyncio
    async def test_list_memories_by_tenant(self, storage):
        """Test listing memories by tenant."""
        # Create memories for different tenants
        await storage.store_memory(
            content="T1M1", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="T1M2", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="T2M1", layer="working", tenant_id="tenant2", agent_id="agent1"
        )

        memories = await storage.list_memories("tenant1")
        assert len(memories) == 2

    @pytest.mark.asyncio
    async def test_list_memories_by_agent(self, storage):
        """Test listing memories by agent."""
        await storage.store_memory(
            content="A1M1", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="A2M1", layer="working", tenant_id="tenant1", agent_id="agent2"
        )

        memories = await storage.list_memories("tenant1", agent_id="agent1")
        assert len(memories) == 1
        assert memories[0]["content"] == "A1M1"

    @pytest.mark.asyncio
    async def test_list_memories_by_layer(self, storage):
        """Test listing memories by layer."""
        await storage.store_memory(
            content="W1", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="E1", layer="episodic", tenant_id="tenant1", agent_id="agent1"
        )

        memories = await storage.list_memories("tenant1", layer="working")
        assert len(memories) == 1
        assert memories[0]["content"] == "W1"

    @pytest.mark.asyncio
    async def test_list_memories_by_tags(self, storage):
        """Test listing memories by tags (OR logic)."""
        await storage.store_memory(
            content="M1",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
            tags=["tag1"],
        )
        await storage.store_memory(
            content="M2",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
            tags=["tag2"],
        )
        await storage.store_memory(
            content="M3",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
            tags=["tag3"],
        )

        memories = await storage.list_memories("tenant1", tags=["tag1", "tag2"])
        assert len(memories) == 2

    @pytest.mark.asyncio
    async def test_list_memories_pagination(self, storage):
        """Test memory listing with pagination."""
        # Create 5 memories
        for i in range(5):
            await storage.store_memory(
                content=f"M{i}",
                layer="working",
                tenant_id="tenant1",
                agent_id="agent1",
            )

        # Get first page
        page1 = await storage.list_memories("tenant1", limit=2, offset=0)
        assert len(page1) == 2

        # Get second page
        page2 = await storage.list_memories("tenant1", limit=2, offset=2)
        assert len(page2) == 2

        # Pages should have different memories
        assert page1[0]["id"] != page2[0]["id"]

    @pytest.mark.asyncio
    async def test_count_memories_by_tenant(self, storage):
        """Test counting memories by tenant."""
        await storage.store_memory(
            content="M1", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="M2", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="M3", layer="working", tenant_id="tenant2", agent_id="agent1"
        )

        count = await storage.count_memories("tenant1")
        assert count == 2

    @pytest.mark.asyncio
    async def test_count_memories_with_filters(self, storage):
        """Test counting memories with filters."""
        await storage.store_memory(
            content="M1", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="M2", layer="episodic", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="M3", layer="working", tenant_id="tenant1", agent_id="agent2"
        )

        count = await storage.count_memories(
            "tenant1", agent_id="agent1", layer="working"
        )
        assert count == 1

    @pytest.mark.asyncio
    async def test_increment_access_count(self, storage):
        """Test incrementing access count."""
        memory_id = await storage.store_memory(
            content="Test",
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
        )

        # Increment 3 times
        for _ in range(3):
            success = await storage.increment_access_count(memory_id, "tenant1")
            assert success is True

        memory = await storage.get_memory(memory_id, "tenant1")
        assert memory["access_count"] == 3

    @pytest.mark.asyncio
    async def test_increment_access_count_nonexistent(self, storage):
        """Test incrementing access count for non-existent memory."""
        success = await storage.increment_access_count(uuid4(), "tenant1")
        assert success is False

    @pytest.mark.asyncio
    async def test_clear_tenant(self, storage):
        """Test clearing all memories for a tenant."""
        # Create memories for different tenants
        await storage.store_memory(
            content="T1M1", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="T1M2", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="T2M1", layer="working", tenant_id="tenant2", agent_id="agent1"
        )

        count = await storage.clear_tenant("tenant1")
        assert count == 2

        # Verify tenant1 memories are gone
        memories = await storage.list_memories("tenant1")
        assert len(memories) == 0

        # Verify tenant2 memories still exist
        memories = await storage.list_memories("tenant2")
        assert len(memories) == 1

    @pytest.mark.asyncio
    async def test_get_statistics(self, storage):
        """Test getting storage statistics."""
        # Create some memories
        await storage.store_memory(
            content="M1", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="M2", layer="episodic", tenant_id="tenant1", agent_id="agent2"
        )

        stats = await storage.get_statistics()

        assert stats["total_memories"] == 2
        assert stats["tenants"] == 1
        assert stats["agents"] >= 1
        assert stats["layers"] >= 1

    @pytest.mark.asyncio
    async def test_clear_all(self, storage):
        """Test clearing all data."""
        # Create memories
        await storage.store_memory(
            content="M1", layer="working", tenant_id="tenant1", agent_id="agent1"
        )
        await storage.store_memory(
            content="M2", layer="working", tenant_id="tenant2", agent_id="agent1"
        )

        count = await storage.clear_all()
        assert count == 2

        # Verify all memories are gone
        stats = await storage.get_statistics()
        assert stats["total_memories"] == 0

    @pytest.mark.asyncio
    async def test_concurrent_operations(self, storage):
        """Test thread safety with concurrent operations."""
        import asyncio

        async def store_memory(i):
            return await storage.store_memory(
                content=f"M{i}",
                layer="working",
                tenant_id="tenant1",
                agent_id="agent1",
            )

        # Store 10 memories concurrently
        tasks = [store_memory(i) for i in range(10)]
        memory_ids = await asyncio.gather(*tasks)

        # Verify all were stored
        assert len(memory_ids) == 10
        assert len(set(memory_ids)) == 10  # All unique

        count = await storage.count_memories("tenant1")
        assert count == 10
