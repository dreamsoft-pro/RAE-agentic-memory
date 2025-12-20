import pytest
from unittest.mock import AsyncMock, MagicMock

from apps.memory_api.adapters.redis_adapter import RedisAdapter
from apps.memory_api.adapters.qdrant_adapter import QdrantAdapter
from apps.memory_api.core.contract import (
    MemoryContract, 
    CacheContract, 
    VectorStoreContract, 
    VectorCollectionContract
)

# --- Redis Adapter Tests ---

@pytest.mark.asyncio
async def test_redis_validation_success():
    mock_redis = AsyncMock()
    mock_redis.ping.return_value = True
    # Mock set/get
    mock_redis.set.return_value = True
    mock_redis.get.return_value = "1"

    contract = MemoryContract(
        version="1.0", 
        entities=[], 
        cache=CacheContract(required_namespaces=["rae:"])
    )

    adapter = RedisAdapter(mock_redis)
    result = await adapter.validate(contract)

    assert result.valid is True
    mock_redis.ping.assert_called_once()
    mock_redis.set.assert_called()
    mock_redis.get.assert_called()

@pytest.mark.asyncio
async def test_redis_validation_connection_fail():
    mock_redis = AsyncMock()
    mock_redis.ping.return_value = False # Ping fail

    contract = MemoryContract(
        version="1.0", 
        entities=[], 
        cache=CacheContract(required_namespaces=["rae:"])
    )

    adapter = RedisAdapter(mock_redis)
    result = await adapter.validate(contract)

    assert result.valid is False
    assert result.violations[0].issue_type == "CONNECTION_FAILED"

@pytest.mark.asyncio
async def test_redis_validation_write_fail():
    mock_redis = AsyncMock()
    mock_redis.ping.return_value = True
    mock_redis.set.return_value = True
    mock_redis.get.return_value = "0" # Incorrect value

    contract = MemoryContract(
        version="1.0", 
        entities=[], 
        cache=CacheContract(required_namespaces=["rae:"])
    )

    adapter = RedisAdapter(mock_redis)
    result = await adapter.validate(contract)

    assert result.valid is False
    assert result.violations[0].issue_type == "WRITE_FAILED"


# --- Qdrant Adapter Tests ---

@pytest.mark.asyncio
async def test_qdrant_validation_success():
    mock_qdrant = AsyncMock()
    
    # Mock collections list
    col_mock = MagicMock()
    col_mock.name = "memories"
    
    collections_resp = MagicMock()
    collections_resp.collections = [col_mock]
    mock_qdrant.get_collections.return_value = collections_resp

    # Mock collection config
    col_info = MagicMock()
    # config.params.vectors can be dict or object
    # Let's mock single vector object style for simplicity or what adapter expects
    vector_params = MagicMock()
    vector_params.size = 384
    vector_params.distance = "Cosine"
    
    col_info.config.params.vectors = vector_params
    
    mock_qdrant.get_collection.return_value = col_info

    contract = MemoryContract(
        version="1.0", 
        entities=[],
        vector_store=VectorStoreContract(
            collections=[
                VectorCollectionContract(name="memories", vector_size=384, distance_metric="Cosine")
            ]
        )
    )

    adapter = QdrantAdapter(mock_qdrant)
    result = await adapter.validate(contract)

    assert result.valid is True

@pytest.mark.asyncio
async def test_qdrant_validation_missing_collection():
    mock_qdrant = AsyncMock()
    collections_resp = MagicMock()
    collections_resp.collections = [] # Empty
    mock_qdrant.get_collections.return_value = collections_resp

    contract = MemoryContract(
        version="1.0", 
        entities=[],
        vector_store=VectorStoreContract(
            collections=[VectorCollectionContract(name="memories", vector_size=384)]
        )
    )

    adapter = QdrantAdapter(mock_qdrant)
    result = await adapter.validate(contract)

    assert result.valid is False
    assert result.violations[0].issue_type == "MISSING_COLLECTION"

@pytest.mark.asyncio
async def test_qdrant_validation_dimension_mismatch():
    mock_qdrant = AsyncMock()
    
    col_mock = MagicMock()
    col_mock.name = "memories"
    collections_resp = MagicMock()
    collections_resp.collections = [col_mock]
    mock_qdrant.get_collections.return_value = collections_resp

    # Mock collection with wrong size
    col_info = MagicMock()
    vector_params = MagicMock()
    vector_params.size = 768 # Wrong size
    vector_params.distance = "Cosine"
    col_info.config.params.vectors = vector_params
    mock_qdrant.get_collection.return_value = col_info

    contract = MemoryContract(
        version="1.0", 
        entities=[],
        vector_store=VectorStoreContract(
            collections=[VectorCollectionContract(name="memories", vector_size=384)]
        )
    )

    adapter = QdrantAdapter(mock_qdrant)
    result = await adapter.validate(contract)

    assert result.valid is False
    assert result.violations[0].issue_type == "DIMENSION_MISMATCH"
