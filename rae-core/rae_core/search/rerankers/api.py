"""API Reranker implementation."""

from typing import Any
from uuid import UUID

import httpx
import structlog

from rae_core.interfaces.reranking import IReranker

logger = structlog.get_logger(__name__)


class APIReranker(IReranker):
    """Reranker that delegates to an external HTTP API (e.g. Cohere, BGE)."""

    def __init__(self, api_url: str, api_key: str | None = None):
        self.api_url = api_url
        self.api_key = api_key

    async def rerank(
        self,
        query: str,
        candidates: list[tuple[UUID, float]],
        tenant_id: str,
        limit: int = 10,
        **kwargs: Any,
    ) -> list[tuple[UUID, float]]:
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.api_url,
                    json={
                        "query": query,
                        "candidates": [
                            {"id": str(c[0]), "score": c[1]} for c in candidates
                        ],
                        "tenant_id": tenant_id,
                        "limit": limit,
                    },
                    headers=headers,
                )
                response.raise_for_status()
                data = response.json()

                reranked_data = data.get("results", [])
                reranked: list[tuple[UUID, float]] = []
                for item in reranked_data:
                    reranked.append((UUID(item["id"]), float(item["score"])))

                return reranked
        except Exception as e:
            logger.error("api_rerank_failed", error=str(e))
            return candidates[:limit]
