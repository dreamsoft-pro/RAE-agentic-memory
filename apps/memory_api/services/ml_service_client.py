"""
ML Service Client - HTTP client for communicating with the ML microservice.

This client provides a clean interface for the main API to call
ML operations without tight coupling.
"""

from typing import List, Dict, Any
import httpx
import structlog
from apps.memory_api.config import settings

logger = structlog.get_logger(__name__)


class MLServiceClient:
    """
    Client for communicating with the ML microservice.

    Handles entity resolution, NLP processing, and other ML operations
    that have been offloaded to a separate service.
    """

    def __init__(self, base_url: str = None):
        """
        Initialize ML service client.

        Args:
            base_url: Base URL of the ML service (default: from settings)
        """
        self.base_url = base_url or getattr(settings, 'ML_SERVICE_URL', 'http://ml-service:8001')
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)
        logger.info("ml_service_client_initialized", base_url=self.base_url)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def resolve_entities(
        self,
        nodes: List[Dict[str, Any]],
        similarity_threshold: float = 0.85
    ) -> Dict[str, Any]:
        """
        Call ML service to resolve duplicate entities.

        Args:
            nodes: List of node dictionaries to resolve
            similarity_threshold: Threshold for considering nodes similar

        Returns:
            Dict containing merge_groups and statistics

        Raises:
            httpx.HTTPError: If ML service call fails
        """
        logger.info(
            "calling_ml_service_resolve_entities",
            node_count=len(nodes),
            threshold=similarity_threshold
        )

        try:
            response = await self.client.post(
                "/resolve-entities",
                json={
                    "nodes": nodes,
                    "similarity_threshold": similarity_threshold
                }
            )
            response.raise_for_status()

            result = response.json()

            logger.info(
                "ml_service_resolve_entities_completed",
                groups_found=len(result.get("merge_groups", []))
            )

            return result

        except httpx.HTTPError as e:
            logger.exception(
                "ml_service_resolve_entities_failed",
                error=str(e)
            )
            raise

    async def extract_triples(
        self,
        text: str,
        language: str = "en"
    ) -> List[Dict[str, str]]:
        """
        Call ML service to extract knowledge triples from text.

        Args:
            text: Text to extract triples from
            language: Language code (default: "en")

        Returns:
            List of triple dictionaries

        Raises:
            httpx.HTTPError: If ML service call fails
        """
        logger.info(
            "calling_ml_service_extract_triples",
            text_length=len(text),
            language=language
        )

        try:
            response = await self.client.post(
                "/extract-triples",
                json={
                    "text": text,
                    "language": language
                }
            )
            response.raise_for_status()

            result = response.json()
            triples = result.get("triples", [])

            logger.info(
                "ml_service_extract_triples_completed",
                triples_found=len(triples)
            )

            return triples

        except httpx.HTTPError as e:
            logger.exception(
                "ml_service_extract_triples_failed",
                error=str(e)
            )
            raise

    async def health_check(self) -> bool:
        """
        Check if ML service is healthy.

        Returns:
            True if service is healthy, False otherwise
        """
        try:
            response = await self.client.get("/health")
            return response.status_code == 200
        except Exception as e:
            logger.warning("ml_service_health_check_failed", error=str(e))
            return False
