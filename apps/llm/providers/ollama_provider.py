"""
Ollama LLM Provider.
"""

import json
import os
import httpx
from collections.abc import AsyncIterator
from typing import Any, Dict, cast, Optional

from ..models import (
    LLMChunk,
    LLMProviderError,
    LLMRequest,
    LLMResponse,
    LLMTransientError,
    TokenUsage,
)

class OllamaProvider:
    """
    LLM provider for local Ollama models.
    """

    def __init__(self, api_url: Optional[str] = None):
        self.name = "ollama"
        self.max_context_tokens = 8192
        self.supports_streaming = True
        self.supports_tools = False
        self.api_url = api_url or os.getenv("OLLAMA_API_URL", "http://ollama-dev:11434")
        self.client = httpx.AsyncClient(base_url=self.api_url, timeout=300.0)

    async def complete(self, request: LLMRequest) -> LLMResponse:
        import requests
        import asyncio
        from functools import partial

        system_msg = ""
        user_msg = ""
        for msg in request.messages:
            if msg.role == "system": system_msg = msg.content
            if msg.role == "user": user_msg = msg.content

        payload = {
            "model": request.model,
            "prompt": user_msg,
            "system": system_msg,
            "stream": False,
            "options": {
                "temperature": request.temperature or 0.1,
                "num_ctx": self.max_context_tokens
            }
        }

        try:
            # We use synchronous requests inside an executor to bypass asyncio/httpx hangs
            loop = asyncio.get_event_loop()
            target_url = f"{self.api_url}/api/generate"
            
            def do_post():
                return requests.post(target_url, json=payload, timeout=300)

            resp = await loop.run_in_executor(None, do_post)
            
            if resp.status_code != 200:
                raise LLMProviderError(f"Ollama error {resp.status_code}: {resp.text[:200]}")
            
            data = resp.json()
            return LLMResponse(
                text=data.get("response", ""),
                model_name=request.model,
                usage=TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
                finish_reason="stop",
                raw=data
            )
        except Exception as e:
            raise LLMProviderError(f"Ollama synchronous failure at {self.api_url}: {type(e).__name__} - {str(e)}")

    def stream(self, request: LLMRequest) -> AsyncIterator[LLMChunk]:
        async def _stream():
            yield LLMChunk(text="Streaming not implemented")
        return _stream()
