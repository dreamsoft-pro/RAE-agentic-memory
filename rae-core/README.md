# RAE-core

**Pure Python memory system for AI agents**

RAE-core is the foundational library for the RAE (Reflective Agentic Engine) ecosystem. It provides a complete, storage-agnostic implementation of:

- **4-layer memory architecture** (Sensory, Working, Long-term, Reflective)
- **3-layer mathematical framework** (Structure Analysis, Dynamics Tracking, Policy Optimization)
- **Hybrid search engine** (Vector + Graph + Sparse + Full-text)
- **Reflection system** (Actor-Evaluator-Reflector pattern)
- **Context management** with intelligent scoring and decay

## Key Features

- **Storage Agnostic**: Works with any storage backend through abstract interfaces
- **LLM Optional**: Can run with rule-based fallbacks (no API calls required)
- **Offline First**: Designed to work completely offline
- **Type Safe**: Full type hints with mypy strict mode
- **Zero Infrastructure**: No FastAPI, PostgreSQL, or Docker required
- **Extensible**: Clean interfaces for custom implementations

## Installation

```bash
pip install rae-core
```

## Quick Start

```python
from rae_core import RAEEngine
from rae_core.adapters import InMemoryStorage, InMemoryVectorStore

# Initialize with in-memory storage (no dependencies)
engine = RAEEngine(
    storage=InMemoryStorage(),
    vector_store=InMemoryVectorStore(),
    enable_llm=False  # Use rule-based fallback
)

# Store a memory
memory_id = await engine.store_memory(
    content="User prefers Python over JavaScript",
    layer="episodic",
    tags=["preference", "programming"]
)

# Search memories
results = await engine.search(
    query="What does the user like?",
    strategy="hybrid",
    limit=5
)

for result in results:
    print(f"{result.score}: {result.content}")
```

## Architecture

```
rae_core/
├── interfaces/     # Abstract interfaces (IStorage, IVectorStore, ILLMProvider)
├── models/         # Pydantic data models
├── layers/         # 4-layer memory architecture
├── math/           # Mathematical scoring and optimization
├── search/         # Hybrid search engine
├── reflection/     # Reflection system
├── context/        # Context building
├── scoring/        # Memory scoring algorithms
├── llm/            # LLM orchestration (optional)
├── sync/           # Sync protocol (for RAE-Sync)
└── engine.py       # Main RAEEngine entry point
```

## Documentation

See the [full documentation](https://github.com/dreamsoft-pro/RAE-agentic-memory/tree/main/rae-core/docs) for:

- Architecture overview
- API reference
- Implementation guides
- Custom adapters

## Ecosystem

RAE-core powers multiple products:

- **RAE-Server**: Enterprise multi-tenant server (FastAPI + PostgreSQL + Qdrant)
- **RAE-Lite**: Local desktop app (SQLite + no Docker)
- **RAE-Mobile**: iOS/Android app (future)
- **RAE-Sync**: Cross-device sync protocol

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

## Author

Grzegorz Leśniowski - [DreamSoft](https://dreamsoft.pro)
