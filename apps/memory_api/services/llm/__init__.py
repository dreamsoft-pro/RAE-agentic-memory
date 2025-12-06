from functools import lru_cache

from apps.llm.broker.orchestrator import LLMOrchestrator

from .base import LLMProvider
from .orchestrator_adapter import OrchestratorAdapter


@lru_cache(maxsize=1)
def get_llm_provider() -> LLMProvider:
    """
    Factory function to get the configured LLM provider.
    Uses the LLM Orchestrator to manage model selection and strategies.
    """
    # Initialize Orchestrator
    # It will load configuration from apps/llm/config/llm_config.yaml
    orchestrator = LLMOrchestrator()

    # Return Adapter that satisfies the LLMProvider protocol
    return OrchestratorAdapter(orchestrator)
