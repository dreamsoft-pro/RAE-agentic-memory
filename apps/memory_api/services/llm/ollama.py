from typing import Type
from pydantic import BaseModel
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
import json
from .base import LLMProvider, LLMResult, LLMResultUsage
from ...config import settings


class OllamaProvider(LLMProvider):
    """
    An LLM provider that uses a local Ollama server.
    """

    def __init__(self, api_url: str = None):
        self.api_url = api_url or settings.OLLAMA_API_URL
        if not self.api_url:
            raise ValueError("OLLAMA_API_URL is not set.")
        self.client = httpx.AsyncClient(base_url=self.api_url, timeout=120.0)

    @retry(wait=wait_exponential(multiplier=1, min=2, max=5), stop=stop_after_attempt(3))
    async def generate(self, *, system: str, prompt: str, model: str) -> LLMResult:
        """
        Generates content using the Ollama /api/generate endpoint.
        """
        try:
            payload = {
                "model": model,
                "system": system,
                "prompt": prompt,
                "stream": False,  # We want a single response
            }
            response = await self.client.post("/api/generate", json=payload)
            response.raise_for_status()

            result_data = response.json()

            usage = LLMResultUsage(
                prompt_tokens=result_data.get("prompt_eval_count", 0),
                candidates_tokens=result_data.get("eval_count", 0),
                total_tokens=result_data.get("prompt_eval_count", 0)
                + result_data.get("eval_count", 0),
            )

            return LLMResult(
                text=result_data.get("response", "").strip(),
                usage=usage,
                model_name=model,
                finish_reason=result_data.get("done_reason", "stop"),
            )
        except httpx.ConnectError as e:
            print(f"Could not connect to Ollama server at {self.api_url}. Is it running?")
            raise
        except Exception as e:
            print(f"Ollama API call failed: {e}")
            raise

    @retry(wait=wait_exponential(multiplier=1, min=2, max=5), stop=stop_after_attempt(3))
    async def generate_structured(
        self, *, system: str, prompt: str, model: str, response_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Generates structured content using the Ollama /api/generate endpoint.
        """
        try:
            payload = {
                "model": model,
                "system": system,
                "prompt": prompt,
                "stream": False,  # We want a single response
                "format": "json",
            }
            response = await self.client.post("/api/generate", json=payload)
            response.raise_for_status()

            result_data = response.json()
            response_json = json.loads(result_data.get("response", "{}"))
            return response_model.model_validate(response_json)

        except httpx.ConnectError as e:
            print(f"Could not connect to Ollama server at {self.api_url}. Is it running?")
            raise
        except Exception as e:
            print(f"Ollama API call failed: {e}")
            raise
