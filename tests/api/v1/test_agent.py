import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from apps.memory_api.api.v1.agent import execute
from apps.memory_api.models import AgentExecuteRequest
from apps.memory_api.services.llm.base import LLMResult, LLMResultUsage
from fastapi import Request

@pytest.mark.asyncio
async def test_agent_execute_direct(mock_app_state_pool):
    with patch("apps.memory_api.api.v1.agent.get_context_cache") as mock_get_cache,          patch("apps.memory_api.api.v1.agent.get_embedding_service") as mock_embed,          patch("apps.memory_api.api.v1.agent.get_vector_store") as mock_vec,          patch("apps.memory_api.api.v1.agent.get_llm_provider") as mock_llm,          patch("apps.memory_api.api.v1.agent._update_memory_access_stats", new=AsyncMock()),          patch("httpx.AsyncClient") as mock_httpx:

        mock_cache_instance = MagicMock()
        mock_cache_instance.get_context.return_value = "Mocked Context"
        mock_get_cache.return_value = mock_cache_instance
        
        mock_embed.return_value.generate_embeddings.return_value = [[0.1]*384]
        
        mock_vec_inst = AsyncMock()
        mock_vec_inst.query = AsyncMock(return_value=[]) 
        mock_vec.return_value = mock_vec_inst
        
        mock_llm_inst = MagicMock()
        mock_llm_inst.generate = AsyncMock(return_value=LLMResult(
            text="Direct Answer",
            usage=LLMResultUsage(prompt_tokens=10, candidates_tokens=10, total_tokens=20),
            model_name="gpt-4",
            finish_reason="stop"
        ))
        mock_llm.return_value = mock_llm_inst
        
        mock_hclient = AsyncMock()
        mock_httpx.return_value.__aenter__.return_value = mock_hclient
        mock_hclient.post.return_value.json = AsyncMock(return_value={"items": []})

        mock_request = MagicMock(spec=Request)
        mock_request.headers.get.return_value = "t1"
        mock_request.app.state.pool = mock_app_state_pool

        payload = AgentExecuteRequest(
            tenant_id="t1",
            project="p1",
            prompt="Hi"
        )

        if hasattr(execute, "__wrapped__"):
            original_func = execute.__wrapped__
        else:
            original_func = execute
        
        response = await original_func(payload, mock_request)

        assert response.answer == "Direct Answer"
        mock_cache_instance.get_context.assert_called()

@pytest.mark.asyncio
async def test_agent_execute_with_context(mock_app_state_pool):
    """Test agent execution with memory context retrieved"""
    with patch("apps.memory_api.api.v1.agent.get_context_cache") as mock_get_cache, \
         patch("apps.memory_api.api.v1.agent.get_embedding_service") as mock_embed, \
         patch("apps.memory_api.api.v1.agent.get_vector_store") as mock_vec, \
         patch("apps.memory_api.api.v1.agent.get_llm_provider") as mock_llm, \
         patch("apps.memory_api.api.v1.agent._update_memory_access_stats", new=AsyncMock()), \
         patch("httpx.AsyncClient") as mock_httpx:

        mock_cache_instance = MagicMock()
        mock_cache_instance.get_context.return_value = "User prefers dark mode"
        mock_get_cache.return_value = mock_cache_instance

        mock_embed.return_value.generate_embeddings.return_value = [[0.1]*384]

        mock_vec_inst = AsyncMock()
        mock_vec_inst.query = AsyncMock(return_value=[])
        mock_vec.return_value = mock_vec_inst

        mock_llm_inst = MagicMock()
        mock_llm_inst.generate = AsyncMock(return_value=LLMResult(
            text="I'll set dark mode for you",
            usage=LLMResultUsage(prompt_tokens=20, candidates_tokens=15, total_tokens=35),
            model_name="gpt-4",
            finish_reason="stop"
        ))
        mock_llm.return_value = mock_llm_inst

        mock_hclient = AsyncMock()
        mock_httpx.return_value.__aenter__.return_value = mock_hclient
        mock_hclient.post.return_value.json = AsyncMock(return_value={"items": []})

        mock_request = MagicMock(spec=Request)
        mock_request.headers.get.return_value = "t1"
        mock_request.app.state.pool = mock_app_state_pool

        payload = AgentExecuteRequest(
            tenant_id="t1",
            project="p1",
            prompt="Set UI theme"
        )

        if hasattr(execute, "__wrapped__"):
            original_func = execute.__wrapped__
        else:
            original_func = execute

        response = await original_func(payload, mock_request)

        assert response.answer == "I'll set dark mode for you"
        assert "dark mode" in mock_cache_instance.get_context.return_value

@pytest.mark.asyncio
async def test_agent_execute_with_empty_prompt(mock_app_state_pool):
    """Test agent execution with empty prompt"""
    with patch("apps.memory_api.api.v1.agent.get_context_cache") as mock_get_cache, \
         patch("apps.memory_api.api.v1.agent.get_embedding_service") as mock_embed, \
         patch("apps.memory_api.api.v1.agent.get_vector_store") as mock_vec, \
         patch("apps.memory_api.api.v1.agent.get_llm_provider") as mock_llm, \
         patch("apps.memory_api.api.v1.agent._update_memory_access_stats", new=AsyncMock()), \
         patch("httpx.AsyncClient") as mock_httpx:

        mock_cache_instance = MagicMock()
        mock_cache_instance.get_context.return_value = ""
        mock_get_cache.return_value = mock_cache_instance

        mock_embed.return_value.generate_embeddings.return_value = [[0.1]*384]

        mock_vec_inst = AsyncMock()
        mock_vec_inst.query = AsyncMock(return_value=[])
        mock_vec.return_value = mock_vec_inst

        mock_llm_inst = MagicMock()
        mock_llm_inst.generate = AsyncMock(return_value=LLMResult(
            text="How can I help you?",
            usage=LLMResultUsage(prompt_tokens=5, candidates_tokens=5, total_tokens=10),
            model_name="gpt-4",
            finish_reason="stop"
        ))
        mock_llm.return_value = mock_llm_inst

        mock_hclient = AsyncMock()
        mock_httpx.return_value.__aenter__.return_value = mock_hclient
        mock_hclient.post.return_value.json = AsyncMock(return_value={"items": []})

        mock_request = MagicMock(spec=Request)
        mock_request.headers.get.return_value = "t1"
        mock_request.app.state.pool = mock_app_state_pool

        payload = AgentExecuteRequest(
            tenant_id="t1",
            project="p1",
            prompt=""
        )

        if hasattr(execute, "__wrapped__"):
            original_func = execute.__wrapped__
        else:
            original_func = execute

        response = await original_func(payload, mock_request)

        assert response.answer == "How can I help you?"

@pytest.mark.asyncio
async def test_agent_execute_with_llm_error(mock_app_state_pool):
    """Test agent execution when LLM provider fails"""
    with patch("apps.memory_api.api.v1.agent.get_context_cache") as mock_get_cache, \
         patch("apps.memory_api.api.v1.agent.get_embedding_service") as mock_embed, \
         patch("apps.memory_api.api.v1.agent.get_vector_store") as mock_vec, \
         patch("apps.memory_api.api.v1.agent.get_llm_provider") as mock_llm, \
         patch("apps.memory_api.api.v1.agent._update_memory_access_stats", new=AsyncMock()), \
         patch("httpx.AsyncClient") as mock_httpx:

        mock_cache_instance = MagicMock()
        mock_cache_instance.get_context.return_value = "Context"
        mock_get_cache.return_value = mock_cache_instance

        mock_embed.return_value.generate_embeddings.return_value = [[0.1]*384]

        mock_vec_inst = AsyncMock()
        mock_vec_inst.query = AsyncMock(return_value=[])
        mock_vec.return_value = mock_vec_inst

        # LLM fails
        mock_llm_inst = MagicMock()
        mock_llm_inst.generate = AsyncMock(side_effect=Exception("LLM API error"))
        mock_llm.return_value = mock_llm_inst

        mock_hclient = AsyncMock()
        mock_httpx.return_value.__aenter__.return_value = mock_hclient
        mock_hclient.post.return_value.json = AsyncMock(return_value={"items": []})

        mock_request = MagicMock(spec=Request)
        mock_request.headers.get.return_value = "t1"
        mock_request.app.state.pool = mock_app_state_pool

        payload = AgentExecuteRequest(
            tenant_id="t1",
            project="p1",
            prompt="test"
        )

        if hasattr(execute, "__wrapped__"):
            original_func = execute.__wrapped__
        else:
            original_func = execute

        # Should raise exception
        with pytest.raises(Exception, match="LLM API error"):
            await original_func(payload, mock_request)