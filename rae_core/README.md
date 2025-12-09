# RAE-Core

> **Core memory engine for AI Agents - Pure business logic, zero infrastructure**

RAE-Core is the extracted core of the RAE memory system providing 4-layer cognitive architecture and 3-tier mathematical foundation. It's designed to be platform-agnostic and can run on servers, desktops, browsers, and mobile devices.

## Features

### 4-Layer Memory Architecture

- **Sensory Layer**: Raw input buffer (milliseconds to seconds)
- **Working Memory**: Active processing (seconds to minutes)
- **Long-Term Memory**: Persistent storage (minutes to forever)
- **Reflective Memory**: Meta-learning and insights (periodic synthesis)

### Hybrid Search

- Multiple search strategies (keyword, recency, importance)
- Score fusion algorithms (RRF, weighted sum, max score)
- Multi-layer search with configurable weighting
- Query analysis and intent detection

### Reflection Engine

- Automatic pattern detection across memories
- Insight generation from usage patterns
- Meta-learning and strategic knowledge extraction

### Importance Scoring

- Multi-factor importance calculation
- Recency decay with configurable half-life
- Frequency-based scoring
- User-assigned importance weighting

## Installation

```bash
cd rae_core
pip install -e .
```

Or from PyPI (when published):

```bash
pip install rae-core
```

## Quick Start

### Basic Usage

```python
from rae_core import RAEEngine

# Initialize engine
engine = RAEEngine()

# Store a memory
memory_id = await engine.store_memory(
    content="User prefers dark mode UI",
    source="user_interaction",
    importance=0.8,
    tags=["preferences", "ui"]
)

# Query memories
response = await engine.query_memory(
    query="What are the user's UI preferences?",
    k=5
)

for result in response.results:
    print(f"[{result.score:.3f}] {result.content}")
```

### Layer-Specific Operations

```python
# Store directly in specific layer
await engine.store_memory(
    content="Critical security update required",
    layer="longterm",
    importance=0.95,
    tags=["security", "critical"]
)

# Query specific layers
response = await engine.query_memory(
    query="security updates",
    search_layers=["reflective", "longterm"]
)
```

### Memory Consolidation

```python
# Automatic consolidation (enabled by default)
engine = RAEEngine(enable_auto_consolidation=True)

# Manual consolidation
results = await engine.consolidate_memories()
print(f"Consolidated {len(results['sensory_to_working'])} memories")
```

### Reflection Generation

```python
# Generate insights from patterns
reflections = await engine.generate_reflections(
    project="my-app"
)

for reflection in reflections:
    print(f"Insight: {reflection.content}")
```

### Statistics

```python
# Get comprehensive statistics
stats = await engine.get_statistics()

print(f"Total memories: {stats['total_memories']}")
print(f"Long-term: {stats['longterm']['count']}")
print(f"Reflections: {stats['reflective']['count']}")
```

## Architecture

### Layer Flow

```
Sensory → Working → Long-Term → Reflective
  (raw)   (active)   (persistent)  (insights)
```

### Consolidation Criteria

- **Sensory → Working**: Importance threshold (default: 0.5)
- **Working → Long-Term**: Importance + usage + age (threshold: 0.6, min usage: 2)
- **Long-Term → Reflective**: Pattern detection + high usage (threshold: 0.7, min usage: 5)

### Search Strategies

1. **Keyword**: TF-IDF-like term matching with Jaccard similarity
2. **Recency**: Exponential decay with configurable half-life (default: 7 days)
3. **Importance**: Multi-factor scoring (importance, frequency, recency)

### Fusion Methods

- **RRF (Reciprocal Rank Fusion)**: `score = Σ(1 / (k + rank))`
- **Weighted Sum**: `score = Σ(weight_i * score_i)`
- **Max Score**: `score = max(score_i)`

## Advanced Usage

### Custom Layer Configuration

```python
engine = RAEEngine(
    sensory_max_size=200,
    sensory_retention_seconds=30,
    working_max_size=100,
    working_retention_minutes=60,
    enable_auto_consolidation=True,
    enable_reflections=True
)
```

### Hybrid Search with Custom Weights

```python
from rae_core.search import SearchEngine, FusionStrategy

search_engine = SearchEngine()

results = await search_engine.search(
    layer=engine.longterm,
    query="Python best practices",
    k=10,
    strategies=["keyword", "importance"],
    fusion=FusionStrategy.WEIGHTED_SUM,
    weights=[0.6, 0.4]
)
```

### Context Building

```python
from rae_core.context import ContextBuilder

builder = ContextBuilder(
    max_context_length=4000,
    format_style="markdown"
)

context = await builder.build_context(
    memories=response.results,
    query="Python best practices"
)
print(context)
```

### Custom Importance Scoring

```python
from rae_core.scoring import ImportanceScorer

scorer = ImportanceScorer(
    recency_weight=0.4,
    frequency_weight=0.3,
    user_weight=0.3,
    recency_half_life_days=14.0
)

importance = scorer.calculate_importance(memory)
```

## Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=rae_core tests/
```

## Dependencies

### Core (Minimal)

- `pydantic>=2.0` - Data validation
- `typing-extensions>=4.5` - Type hints

### Development

- `pytest>=7.0` - Testing
- `pytest-cov>=4.0` - Coverage
- `black>=23.0` - Formatting
- `ruff>=0.1.0` - Linting

## Design Principles

1. **Zero Infrastructure**: No database, no web framework, no external services
2. **Platform Agnostic**: Runs anywhere Python runs
3. **Adapter Pattern**: Storage adapters implemented separately per platform
4. **Pure Business Logic**: All cognitive architecture is pure Python
5. **Async First**: All operations are async for modern Python

## Roadmap

### Phase 1: Core (Current)

- ✅ 4-layer memory architecture
- ✅ Hybrid search with fusion
- ✅ Reflection engine
- ✅ Context building
- ✅ Importance scoring
- ✅ In-memory implementation

### Phase 2: Storage Adapters

- [ ] PostgreSQL adapter (for RAE-Server)
- [ ] SQLite adapter (for RAE-Lite)
- [ ] Redis adapter (for caching)
- [ ] Vector store adapters (Qdrant, Milvus, etc.)

### Phase 3: Advanced Features

- [ ] Graph-based search (knowledge graph)
- [ ] Semantic search (embedding-based)
- [ ] LLM integration for reflections
- [ ] CRDT-based sync protocol

## License

Apache-2.0

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Links

- **GitHub**: https://github.com/dreamsoft-pro/RAE-agentic-memory
- **Documentation**: https://github.com/dreamsoft-pro/RAE-agentic-memory/tree/main/docs
- **PyPI** (coming soon): https://pypi.org/project/rae-core/

---

**Version**: 0.1.0
**Status**: Alpha - API may change
**Python**: >=3.10
