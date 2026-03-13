from dataclasses import dataclass
from typing import Any, Dict, Optional
from orchestrator_v3.providers import ModelInfo, ModelTier, ProviderRegistry

@dataclass
class RoutingDecision:
    model_id: str
    provider: str
    model_info: Any
    rationale: str
    estimated_cost: float
    confidence: float

class ModelRouterV2:
    def __init__(self, registry: ProviderRegistry): self.registry = registry
    def _get_ollama(self):
        return RoutingDecision(model_id="qwen2.5-coder:7b", provider="ollama", model_info=None, rationale="FORCED LOCAL", estimated_cost=0.0, confidence=1.0)
    def choose_planner(self, risk, area, complexity): return self._get_ollama()
    def choose_plan_reviewer(self, model_id, risk): return self._get_ollama()
    def choose_implementer(self, risk, complexity, type, area): return self._get_ollama()
    def choose_code_reviewer(self, model_id, risk): return self._get_ollama()
    def estimate_task_cost(self, risk, area, complexity, steps=5): return {"total_cost": 0.0}
