import json
import httpx
from typing import Any, Dict, List, Optional
from .base import ModelAdapter, TaskComplexity, TaskRisk, ModelType, AgentContext, AgentResult

class OllamaAdapter(ModelAdapter):
    def __init__(self, model_type: ModelType, working_dir: str):
        self.model_type = model_type
        self.working_dir = working_dir
        self.endpoint = "http://localhost:11434/api/chat"

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "qwen2.5-coder:14b",
            "messages": messages,
            "stream": False
        }
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(self.endpoint, json=payload)
            return response.json()["message"]["content"]

    async def execute(self, context: AgentContext) -> AgentResult:
        resp = await self.generate_response(str(context))
        return AgentResult(success=True, output=resp, files_changed=[], metadata={})

    def get_cost_per_1k_tokens(self) -> float: return 0.0
    def is_available(self) -> bool: return True
