from typing import Any, Dict, List, Optional

import httpx
import structlog
from pydantic_settings import BaseSettings

from .models import (
    DeleteMemoryResponse,
    QueryMemoryRequest,
    QueryMemoryResponse,
    StoreMemoryRequest,
    StoreMemoryResponse,
)

logger = structlog.get_logger(__name__)


class RAEClientConfig(BaseSettings):
    """
    Configuration settings for the RAE Memory Client.
    """

    RAE_API_URL: str = "http://localhost:8000"
    RAE_API_KEY: str = "your-rae-api-key"
    RAE_TENANT_ID: str = "default-tenant"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields from .env file


class MemoryClient:
    """
    Enterprise-grade client for interacting with the RAE Memory API.

    Supports both synchronous and asynchronous operations.
    """

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        tenant_id: Optional[str] = None,
        config: Optional[RAEClientConfig] = None,
    ):
        if config:
            self.config = config
        else:
            self.config = RAEClientConfig(
                RAE_API_URL=api_url or RAEClientConfig().RAE_API_URL,
                RAE_API_KEY=api_key or RAEClientConfig().RAE_API_KEY,
                RAE_TENANT_ID=tenant_id or RAEClientConfig().RAE_TENANT_ID,
            )

        self._http_client = httpx.Client(base_url=self.config.RAE_API_URL)
        self._async_http_client = httpx.AsyncClient(base_url=self.config.RAE_API_URL)
        self._headers = {
            "X-API-Key": self.config.RAE_API_KEY,
            "X-Tenant-Id": self.config.RAE_TENANT_ID,
            "Content-Type": "application/json",
        }

    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Synchronous HTTP request wrapper."""
        try:
            response = self._http_client.request(
                method, url, headers=self._headers, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                "http_error",
                url=url,
                status_code=e.response.status_code,
                response_text=e.response.text,
            )
            raise
        except httpx.RequestError as e:
            logger.error("request_error", url=url, error=str(e))
            raise

    async def _async_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Asynchronous HTTP request wrapper."""
        try:
            response = await self._async_http_client.request(
                method, url, headers=self._headers, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                "async_http_error",
                url=url,
                status_code=e.response.status_code,
                response_text=e.response.text,
            )
            raise
        except httpx.RequestError as e:
            logger.error("async_request_error", url=url, error=str(e))
            raise

    def store(self, memory: StoreMemoryRequest) -> StoreMemoryResponse:
        """
        Stores a new memory record.
        """
        response_data = self._request(
            "POST", "/memory/store", json=memory.dict(exclude_none=True)
        )
        return StoreMemoryResponse(**response_data)

    def query(
        self, query_text: str, k: int = 10, filters: Optional[Dict[str, Any]] = None
    ) -> QueryMemoryResponse:
        """
        Queries the memory for relevant records.
        """
        request_body = QueryMemoryRequest(query_text=query_text, k=k, filters=filters)
        response_data = self._request(
            "POST", "/memory/query", json=request_body.dict(exclude_none=True)
        )
        return QueryMemoryResponse(**response_data)

    def delete(self, memory_id: str) -> DeleteMemoryResponse:
        """
        Deletes a memory record by its ID.
        """
        response_data = self._request("DELETE", f"/memory/delete?memory_id={memory_id}")
        return DeleteMemoryResponse(**response_data)

    # GraphRAG Methods

    def extract_knowledge_graph(
        self,
        project_id: str,
        limit: int = 50,
        min_confidence: float = 0.5,
        auto_store: bool = True,
    ) -> Dict[str, Any]:
        """
        Extract knowledge graph from episodic memories.

        Args:
            project_id: Project identifier
            limit: Maximum number of memories to process
            min_confidence: Minimum confidence threshold for triples
            auto_store: Whether to automatically store extracted triples

        Returns:
            Dict containing extracted triples, entities, and statistics
        """
        request_body = {
            "project_id": project_id,
            "limit": limit,
            "min_confidence": min_confidence,
            "auto_store": auto_store,
        }
        return self._request("POST", "/v1/graph/extract", json=request_body)

    def query_graph(
        self,
        query: str,
        project_id: str,
        top_k_vector: int = 5,
        graph_depth: int = 2,
        traversal_strategy: str = "bfs",
    ) -> Dict[str, Any]:
        """
        Advanced hybrid search combining vector and graph traversal.

        Args:
            query: Search query
            project_id: Project identifier
            top_k_vector: Number of vector results
            graph_depth: Maximum graph traversal depth
            traversal_strategy: 'bfs' or 'dfs'

        Returns:
            Dict with vector_matches, graph_nodes, graph_edges, and synthesized_context
        """
        request_body = {
            "query": query,
            "project_id": project_id,
            "top_k_vector": top_k_vector,
            "graph_depth": graph_depth,
            "traversal_strategy": traversal_strategy,
        }
        return self._request("POST", "/v1/graph/query", json=request_body)

    def get_graph_stats(self, project_id: str) -> Dict[str, Any]:
        """
        Get knowledge graph statistics for a project.

        Args:
            project_id: Project identifier

        Returns:
            Dict with total_nodes, total_edges, unique_relations, and statistics
        """
        return self._request("GET", f"/v1/graph/stats?project_id={project_id}")

    def get_graph_nodes(
        self,
        project_id: str,
        limit: int = 100,
        use_pagerank: bool = False,
        min_pagerank_score: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve graph nodes with optional PageRank filtering.

        Args:
            project_id: Project identifier
            limit: Maximum nodes to return
            use_pagerank: Enable PageRank filtering
            min_pagerank_score: Minimum PageRank threshold

        Returns:
            List of node dictionaries
        """
        params = {
            "project_id": project_id,
            "limit": limit,
            "use_pagerank": use_pagerank,
            "min_pagerank_score": min_pagerank_score,
        }
        return self._request("GET", "/v1/graph/nodes", params=params)

    def get_graph_edges(
        self, project_id: str, limit: int = 100, relation: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve graph edges with optional relation filtering.

        Args:
            project_id: Project identifier
            limit: Maximum edges to return
            relation: Filter by relation type

        Returns:
            List of edge dictionaries
        """
        params = {"project_id": project_id, "limit": limit}
        if relation:
            params["relation"] = relation
        return self._request("GET", "/v1/graph/edges", params=params)

    def get_subgraph(
        self, project_id: str, node_ids: List[str], depth: int = 1
    ) -> Dict[str, Any]:
        """
        Retrieve a subgraph starting from specific nodes.

        Args:
            project_id: Project identifier
            node_ids: List of starting node IDs
            depth: Maximum traversal depth

        Returns:
            Dict with nodes, edges, and statistics
        """
        params = {
            "project_id": project_id,
            "node_ids": ",".join(node_ids),
            "depth": depth,
        }
        return self._request("GET", "/v1/graph/subgraph", params=params)

    # Agent Methods

    def execute_agent(
        self, tenant_id: str, project: str, prompt: str
    ) -> Dict[str, Any]:
        """
        Execute an AI agent task with full memory retrieval and context management.

        This orchestrates:
        1. Retrieval of cached semantic & reflective context
        2. Vector search for episodic memories
        3. Reranking of retrieved memories
        4. LLM inference with full context
        5. Automatic reflection generation
        6. Cost tracking

        Args:
            tenant_id: Tenant identifier
            project: Project identifier
            prompt: Agent task prompt

        Returns:
            Dict with answer, used_memories, and cost breakdown
        """
        request_body = {"tenant_id": tenant_id, "project": project, "prompt": prompt}
        return self._request("POST", "/v1/agent/execute", json=request_body)

    # Governance Methods

    def get_governance_overview(self, days: int = 30) -> Dict[str, Any]:
        """
        Get system-wide governance overview (admin only).

        Args:
            days: Number of days to analyze

        Returns:
            Dict with total costs, calls, tokens, and top tenants/models
        """
        return self._request("GET", f"/v1/governance/overview?days={days}")

    def get_tenant_governance(self, tenant_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive governance statistics for a tenant.

        Args:
            tenant_id: Tenant identifier
            days: Number of days to analyze

        Returns:
            Dict with costs, usage, cache stats, breakdowns by project/model/operation
        """
        return self._request("GET", f"/v1/governance/tenant/{tenant_id}?days={days}")

    def get_tenant_budget(self, tenant_id: str) -> Dict[str, Any]:
        """
        Get current budget status and projections for a tenant.

        Args:
            tenant_id: Tenant identifier

        Returns:
            Dict with budget limits, current usage, projections, and alerts
        """
        return self._request("GET", f"/v1/governance/tenant/{tenant_id}/budget")

    # Reflection Methods

    def rebuild_reflections(self, tenant_id: str, project: str) -> Dict[str, Any]:
        """
        Trigger background task to rebuild reflective memories.

        Args:
            tenant_id: Tenant identifier
            project: Project identifier

        Returns:
            Dict with confirmation message
        """
        request_body = {"tenant_id": tenant_id, "project": project}
        return self._request(
            "POST", "/v1/memory/rebuild-reflections", json=request_body
        )

    def get_reflection_stats(self, project: str) -> Dict[str, Any]:
        """
        Get statistics about reflective memories.

        Args:
            project: Project identifier

        Returns:
            Dict with reflective_memory_count and average_strength
        """
        return self._request("GET", f"/v1/memory/reflection-stats?project={project}")

    def generate_hierarchical_reflection(
        self, project: str, bucket_size: int = 10, max_episodes: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate hierarchical (map-reduce) reflection from episodes.

        Args:
            project: Project identifier
            bucket_size: Number of episodes per bucket
            max_episodes: Maximum episodes to process

        Returns:
            Dict with summary and statistics
        """
        params = {"project": project, "bucket_size": bucket_size}
        if max_episodes:
            params["max_episodes"] = max_episodes
        return self._request(
            "POST", "/v1/memory/reflection/hierarchical", params=params
        )

    # Health & Cache Methods

    def get_health(self) -> Dict[str, Any]:
        """Get comprehensive health check of all system components."""
        return self._request("GET", "/health")

    def rebuild_cache(self) -> Dict[str, Any]:
        """Trigger background task to rebuild context cache."""
        return self._request("POST", "/v1/cache/rebuild")

    # Async methods for non-blocking operations

    async def store_async(self, memory: StoreMemoryRequest) -> StoreMemoryResponse:
        """
        Asynchronously stores a new memory record.

        Args:
            memory: StoreMemoryRequest with memory data

        Returns:
            StoreMemoryResponse with ID and confirmation

        Example:
            ```python
            memory_request = StoreMemoryRequest(
                content="User logged in successfully",
                layer="episodic",
                tags=["auth", "login"]
            )
            response = await client.store_async(memory_request)
            ```
        """
        response_data = await self._async_request(
            "POST", "/memory/store", json=memory.dict(exclude_none=True)
        )
        return StoreMemoryResponse(**response_data)

    async def query_async(
        self, query_text: str, k: int = 10, filters: Optional[Dict[str, Any]] = None
    ) -> QueryMemoryResponse:
        """
        Asynchronously queries the memory for relevant records.

        Args:
            query_text: Search query
            k: Number of results to return
            filters: Optional filters

        Returns:
            QueryMemoryResponse with scored results
        """
        request_body = QueryMemoryRequest(query_text=query_text, k=k, filters=filters)
        response_data = await self._async_request(
            "POST", "/memory/query", json=request_body.dict(exclude_none=True)
        )
        return QueryMemoryResponse(**response_data)

    async def delete_async(self, memory_id: str) -> DeleteMemoryResponse:
        """
        Asynchronously deletes a memory record by its ID.

        Args:
            memory_id: ID of the memory to delete

        Returns:
            DeleteMemoryResponse with confirmation
        """
        response_data = await self._async_request(
            "DELETE", f"/memory/delete?memory_id={memory_id}"
        )
        return DeleteMemoryResponse(**response_data)

    # Async GraphRAG Methods

    async def extract_knowledge_graph_async(
        self,
        project_id: str,
        limit: int = 50,
        min_confidence: float = 0.5,
        auto_store: bool = True,
    ) -> Dict[str, Any]:
        """Async version of extract_knowledge_graph."""
        request_body = {
            "project_id": project_id,
            "limit": limit,
            "min_confidence": min_confidence,
            "auto_store": auto_store,
        }
        return await self._async_request("POST", "/v1/graph/extract", json=request_body)

    async def query_graph_async(
        self,
        query: str,
        project_id: str,
        top_k_vector: int = 5,
        graph_depth: int = 2,
        traversal_strategy: str = "bfs",
    ) -> Dict[str, Any]:
        """Async version of query_graph."""
        request_body = {
            "query": query,
            "project_id": project_id,
            "top_k_vector": top_k_vector,
            "graph_depth": graph_depth,
            "traversal_strategy": traversal_strategy,
        }
        return await self._async_request("POST", "/v1/graph/query", json=request_body)

    async def get_graph_stats_async(self, project_id: str) -> Dict[str, Any]:
        """Async version of get_graph_stats."""
        return await self._async_request(
            "GET", f"/v1/graph/stats?project_id={project_id}"
        )

    async def execute_agent_async(
        self, tenant_id: str, project: str, prompt: str
    ) -> Dict[str, Any]:
        """Async version of execute_agent."""
        request_body = {"tenant_id": tenant_id, "project": project, "prompt": prompt}
        return await self._async_request("POST", "/v1/agent/execute", json=request_body)

    async def close(self):
        """Close async HTTP client connections."""
        await self._async_http_client.aclose()

    def __del__(self):
        """Cleanup on deletion."""
        try:
            self._http_client.close()
        except Exception:
            pass


# Aliases for backward compatibility and documentation consistency
RAEClient = MemoryClient
AsyncRAEClient = MemoryClient  # Same class, supports both sync and async methods
