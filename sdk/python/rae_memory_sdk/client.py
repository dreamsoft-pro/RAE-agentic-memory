import httpx
from typing import Optional, List, Dict, Any
from pydantic_settings import BaseSettings
import structlog

from .models import (
    StoreMemoryRequest,
    StoreMemoryResponse,
    QueryMemoryRequest,
    QueryMemoryResponse,
    DeleteMemoryResponse,
    MemoryRecord,
    ScoredMemoryRecord,
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
        config: Optional[RAEClientConfig] = None
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
            response = self._http_client.request(method, url, headers=self._headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                "http_error",
                url=url,
                status_code=e.response.status_code,
                response_text=e.response.text
            )
            raise
        except httpx.RequestError as e:
            logger.error("request_error", url=url, error=str(e))
            raise

    async def _async_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Asynchronous HTTP request wrapper."""
        try:
            response = await self._async_http_client.request(method, url, headers=self._headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                "async_http_error",
                url=url,
                status_code=e.response.status_code,
                response_text=e.response.text
            )
            raise
        except httpx.RequestError as e:
            logger.error("async_request_error", url=url, error=str(e))
            raise

    def store(self, memory: StoreMemoryRequest) -> StoreMemoryResponse:
        """
        Stores a new memory record.
        """
        response_data = self._request("POST", "/memory/store", json=memory.dict(exclude_none=True))
        return StoreMemoryResponse(**response_data)

    def query(self, query_text: str, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> QueryMemoryResponse:
        """
        Queries the memory for relevant records.
        """
        request_body = QueryMemoryRequest(query_text=query_text, k=k, filters=filters)
        response_data = self._request("POST", "/memory/query", json=request_body.dict(exclude_none=True))
        return QueryMemoryResponse(**response_data)

    def delete(self, memory_id: str) -> DeleteMemoryResponse:
        """
        Deletes a memory record by its ID.
        """
        response_data = self._request("DELETE", f"/memory/delete?memory_id={memory_id}")
        return DeleteMemoryResponse(**response_data)

    def evaluate(self) -> Dict[str, Any]:
        """
        (Stub) Evaluates memory performance.
        """
        print("Evaluate endpoint is a stub.")
        return self._request("POST", "/memory/evaluate")

    def reflect(self) -> Dict[str, Any]:
        """
        (Stub) Triggers memory reflection.
        """
        print("Reflect endpoint is a stub.")
        return self._request("POST", "/memory/reflect")

    def get_tags(self) -> Dict[str, Any]:
        """
        (Stub) Retrieves all available tags.
        """
        print("Get tags endpoint is a stub.")
        return self._request("GET", "/memory/tags")

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
            "POST",
            "/memory/store",
            json=memory.dict(exclude_none=True)
        )
        return StoreMemoryResponse(**response_data)

    async def query_async(
        self,
        query_text: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
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
            "POST",
            "/memory/query",
            json=request_body.dict(exclude_none=True)
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
            "DELETE",
            f"/memory/delete?memory_id={memory_id}"
        )
        return DeleteMemoryResponse(**response_data)

    async def close(self):
        """Close async HTTP client connections."""
        await self._async_http_client.aclose()

    def __del__(self):
        """Cleanup on deletion."""
        try:
            self._http_client.close()
        except Exception:
            pass
