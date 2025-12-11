import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime, timedelta, timezone

from rae_core.layers.sensory import SensoryLayer
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.models.memory import MemoryItem, MemoryLayer

@pytest.fixture
def mock_storage():
    storage = Mock(spec=IMemoryStorage)
    storage.store_memory = AsyncMock()
    storage.get_memory = AsyncMock()
    storage.delete_memory = AsyncMock()
    storage.count_memories = AsyncMock(return_value=0)
    storage.delete_expired_memories = AsyncMock(return_value=0)
    storage.update_memory_expiration = AsyncMock(return_value=True)
    return storage

@pytest.fixture
def sensory_layer(mock_storage):
    return SensoryLayer(
        storage=mock_storage,
        tenant_id="tenant_1",
        agent_id="agent_1",
        default_ttl_seconds=60,
        max_capacity=100
    )

@pytest.mark.asyncio
async def test_add_memory_with_ttl(sensory_layer, mock_storage):
    expected_id = uuid4()
    mock_storage.store_memory.return_value = expected_id
    
    mem_id = await sensory_layer.add_memory("test content", ttl_seconds=30)
    
    assert mem_id == expected_id
    
    # Check arguments
    call_kwargs = mock_storage.store_memory.call_args.kwargs
    assert call_kwargs["content"] == "test content"
    assert call_kwargs["layer"] == "sensory"
    assert call_kwargs["expires_at"] is not None
    
    # Check if expires_at is roughly 30s from now
    expires_at = call_kwargs["expires_at"]
    now = datetime.now(timezone.utc)
    diff = (expires_at - now).total_seconds()
    assert 28 < diff < 32

@pytest.mark.asyncio
async def test_get_memory_active(sensory_layer, mock_storage):
    mem_id = uuid4()
    now = datetime.now(timezone.utc)
    future = now + timedelta(seconds=100)
    
    # Mock active memory
    mock_storage.get_memory.return_value = {
        "id": mem_id,
        "content": "active",
        "layer": "sensory",
        "tenant_id": "t",
        "agent_id": "a",
        "expires_at": future,
        "created_at": now,
        "last_accessed_at": now
    }
    
    item = await sensory_layer.get_memory(mem_id)
    assert item is not None
    assert item.content == "active"
    mock_storage.delete_memory.assert_not_called()

@pytest.mark.asyncio
async def test_get_memory_expired(sensory_layer, mock_storage):
    mem_id = uuid4()
    now = datetime.now(timezone.utc)
    past = now - timedelta(seconds=100)
    
    # Mock expired memory
    mock_storage.get_memory.return_value = {
        "id": mem_id,
        "content": "expired",
        "layer": "sensory",
        "tenant_id": "t",
        "agent_id": "a",
        "expires_at": past,
        "created_at": past,
        "last_accessed_at": past
    }
    
    item = await sensory_layer.get_memory(mem_id)
    
    # Should be None and triggered deletion
    assert item is None
    mock_storage.delete_memory.assert_called_once_with(
        memory_id=mem_id,
        tenant_id="tenant_1"
    )

@pytest.mark.asyncio
async def test_cleanup_trigger(sensory_layer, mock_storage):
    # Setup capacity overflow
    mock_storage.count_memories.return_value = 101 # max is 100
    mock_storage.store_memory.return_value = uuid4()
    
    await sensory_layer.add_memory("overflow")
    
    mock_storage.delete_expired_memories.assert_called_once()

@pytest.mark.asyncio
async def test_extend_ttl(sensory_layer, mock_storage):
    mem_id = uuid4()
    now = datetime.now(timezone.utc)
    expires = now + timedelta(seconds=10)
    
    mock_storage.get_memory.return_value = {
        "id": mem_id,
        "content": "test",
        "layer": "sensory",
        "tenant_id": "t",
        "agent_id": "a",
        "expires_at": expires,
        "created_at": now,
        "last_accessed_at": now
    }
    
    await sensory_layer.extend_ttl(mem_id, 60)
    
    mock_storage.update_memory_expiration.assert_called_once()
    args = mock_storage.update_memory_expiration.call_args.kwargs
    new_expires = args["expires_at"]
    
    # Should be old expires + 60s
    assert (new_expires - expires).total_seconds() == 60.0
