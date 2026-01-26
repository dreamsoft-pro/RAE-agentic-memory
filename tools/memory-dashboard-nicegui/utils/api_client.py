import httpx
import os
import logging
from typing import Optional, Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAEClient:
    def __init__(self, api_url: str, api_key: str, tenant_id: str = "default", project_id: str = "default"):
        self.api_url = api_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "X-Tenant-ID": tenant_id,
            "X-Project-ID": project_id,
            "Content-Type": "application/json"
        }
        self.timeout = 10.0

    async def check_connection(self) -> bool:
        """Verifies API connectivity."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{self.api_url}/health")
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            return False

    async def get_tenants(self) -> List[Dict[str, str]]:
        """Fetch available tenants from /v1/system/tenants."""
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(f"{self.api_url}/v1/system/tenants")
                if resp.status_code == 200:
                    return resp.json()
                return []
        except Exception as e:
            logger.error(f"Failed to fetch tenants: {e}")
            return []

    async def get_projects(self) -> List[str]:
        """Fetch available projects from /v1/system/projects."""
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(f"{self.api_url}/v1/system/projects")
                if resp.status_code == 200:
                    data = resp.json()
                    # Endpoint returns List[str]
                    if isinstance(data, list):
                        # Ensure basic defaults are present if list is empty or partial
                        defaults = {"default", "default_agent"}
                        return list(set(data) | defaults)
                    return ["default", "default_agent"]
                
                logger.warning(f"Failed to fetch projects: {resp.status_code}")
                return ["default", "default_agent"]
        except Exception as e:
            logger.error(f"Failed to fetch projects: {e}")
            return ["default", "default_agent"]

    async def update_context(self, tenant_id: str, project_id: str):
        """Update client headers with new context."""
        self.headers["X-Tenant-ID"] = tenant_id
        self.headers["X-Project-ID"] = project_id
        # Also re-verify connection or similar if needed

    async def get_stats(self) -> Dict[str, Any]:
        """Fetches memory statistics using v2 API (RAE-Core native)."""
        project = self.headers.get("X-Project-ID", "default")
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(f"{self.api_url}/v2/memories/stats?project={project}")
                if resp.status_code == 200:
                    data = resp.json()
                    stats = data.get("statistics", {})
                    return {
                        "total": stats.get("total_count", 0),
                        "episodic": stats.get("layers", {}).get("episodic", 0),
                        "working": stats.get("layers", {}).get("working", 0),
                        "semantic": stats.get("layers", {}).get("semantic", 0),
                        "ltm": stats.get("layers", {}).get("ltm", 0)
                    }
                return {"total": 0, "episodic": 0, "working": 0, "semantic": 0, "ltm": 0}
        except Exception as e:
            logger.error(f"Stats fetch failed: {e}")
            return {"total": 0, "episodic": 0, "working": 0, "semantic": 0, "ltm": 0}

    async def get_recent_memories(self, limit: int = 50) -> List[Dict]:
        """Fetches recent memories using v2 API."""
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                payload = {
                    "query": "*", # Wildcard for retrieval
                    "k": limit,
                    "project": self.headers.get("X-Project-ID", "default"),
                    # We can use filters to sort by time if engine supports "sort_by" in filters,
                    # but typically engine returns most relevant (or recent if query is wildcard).
                    "filters": {} 
                }
                resp = await client.post(f"{self.api_url}/v2/memories/query", json=payload)
                
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("results", [])
                return []
        except Exception as e:
            logger.error(f"Failed to fetch memories: {e}")
            return []

    async def update_memory(self, memory_id: str, new_content: str, new_tags: List[str], reason: str, user: str) -> bool:
        """
        ISO 27001 Compliant Update (Append-Only) via v2 API.
        1. DELETE /v2/memories/{id}
        2. POST /v2/memories/
        """
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                # 1. Delete Old
                audit_headers = self.headers.copy()
                audit_headers["X-Audit-Reason"] = reason
                audit_headers["X-Audit-User"] = user
                
                del_resp = await client.delete(
                    f"{self.api_url}/v2/memories/{memory_id}",
                    headers=audit_headers
                )
                
                if del_resp.status_code not in [200, 404]:
                    logger.error(f"Failed to delete old memory: {del_resp.text}")
                    # In strict ISO, we might want to abort here. But for usability, if 404, proceed.
                    if del_resp.status_code != 404:
                        return False

                # 2. Create New (v2 Store)
                payload = {
                    "content": new_content,
                    "tags": new_tags,
                    "project": self.headers.get("X-Project-ID", "default"),
                    "source": "dashboard-iso-edit",
                    "importance": 1.0, 
                    "metadata": {
                        "previous_version_id": memory_id,
                        "modification_reason": reason,
                        "modified_by": user,
                        "is_manual_correction": True,
                        "lineage_action": "update"
                    }
                }
                
                create_resp = await client.post(
                    f"{self.api_url}/v2/memories/",
                    json=payload,
                    headers=audit_headers
                )
                
                return create_resp.status_code == 200
        except Exception as e:
            logger.error(f"Update failed: {e}")
            return False

    async def delete_memory(self, memory_id: str, reason: str, user: str) -> bool:
        """ISO 27001 Compliant Delete."""
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                audit_headers = self.headers.copy()
                audit_headers["X-Audit-Reason"] = reason
                audit_headers["X-Audit-User"] = user
                
                resp = await client.delete(
                    f"{self.api_url}/memories/{memory_id}",
                    headers=audit_headers
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return False
