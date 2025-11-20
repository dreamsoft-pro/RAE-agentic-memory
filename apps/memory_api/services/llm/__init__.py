from functools import lru_cache
from .base import LLMProvider
from .gemini import GeminiProvider
from .openai import OpenAIProvider
from .ollama import OllamaProvider
from .anthropic import AnthropicProvider
from .litellm_provider import LiteLLMProvider
from ...config import settings

@lru_cache(maxsize=1)
def get_llm_provider() -> LLMProvider:
    """
    Factory function to get the configured LLM provider.
    Uses a singleton pattern to ensure only one provider instance is created.
    """
    provider_name = settings.RAE_LLM_BACKEND
    
    if provider_name == "gemini":
        return GeminiProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    elif provider_name == "ollama":
        return OllamaProvider()
    elif provider_name == "anthropic":
        return AnthropicProvider()
    else:
        # For any other provider, use the generic LiteLLMProvider.
        # This assumes the provider name is a valid litellm provider name (e.g., "mistral", "deepseek").
        # The model name should be set in RAE_LLM_MODEL_DEFAULT.
        # e.g., RAE_LLM_BACKEND="mistral", RAE_LLM_MODEL_DEFAULT="mistral/mistral-large-latest"
        return LiteLLMProvider()
