import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from apps.memory_api.services.reflection_engine import ReflectionEngine
from apps.memory_api.services.llm.base import LLMResult, LLMResultUsage

@pytest.mark.asyncio
async def test_reflection_flow():
    mock_pool = MagicMock()
    mock_conn = AsyncMock()
    mock_acquire_cm = AsyncMock()
    mock_acquire_cm.__aenter__.return_value = mock_conn
    mock_acquire_cm.__aexit__.return_value = None
    mock_pool.acquire.return_value = mock_acquire_cm
    
    mock_conn.fetch.return_value = [{"id": "1", "content": "Event"}]

    engine = ReflectionEngine(mock_pool)
    engine.llm_provider = MagicMock()
    engine.llm_provider.generate = AsyncMock(return_value=LLMResult(
        text="Insight",
        usage=LLMResultUsage(prompt_tokens=1, candidates_tokens=1, total_tokens=2),
        model_name="gpt",
        finish_reason="stop"
    ))

    with patch("apps.memory_api.services.reflection_engine.settings") as mock_settings,          patch("httpx.AsyncClient") as mock_http:
        
        mock_settings.API_KEY = "key"
        mock_settings.MEMORY_API_URL = "http://mem"
        mock_settings.RAE_LLM_MODEL_DEFAULT = "gpt"
        
        mock_http.return_value.__aenter__.return_value.post = AsyncMock()
        
        res = await engine.generate_reflection("p1", "t1")
        
        assert "Insight" in res