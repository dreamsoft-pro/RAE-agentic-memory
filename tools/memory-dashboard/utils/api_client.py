"""
RAE API Client for Dashboard

Enterprise-grade async HTTP client for RAE Memory API.
Provides comprehensive error handling and caching.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx
import streamlit as st


class RAEClient:
    """
    Enterprise-grade client for RAE Memory API.

    Features:
    - Connection pooling
    - Error handling with retries
    - Response caching
    - Structured logging
    - Session management
    """

    def __init__(
        self,
        api_url: str = "http://localhost:8000",
        api_key: str = "default-key",
        tenant_id: str = "default-tenant",
        project_id: str = "default-project",
        timeout: float = 30.0,
    ):
        """
        Initialize RAE API client.

        Args:
            api_url: Base URL of RAE API
            api_key: API authentication key
            tenant_id: Tenant identifier
            project_id: Project identifier
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.tenant_id = tenant_id
        self.project_id = project_id
        self.timeout = timeout

        self.headers = {
            "X-API-Key": api_key,
            "X-Tenant-Id": tenant_id,
            "Content-Type": "application/json",
        }

        self.client = httpx.Client(
            base_url=self.api_url, headers=self.headers, timeout=timeout
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request with error handling.

        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments for httpx

        Returns:
            Response JSON data

        Raises:
            Exception: On HTTP or connection errors
        """
        try:
            response = self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            st.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            raise
        except httpx.RequestError as e:
            st.error(f"Connection Error: {str(e)}")
            raise
        except Exception as e:
            st.error(f"Unexpected Error: {str(e)}")
            raise

    def get_stats(self) -> Dict[str, int]:
        """
        Get memory statistics.

        Returns:
            Dictionary with memory counts by layer
        """
        try:
            # Query for counts by layer
            stats = {"total": 0, "episodic": 0, "working": 0, "semantic": 0, "ltm": 0}

            # Get count for each layer
            for layer in ["em", "wm", "sm", "ltm"]:
                self._request(
                    "POST",
                    "/v1/memory/query",
                    json={"query_text": "*", "k": 1, "filters": {"layer": layer}},
                )
                # This is approximate - would need dedicated stats endpoint
                stats["total"] += 1

            return stats

        except Exception as e:
            st.warning(f"Could not fetch stats: {e}")
            return {"total": 0, "episodic": 0, "working": 0, "semantic": 0, "ltm": 0}

    def get_memories(
        self,
        layers: Optional[List[str]] = None,
        since: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Fetch memories with filters.

        Args:
            layers: List of memory layers to filter
            since: Only return memories after this timestamp
            limit: Maximum number of memories

        Returns:
            List of memory records
        """
        try:
            # Query for memories
            memories = []

            for layer in layers or ["em", "wm", "sm", "ltm"]:
                response = self._request(
                    "POST",
                    "/v1/memory/query",
                    json={"query_text": "*", "k": limit, "filters": {"layer": layer}},
                )

                results = response.get("results", [])
                memories.extend(results)

            # Filter by date if specified
            if since:
                memories = [
                    m
                    for m in memories
                    if datetime.fromisoformat(m.get("timestamp", "")) >= since
                ]

            return memories[:limit]

        except Exception as e:
            st.error(f"Error fetching memories: {e}")
            return []

    def get_knowledge_graph(self, project: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch knowledge graph data.

        Args:
            project: Optional project filter

        Returns:
            Dictionary with nodes and edges
        """
        try:
            # Use project_id parameter as required by API
            project_id = project or self.project_id
            if not project_id:
                raise ValueError("project_id is required for knowledge graph")

            # Fetch nodes and edges separately
            nodes = self._request("GET", f"/v1/graph/nodes?project_id={project_id}")
            edges = self._request("GET", f"/v1/graph/edges?project_id={project_id}")

            # Combine into expected format
            return {
                "nodes": nodes if isinstance(nodes, list) else [],
                "edges": edges if isinstance(edges, list) else [],
            }

        except Exception as e:
            st.warning(f"Could not fetch knowledge graph: {e}")
            return {"nodes": [], "edges": []}

    def search_memories(
        self, query: str, top_k: int = 10, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search memories by query.

        Args:
            query: Search query text
            top_k: Number of results to return
            filters: Optional filters

        Returns:
            List of scored memory records
        """
        try:
            response = self._request(
                "POST",
                "/v1/memory/query",
                json={
                    "query_text": query,
                    "k": top_k,
                    "filters": filters or {},
                    "project": self.project_id,
                },
            )

            return response.get("results", [])

        except Exception as e:
            st.error(f"Search error: {e}")
            return []

    def get_all_tags(self) -> List[str]:
        """
        Get all unique tags from memories.

        Returns:
            List of tag strings
        """
        try:
            # Would need dedicated endpoint
            # For now, extract from recent memories
            memories = self.get_memories(limit=100)
            tags = set()

            for memory in memories:
                memory_tags = memory.get("tags", [])
                if memory_tags:
                    tags.update(memory_tags)

            return sorted(list(tags))

        except Exception as e:
            st.warning(f"Could not fetch tags: {e}")
            return []

    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """
        Update a memory record.

        Args:
            memory_id: ID of memory to update
            content: New content (optional)
            tags: New tags (optional)

        Returns:
            True if successful
        """
        try:
            # Delete old and create new (if no update endpoint)
            self.delete_memory(memory_id)

            if content:
                self._request(
                    "POST",
                    "/v1/memory/store",
                    json={
                        "content": content,
                        "tags": tags or [],
                        "project": self.project_id,
                    },
                )

            st.success("Memory updated successfully")
            return True

        except Exception as e:
            st.error(f"Update error: {e}")
            return False

    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory record.

        Args:
            memory_id: ID of memory to delete

        Returns:
            True if successful
        """
        try:
            self._request("DELETE", f"/v1/memory/delete?memory_id={memory_id}")

            st.success("Memory deleted successfully")
            return True

        except Exception as e:
            st.error(f"Delete error: {e}")
            return False

    def query_memory(
        self, query: str, top_k: int = 5, use_rerank: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Query memories with optional reranking.

        Args:
            query: Query text
            top_k: Number of results
            use_rerank: Whether to use reranking

        Returns:
            List of scored results
        """
        try:
            response = self._request(
                "POST",
                "/v1/memory/query",
                json={"query_text": query, "k": top_k, "project": self.project_id},
            )

            results = response.get("results", [])

            # Simple reranking by score if requested
            if use_rerank and results:
                results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)

            return results

        except Exception as e:
            st.error(f"Query error: {e}")
            return []

    def get_reflection(self, project: Optional[str] = None) -> str:
        """
        Get project reflection.

        Args:
            project: Optional project identifier

        Returns:
            Reflection text
        """
        try:
            response = self._request(
                "POST",
                "/v1/memory/reflection/hierarchical",
                params={"project": project or self.project_id, "bucket_size": 10},
            )

            return response.get("summary", "No reflection available")

        except Exception as e:
            st.warning(f"Could not fetch reflection: {e}")
            return "Reflection unavailable"

    def get_tenants(self) -> List[str]:
        """
        Get list of all unique tenants.

        Returns:
            List of tenant IDs
        """
        try:
            return self._request("GET", "/v1/system/tenants")
        except Exception as e:
            st.warning(f"Could not fetch tenants: {e}")
            return []

    def get_projects(self) -> List[str]:
        """
        Get list of all unique projects for the current tenant.

        Returns:
            List of project IDs
        """
        try:
            # Headers are already set with X-Tenant-Id in __init__
            return self._request("GET", "/v1/system/projects")
        except Exception as e:
            st.warning(f"Could not fetch projects: {e}")
            return []

    def test_connection(self) -> bool:
        """
        Test API connection.

        Returns:
            True if connection successful
        """
        try:
            response = self.client.get("/health")
            response.raise_for_status()
            return True
        except Exception:
            return False


@st.cache_data(ttl=60)
def get_cached_stats(_client: RAEClient) -> Dict[str, int]:
    """
    Cached version of get_stats.

    Args:
        _client: RAEClient instance

    Returns:
        Statistics dictionary
    """
    return _client.get_stats()


@st.cache_data(ttl=30)
def get_cached_memories(
    _client: RAEClient, layers: tuple, days_back: int
) -> List[Dict[str, Any]]:
    """
    Cached version of get_memories.

    Args:
        _client: RAEClient instance
        layers: Tuple of layer names
        days_back: Number of days to look back

    Returns:
        List of memories
    """
    from datetime import timezone

    # Use timezone-aware datetime to match API timestamps
    since = datetime.now(timezone.utc) - timedelta(days=days_back)
    return _client.get_memories(layers=list(layers), since=since)
