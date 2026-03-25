🧠 RAE_Architecture_Refactoring_Plan
RAE-core + RAE-Local-Memory
Wersja: 1.0
Data: 2025-12-08
Autor: Plan przygotowany dla projektu RAE-agentic-memory

📋 Spis treści

Analiza obecnego stanu RAE
Cel: Wydzielenie RAE-core
Cel: RAE-Local-Memory (wtyczka przeglądarkowa)
Propozycja architektury RAE-core
Propozycja architektury RAE-Local-Memory
Plan refaktoryzacji w krokach
Szczegółowe mapowanie plików
Abstrakcje storage
Harmonogram i kolejność prac


1. Analiza obecnego stanu RAE
1.1 Obecna struktura katalogów (z README)
RAE-agentic-memory/
├── apps/
│   ├── memory_api/          # 🎯 Główna logika - TUTAJ JEST CORE
│   │   ├── core/            # ⭐ Logika matematyczna, warstwy pamięci
│   │   ├── services/        # ⭐ HybridSearch, Reflection, ContextBuilder
│   │   ├── repositories/    # ⭐ DAO pattern - abstrakcje dostępu
│   │   ├── models/          # ⭐ Pydantic modele danych
│   │   ├── routers/         # ❌ FastAPI endpoints (nie do core)
│   │   ├── tasks/           # Celery workers
│   │   └── tests/
│   ├── ml_service/          # Oddzielny mikroserwis ML
│   ├── reranker-service/    # Oddzielny mikroserwis
│   └── llm/                 # LLM Orchestrator
├── sdk/python/rae_memory_sdk/  # SDK klienckie
├── integrations/
│   ├── mcp/                 # Model Context Protocol
│   ├── context-watcher/     # File watcher
│   ├── ollama-wrapper/      # Local LLM
│   ├── langchain/           # LangChain adapter
│   └── llama_index/         # LlamaIndex adapter
├── infra/                   # Docker, Prometheus, Grafana
├── tools/
│   └── memory-dashboard/    # Streamlit dashboard
├── docs/
├── tests/
├── benchmarking/
├── config/
├── migrations/
├── alembic/
├── docker compose.yml
├── docker compose.lite.yml  # ⚠️ Już istnieje RAE Lite!
└── docker compose.dev.yml
1.2 Architektura pamięci (4 warstwy)
WarstwaNazwaOpisTyp w APILayer 1SensoryRaw inputs, immediate observationslayer=stm, memory_type=sensoryLayer 2WorkingActive task context, reflectionslayer=stm/em, memory_type=episodicLayer 3Long-TermEpisodic + Semantic + Profileslayer=ltm/em, memory_type=episodic/semantic/profileLayer 4ReflectiveMeta-learnings, strategieslayer=rm, memory_type=reflection/strategy
1.3 Architektura matematyczna (3 warstwy)
WarstwaNazwaFunkcjaMetrykiMath-1StructureGeometria pamięciGraph Connectivity, Semantic Coherence, EntropyMath-2DynamicsEwolucja pamięciMemory Drift Index, Retention Curve, Compression FidelityMath-3PolicyDecyzjeCost-Quality Frontier, Optimal Retrieval Ratio
1.4 Hybrid Search (4 strategie)

Vector Search (Qdrant) - dense embeddings
Graph Traversal (PostgreSQL) - BFS/DFS po grafie wiedzy
Sparse Vectors (BM25-style) - keyword matching
Full-Text Search (PostgreSQL FTS) - exact phrases

1.5 Storage Layer
KomponentTechnologiaFunkcjaRelational DBPostgreSQLMetadane, graf wiedzy, FTS, RLSVector DBQdrant / pgvectorDense embeddings, sparse vectorsCacheRedisQuery cache, Celery queue
1.6 Istniejące RAE Lite
RAE już ma docker compose.lite.yml który zawiera:

Core API
PostgreSQL
Qdrant
Redis

Różnica wobec RAE-Local-Memory:

RAE Lite = mniejszy Docker stack
RAE-Local-Memory = kompilowany do exe, SQLite, wtyczka przeglądarkowa


2. Cel: Wydzielenie RAE-core
2.1 Co trafia do RAE-core
rae_core/
├── __init__.py
├── py.typed                    # PEP 561 type hints
├── version.py
│
├── models/                     # 📦 Modele danych (Pydantic)
│   ├── __init__.py
│   ├── memory.py              # MemoryItem, Episode, MemoryLayer
│   ├── graph.py               # GraphNode, GraphEdge, KnowledgeGraph
│   ├── reflection.py          # Reflection, ReflectionPolicy
│   ├── search.py              # SearchQuery, SearchResult, SearchStrategy
│   ├── context.py             # WorkingContext, ContextWindow
│   └── scoring.py             # ScoringWeights, QualityMetrics
│
├── layers/                     # 🧠 4-warstwowa architektura pamięci
│   ├── __init__.py
│   ├── base.py                # AbstractMemoryLayer interface
│   ├── sensory.py             # Layer 1: Sensory Memory
│   ├── working.py             # Layer 2: Working Memory
│   ├── longterm.py            # Layer 3: Long-Term (Episodic + Semantic)
│   └── reflective.py          # Layer 4: Reflective Memory
│
├── math/                       # 🔢 3-warstwowa matematyka
│   ├── __init__.py
│   ├── base.py                # MathLayerController interface
│   ├── math1_structure.py     # Math-1: Structure Analysis
│   ├── math2_dynamics.py      # Math-2: Dynamics Tracking
│   ├── math3_policy.py        # Math-3: Policy Optimization
│   └── metrics.py             # GraphConnectivity, DriftIndex, etc.
│
├── search/                     # 🔍 Hybrid Search Engine
│   ├── __init__.py
│   ├── base.py                # AbstractSearchStrategy interface
│   ├── hybrid.py              # HybridSearchEngine (orchestrator)
│   ├── vector.py              # VectorSearchStrategy
│   ├── graph.py               # GraphTraversalStrategy
│   ├── sparse.py              # SparseVectorStrategy (BM25)
│   ├── fulltext.py            # FullTextSearchStrategy
│   ├── query_analyzer.py      # Query intent classification
│   └── fusion.py              # Result fusion and ranking
│
├── reflection/                 # 🎭 Reflection Engine V2
│   ├── __init__.py
│   ├── engine.py              # ReflectionEngineV2
│   ├── actor.py               # Actor component
│   ├── evaluator.py           # Evaluator component
│   └── reflector.py           # Reflector component
│
├── context/                    # 📝 Context Building
│   ├── __init__.py
│   ├── builder.py             # ContextBuilder
│   └── window.py              # ContextWindow management
│
├── scoring/                    # 📊 Memory Scoring
│   ├── __init__.py
│   ├── scorer.py              # MemoryScoringV2
│   └── decay.py               # ImportanceDecay logic
│
├── interfaces/                 # 🔌 Abstrakcyjne interfejsy (dla DI)
│   ├── __init__.py
│   ├── storage.py             # IMemoryStorage, IVectorStore, IGraphStore
│   ├── llm.py                 # ILLMProvider interface
│   ├── embedding.py           # IEmbeddingProvider interface
│   └── cache.py               # ICacheProvider interface
│
├── llm/                        # 🤖 LLM Orchestrator (abstrakcja)
│   ├── __init__.py
│   ├── orchestrator.py        # LLMOrchestrator (bez konkretnych providerów)
│   ├── strategies.py          # Single, Fallback, Ensemble strategies
│   └── config.py              # LLMConfig models
│
├── config/                     # ⚙️ Konfiguracja
│   ├── __init__.py
│   ├── settings.py            # RAESettings (pydantic-settings)
│   └── defaults.py            # Default values
│
├── exceptions/                 # ❌ Wyjątki
│   ├── __init__.py
│   └── errors.py              # RAEError, MemoryNotFound, etc.
│
└── utils/                      # 🛠️ Utilities
    ├── __init__.py
    ├── hashing.py             # Content hashing
    ├── temporal.py            # Timestamp utilities
    └── validation.py          # Input validation
2.2 Co zostaje w "Dużym RAE"
RAE-agentic-memory/
├── apps/
│   ├── memory_api/
│   │   ├── routers/           # FastAPI endpoints
│   │   ├── middleware/        # Auth, CORS, rate limiting
│   │   ├── dependencies/      # FastAPI DI
│   │   ├── adapters/          # 🔌 Konkretne implementacje
│   │   │   ├── storage/
│   │   │   │   ├── postgres.py    # PostgresMemoryStorage
│   │   │   │   ├── qdrant.py      # QdrantVectorStore
│   │   │   │   └── redis.py       # RedisCacheProvider
│   │   │   ├── llm/
│   │   │   │   ├── openai.py      # OpenAI provider
│   │   │   │   ├── anthropic.py   # Anthropic provider
│   │   │   │   ├── ollama.py      # Ollama provider
│   │   │   │   └── ...
│   │   │   └── embedding/
│   │   │       ├── openai.py
│   │   │       └── sentence_transformers.py
│   │   ├── tasks/             # Celery workers
│   │   └── main.py            # FastAPI app
│   ├── ml_service/
│   └── reranker-service/
├── infra/                     # Docker infrastructure
├── integrations/              # MCP, LangChain, etc.
└── tools/                     # Dashboard, CLI
2.3 Zasady wydzielenia
ZasadaOpisZero zależności infraRAE-core nie importuje: FastAPI, SQLAlchemy, psycopg2, qdrant-client, redisPure Python + PydanticTylko: pydantic, numpy, typing-extensionsInterfejsy zamiast implementacjiAbstrakcyjne klasy bazowe, DI przez konstruktoryBehavior-preservingNie zmieniamy logiki, tylko strukturęTestowalne w izolacjiUnit testy bez żadnej infrastruktury

3. Cel: RAE-Local-Memory
3.1 Wizja produktu
RAE-Local-Memory to:

🌐 Wtyczka przeglądarkowa (Chrome, Firefox, Edge)
💾 SQLite jako storage (local-first)
📦 Kompilowana do .exe (PyInstaller/Nuitka)
🔒 Prywatna pamięć rozmów z LLM (ChatGPT, Claude, Gemini, Grok, etc.)
🧠 RAE-core jako silnik refleksyjnej pamięci

3.2 Architektura RAE-Local-Memory
┌─────────────────────────────────────────────────────────────────────┐
│                    Browser Extension (JS)                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Content Scripts (per chat page)                             │   │
│  │  - ChatGPT interceptor                                       │   │
│  │  - Claude interceptor                                        │   │
│  │  - Gemini interceptor                                        │   │
│  │  - Grok interceptor                                          │   │
│  │  - DeepSeek interceptor                                      │   │
│  │  - Qwen interceptor                                          │   │
│  │  - Mistral interceptor                                       │   │
│  │  - Bielik interceptor                                        │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
│                             │ Native Messaging                       │
└─────────────────────────────┼───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│              RAE-Local-Memory Backend (.exe)                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Native Messaging Host (Python)                              │   │
│  │  - Odbiera messages z extension                              │   │
│  │  - Przetwarza przez RAE-core                                 │   │
│  │  - Zapisuje do SQLite                                        │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
│                             │                                        │
│  ┌──────────────────────────┴───────────────────────────────────┐   │
│  │                      RAE-core                                │   │
│  │  - 4-warstwowa pamięć                                        │   │
│  │  - Reflection Engine                                         │   │
│  │  - Hybrid Search (uproszczony)                               │   │
│  │  - Math layers (opcjonalne)                                  │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
│                             │                                        │
│  ┌──────────────────────────┴───────────────────────────────────┐   │
│  │           Storage Adapters (SQLite)                          │   │
│  │  - SQLiteMemoryStorage                                       │   │
│  │  - SQLiteVectorStore (sqlite-vec lub numpy)                  │   │
│  │  - SQLiteGraphStore                                          │   │
│  │  - In-memory cache                                           │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │           LLM Adapters (opcjonalne)                          │   │
│  │  - Ollama (local)                                            │   │
│  │  - None (rule-based fallback)                                │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
3.3 Struktura projektu RAE-Local-Memory
rae-local-memory/
├── extension/                  # Browser Extension
│   ├── manifest.json          # Chrome/Firefox manifest v3
│   ├── background.js          # Service worker
│   ├── content-scripts/
│   │   ├── chatgpt.js         # ChatGPT DOM interceptor
│   │   ├── claude.js          # Claude interceptor
│   │   ├── gemini.js          # Gemini interceptor
│   │   ├── grok.js            # Grok interceptor
│   │   ├── deepseek.js        # DeepSeek interceptor
│   │   ├── qwen.js            # Qwen interceptor
│   │   ├── mistral.js         # Mistral interceptor
│   │   └── bielik.js          # Bielik interceptor
│   ├── popup/
│   │   ├── popup.html
│   │   ├── popup.js
│   │   └── popup.css
│   └── options/
│       ├── options.html
│       └── options.js
│
├── backend/                    # Python Backend (kompilowany do .exe)
│   ├── __init__.py
│   ├── main.py                # Entry point
│   ├── native_messaging.py    # Native messaging host
│   ├── api.py                 # Optional REST API (localhost)
│   │
│   ├── adapters/              # SQLite adapters
│   │   ├── __init__.py
│   │   ├── sqlite_storage.py  # SQLiteMemoryStorage
│   │   ├── sqlite_vector.py   # SQLiteVectorStore (sqlite-vec)
│   │   ├── sqlite_graph.py    # SQLiteGraphStore
│   │   └── memory_cache.py    # In-memory LRU cache
│   │
│   ├── embedding/             # Local embeddings
│   │   ├── __init__.py
│   │   └── local.py           # sentence-transformers lub TFLite
│   │
│   ├── llm/                   # Optional LLM
│   │   ├── __init__.py
│   │   ├── ollama.py          # Ollama adapter
│   │   └── none.py            # No-LLM fallback
│   │
│   └── config.py              # Local configuration
│
├── rae_core/                   # 🔗 Symlink lub git submodule do rae-core
│
├── scripts/
│   ├── build_exe.py           # PyInstaller/Nuitka build
│   ├── install_host.py        # Register native messaging host
│   └── package_extension.py   # Package for Chrome/Firefox
│
├── tests/
├── pyproject.toml
└── README.md
3.4 Wymagania techniczne RAE-Local-Memory
KomponentTechnologiaUzasadnienieStorageSQLite + sqlite-vecJednoplikowa baza, embeddable, bez serweraVector Searchsqlite-vec lub numpyLokalne wyszukiwanie wektoroweEmbeddingsentence-transformers (all-MiniLM-L6-v2)Małe, szybkie, lokalneLLM (opcja)OllamaLokalne LLM dla refleksjiBuildPyInstaller / NuitkaKompilacja do .exeExtensionManifest V3Chrome/Firefox/EdgeIPCNative MessagingKomunikacja extension ↔ backend
3.5 Interceptory dla platform LLM
PlatformaURL PatternDOM Selector StrategyChatGPTchat.openai.com/*Message divs, streaming textClaudeclaude.ai/*Conversation containersGeminigemini.google.com/*Chat bubblesGrokx.com/i/grok, grok.x.ai/*Message elementsDeepSeekchat.deepseek.com/*Chat interfaceQwenqwenlm.ai/*, tongyi.aliyun.com/*Chat containersMistralchat.mistral.ai/*Message elementsBielikbielik.ai/* (jeśli istnieje chat)TBD

4. Propozycja architektury RAE-core
4.1 Główne interfejsy (interfaces/)
python# rae_core/interfaces/storage.py

from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.memory import MemoryItem
from ..models.graph import GraphNode, GraphEdge
from ..models.search import SearchResult

class IMemoryStorage(ABC):
    """Interfejs do storage pamięci (bez konkretnej bazy)"""
    
    @abstractmethod
    async def store(self, memory: MemoryItem) -> str:
        """Store memory, return ID"""
        pass
    
    @abstractmethod
    async def get(self, memory_id: str) -> Optional[MemoryItem]:
        """Get memory by ID"""
        pass
    
    @abstractmethod
    async def delete(self, memory_id: str) -> bool:
        """Delete memory"""
        pass
    
    @abstractmethod
    async def list_by_layer(
        self, 
        layer: str, 
        tenant_id: str,
        limit: int = 100
    ) -> List[MemoryItem]:
        """List memories by layer"""
        pass


class IVectorStore(ABC):
    """Interfejs do vector storage"""
    
    @abstractmethod
    async def upsert(
        self, 
        id: str, 
        vector: List[float], 
        metadata: dict
    ) -> None:
        """Upsert vector"""
        pass
    
    @abstractmethod
    async def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[dict] = None
    ) -> List[SearchResult]:
        """Vector similarity search"""
        pass


class IGraphStore(ABC):
    """Interfejs do knowledge graph"""
    
    @abstractmethod
    async def add_node(self, node: GraphNode) -> str:
        pass
    
    @abstractmethod
    async def add_edge(self, edge: GraphEdge) -> str:
        pass
    
    @abstractmethod
    async def traverse(
        self,
        start_node_id: str,
        max_depth: int = 2,
        direction: str = "both"
    ) -> List[GraphNode]:
        """BFS/DFS traversal"""
        pass


class ICacheProvider(ABC):
    """Interfejs do cache"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[bytes]:
        pass
    
    @abstractmethod
    async def set(self, key: str, value: bytes, ttl: int = 3600) -> None:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        pass
4.2 Modele danych (models/)
python# rae_core/models/memory.py

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid

class MemoryLayer(str, Enum):
    """4 warstwy pamięci RAE"""
    SENSORY = "sensory"       # Layer 1
    WORKING = "working"       # Layer 2  
    LONGTERM = "longterm"     # Layer 3
    REFLECTIVE = "reflective" # Layer 4

class MemoryType(str, Enum):
    """Typy pamięci w warstwach"""
    SENSORY = "sensory"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROFILE = "profile"
    REFLECTION = "reflection"
    STRATEGY = "strategy"

class MemoryItem(BaseModel):
    """Główny model pamięci RAE"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    layer: MemoryLayer
    memory_type: MemoryType
    
    # Metadata
    tenant_id: str
    project: Optional[str] = None
    source: Optional[str] = None  # "chatgpt", "claude", "user", etc.
    
    # Temporal
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    accessed_at: Optional[datetime] = None
    
    # Scoring
    importance: float = 0.5
    relevance_score: Optional[float] = None
    decay_rate: float = 0.01
    
    # Relations
    tags: List[str] = Field(default_factory=list)
    related_ids: List[str] = Field(default_factory=list)
    
    # Embedding (opcjonalne - może być w VectorStore)
    embedding: Optional[List[float]] = None
    
    # Extra metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True
4.3 Memory Layer Base Class
python# rae_core/layers/base.py

from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.memory import MemoryItem, MemoryLayer
from ..interfaces.storage import IMemoryStorage

class AbstractMemoryLayer(ABC):
    """Bazowa klasa dla warstw pamięci"""
    
    def __init__(
        self,
        storage: IMemoryStorage,
        layer: MemoryLayer
    ):
        self.storage = storage
        self.layer = layer
    
    @abstractmethod
    async def process(self, item: MemoryItem) -> MemoryItem:
        """Process incoming memory item for this layer"""
        pass
    
    @abstractmethod
    async def consolidate(self) -> List[MemoryItem]:
        """Consolidate memories (np. transfer STM → LTM)"""
        pass
    
    async def store(self, item: MemoryItem) -> str:
        """Store memory in this layer"""
        item.layer = self.layer
        processed = await self.process(item)
        return await self.storage.store(processed)
    
    async def retrieve(
        self,
        tenant_id: str,
        limit: int = 100
    ) -> List[MemoryItem]:
        """Retrieve memories from this layer"""
        return await self.storage.list_by_layer(
            layer=self.layer.value,
            tenant_id=tenant_id,
            limit=limit
        )
4.4 Hybrid Search Engine
python# rae_core/search/hybrid.py

from typing import List, Optional, Dict
from dataclasses import dataclass
from ..interfaces.storage import IVectorStore, IGraphStore
from ..models.search import SearchQuery, SearchResult
from .base import AbstractSearchStrategy

@dataclass
class SearchWeights:
    """Wagi dla strategii wyszukiwania"""
    vector: float = 0.4
    graph: float = 0.3
    sparse: float = 0.2
    fulltext: float = 0.1

class HybridSearchEngine:
    """Orkiestrator hybrid search"""
    
    def __init__(
        self,
        vector_store: IVectorStore,
        graph_store: IGraphStore,
        strategies: Dict[str, AbstractSearchStrategy],
        default_weights: Optional[SearchWeights] = None
    ):
        self.vector_store = vector_store
        self.graph_store = graph_store
        self.strategies = strategies
        self.weights = default_weights or SearchWeights()
    
    async def search(
        self,
        query: SearchQuery,
        weights: Optional[SearchWeights] = None
    ) -> List[SearchResult]:
        """Execute hybrid search across all strategies"""
        w = weights or self.weights
        results = []
        
        # Execute strategies in parallel
        # (w rzeczywistej implementacji - asyncio.gather)
        
        if "vector" in self.strategies and w.vector > 0:
            vector_results = await self.strategies["vector"].search(query)
            results.extend(self._weight_results(vector_results, w.vector))
        
        if "graph" in self.strategies and w.graph > 0:
            graph_results = await self.strategies["graph"].search(query)
            results.extend(self._weight_results(graph_results, w.graph))
        
        # ... sparse, fulltext
        
        # Fusion: deduplicate and rank
        return self._fuse_results(results)
    
    def _weight_results(
        self, 
        results: List[SearchResult], 
        weight: float
    ) -> List[SearchResult]:
        for r in results:
            r.score *= weight
        return results
    
    def _fuse_results(
        self, 
        results: List[SearchResult]
    ) -> List[SearchResult]:
        """Deduplicate and rank by combined score"""
        seen = {}
        for r in results:
            if r.id in seen:
                seen[r.id].score += r.score
            else:
                seen[r.id] = r
        
        return sorted(seen.values(), key=lambda x: x.score, reverse=True)

5. Propozycja architektury RAE-Local-Memory
5.1 SQLite Storage Adapter
python# rae_local_memory/adapters/sqlite_storage.py

import sqlite3
import json
from typing import List, Optional
from pathlib import Path
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.models.memory import MemoryItem

class SQLiteMemoryStorage(IMemoryStorage):
    """SQLite implementation of IMemoryStorage"""
    
    def __init__(self, db_path: str = "~/.rae/memory.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    layer TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    tenant_id TEXT NOT NULL,
                    project TEXT,
                    source TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT,
                    accessed_at TEXT,
                    importance REAL DEFAULT 0.5,
                    relevance_score REAL,
                    decay_rate REAL DEFAULT 0.01,
                    tags TEXT,  -- JSON array
                    related_ids TEXT,  -- JSON array
                    metadata TEXT  -- JSON object
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_layer 
                ON memories(layer, tenant_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_created 
                ON memories(created_at DESC)
            """)
    
    async def store(self, memory: MemoryItem) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO memories 
                (id, content, layer, memory_type, tenant_id, project,
                 source, created_at, updated_at, importance, decay_rate,
                 tags, related_ids, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.id,
                memory.content,
                memory.layer,
                memory.memory_type,
                memory.tenant_id,
                memory.project,
                memory.source,
                memory.created_at.isoformat(),
                memory.updated_at.isoformat() if memory.updated_at else None,
                memory.importance,
                memory.decay_rate,
                json.dumps(memory.tags),
                json.dumps(memory.related_ids),
                json.dumps(memory.metadata)
            ))
        return memory.id
    
    async def get(self, memory_id: str) -> Optional[MemoryItem]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM memories WHERE id = ?", 
                (memory_id,)
            ).fetchone()
            
            if row:
                return self._row_to_memory(row)
        return None
    
    async def delete(self, memory_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM memories WHERE id = ?",
                (memory_id,)
            )
            return cursor.rowcount > 0
    
    async def list_by_layer(
        self,
        layer: str,
        tenant_id: str,
        limit: int = 100
    ) -> List[MemoryItem]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM memories 
                WHERE layer = ? AND tenant_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (layer, tenant_id, limit)).fetchall()
            
            return [self._row_to_memory(row) for row in rows]
    
    def _row_to_memory(self, row: sqlite3.Row) -> MemoryItem:
        return MemoryItem(
            id=row["id"],
            content=row["content"],
            layer=row["layer"],
            memory_type=row["memory_type"],
            tenant_id=row["tenant_id"],
            project=row["project"],
            source=row["source"],
            importance=row["importance"],
            decay_rate=row["decay_rate"],
            tags=json.loads(row["tags"]) if row["tags"] else [],
            related_ids=json.loads(row["related_ids"]) if row["related_ids"] else [],
            metadata=json.loads(row["metadata"]) if row["metadata"] else {}
        )
5.2 SQLite Vector Store (sqlite-vec)
python# rae_local_memory/adapters/sqlite_vector.py

import sqlite3
from typing import List, Optional
import numpy as np
from rae_core.interfaces.storage import IVectorStore
from rae_core.models.search import SearchResult

class SQLiteVectorStore(IVectorStore):
    """SQLite + sqlite-vec for local vector search"""
    
    def __init__(self, db_path: str, dimension: int = 384):
        self.db_path = db_path
        self.dimension = dimension
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            # Load sqlite-vec extension
            conn.enable_load_extension(True)
            conn.load_extension("vec0")
            
            # Create virtual table for vectors
            conn.execute(f"""
                CREATE VIRTUAL TABLE IF NOT EXISTS vec_memories
                USING vec0(
                    id TEXT PRIMARY KEY,
                    embedding FLOAT[{self.dimension}],
                    +tenant_id TEXT,
                    +layer TEXT,
                    +source TEXT
                )
            """)
    
    async def upsert(
        self,
        id: str,
        vector: List[float],
        metadata: dict
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.enable_load_extension(True)
            conn.load_extension("vec0")
            
            conn.execute("""
                INSERT OR REPLACE INTO vec_memories 
                (id, embedding, tenant_id, layer, source)
                VALUES (?, ?, ?, ?, ?)
            """, (
                id,
                np.array(vector, dtype=np.float32).tobytes(),
                metadata.get("tenant_id"),
                metadata.get("layer"),
                metadata.get("source")
            ))
    
    async def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[dict] = None
    ) -> List[SearchResult]:
        with sqlite3.connect(self.db_path) as conn:
            conn.enable_load_extension(True)
            conn.load_extension("vec0")
            
            query_bytes = np.array(query_vector, dtype=np.float32).tobytes()
            
            # Build filter clause
            where_clause = ""
            params = [query_bytes, top_k]
            
            if filters:
                conditions = []
                if "tenant_id" in filters:
                    conditions.append("tenant_id = ?")
                    params.insert(-1, filters["tenant_id"])
                if "layer" in filters:
                    conditions.append("layer = ?")
                    params.insert(-1, filters["layer"])
                if conditions:
                    where_clause = "WHERE " + " AND ".join(conditions)
            
            rows = conn.execute(f"""
                SELECT id, distance
                FROM vec_memories
                {where_clause}
                ORDER BY embedding <-> ?
                LIMIT ?
            """, params).fetchall()
            
            return [
                SearchResult(
                    id=row[0],
                    score=1.0 - row[1],  # Convert distance to similarity
                    source="vector"
                )
                for row in rows
            ]
5.3 Browser Extension Content Script (ChatGPT)
javascript// extension/content-scripts/chatgpt.js

class ChatGPTInterceptor {
    constructor() {
        this.observer = null;
        this.messageHistory = [];
    }

    init() {
        console.log('[RAE] ChatGPT interceptor initialized');
        this.setupMutationObserver();
        this.interceptNetworkRequests();
    }

    setupMutationObserver() {
        // Observe DOM changes for new messages
        const chatContainer = document.querySelector('main');
        if (!chatContainer) {
            setTimeout(() => this.setupMutationObserver(), 1000);
            return;
        }

        this.observer = new MutationObserver((mutations) => {
            for (const mutation of mutations) {
                if (mutation.type === 'childList') {
                    this.processNewMessages(mutation.addedNodes);
                }
            }
        });

        this.observer.observe(chatContainer, {
            childList: true,
            subtree: true
        });
    }

    processNewMessages(nodes) {
        for (const node of nodes) {
            if (node.nodeType !== Node.ELEMENT_NODE) continue;
            
            // ChatGPT message selectors (may need updates)
            const userMessages = node.querySelectorAll('[data-message-author-role="user"]');
            const assistantMessages = node.querySelectorAll('[data-message-author-role="assistant"]');
            
            userMessages.forEach(msg => this.captureMessage('user', msg));
            assistantMessages.forEach(msg => this.captureMessage('assistant', msg));
        }
    }

    captureMessage(role, element) {
        const content = element.innerText?.trim();
        if (!content) return;
        
        const message = {
            role,
            content,
            source: 'chatgpt',
            timestamp: new Date().toISOString(),
            url: window.location.href
        };

        // Avoid duplicates
        const hash = this.hashMessage(message);
        if (this.messageHistory.includes(hash)) return;
        this.messageHistory.push(hash);

        // Send to backend via Native Messaging
        this.sendToRAE(message);
    }

    sendToRAE(message) {
        chrome.runtime.sendMessage({
            type: 'RAE_CAPTURE_MESSAGE',
            payload: message
        }, (response) => {
            if (response?.success) {
                console.log('[RAE] Message captured:', message.role);
            }
        });
    }

    interceptNetworkRequests() {
        // Intercept fetch for streaming responses
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            const response = await originalFetch(...args);
            
            // Check if this is a ChatGPT API call
            if (args[0]?.includes?.('/backend-api/conversation')) {
                this.handleConversationResponse(response.clone());
            }
            
            return response;
        };
    }

    async handleConversationResponse(response) {
        try {
            const text = await response.text();
            // Parse streaming response
            const lines = text.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    if (data.message?.content?.parts) {
                        // Process complete message
                    }
                }
            }
        } catch (e) {
            // Streaming, ignore
        }
    }

    hashMessage(msg) {
        return `${msg.role}:${msg.content.slice(0, 100)}:${msg.timestamp}`;
    }
}

// Initialize
const interceptor = new ChatGPTInterceptor();
interceptor.init();
5.4 Native Messaging Host
python# rae_local_memory/native_messaging.py

import sys
import json
import struct
import asyncio
from typing import Optional
from rae_core.models.memory import MemoryItem, MemoryLayer, MemoryType
from .adapters.sqlite_storage import SQLiteMemoryStorage
from .adapters.sqlite_vector import SQLiteVectorStore

class NativeMessagingHost:
    """Native Messaging host for browser extension communication"""
    
    def __init__(self, db_path: str = "~/.rae/memory.db"):
        self.storage = SQLiteMemoryStorage(db_path)
        self.vector_store = SQLiteVectorStore(db_path)
        self.embedding_model = None  # Lazy load
    
    def run(self):
        """Main loop for native messaging"""
        while True:
            message = self._read_message()
            if message is None:
                break
            
            response = asyncio.run(self._handle_message(message))
            self._send_message(response)
    
    def _read_message(self) -> Optional[dict]:
        """Read message from stdin (Chrome native messaging format)"""
        raw_length = sys.stdin.buffer.read(4)
        if not raw_length:
            return None
        
        message_length = struct.unpack('I', raw_length)[0]
        message = sys.stdin.buffer.read(message_length).decode('utf-8')
        return json.loads(message)
    
    def _send_message(self, message: dict):
        """Send message to stdout"""
        encoded = json.dumps(message).encode('utf-8')
        sys.stdout.buffer.write(struct.pack('I', len(encoded)))
        sys.stdout.buffer.write(encoded)
        sys.stdout.buffer.flush()
    
    async def _handle_message(self, message: dict) -> dict:
        """Handle incoming message from extension"""
        msg_type = message.get('type')
        payload = message.get('payload', {})
        
        try:
            if msg_type == 'RAE_CAPTURE_MESSAGE':
                return await self._capture_message(payload)
            elif msg_type == 'RAE_SEARCH':
                return await self._search(payload)
            elif msg_type == 'RAE_GET_REFLECTIONS':
                return await self._get_reflections(payload)
            else:
                return {'success': False, 'error': f'Unknown type: {msg_type}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _capture_message(self, payload: dict) -> dict:
        """Capture chat message to RAE memory"""
        memory = MemoryItem(
            content=payload['content'],
            layer=MemoryLayer.SENSORY,  # Start in sensory
            memory_type=MemoryType.EPISODIC,
            tenant_id="local",  # Local user
            source=payload.get('source', 'unknown'),
            metadata={
                'role': payload.get('role'),
                'url': payload.get('url'),
                'original_timestamp': payload.get('timestamp')
            }
        )
        
        # Store in SQLite
        memory_id = await self.storage.store(memory)
        
        # Generate embedding and store in vector DB
        embedding = await self._get_embedding(memory.content)
        if embedding:
            await self.vector_store.upsert(
                id=memory_id,
                vector=embedding,
                metadata={
                    'tenant_id': memory.tenant_id,
                    'layer': memory.layer,
                    'source': memory.source
                }
            )
        
        return {'success': True, 'memory_id': memory_id}
    
    async def _get_embedding(self, text: str) -> Optional[list]:
        """Get embedding for text (lazy load model)"""
        if self.embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            except ImportError:
                return None
        
        return self.embedding_model.encode(text).tolist()
    
    async def _search(self, payload: dict) -> dict:
        """Search memories"""
        query = payload.get('query', '')
        top_k = payload.get('top_k', 10)
        
        embedding = await self._get_embedding(query)
        if not embedding:
            return {'success': False, 'error': 'Embedding model not available'}
        
        results = await self.vector_store.search(
            query_vector=embedding,
            top_k=top_k,
            filters={'tenant_id': 'local'}
        )
        
        # Fetch full memories
        memories = []
        for result in results:
            memory = await self.storage.get(result.id)
            if memory:
                memories.append({
                    'id': memory.id,
                    'content': memory.content,
                    'score': result.score,
                    'source': memory.source,
                    'created_at': memory.created_at.isoformat()
                })
        
        return {'success': True, 'results': memories}


if __name__ == '__main__':
    host = NativeMessagingHost()
    host.run()

6. Plan refaktoryzacji
6.1 Faza 1: Przygotowanie (1-2 dni)
KrokZadanieOpis1.1Analiza zależnościZmapuj wszystkie importy w apps/memory_api/1.2Identyfikacja coreOznacz pliki które idą do rae_core1.3Setup repoUtwórz repo rae-core (lub monorepo z workspace)1.4CI/CDSkonfiguruj GitHub Actions dla rae-core
6.2 Faza 2: Wydzielenie interfejsów (2-3 dni)
KrokZadanieOpis2.1InterfacesUtwórz rae_core/interfaces/ z abstrakcjami2.2ModelsPrzenieś modele Pydantic (bez SQLAlchemy)2.3ExceptionsUtwórz hierarchię wyjątków2.4ConfigPrzenieś konfigurację (pydantic-settings)
6.3 Faza 3: Wydzielenie logiki (3-5 dni)
KrokZadanieOpis3.1Memory LayersPrzenieś logikę 4 warstw pamięci3.2Math LayersPrzenieś Math-1/2/33.3Hybrid SearchPrzenieś search engine (bez konkretnych store)3.4Reflection EnginePrzenieś Actor-Evaluator-Reflector3.5Context BuilderPrzenieś context building3.6ScoringPrzenieś MemoryScoringV2
6.4 Faza 4: Adaptery w "Dużym RAE" (2-3 dni)
KrokZadanieOpis4.1PostgresAdapterImplementuj IMemoryStorage dla Postgres4.2QdrantAdapterImplementuj IVectorStore dla Qdrant4.3RedisAdapterImplementuj ICacheProvider dla Redis4.4LLM AdaptersImplementuj ILLMProvider dla OpenAI/Anthropic/etc.4.5IntegracjaZrefaktoryzuj importy w apps/memory_api
6.5 Faza 5: RAE-Local-Memory (5-7 dni)
KrokZadanieOpis5.1SQLite AdaptersImplementuj adaptery SQLite5.2ExtensionZbuduj browser extension (manifest v3)5.3Native HostImplementuj native messaging host5.4InterceptorsNapisz interceptory dla każdej platformy5.5BuildSkonfiguruj PyInstaller/Nuitka5.6PackagingPrzygotuj instalatory
6.6 Faza 6: Testy i dokumentacja (2-3 dni)
KrokZadanieOpis6.1Unit TestsTesty dla rae-core (bez infra)6.2IntegrationTesty integracyjne z adapterami6.3E2ETesty end-to-end extension + backend6.4DocsDokumentacja API, README, examples

7. Mapowanie plików
7.1 Pliki do RAE-core
Na podstawie struktury z README, prawdopodobne mapowanie:
Źródło (RAE-agentic-memory)Cel (rae_core)apps/memory_api/core/math*.pyrae_core/math/apps/memory_api/models/*.pyrae_core/models/ (bez SQLAlchemy)apps/memory_api/services/hybrid_search.pyrae_core/search/hybrid.pyapps/memory_api/services/reflection_engine.pyrae_core/reflection/apps/memory_api/services/context_builder.pyrae_core/context/apps/memory_api/services/memory_scoring.pyrae_core/scoring/apps/memory_api/services/query_analyzer.pyrae_core/search/query_analyzer.py
7.2 Pliki zostające w "Dużym RAE"
Plik/KatalogPowódapps/memory_api/routers/FastAPI specificzneapps/memory_api/repositories/SQLAlchemy/Postgres specificapps/memory_api/middleware/FastAPI middlewareapps/memory_api/tasks/Celery workersapps/ml_service/ML microserviceinfra/Docker infrastructureintegrations/External integrations

8. Abstrakcje storage
8.1 Diagram zależności
┌─────────────────────────────────────────────────────────────────┐
│                         rae_core                                │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │  Memory Layers  │───▶│   Interfaces    │                    │
│  │  Math Layers    │    │  IMemoryStorage │                    │
│  │  Search Engine  │    │  IVectorStore   │                    │
│  │  Reflection     │    │  IGraphStore    │                    │
│  └─────────────────┘    │  ILLMProvider   │                    │
│                         └────────┬────────┘                    │
└────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
┌───────────────────────────────┐   ┌───────────────────────────────┐
│     "Duże RAE" Adapters       │   │   RAE-Local-Memory Adapters   │
│                               │   │                               │
│  PostgresMemoryStorage        │   │  SQLiteMemoryStorage          │
│  QdrantVectorStore            │   │  SQLiteVectorStore            │
│  PostgresGraphStore           │   │  SQLiteGraphStore             │
│  RedisCacheProvider           │   │  InMemoryCache                │
│  OpenAIProvider               │   │  OllamaProvider               │
│  AnthropicProvider            │   │  NoLLMFallback                │
└───────────────────────────────┘   └───────────────────────────────┘
8.2 Dependency Injection Pattern
python# rae_core/engine.py

from .interfaces.storage import IMemoryStorage, IVectorStore, IGraphStore
from .interfaces.llm import ILLMProvider
from .layers.sensory import SensoryMemoryLayer
from .layers.working import WorkingMemoryLayer
from .layers.longterm import LongTermMemoryLayer
from .layers.reflective import ReflectiveMemoryLayer
from .search.hybrid import HybridSearchEngine

class RAEEngine:
    """Main RAE engine with DI for all adapters"""
    
    def __init__(
        self,
        memory_storage: IMemoryStorage,
        vector_store: IVectorStore,
        graph_store: IGraphStore,
        llm_provider: Optional[ILLMProvider] = None
    ):
        # Storage
        self.memory_storage = memory_storage
        self.vector_store = vector_store
        self.graph_store = graph_store
        self.llm_provider = llm_provider
        
        # Initialize layers
        self.sensory = SensoryMemoryLayer(memory_storage)
        self.working = WorkingMemoryLayer(memory_storage)
        self.longterm = LongTermMemoryLayer(memory_storage)
        self.reflective = ReflectiveMemoryLayer(memory_storage, llm_provider)
        
        # Initialize search
        self.search = HybridSearchEngine(
            vector_store=vector_store,
            graph_store=graph_store
        )
    
    async def store(self, content: str, **kwargs) -> str:
        """Store new memory (starts in sensory layer)"""
        pass
    
    async def query(self, query: str, **kwargs) -> list:
        """Query memories using hybrid search"""
        pass
    
    async def reflect(self) -> list:
        """Generate reflections"""
        pass

9. Harmonogram
9.1 Timeline (szacunkowy)
Tydzień 1-2: Faza 1-2 (Przygotowanie + Interfejsy)
├── Dzień 1-2: Analiza, setup repo
├── Dzień 3-5: Interfaces, Models
└── Dzień 6-7: Exceptions, Config, testy jednostkowe

Tydzień 3-4: Faza 3 (Wydzielenie logiki)
├── Dzień 8-10: Memory Layers, Math Layers
├── Dzień 11-13: Search, Reflection
└── Dzień 14: Context, Scoring, testy

Tydzień 5: Faza 4 (Adaptery "Dużego RAE")
├── Dzień 15-16: Postgres, Qdrant adapters
├── Dzień 17-18: Redis, LLM adapters
└── Dzień 19: Integracja, refaktor importów

Tydzień 6-7: Faza 5 (RAE-Local-Memory)
├── Dzień 20-21: SQLite adapters
├── Dzień 22-24: Browser extension
├── Dzień 25-26: Native host, interceptors
└── Dzień 27-28: Build, packaging

Tydzień 8: Faza 6 (Testy i dokumentacja)
├── Dzień 29-30: Wszystkie testy
└── Dzień 31-32: Dokumentacja, release
9.2 Kamienie milowe
MilestoneData (od startu)DeliverableM1Tydzień 2rae_core v0.1 (interfaces + models)M2Tydzień 4rae_core v0.5 (pełna logika core)M3Tydzień 5RAE v3.0 (używa rae_core)M4Tydzień 7RAE-Local-Memory v0.1-alphaM5Tydzień 8RAE-Local-Memory v0.1-beta (release)

10. Następne kroki

Potwierdź strukturę - czy proponowana architektura jest OK?
Dostęp do kodu - wgraj kluczowe pliki z apps/memory_api/core/ i services/
Zacznij od interfejsów - pierwszy PR: rae_core/interfaces/
Iteracyjne przenoszenie - jeden moduł na raz


Appendix A: Zależności RAE-core
toml# rae_core/pyproject.toml

[project]
name = "rae-core"
version = "0.1.0"
description = "Core library for RAE (Reflective Agentic-memory Engine)"
requires-python = ">=3.10"

dependencies = [
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "numpy>=1.24",
    "typing-extensions>=4.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.0",
    "mypy>=1.0",
    "ruff>=0.1",
]
Appendix B: Zależności RAE-Local-Memory
toml# rae_local_memory/pyproject.toml

[project]
name = "rae-local-memory"
version = "0.1.0"
description = "Local-first RAE memory with browser extension"
requires-python = ">=3.10"

dependencies = [
    "rae-core>=0.1.0",
    "sentence-transformers>=2.2",  # lub tflite-runtime
]

[project.optional-dependencies]
sqlite-vec = [
    "sqlite-vec>=0.1",
]
ollama = [
    "ollama>=0.1",
]
build = [
    "pyinstaller>=6.0",
    # lub nuitka>=1.0
]

Dokument przygotowany dla projektu RAE-agentic-memory
Wersja: 1.0 | Data: 2025-12-08