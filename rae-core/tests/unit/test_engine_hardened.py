"""Hardened unit tests for RAEEngine core logic (Szubar, Resonance, Failbacks)."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4, UUID
import numpy as np
from rae_core.engine import RAEEngine
from rae_core.math.types import MathLevel

class TestEngineHardened:
    @pytest.fixture
    def mock_storage(self):
        storage = MagicMock()
        storage.get_memory = AsyncMock()
        storage.get_memories_batch = AsyncMock()
        storage.get_neighbors_batch = AsyncMock()
        storage.store_memory = AsyncMock(return_value=uuid4())
        return storage

    @pytest.fixture
    def mock_vector_store(self):
        vs = MagicMock()
        vs.search_similar = AsyncMock()
        vs.store_vector = AsyncMock(return_value=True)
        return vs

    @pytest.fixture
    def mock_embedding_provider(self):
        ep = MagicMock()
        ep.embed_text = AsyncMock(return_value=[0.1]*384)
        ep.generate_all_embeddings = AsyncMock(return_value={"default": [[0.1]*384]})
        return ep

    @pytest.fixture
    def engine(self, mock_storage, mock_vector_store, mock_embedding_provider):
        engine = RAEEngine(
            memory_storage=mock_storage,
            vector_store=mock_vector_store,
            embedding_provider=mock_embedding_provider
        )
        # Configure search engine mock with Quantum methods
        engine.search_engine = MagicMock()
        engine.search_engine.search = AsyncMock(return_value=[])
        engine.search_engine._unpack_candidate_with_audit = MagicMock(
            side_effect=lambda x: (x[0], x[1], x[2] if len(x) > 2 else 0.5, x[3] if len(x) > 3 else {})
        )
        return engine

    @pytest.mark.asyncio
    async def test_search_memories_szubar_induction(self, engine, mock_storage):
        """Test that Szubar induction recruits neighbors when score is low."""
        id1 = uuid4()
        id2 = uuid4()
        
        # 1. Mock search results
        engine.search_engine.search.return_value = [(id1, 0.5, 0.8, {})]
        mock_storage.get_memory.return_value = {"id": id1, "content": "A", "metadata": {}}
        
        # 2. Mock neighbors from storage
        mock_storage.get_neighbors_batch.return_value = {str(id1): [(id2, "related")]}
        mock_storage.get_memories_batch.return_value = [{"id": id2, "content": "B", "metadata": {}}]
        
        # 3. Patch Resonance Engine to accept current tuple format or mock it entirely
        # RAEEngine converts storage format to (u, v, weight) internally
        with patch.object(engine.resonance_engine, "compute_resonance") as mock_res:
            mock_res.return_value = ([{"id": id1}, {"id": id2}], {str(id1): 1.0, str(id2): 0.8})
            results = await engine.search_memories("test", "t1")
            
        assert len(results) >= 2

    @pytest.mark.asyncio
    async def test_search_memories_resonance_boost(self, engine, mock_storage):
        """Test that semantic resonance induces missing high-energy nodes."""
        id1 = uuid4()
        id2 = uuid4()
        
        engine.search_engine.search.return_value = [(id1, 0.9, 0.5, {})]
        mock_storage.get_memory.return_value = {"id": id1, "content": "A", "metadata": {}}
        mock_storage.get_neighbors_batch.return_value = {str(id1): [(id2, "strong")]}
        
        with patch.object(engine.resonance_engine, "compute_resonance") as mock_res:
            mock_res.return_value = ([{"id": id1}, {"id": id2}], {str(id1): 1.0, str(id2): 0.9})
            results = await engine.search_memories("test", "t1")
            
        assert len(results) >= 2

    @pytest.mark.asyncio
    async def test_generate_text_fallback(self, engine):
        """Test text generation fails gracefully if provider missing."""
        engine.llm_provider = None
        with pytest.raises(RuntimeError, match="LLM provider not configured"):
            await engine.generate_text("hi")

    @pytest.mark.asyncio
    async def test_store_memory_logic_flow(self, engine, mock_storage):
        """Test the logic flow of store_memory including ingest pipeline."""
        engine.cache_provider = AsyncMock()
        engine.cache_provider.get.return_value = None
        
        await engine.store_memory(content="Unique", tenant_id="t1")
        
        assert mock_storage.store_memory.called
        assert engine.cache_provider.set.called
