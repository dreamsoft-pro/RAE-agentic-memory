from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from apps.memory_api.services.llm.base import LLMResult, LLMResultUsage
from apps.memory_api.services.reflection_engine import ReflectionEngine, Triples


@pytest.mark.asyncio
async def test_reflection_flow():
    mock_pool = MagicMock()
    mock_conn = AsyncMock()
    mock_acquire_cm = AsyncMock()
    mock_acquire_cm.__aenter__.return_value = mock_conn
    mock_acquire_cm.__aexit__.return_value = None
    mock_pool.acquire.return_value = mock_acquire_cm

    mock_conn.fetch.return_value = [{"id": "1", "content": "Event"}]
    mock_conn.execute = AsyncMock(return_value="INSERT 0 1")
    mock_conn.fetchrow = AsyncMock(return_value={"id": 1})

    # Mock transaction context
    class TransactionContext:
        async def __aenter__(self):
            return None

        async def __aexit__(self, *args):
            return None

    mock_conn.transaction = MagicMock(return_value=TransactionContext())

    engine = ReflectionEngine(mock_pool)
    engine.llm_provider = MagicMock()
    engine.llm_provider.generate = AsyncMock(
        return_value=LLMResult(
            text="Insight",
            usage=LLMResultUsage(prompt_tokens=1, candidates_tokens=1, total_tokens=2),
            model_name="gpt",
            finish_reason="stop",
        )
    )
    # Return a Triples model instance
    engine.llm_provider.generate_structured = AsyncMock(
        return_value=Triples(triples=[])
    )

    with patch(
        "apps.memory_api.services.reflection_engine.settings"
    ) as mock_settings, patch("httpx.AsyncClient") as mock_http:

        mock_settings.API_KEY = "key"
        mock_settings.MEMORY_API_URL = "http://mem"
        mock_settings.RAE_LLM_MODEL_DEFAULT = "gpt"

        mock_http.return_value.__aenter__.return_value.post = AsyncMock()

        res = await engine.generate_reflection("p1", "t1")

        # Result should contain project name and be a string
        assert isinstance(res, str)
        assert "p1" in res
