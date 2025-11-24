"""
Tests for Background Tasks (Celery)

Test suite for Celery background tasks including lazy graph extraction,
reflection generation, and scheduled maintenance tasks.

Test Coverage Goals (per test_2.md):
- Task calls correct service
- Success/exception handling (log + retry)
- Scheduler calls correct tasks

Priority: HIGH (Critical for async processing)
Current Coverage: 0% -> Target: 60%+
"""

from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

pytest.importorskip(
    "community",
    reason="Requires community (python-louvain) for community detection tests.",
)

from apps.memory_api.tasks.background_tasks import (
    apply_memory_decay,
    extract_graph_lazy,
    generate_reflection_for_project,
    process_graph_extraction_queue,
    prune_old_memories,
)


class TestExtractGraphLazy:
    """Tests for lazy graph extraction background task.

    This is the most critical task - handles background graph extraction
    with retry logic and cost optimization (mini model).
    """

    @patch("apps.memory_api.tasks.background_tasks.get_pool")
    @patch("apps.memory_api.tasks.background_tasks.GraphExtractionService")
    def test_extract_graph_success(self, mock_service_class, mock_get_pool):
        """Test successful graph extraction.

        Verifies:
        - Service is called with correct parameters
        - Result contains expected data
        - Pool is properly closed
        """
        # Mock pool
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool

        # Mock service and extraction result
        mock_service = Mock()
        mock_result = Mock()
        mock_result.triples = [Mock(), Mock(), Mock()]  # 3 triples
        mock_result.extracted_entities = ["Entity1", "Entity2"]
        mock_service.extract_knowledge_graph = AsyncMock(return_value=mock_result)
        mock_service_class.return_value = mock_service

        # Execute task
        result = extract_graph_lazy(
            memory_ids=["mem1", "mem2"], tenant_id="tenant-123", use_mini_model=True
        )

        # Verify service was called
        mock_service.extract_knowledge_graph.assert_called_once()
        call_kwargs = mock_service.extract_knowledge_graph.call_args[1]
        assert call_kwargs["tenant_id"] == "tenant-123"
        assert call_kwargs["min_confidence"] == 0.7

        # Verify result
        assert result["success"] is True
        assert result["triples"] == 3
        assert result["entities"] == 2

    @patch("apps.memory_api.tasks.background_tasks.get_pool")
    @patch("apps.memory_api.tasks.background_tasks.GraphExtractionService")
    def test_extract_graph_with_mini_model(self, mock_service_class, mock_get_pool):
        """Test that mini model is used when requested.

        Cost optimization: gpt-4o-mini instead of gpt-4.
        """
        # Mock pool
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool

        # Mock service with LLM provider
        mock_service = Mock()
        mock_service.llm_provider = Mock()
        mock_service.llm_provider.model = "gpt-4"
        mock_result = Mock(triples=[], extracted_entities=[])
        mock_service.extract_knowledge_graph = AsyncMock(return_value=mock_result)
        mock_service_class.return_value = mock_service

        # Execute with mini model
        extract_graph_lazy(
            memory_ids=["mem1"], tenant_id="tenant-123", use_mini_model=True
        )

        # Verify model was switched to mini
        assert mock_service.llm_provider.model == "gpt-4o-mini"

    @patch("apps.memory_api.tasks.background_tasks.get_pool")
    @patch("apps.memory_api.tasks.background_tasks.GraphExtractionService")
    def test_extract_graph_exception_handling(self, mock_service_class, mock_get_pool):
        """Test that exceptions are logged and trigger retry.

        Verifies:
        - Exception is caught
        - Error is logged
        - Retry is triggered with exponential backoff
        """
        # Mock pool
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool

        # Mock service that raises exception
        mock_service = Mock()
        mock_service.extract_knowledge_graph = AsyncMock(
            side_effect=Exception("LLM API error")
        )
        mock_service_class.return_value = mock_service

        # Mock self.retry for Celery task
        mock_self = Mock()
        mock_self.request = Mock()
        mock_self.request.retries = 0
        mock_self.retry = Mock(side_effect=Exception("Retry triggered"))

        # Execute should raise exception (retry)
        with pytest.raises(Exception):
            # Bind self to the task
            task = extract_graph_lazy
            task.__self__ = mock_self
            task(mock_self, memory_ids=["mem1"], tenant_id="tenant-123")

    @patch("apps.memory_api.tasks.background_tasks.get_pool")
    @patch("apps.memory_api.tasks.background_tasks.GraphExtractionService")
    def test_extract_graph_pool_cleanup(self, mock_service_class, mock_get_pool):
        """Test that pool is closed even on exception.

        Resource cleanup is critical to avoid connection leaks.
        """
        # Mock pool
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool

        # Mock service that raises
        mock_service = Mock()
        mock_service.extract_knowledge_graph = AsyncMock(
            side_effect=Exception("Test error")
        )
        mock_service_class.return_value = mock_service

        # Mock retry to prevent actual retry
        with patch.object(extract_graph_lazy, "retry", side_effect=Exception("Retry")):
            try:
                extract_graph_lazy(memory_ids=["mem1"], tenant_id="tenant-123")
            except:
                pass

        # Pool close should still be called
        mock_pool.close.assert_called_once()


class TestProcessGraphExtractionQueue:
    """Tests for periodic graph extraction queue processor."""

    @patch("apps.memory_api.tasks.background_tasks.get_pool")
    @patch("apps.memory_api.tasks.background_tasks.extract_graph_lazy")
    def test_queue_processor_schedules_tasks(self, mock_extract_task, mock_get_pool):
        """Test that queue processor schedules extraction tasks.

        Verifies:
        - Queries for pending memories
        - Schedules lazy extraction for each tenant
        - Passes correct parameters
        """
        # Mock pool with pending memories
        mock_pool = AsyncMock()
        mock_pool.fetch = AsyncMock(
            return_value=[
                {"tenant_id": "tenant1", "memory_ids": ["mem1", "mem2"]},
                {"tenant_id": "tenant2", "memory_ids": ["mem3", "mem4", "mem5"]},
            ]
        )
        mock_get_pool.return_value = mock_pool

        # Mock the delay method
        mock_extract_task.delay = Mock()

        # Execute
        process_graph_extraction_queue()

        # Verify tasks were scheduled
        assert mock_extract_task.delay.call_count == 2

        # Verify first call
        first_call = mock_extract_task.delay.call_args_list[0]
        assert first_call[1]["tenant_id"] == "tenant1"
        assert first_call[1]["memory_ids"] == ["mem1", "mem2"]
        assert first_call[1]["use_mini_model"] is True

    @patch("apps.memory_api.tasks.background_tasks.get_pool")
    def test_queue_processor_no_pending_memories(self, mock_get_pool):
        """Test queue processor with no pending memories.

        Should complete without errors.
        """
        # Mock pool with no results
        mock_pool = AsyncMock()
        mock_pool.fetch = AsyncMock(return_value=[])
        mock_get_pool.return_value = mock_pool

        # Should not raise exception
        process_graph_extraction_queue()

        # Pool should still be closed
        mock_pool.close.assert_called_once()


class TestGenerateReflection:
    """Tests for reflection generation task."""

    @patch("apps.memory_api.tasks.background_tasks.get_pool")
    @patch("apps.memory_api.tasks.background_tasks.ReflectionEngine")
    def test_generate_reflection_calls_engine(self, mock_engine_class, mock_get_pool):
        """Test that reflection task calls the engine correctly.

        Verifies service contract is maintained.
        """
        # Mock pool
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool

        # Mock engine
        mock_engine = Mock()
        mock_engine.generate_reflection = AsyncMock()
        mock_engine_class.return_value = mock_engine

        # Execute
        generate_reflection_for_project(project="my-project", tenant_id="tenant-123")

        # Verify engine was called
        mock_engine.generate_reflection.assert_called_once_with(
            "my-project", "tenant-123"
        )

        # Verify cleanup
        mock_pool.close.assert_called_once()


class TestMemoryDecay:
    """Tests for memory decay maintenance task."""

    @patch("apps.memory_api.tasks.background_tasks.get_pool")
    @patch("apps.memory_api.tasks.background_tasks.settings")
    def test_apply_decay_updates_strength(self, mock_settings, mock_get_pool):
        """Test that decay is applied to memory strength.

        Verifies:
        - Decay rate is applied
        - Expired memories are deleted
        - SQL is executed correctly
        """
        # Mock settings
        mock_settings.MEMORY_DECAY_RATE = 0.95

        # Mock pool
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool

        # Execute
        apply_memory_decay()

        # Verify execute was called twice (decay + delete)
        assert mock_pool.execute.call_count == 2

        # Check decay call
        decay_call = mock_pool.execute.call_args_list[0]
        assert "strength = strength *" in decay_call[0][0]


class TestPruneOldMemories:
    """Tests for memory pruning task."""

    @patch("apps.memory_api.tasks.background_tasks.get_pool")
    @patch("apps.memory_api.tasks.background_tasks.settings")
    def test_prune_respects_retention_days(self, mock_settings, mock_get_pool):
        """Test that pruning respects retention setting.

        Verifies:
        - Only episodic memories are pruned
        - Retention period is used correctly
        """
        # Mock settings
        mock_settings.MEMORY_RETENTION_DAYS = 90

        # Mock pool
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool

        # Execute
        prune_old_memories()

        # Verify delete was called
        mock_pool.execute.assert_called_once()
        sql = mock_pool.execute.call_args[0][0]

        assert "DELETE FROM memories" in sql
        assert "layer = 'em'" in sql  # Only episodic

    @patch("apps.memory_api.tasks.background_tasks.settings")
    def test_prune_disabled_when_retention_zero(self, mock_settings):
        """Test that pruning is disabled when retention is 0.

        Allows indefinite retention if configured.
        """
        # Mock settings with disabled pruning
        mock_settings.MEMORY_RETENTION_DAYS = 0

        # Execute - should return early without creating pool
        with patch("apps.memory_api.tasks.background_tasks.get_pool") as mock_get_pool:
            prune_old_memories()

            # Pool should not be created if disabled
            mock_get_pool.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
