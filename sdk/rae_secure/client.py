import os
from typing import Optional

import requests

from .types import AgentIntent, KernelResponse


class RAEClient:
    """
    Thin Client for RAE Kernel.
    NO LLM LOGIC HERE. Just transport.
    """

    def __init__(self, kernel_url: Optional[str] = None, api_key: Optional[str] = None):
        self.kernel_url = kernel_url or os.getenv(
            "RAE_KERNEL_URL", "http://rae-kernel:8000"
        )
        self.api_key: str = (
            api_key or os.getenv("RAE_AGENT_KEY", "dev-key") or "dev-key"
        )
        self._session = requests.Session()
        self._session.headers.update(
            {"X-RAE-Agent-Key": self.api_key, "Content-Type": "application/json"}
        )

    def ask(self, intent_name: str, **kwargs) -> KernelResponse:
        """
        Send an intent to the Kernel.
        The Kernel decides which model (if any) to use.
        """
        intent = AgentIntent(name=intent_name, parameters=kwargs)

        try:
            resp = self._session.post(
                f"{self.kernel_url}/v1/agent/ask", json=intent.model_dump()
            )
            resp.raise_for_status()
            return KernelResponse(**resp.json())
        except Exception as e:
            return KernelResponse(success=False, error=str(e))

    def save_memory(self, content: str, importance: float = 0.5) -> bool:
        """
        Request the Kernel to save a memory.
        The Kernel will validate/sanitize it first.
        """
        payload = {"content": content, "importance": importance}
        try:
            resp = self._session.post(
                f"{self.kernel_url}/v1/agent/memory", json=payload
            )
            return resp.status_code == 200
        except Exception:
            return False


# Singleton instance for easy import
rae = RAEClient()
