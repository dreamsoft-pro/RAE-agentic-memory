from unittest.mock import AsyncMock, mock_open, patch

import pytest

from apps.llm.broker.llm_router import LLMRouter
from apps.llm.models import (
    LLMAuthError,
    LLMMessage,
    LLMRateLimitError,
    LLMRequest,
    LLMResponse,
    TokenUsage,
)


@pytest.fixture
def mock_config():
    return {
        "providers": {
            "openai": {"api_key_env": "OPENAI_API_KEY"},
            "anthropic": {"api_key_env": "ANTHROPIC_API_KEY"},
            "ollama": {"endpoint": "http://localhost:11434"},
        }
    }


@pytest.fixture
def router(mock_config):
    with patch("builtins.open", mock_open(read_data="data")), patch(
        "yaml.safe_load", return_value=mock_config
    ), patch("apps.llm.broker.llm_router.OpenAIProvider") as MockOpenAI, patch(
        "apps.llm.broker.llm_router.AnthropicProvider"
    ) as MockAnthropic, patch(
        "apps.llm.broker.llm_router.OllamaProvider"
    ) as MockOllama:

        # Setup mock instances
        mock_openai = MockOpenAI.return_value
        mock_openai.name = "openai"
        mock_openai.complete = AsyncMock()

        mock_anthropic = MockAnthropic.return_value
        mock_anthropic.name = "anthropic"
        mock_anthropic.complete = AsyncMock()

        mock_ollama = MockOllama.return_value
        mock_ollama.name = "ollama"
        mock_ollama.complete = AsyncMock()

        router = LLMRouter(config_path="dummy.yaml")
        return router


@pytest.mark.asyncio
async def test_initialization(router):
    assert "openai" in router.providers
    assert "anthropic" in router.providers
    assert "ollama" in router.providers


@pytest.mark.asyncio
async def test_get_provider_for_model(router):
    # GPT -> OpenAI
    provider = router._get_provider_for_model("gpt-4")
    assert provider.name == "openai"

    # Claude -> Anthropic
    provider = router._get_provider_for_model("claude-3")
    assert provider.name == "anthropic"

    # Llama -> Ollama
    provider = router._get_provider_for_model("llama-3")
    assert provider.name == "ollama"

    # Unknown -> Default (first available)
    provider = router._get_provider_for_model("unknown-model")
    assert provider is not None


@pytest.mark.asyncio
async def test_complete_success(router):
    request = LLMRequest(
        model="gpt-4", messages=[LLMMessage(role="user", content="Hi")]
    )
    mock_response = LLMResponse(
        text="Hello",
        finish_reason="stop",
        usage=TokenUsage(prompt_tokens=5, completion_tokens=5, total_tokens=10),
        raw={},
    )

    provider = router.providers["openai"]
    provider.complete.return_value = mock_response

    response = await router.complete(request)

    assert response == mock_response
    provider.complete.assert_called_once_with(request)


@pytest.mark.asyncio
async def test_complete_no_provider(router):
    # Clear providers to force error
    router.providers = {}
    request = LLMRequest(model="gpt-4", messages=[])

    with pytest.raises(ValueError, match="No provider available"):
        await router.complete(request)


@pytest.mark.asyncio
async def test_complete_auth_error(router):
    request = LLMRequest(model="gpt-4", messages=[])
    provider = router.providers["openai"]
    provider.complete.side_effect = LLMAuthError("Auth failed")

    with pytest.raises(LLMAuthError):
        await router.complete(request)


@pytest.mark.asyncio
async def test_complete_rate_limit_error(router):
    request = LLMRequest(model="gpt-4", messages=[])
    provider = router.providers["openai"]
    provider.complete.side_effect = LLMRateLimitError("Rate limit")

    # Should re-raise (fallback logic in code is TODO)
    with pytest.raises(LLMRateLimitError):
        await router.complete(request)


@pytest.mark.asyncio
async def test_stream_success(router):
    request = LLMRequest(model="gpt-4", messages=[])
    provider = router.providers["openai"]
    provider.supports_streaming = True

    async def mock_stream(req):
        yield "chunk1"
        yield "chunk2"

    provider.stream = mock_stream

    chunks = []
    async for chunk in router.stream(request):
        chunks.append(chunk)

    assert chunks == ["chunk1", "chunk2"]


@pytest.mark.asyncio
async def test_stream_not_supported(router):
    request = LLMRequest(model="gpt-4", messages=[])
    provider = router.providers["openai"]
    provider.supports_streaming = False

    with pytest.raises(ValueError, match="does not support streaming"):
        async for _ in router.stream(request):
            pass
