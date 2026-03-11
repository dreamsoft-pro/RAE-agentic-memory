# rae_core/utils/memory_bridge.py
import os
import requests
import logging
from rae_core.utils.context import RAEContextLocator

class RAEMemoryBridge:
    """Enterprise bridge with automatic context detection."""
    
    def __init__(self, project_name: str = None):
        self.api_url = os.getenv("RAE_API_URL", "http://rae-api-dev:8000")
        self.tenant_id = RAEContextLocator.get_current_tenant_id()
        self.project = project_name or RAEContextLocator.get_project_name()
        self.logger = logging.getLogger(f"RAE.Bridge.{self.project}")

    def save_event(self, content: str, human_label: str, metadata: dict = None):
        if self.tenant_id == "UNKNOWN_TENANT":
            self.logger.warning("⚠️ Cannot save memory: Unknown Tenant Context")
            return False

        url = f"{self.api_url}/v2/memories"
        payload = {
            "content": content,
            "project": self.project,
            "human_label": human_label,
            "metadata": metadata or {},
            "importance": 0.5
        }
        headers = {"X-Tenant-Id": self.tenant_id}
        
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=5)
            return r.status_code in [200, 201]
        except Exception as e:
            self.logger.error(f"⚠️ Memory Bridge Error: {e}")
        return False
