"""Unit tests for ReflectionEngine to achieve 100% coverage."""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from rae_core.reflection.engine import ReflectionEngine


class TestReflectionEngineCoverage:
    """Test suite for ReflectionEngine coverage gaps."""

    @pytest.fixture
    def mock_deps(self):
        ms = MagicMock()
        ms.list_memories = AsyncMock(return_value=[])
        ms.get_memory = AsyncMock()
        ms.store_memory = AsyncMock(return_value=uuid4())

        llm = MagicMock()
        return ms, llm

    @pytest.mark.asyncio
    async def test_run_cycle_no_candidates(self, mock_deps):
        ms, llm = mock_deps
        # By default identify_reflection_candidates returns [] if storage is empty
        engine = ReflectionEngine(ms, llm)
        res = await engine.run_reflection_cycle("t", "a")
        assert res["success"] is False
        assert res["reason"] == "No reflection candidates found"

    @pytest.mark.asyncio
    async def test_generate_reflection_wrapper(self, mock_deps):
        ms, llm = mock_deps
        llm.summarize = AsyncMock(return_value="Summary")
        engine = ReflectionEngine(ms, llm)
        mid = uuid4()
        ms.get_memory.return_value = {"id": mid, "content": "c"}
        res = await engine.generate_reflection([mid], "t", "a")
        assert res["success"] is True

    @pytest.mark.asyncio
    async def test_execute_action_and_evaluate(self, mock_deps):
        ms, llm = mock_deps
        engine = ReflectionEngine(ms, llm)

        # Mock actor and evaluator explicitly if needed, but they are initialized in __init__
        # We can patch them on the engine instance
        engine.actor.execute_action = AsyncMock(
            return_value={"success": True, "action": "test"}
        )
        engine.evaluator.evaluate_action_outcome = AsyncMock(
            return_value={"score": 1.0}
        )

        res = await engine.execute_action("consolidate", {}, "t", evaluate=True)
        assert res["success"] is True
        assert "evaluation" in res
        assert res["evaluation"]["score"] == 1.0

    @pytest.mark.asyncio
    async def test_evaluate_memory_quality(self, mock_deps):
        ms, llm = mock_deps
        engine = ReflectionEngine(ms, llm)
        engine.evaluator.evaluate_memory_quality = AsyncMock(
            return_value={"quality": 0.8}
        )
        res = await engine.evaluate_memory_quality(uuid4(), "t")
        assert res["quality"] == 0.8

    @pytest.mark.asyncio
    async def test_identify_low_quality_memories(self, mock_deps):
        ms, llm = mock_deps
        mid1 = uuid4()
        ms.list_memories.return_value = [{"id": mid1}]
        engine = ReflectionEngine(ms, llm)
        engine.evaluator.evaluate_memory_quality = AsyncMock(
            return_value={"quality": 0.1}
        )

        low = await engine.identify_low_quality_memories("t", quality_threshold=0.4)
        assert len(low) == 1
        assert low[0] == mid1

    @pytest.mark.asyncio
    async def test_prune_low_quality_none_found(self, mock_deps):
        ms, llm = mock_deps
        engine = ReflectionEngine(ms, llm)
        # identify_low_quality_memories uses list_memories which is [] by default
        res = await engine.prune_low_quality_memories("t")
        assert res["success"] is True
        assert res["pruned_count"] == 0

    @pytest.mark.asyncio
    async def test_prune_low_quality_execute(self, mock_deps):
        ms, llm = mock_deps
        mid = uuid4()
        ms.list_memories.return_value = [{"id": mid}]
        engine = ReflectionEngine(ms, llm)
        engine.evaluator.evaluate_memory_quality = AsyncMock(
            return_value={"quality": 0.1}
        )
        engine.actor.execute_action = AsyncMock(
            return_value={"success": True, "count": 1}
        )

        res = await engine.prune_low_quality_memories("t")
        assert res["success"] is True
        engine.actor.execute_action.assert_called_once()
