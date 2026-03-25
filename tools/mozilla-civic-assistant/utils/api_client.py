import logging
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Standard RAE Tenant ID for Mozilla Civic
CIVIC_TENANT_ID = "c1b1c1c1-c1c1-c1c1-c1c1-c1b1c1c1c1c1"

class CivicRAEClient:
    def __init__(
        self,
        api_url: str,
        api_key: str,
        tenant_id: str = CIVIC_TENANT_ID,
        project: str = "civic-watchdog",
    ):
        self.api_url = api_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "X-Tenant-ID": tenant_id,
            "X-Project-ID": project,
            "X-Agent-ID": "mozilla-civic-assistant",
            "Content-Type": "application/json",
        }
        self.tenant_id = tenant_id
        self.project = project
        self.timeout = 180.0 

    async def check_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{self.api_url}/health")
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            return False

    async def get_stats(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=10.0) as client:
                resp = await client.get(f"{self.api_url}/v2/memories/stats", params={"project": self.project})
                if resp.status_code == 200:
                    data = resp.json()
                    stats = data.get("statistics", {})
                    layers = stats.get("layers", {})
                    return {
                        "total": stats.get("total_count", 0),
                        "sensory": layers.get("sensory", 0),
                        "episodic": layers.get("episodic", 0),
                        "working": layers.get("working", 0),
                        "semantic": layers.get("semantic", 0),
                        "reflective": layers.get("reflective", 0),
                    }
                return {"total": 0, "semantic": 0, "reflective": 0}
        except Exception as e:
            logger.error(f"Stats fetch failed: {e}")
            return {"total": 0, "semantic": 0, "reflective": 0}

    async def ingest_v5(self, content: str, source: str, metadata: Optional[Dict] = None) -> bool:
        human_label = f"[CIVIC] Unified Ingest: {source}"
        try:
            payload = {
                "content": content,
                "project": self.project,
                "source": source,
                "human_label": human_label,
                "importance": 0.7,
                "info_class": "public",
                "trust_level": "high",
                "tags": ["civic", "v5_ingestion"],
                "metadata": {
                    **(metadata or {}),
                    "ingestion_method": "5-layer-pipeline",
                    "provenance_source": source
                }
            }
            async with httpx.AsyncClient(headers=self.headers, timeout=60.0) as client:
                resp = await client.post(f"{self.api_url}/v2/memories/", json=payload)
                return resp.status_code in [200, 201]
        except Exception as e:
            logger.error(f"V5 Ingestion failed: {e}")
            return False

    async def civic_query(self, query: str) -> Dict[str, Any]:
        try:
            payload = {
                "query": query,
                "project": self.project,
                "mode": "procedural",
                "stream": False
            }
            async with httpx.AsyncClient(headers=self.headers, timeout=180.0) as client:
                # Procedural reasoning path
                resp = await client.post(f"{self.api_url}/procedural/query", json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    # If LLM returned error message, fall back to search
                    if "Error" in str(data.get("instruction", "")):
                        pass # trigger fallback below
                    else:
                        return data
                
                # Hybrid search fallback
                resp_search = await client.post(f"{self.api_url}/v2/memories/query", json={
                    "query": query,
                    "project": self.project,
                    "k": 10
                })
                if resp_search.status_code == 200:
                    return {
                        "instruction": "Search Results (Grounding provided via RAE Semantic Layer)",
                        "results": resp_search.json().get("results", []),
                        "audit": {"status": "grounded"}
                    }
                return {"error": f"Query failed: {resp.status_code}"}
        except Exception as e:
            logger.error(f"Civic query failed: {e}")
            return {"error": str(e)}

    async def trigger_3layer_reflection(self) -> Dict[str, Any]:
        """
        Fixed Reflection Trigger using V2 /generate endpoint.
        """
        try:
            payload = {
                "tenant_id": self.tenant_id,
                "project": self.project,
                "max_memories": 100,
                "min_cluster_size": 2, # Smaller for demo
                "enable_clustering": True
            }
            async with httpx.AsyncClient(headers=self.headers, timeout=120.0) as client:
                # Correct RAE V2 Reflection Endpoint
                resp = await client.post(f"{self.api_url}/v2/reflections/generate", json=payload)
                if resp.status_code == 200:
                    return resp.json()
                return {"error": f"Reflection failed ({resp.status_code}): {resp.text}"}
        except Exception as e:
            logger.error(f"Reflection trigger failed: {e}")
            return {"error": str(e)}
