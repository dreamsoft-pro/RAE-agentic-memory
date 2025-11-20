import sys
import os
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from apps.memory_api.main import app
from apps.memory_api.dependencies import get_api_key
from apps.memory_api.security import auth

sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(autouse=True)
def mock_env_and_settings(monkeypatch):
    envs = {
        "POSTGRES_HOST": "localhost",
        "POSTGRES_DB": "test_db",
        "POSTGRES_USER": "test_user",
        "POSTGRES_PASSWORD": "test_pass",
        "QDRANT_HOST": "localhost",
        "REDIS_URL": "redis://localhost:6379/0",
        "RAE_LLM_BACKEND": "openai",
        "OPENAI_API_KEY": "sk-test-key",
        "API_KEY": "test-api-key", 
        "OAUTH_ENABLED": "False"
    }
    for k, v in envs.items():
        monkeypatch.setenv(k, v)

    with patch("apps.memory_api.config.settings") as mock_settings:
        mock_settings.API_KEY = "test-api-key"
        mock_settings.POSTGRES_HOST = "localhost"
        mock_settings.POSTGRES_DB = "test"
        mock_settings.POSTGRES_USER = "user"
        mock_settings.POSTGRES_PASSWORD = "pass"
        mock_settings.QDRANT_HOST = "localhost"
        mock_settings.RERANKER_API_URL = "http://reranker"
        mock_settings.MEMORY_API_URL = "http://memory"
        mock_settings.RAE_LLM_MODEL_DEFAULT = "gpt-4"
        yield mock_settings

@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_api_key] = lambda: "test-api-key"
    app.dependency_overrides[auth.verify_token] = lambda: {"sub": "test-user", "scope": "admin"}
    yield
    app.dependency_overrides = {}

@pytest.fixture
def mock_app_state_pool():
    mock_pool = MagicMock()
    mock_pool.fetch = AsyncMock()
    mock_pool.fetchrow = AsyncMock()
    mock_pool.execute = AsyncMock()
    mock_pool.close = AsyncMock()

    mock_conn = MagicMock()
    mock_conn.fetchrow = AsyncMock()
    mock_conn.fetch = AsyncMock()
    mock_conn.fetchval = AsyncMock()
    mock_conn.execute = AsyncMock()

    mock_transaction_cm = AsyncMock()
    mock_transaction_cm.__aenter__.return_value = None
    mock_transaction_cm.__aexit__.return_value = None
    mock_conn.transaction.return_value = mock_transaction_cm

    mock_acquire_cm = AsyncMock()
    mock_acquire_cm.__aenter__.return_value = mock_conn
    mock_acquire_cm.__aexit__.return_value = None
    
    mock_pool.acquire.return_value = mock_acquire_cm
    
    app.state.pool = mock_pool
    yield mock_pool
    del app.state.pool