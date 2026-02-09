import os
from typing import Optional

import requests

from .types import KernelResponse


class RAEClient:
    """
    Thin Client for RAE Kernel.
    NO LLM LOGIC HERE. Just transport.
    """

    def __init__(
        self,
        kernel_url: Optional[str] = None,
        api_key: Optional[str] = None,
        project: str = "default",
    ):
        self.kernel_url = kernel_url or os.getenv(
            "RAE_KERNEL_URL", "http://rae-kernel:8000"
        )
        self.api_key: str = (
            api_key or os.getenv("RAE_AGENT_KEY", "dev-key") or "dev-key"
        )
        self.project = project
        self._session = requests.Session()
        self._session.headers.update(
            {"X-RAE-Agent-Key": self.api_key, "Content-Type": "application/json"}
        )

    def ask(self, intent_name: str, **kwargs) -> KernelResponse:
        """
        Send an intent to the Kernel.
        The Kernel decides which model (if any) to use.
        """
        # Map intent to V2 Agent Execute
        payload = {"prompt": intent_name, "project": self.project, "metadata": kwargs}

        try:
            resp = self._session.post(
                f"{self.kernel_url}/v2/agent/execute", json=payload
            )
            resp.raise_for_status()
            # Map V2 response back to KernelResponse
            data = resp.json()
            return KernelResponse(success=True, data=data.get("answer"))
        except Exception as e:
            return KernelResponse(success=False, error=str(e))

    def save_memory(self, content: str, importance: float = 0.5) -> bool:
        """
        Request the Kernel to save a memory.
        The Kernel will validate/sanitize it first.
        """
        payload = {
            "content": content,
            "importance": importance,
            "project": self.project,
            "layer": "working",
            "source": "sdk",
        }
        try:
            resp = self._session.post(f"{self.kernel_url}/v2/memories/", json=payload)
            return resp.status_code == 200
        except Exception:
            return False


# Singleton instance for easy import
rae = RAEClient()
