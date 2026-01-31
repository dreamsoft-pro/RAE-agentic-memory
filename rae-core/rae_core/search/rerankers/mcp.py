"""MCP Reranker implementation."""

from typing import Any
from uuid import UUID

import structlog

from rae_core.interfaces.reranking import IReranker

logger = structlog.get_logger(__name__)


class MCPreranker(IReranker):
    """Reranker that delegates to an MCP Tool."""

    def __init__(self, client: Any, tool_name: str = "rerank_memories"):
        self.client = client
        self.tool_name = tool_name

    async def rerank(
        self,
        query: str,
        candidates: list[tuple[UUID, float]],
        tenant_id: str,
        limit: int = 10,
        **kwargs: Any,
    ) -> list[tuple[UUID, float]]:
        if not self.client:
            logger.warning("mcp_client_not_available_for_reranking")
            return candidates[:limit]

        try:
            # Convert UUIDs to strings for JSON-RPC
            m_ids = [str(c[0]) for c in candidates]
            scores = [float(c[1]) for c in candidates]

            result = await self.client.call_tool(
                self.tool_name,
                {
                    "query": query,
                    "memory_ids": m_ids,
                    "scores": scores,
                    "tenant_id": tenant_id,
                    "limit": limit,
                },
            )

            # Expecting list of {"id": str, "score": float}
            reranked_data = result.get("results", [])
            reranked: list[tuple[UUID, float]] = []
            for item in reranked_data:
                reranked.append((UUID(item["id"]), float(item["score"])))

            return reranked
        except Exception as e:
            logger.error("mcp_rerank_failed", error=str(e))
            return candidates[:limit]
