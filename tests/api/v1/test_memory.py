import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from apps.memory_api.main import app
from apps.memory_api.models import ScoredMemoryRecord
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def mock_vector_store():
    with patch("apps.memory_api.api.v1.memory.get_vector_store") as mock:
        instance = AsyncMock()
        instance.upsert = AsyncMock()
        instance.query = AsyncMock(return_value=[])
        instance.delete = AsyncMock()
        
        mock.return_value = instance
        yield instance

@pytest.fixture
def mock_embedding_service():
    with patch("apps.memory_api.api.v1.memory.get_embedding_service") as mock:
        instance = MagicMock()
        instance.generate_embeddings.return_value = [[0.1] * 384]
        mock.return_value = instance
        yield instance

@pytest.mark.asyncio
async def test_store_memory_success(mock_app_state_pool, mock_vector_store, mock_embedding_service):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    
    mock_conn.fetchrow.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "created_at": datetime.now(),
        "last_accessed_at": datetime.now(),
        "usage_count": 0
    }

    # POPRAWKA: Dodano 'importance', aby uniknąć błędu walidacji w API
    payload = {
        "content": "Test content",
        "source": "cli",
        "layer": "ltm",
        "tags": ["test"],
        "project": "default",
        "importance": 0.5 
    }
    
    response = client.post(
        "/v1/memory/store", 
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )
    
    if response.status_code != 200:
        print("STORE ERROR:", response.json())

    assert response.status_code == 200
    assert response.json()["id"] == "123e4567-e89b-12d3-a456-426614174000"

@pytest.mark.asyncio
async def test_query_memory_success(mock_app_state_pool, mock_vector_store, mock_embedding_service):
    record = ScoredMemoryRecord(
        id="mem-1",
        content="Found",
        score=0.95,
        importance=0.5,
        layer="ltm",
        tags=[],
        source="src",
        project="proj",
        timestamp=datetime.now(),
        last_accessed_at=datetime.now(),
        usage_count=10
    )

    mock_vector_store.query.return_value = [record]

    payload = {"query_text": "test query", "k": 1}

    response = client.post(
        "/v1/memory/query",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1

@pytest.mark.asyncio
async def test_delete_memory_success(mock_app_state_pool, mock_vector_store):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.execute.return_value = "DELETE 1"

    response = client.delete(
        "/v1/memory/delete?memory_id=mem-1",
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200