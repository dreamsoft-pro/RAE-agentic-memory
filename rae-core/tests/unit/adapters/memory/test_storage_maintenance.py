"""Hardened unit tests for InMemoryStorage maintenance and analytics."""

import pytest
from uuid import uuid4
from rae_core.adapters.memory.storage import InMemoryStorage

class TestStorageMaintenance:
    @pytest.fixture
    async def storage(self):
        s = InMemoryStorage()
        # Seed with data for metrics
        for i in range(5):
            await s.store_memory(
                content=f"mem{i}",
                tenant_id="t1",
                importance=0.2 * i,
                metadata={"val": i * 10}
            )
        return s

    @pytest.mark.asyncio
    async def test_get_metric_aggregate_functions(self, storage):
        # Count
        assert await storage.get_metric_aggregate("t1", "importance", "count") == 5.0
        # Sum: 0.0 + 0.2 + 0.4 + 0.6 + 0.8 = 2.0
        assert abs(await storage.get_metric_aggregate("t1", "importance", "sum") - 2.0) < 1e-5
        # Avg: 2.0 / 5 = 0.4
        assert abs(await storage.get_metric_aggregate("t1", "importance", "avg") - 0.4) < 1e-5
        # Max
        assert await storage.get_metric_aggregate("t1", "importance", "max") == 0.8
        # Min
        assert await storage.get_metric_aggregate("t1", "importance", "min") == 0.0
        # Unknown func
        assert await storage.get_metric_aggregate("t1", "importance", "unknown") == 0.0

    @pytest.mark.asyncio
    async def test_get_metric_aggregate_with_filters(self, storage):
        # Average importance for memories with metadata val=20
        res = await storage.get_metric_aggregate(
            "t1", "importance", "avg", filters={"val": 20}
        )
        assert res == 0.4 # importance for i=2 is 0.2*2=0.4

    @pytest.mark.asyncio
    async def test_get_metric_aggregate_empty_or_wrong_tenant(self, storage):
        assert await storage.get_metric_aggregate("t2", "importance", "sum") == 0.0
        assert await storage.get_metric_aggregate("t1", "nonexistent", "sum") == 0.0

    @pytest.mark.asyncio
    async def test_adjust_importance_logic(self, storage):
        m_id = uuid4()
        await storage.store_memory(id=m_id, content="test", tenant_id="t1", importance=0.5)
        
        # Increase
        new_val = await storage.adjust_importance(m_id, 0.2, "t1")
        assert new_val == 0.7
        
        # Clamp Max
        new_val = await storage.adjust_importance(m_id, 1.0, "t1")
        assert new_val == 1.0
        
        # Clamp Min
        new_val = await storage.adjust_importance(m_id, -2.0, "t1")
        assert new_val == 0.0
        
        # Non-existent
        assert await storage.adjust_importance(uuid4(), 0.1, "t1") == 0.0

    @pytest.mark.asyncio
    async def test_update_memory_access_batch(self, storage):
        mids = [m["id"] for m in (await storage.list_memories("t1"))]
        success = await storage.update_memory_access_batch(mids, "t1")
        assert success is True
        
        for mid in mids:
            mem = await storage.get_memory(mid, "t1")
            assert mem["access_count"] == 1
