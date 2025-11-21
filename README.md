# 🧠 RAE - Reflective Agentic Memory Engine

> Give your AI agents human-like memory: Learn, remember, and improve over time.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[📖 Documentation](#documentation) | [🚀 Quick Start](#quick-start-5-minutes) | [💬 Community](#community--support) | [🎯 Examples](#real-world-examples)

---

## Why RAE?

Current AI agents are **stateless** - they forget everything after each conversation. RAE changes that by giving them **persistent, structured memory** that evolves over time.

### The Problem

🔴 ChatGPT forgets your preferences between sessions
🔴 Code assistants ask the same questions repeatedly
🔴 Customer support bots don't learn from past interactions
🔴 Agents can't build on previous experiences

### The RAE Solution

✅ **Multi-layered memory** (episodic → working → semantic → long-term)
✅ **Automatic insight extraction** via Reflection Engine
✅ **Graph-based knowledge connections** (GraphRAG)
✅ **IDE integration** via Model Context Protocol (MCP)
✅ **Cost-aware caching** to minimize LLM API costs
✅ **Production-ready** with multi-tenancy and security

---

## Quick Start (< 5 minutes)

```bash
# 1. Clone & setup
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory
cd RAE-agentic-memory

# 2. Start services (one command!)
make start

# 3. Try it out
python examples/quickstart.py
```

That's it! RAE is now running at `http://localhost:8000`

---

## Real-World Examples

### 🎯 Personal AI Assistant
```python
from rae_memory_sdk import MemoryClient

agent = MemoryClient()

# Store preferences
agent.store("User prefers dark mode in all applications")
agent.store("User is learning Python and FastAPI")

# Later, agent remembers...
results = agent.query("What are the user's UI preferences?")
# Returns: "User prefers dark mode in all applications"
```

### 🏢 Team Knowledge Base
- Auto-indexes Slack conversations, PRs, and meeting notes
- Answers questions with full context from past discussions
- Discovers hidden patterns in team behavior

### 💻 Smart Code Review Bot
- Learns your team's code standards over time
- Remembers past architectural decisions
- Prevents repeated mistakes automatically

### 🔬 Research Assistant
- Stores insights from papers and documents
- Builds knowledge graph of connected concepts
- Answers questions with cited sources

[See more examples →](examples/)

---

## Architecture

RAE implements a **4-layer cognitive memory system** inspired by human cognition:

```
┌─────────────────────────────────────────────────────────┐
│  EPISODIC MEMORY (EM)                                   │
│  Raw events, observations, conversations                │
│  "User fixed bug in auth.py on Jan 5"                  │
└──────────────────┬──────────────────────────────────────┘
                   │ Reflection Engine
                   ▼
┌─────────────────────────────────────────────────────────┐
│  WORKING MEMORY (WM)                                    │
│  Active context for current task                        │
│  "Currently debugging authentication issues"            │
└──────────────────┬──────────────────────────────────────┘
                   │ Pattern Detection
                   ▼
┌─────────────────────────────────────────────────────────┐
│  SEMANTIC MEMORY (SM)                                   │
│  Facts, rules, patterns extracted from episodes         │
│  "auth.py frequently has bugs"                         │
└──────────────────┬──────────────────────────────────────┘
                   │ Knowledge Graph (GraphRAG)
                   ▼
┌─────────────────────────────────────────────────────────┐
│  LONG-TERM MEMORY (LTM)                                 │
│  Consolidated knowledge, insights, wisdom               │
│  "Authentication module needs refactoring"              │
└─────────────────────────────────────────────────────────┘
```

**Key Components:**
- **Vector Store** (Qdrant/pgvector) - Semantic search across memories
- **Knowledge Graph** (PostgreSQL) - Entity relationships and connections
- **Reflection Engine** - LLM-powered insight extraction
- **Context Cache** (Redis) - Cost-aware caching layer
- **MCP Server** - IDE integration for Cursor, VSCode, Claude Desktop

---

## Comparison

| Feature | RAE | LangChain Memory | MemGPT | Chroma |
|---------|-----|------------------|---------|--------|
| Multi-layer memory | ✅ Full (4 layers) | ⚠️ Basic | ✅ Limited | ❌ |
| Auto-reflection | ✅ Yes | ❌ No | ⚠️ Limited | ❌ |
| Knowledge graph | ✅ GraphRAG | ❌ No | ❌ No | ❌ |
| Hybrid search | ✅ Vector + Graph | ⚠️ Vector only | ⚠️ Vector only | ⚠️ Vector only |
| MCP integration | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Multi-tenancy | ✅ Built-in | ❌ No | ❌ No | ⚠️ Manual |
| Self-hosted | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Production-ready | ✅ Yes | ⚠️ DIY | ⚠️ DIY | ✅ Yes |
| Cost optimization | ✅ Built-in cache | ❌ No | ❌ No | ❌ No |

---

## Core Features

### 🧠 Multi-Layer Memory Architecture
- **Episodic**: Chronological events and observations
- **Working**: Active context for current tasks
- **Semantic**: Extracted facts and patterns
- **Long-Term**: Consolidated knowledge and insights

### 🔍 Hybrid Search (Vector + Graph)
- Semantic similarity via embeddings
- Graph traversal for connected concepts
- BFS/DFS strategies for knowledge exploration
- Context synthesis from multiple sources

### 🔄 Reflection Engine
- Automatic insight extraction from episodes
- Pattern detection across memories
- LLM-powered knowledge consolidation
- Configurable reflection schedules

### 🔌 IDE Integration
- Model Context Protocol (MCP) server
- Works with Cursor, VSCode, Claude Desktop
- Save/search memories directly from your editor
- Auto-context injection

### 💰 Cost-Aware Caching
- Redis-based intelligent caching
- Embedding deduplication
- Budget tracking and alerts
- Compression for large contexts

### 🔒 Production-Ready
- Multi-tenant with Row Level Security (RLS)
- API authentication and rate limiting
- Health checks and monitoring
- Horizontal scaling support

### 🎯 LLM-Agnostic
- OpenAI, Anthropic, Google Gemini
- Ollama for local models
- Custom embedding models
- Pluggable architecture

---

## Installation

### Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory
cd RAE-agentic-memory

# Configure environment
cp .env.example .env
# Edit .env with your LLM API keys

# Start all services
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

### Manual Setup

```bash
# 1. Start infrastructure
cd infra
docker-compose up -d  # Postgres, Redis, Qdrant

# 2. Install Python dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r apps/memory_api/requirements.txt

# 3. Initialize database
make db-init

# 4. Run API server
uvicorn apps.memory_api.main:app --reload
```

### Python SDK

```bash
pip install rae-memory-sdk
```

```python
from rae_memory_sdk import MemoryClient

client = MemoryClient(
    api_url="http://localhost:8000",
    tenant_id="my-tenant",
    project_id="my-project"
)

# Store memory
await client.store_memory(
    content="User prefers TypeScript over JavaScript",
    layer="episodic",
    tags=["preference", "coding"]
)

# Query memory
results = await client.query_memory(
    query="What languages does the user prefer?",
    top_k=5
)

# Generate reflection
reflection = await client.generate_reflection()
```

---

## Components Overview

- **`apps/memory_api`** - Main FastAPI service exposing the memory engine
- **`apps/reranker-service`** - Optional re-ranking service for improved relevance
- **`sdk/python/rae_memory_sdk`** - Python client library
- **`integrations/mcp-server`** - Model Context Protocol server for IDEs
- **`integrations/ollama-wrapper`** - Local LLM integration
- **`tools/memory-dashboard`** - Streamlit dashboard for visualization
- **`infra/`** - Docker infrastructure (Postgres, Qdrant, Redis, monitoring)
- **`examples/`** - Real-world example projects
- **`eval/`** - Evaluation harness and test suite

---

## Documentation

- 📖 **[Getting Started Guide](docs/getting-started/)** - Installation and first steps
- 🏗️ **[Architecture Overview](docs/concepts/architecture.md)** - System design
- 🔧 **[API Reference](http://localhost:8000/docs)** - Interactive API docs
- 🎓 **[Tutorials](docs/guides/)** - Step-by-step guides
- 💡 **[Examples](examples/)** - Real-world use cases
- 🤝 **[Contributing](CONTRIBUTING.md)** - How to contribute

---

## Quick Examples

### Store and Query

```bash
# Store a memory
curl -X POST http://localhost:8000/v1/memory/store \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: demo-tenant" \
  -d '{
    "layer": "episodic",
    "content": "User asked about authentication best practices",
    "tags": ["security", "auth"]
  }'

# Query memories
curl -X POST http://localhost:8000/v1/memory/query \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: demo-tenant" \
  -d '{
    "query": "What security topics has user discussed?",
    "top_k": 5
  }'
```

### GraphRAG Hybrid Search

```python
from rae_memory_sdk import MemoryClient

client = MemoryClient()

# Hybrid search: Vector similarity + Graph traversal
results = await client.hybrid_search(
    query="authentication system architecture",
    use_graph=True,
    graph_depth=2,
    top_k=10
)

# Results include:
# - Semantically similar memories
# - Connected concepts from knowledge graph
# - Synthesized context from multiple sources
```

### IDE Integration (MCP)

1. Install MCP server:
```bash
cd integrations/mcp-server
pip install -e .
```

2. Configure Cursor/VSCode:
```json
{
  "mcpServers": {
    "rae-memory": {
      "command": "python",
      "args": ["-m", "rae_mcp_server"],
      "env": {
        "RAE_API_URL": "http://localhost:8000",
        "RAE_PROJECT_ID": "my-project"
      }
    }
  }
}
```

3. Use in your editor:
   - Save important context: "Remember this architectural decision"
   - Search memories: "What did we decide about the database schema?"
   - Auto-inject context: Relevant memories added to prompts

---

## Status & Roadmap

RAE is currently in **beta** and actively developed.

**Current Status:**
- ✅ Core memory layers (EM, WM, SM, LTM)
- ✅ Vector search with multiple backends
- ✅ Knowledge graph (GraphRAG)
- ✅ Reflection engine
- ✅ MCP server for IDEs
- ✅ Python SDK
- ✅ Multi-tenancy
- ✅ Docker deployment

**Coming Soon:**
- 🚧 Web dashboard enhancements
- 🚧 Advanced analytics
- 🚧 Plugin system
- 🚧 Multi-modal memories (images, audio)
- 🚧 Memory consolidation/pruning
- 🚧 Enterprise features (SSO, RBAC)



---

## Community & Support

- 📖 **[Documentation](docs/)** - Comprehensive guides
- 🐛 **[GitHub Issues](https://github.com/dreamsoft-pro/RAE-agentic-memory/issues)** - Bug reports and features
- 🤝 **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- 📧 **[Contact](mailto:lesniowskig@gmail.com)** - Direct support

---

## Contributing

We welcome contributions! Whether it's:
- 🐛 Bug reports
- ✨ Feature requests
- 📝 Documentation improvements
- 🔧 Code contributions

Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

### Quick Start for Contributors

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/RAE-agentic-memory
cd RAE-agentic-memory

# Install dev dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest

# Make changes and submit PR!
```

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

**What this means:**
- ✅ Free for commercial use
- ✅ Modify and distribute
- ✅ Patent grant included
- ⚠️ Must include copyright notice
- ⚠️ State significant changes

---

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Qdrant](https://qdrant.tech/) - Vector search engine
- [PostgreSQL](https://www.postgresql.org/) + [pgvector](https://github.com/pgvector/pgvector) - Database with vector support
- [Redis](https://redis.io/) - Caching layer
- [LangChain](https://www.langchain.com/) - LLM framework integration

**Author:** Grzegorz Leśniowski

---

⭐ **Star us on GitHub if RAE helps you build better AI agents!** ⭐

[⬆ Back to top](#-rae---reflective-agentic-memory-engine)
