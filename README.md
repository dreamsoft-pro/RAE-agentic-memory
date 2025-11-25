# 🧠 RAE - Reflective Agentic Memory Engine

> Give your AI agents human-like memory: Learn, remember, and improve over time.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://docs.docker.com/get-docker/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()
[![Build Status](https://img.shields.io/badge/build-stable-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Version](https://img.shields.io/badge/version-2.0.0--enterprise-blue.svg)](docs/VERSION_MATRIX.md)

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

**One-line install:**

```bash
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory && cd RAE-agentic-memory && ./scripts/quickstart.sh
```

Or step by step:

```bash
# 1. Clone the repository
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory
cd RAE-agentic-memory

# 2. Run quickstart script (handles everything!)
./scripts/quickstart.sh

# 3. Seed demo data (optional)
python3 scripts/seed_demo_data.py
```

That's it! 🎉

- **API Documentation**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501
- **Health Check**: http://localhost:8000/health

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
│  "User fixed bug in auth.py on Jan 5"                   │
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
│  "auth.py frequently has bugs"                          │
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

### Microservices Architecture (v2.0)

```
┌──────────────────────────────────────────────────────────────────────┐
│                      RAE Memory API (Port 8000)                      │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  API Layer (FastAPI)                                          │   │
│  ├───────────────────────────────────────────────────────────────┤   │
│  │  Core Services (Business Logic)                               │   │
│  │  • HybridSearchService + Cache  • QueryAnalyzer               │   │
│  │  • ReflectionEngine  • EntityResolution                       │   │
│  │  • TemporalGraph  • SemanticExtractor                         │   │
│  ├───────────────────────────────────────────────────────────────┤   │
│  │  Enterprise Services                                          │   │
│  │  • RulesEngine (Event Triggers)  • EvaluationService          │   │
│  │  • DriftDetector  • PIIScrubber  • CostController             │   │
│  │  • DashboardWebSocket  • Analytics                            │   │
│  ├───────────────────────────────────────────────────────────────┤   │
│  │  Repositories (Data Access Layer - DAO Pattern)               │   │
│  │  • GraphRepository  • MemoryRepository                        │   │
│  └───────────────────────────────────────────────────────────────┘   │
└────────────────────────┬──────────────────┬─────────────────────────┘
                         │                  │
          ┌──────────────┴────────┐    ┌────┴─────────┐
          │                       │    │              │
          ▼                       ▼    ▼              ▼
┌──────────────────────┐  ┌────────────────────┐  ┌──────────────────────┐
│ ML Service (8001)    │  │ Reranker (8002)    │  │   Storage Layer      │
│ ┌──────────────────┐ │  │ ┌────────────────┐ │  │ • PostgreSQL         │
│ │ ML Operations:   │ │  │ │ CrossEncoder   │ │  │   (pgvector + RLS)   │
│ │ • Entity Resol.  │ │  │ │ Re-ranking     │ │  │ • Qdrant Vector DB   │
│ │ • Embeddings     │ │  │ │ for improved   │ │  │ • Redis Cache        │
│ │ • NLP Processing │ │  │ │ search results │ │  │ • Celery (async)     │
│ └──────────────────┘ │  │ └────────────────┘ │  └──────────────────────┘
└──────────────────────┘  └────────────────────┘
```

**Architecture Highlights:**
- **Separation of Concerns**: DAO pattern isolates database operations from business logic
- **Microservices**: Heavy ML dependencies (PyTorch, transformers) isolated in separate services
- **Lightweight Main API**: Faster startup, smaller Docker images (~500MB vs 3-5GB)
- **Scalable**: ML and Reranker services can be scaled independently based on load
- **Clean Architecture**: Repository pattern, dependency injection, testable code
- **Enterprise Ready**: Built-in PII scrubbing, drift detection, cost control, event automation

**Core Services:**
- **HybridSearchService** - Multi-strategy search (vector, semantic, graph, fulltext) with caching
- **QueryAnalyzer** - LLM-powered query intent classification and dynamic weight calculation
- **ReflectionEngine** - Automatic insight extraction from episodic memories
- **RulesEngine** - Event-driven automation with triggers, conditions, and actions
- **EvaluationService** - Search quality metrics (MRR, NDCG, Precision@K, Recall@K)
- **TemporalGraph** - Knowledge graph evolution tracking and time-travel queries
- **PIIScrubber** - Automatic PII detection and anonymization
- **DriftDetector** - Memory quality and semantic drift monitoring
- **DashboardWebSocket** - Real-time updates for dashboard visualization

**Storage & Infrastructure:**
- **Vector Store** (Qdrant/pgvector) - Semantic search across memories
- **Knowledge Graph** (PostgreSQL) - Entity relationships with temporal tracking
- **ML Service** - Entity resolution, embeddings, NLP processing (isolated)
- **Reranker Service** - CrossEncoder-based result re-ranking for improved relevance
- **Context Cache** (Redis) - Cost-aware caching layer with hybrid search cache
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

### 🔍 Hybrid Search 2.0 (GraphRAG)
- **Multi-Strategy Search**: Vector similarity, Semantic nodes, Graph traversal, Full-text
- **Query Analyzer**: LLM-powered intent classification and dynamic weight calculation
- **Graph Traversal**: BFS graph exploration for discovering connected concepts (GraphRAG)
- **LLM Re-ranking**: Optional re-ranking with Claude/GPT for contextual relevance
- **Intelligent Caching**: Hash-based cache with temporal windowing for performance
- **Adaptive Weighting**: Automatically adjusts search strategy weights based on query intent

### 🔄 Reflection Engine
- Automatic insight extraction from episodes
- Pattern detection across memories
- LLM-powered knowledge consolidation
- Configurable reflection schedules

### 🏢 Enterprise Features

#### Event Automation & Rules Engine
- **Event-Driven Triggers**: React to memory creation, reflections, threshold breaches
- **Complex Conditions**: AND/OR logic with nested condition groups
- **Rate Limiting**: Per-trigger execution limits and cooldown periods
- **Action Execution**: Webhook calls, notifications, automated reflections
- **Retry Logic**: Automatic retries with exponential backoff

#### Cost Control & Budget Management
- **Real-time Cost Tracking**: Track LLM API costs across all providers (OpenAI, Anthropic, Google)
- **Budget Enforcement**: Daily and monthly limits with automatic HTTP 402 responses when exceeded
- **Multi-tenant Isolation**: Per-tenant and per-project cost tracking
- **Budget Alerts**: Configurable thresholds (default: 80%, 95%) with notifications
- **Cost Analytics**: Detailed cost logs, usage trends, and optimization recommendations
- **Model Selection**: Cost-aware model selection based on budget availability

See [Cost Controller Documentation](docs/concepts/cost-controller.md) for implementation details.

#### Quality & Monitoring
- **Evaluation Service**: Industry-standard IR metrics (MRR, NDCG, Precision@K, Recall@K, MAP)
- **Drift Detection**: Automatic detection of semantic drift in memory quality
- **PII Scrubbing**: Automatic detection and anonymization of sensitive data
- **Analytics Dashboard**: Real-time metrics and performance monitoring

#### Temporal Knowledge Graph
- **Graph Snapshots**: Point-in-time graph state capture
- **Time Travel**: Query graph state at any historical moment
- **Change Tracking**: Complete audit trail of graph evolution
- **Growth Analytics**: Track knowledge graph expansion over time

#### Search Quality
- **A/B Testing**: Statistical comparison of search variants
- **Query Analysis**: Automatic query intent classification
- **Dynamic Weights**: Adaptive search strategy selection
- **Result Caching**: Intelligent caching with temporal windowing

### 🔌 IDE Integration

RAE provides two complementary integration methods:

| Integration | Protocol | Use Case | Documentation |
|-------------|----------|----------|---------------|
| **MCP Server** (IDE) | Model Context Protocol (JSON-RPC/STDIO) | AI assistant tools in Claude Desktop, Cursor, Cline | [docs/integrations/mcp_protocol_server.md](docs/integrations/mcp_protocol_server.md) |
| **Context Watcher** | HTTP + File Watcher | Automatic file sync to RAE memory | [docs/integrations/context_watcher_daemon.md](docs/integrations/context_watcher_daemon.md) |

**Key Features**:
- **MCP Server**: Save/search memories directly from your editor, automatic context injection
- **Context Watcher**: Monitors file changes and automatically stores them in RAE
- **Works Together**: Use both for comprehensive context capture

### 💰 Cost Control & Budget Management
- **Real-time cost tracking** for all LLM providers (OpenAI, Anthropic, Google)
- **Budget enforcement** with daily/monthly limits (HTTP 402 when exceeded)
- **Multi-tenant cost isolation** for accurate per-project tracking
- **Redis-based intelligent caching** to minimize LLM API calls
- **Embedding deduplication** to avoid redundant computations
- **Budget alerts** and notifications at configurable thresholds

See [Cost Controller Documentation](docs/concepts/cost-controller.md) for detailed usage.

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

### Docker Compose (Recommended for Development)

```bash
# Clone repository
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory
cd RAE-agentic-memory

# Configure environment
cp .env.example .env
# Edit .env with your LLM API keys

# Start all services (including ML service)
docker-compose up -d

# Services will be available at:
# - Memory API: http://localhost:8000
# - ML Service: http://localhost:8001
# - Dashboard: http://localhost:8501

# Check health
curl http://localhost:8000/health
curl http://localhost:8001/health
```

### Kubernetes (Recommended for Production)

Enterprise-grade deployment with cost control, auto-scaling, and monitoring:

```bash
# Quick install
helm install rae-memory ./helm/rae-memory \
  --namespace rae-memory \
  --create-namespace \
  --set ingress.hosts[0].host=rae-api.yourdomain.com

# With cost control
helm install rae-memory ./helm/rae-memory \
  --namespace rae-memory \
  --set configMap.ENABLE_COST_TRACKING=true \
  --set configMap.DEFAULT_MONTHLY_LIMIT=500.00
```

**Features:**
- Auto-scaling (HPA) for API, ML Service, and Celery Workers
- Cost tracking and budget enforcement
- NetworkPolicy for security
- Prometheus monitoring with Grafana dashboards
- External Secrets Operator support
- TLS with cert-manager

See [Kubernetes Deployment Guide](docs/deployment/kubernetes.md) for complete documentation.

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
- **`integrations/mcp/`** - Model Context Protocol (MCP) server for IDE integration
- **`integrations/context-watcher/`** - HTTP daemon for automatic file watching
- **`integrations/ollama-wrapper/`** - Local LLM integration
- **`integrations/langchain/`** - LangChain RAE retriever
- **`integrations/llama_index/`** - LlamaIndex RAE integration
- **`tools/memory-dashboard`** - Streamlit dashboard for visualization
- **`infra/`** - Docker infrastructure (Postgres, Qdrant, Redis, monitoring)
- **`examples/`** - Real-world example projects
- **`eval/`** - Evaluation harness and test suite

---

## Documentation

### Project Status & Progress
- 📊 **[Project Status](STATUS.md)** - Current implementation status and features
- ✅ **[TODO List](TODO.md)** - Upcoming features and improvements
- 🧪 **[Testing Guide](TESTING.md)** - Test coverage, running tests, and writing new tests

### Getting Started
- 📖 **[Getting Started Guide](docs/getting-started/)** - Installation and first steps
- 🚀 **[Quick Start](docs/getting-started/)** - 5-minute setup guide
- 🎓 **[Tutorials](docs/guides/)** - Step-by-step guides

### Architecture & Concepts
- 🏗️ **[Architecture Overview](docs/concepts/architecture.md)** - System design and components
- 🏛️ **[Repository Pattern](docs/architecture/repository-pattern.md)** - Data access layer design
- 💰 **[Cost Controller](docs/concepts/cost-controller.md)** - Budget management and cost tracking
- 🔄 **[Reflection Engine](docs/concepts/)** - Automatic insight extraction
- 🔍 **[Hybrid Search](docs/concepts/)** - Multi-strategy search with GraphRAG

### Deployment
- 🐳 **[Docker Compose Setup](docs/getting-started/)** - Local development
- ☸️ **[Kubernetes Deployment](docs/deployment/kubernetes.md)** - Enterprise production deployment
- 📊 **[Helm Chart Configuration](helm/rae-memory/README.md)** - Detailed Helm values reference

### API Documentation
- 🔧 **[REST API Reference](docs/api/rest-api.md)** - Complete API documentation
- 📚 **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (when running)
- 🔌 **[MCP Integration](docs/integrations/mcp_protocol_server.md)** - IDE integration guide

### Examples & Use Cases
- 💡 **[Examples](examples/)** - Real-world use cases and code samples
- 🤝 **[Contributing](CONTRIBUTING.md)** - How to contribute to RAE

---

## Quick Examples

### Store and Query

```bash
# Store a memory
curl -X POST http://localhost:8000/v1/memories/create \
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

## Enterprise Features (v2.0)

RAE includes production-grade enterprise capabilities:

### 🎯 Hierarchical Reflection Engine
- **HDBSCAN Clustering** - Automatic memory grouping by semantic similarity
- **Meta-Insights** - Multi-level reflections (insight → meta-insight)
- **Cycle Detection** - Prevents circular reflection dependencies
- **Adaptive Scoring** - Novelty, importance, utility, confidence metrics

### 🧠 Semantic Memory System
- **Knowledge Extraction** - Automatic entity and concept extraction from memories
- **TTL/LTM Decay Model** - Time-based knowledge degradation with reinforcement
- **3-Stage Search** - Topic matching → Canonicalization → LLM re-ranking
- **Graph Integration** - Semantic nodes connected in knowledge graph

### 📊 Hybrid Search Engine
- **Query Intent Analysis** - LLM-powered classification (6 intent types)
- **Multi-Strategy Fusion** - Vector + Semantic + Graph + Full-text
- **Dynamic Weighting** - Auto-adjusts strategy weights based on query type
- **5 Weight Profiles** - Balanced, Quality, Speed, Comprehensive, Exploratory

### 📈 Evaluation & Monitoring Suite
- **IR Metrics** - MRR, NDCG@K, Precision@K, Recall@K, MAP
- **Drift Detection** - Kolmogorov-Smirnov test, PSI, severity classification
- **A/B Testing** - Compare search strategies and configurations
- **Quality Alerts** - Automatic degradation detection

### ⚡ Event Triggers & Automation
- **Rules Engine** - Complex condition evaluation (AND/OR logic, 12 operators)
- **13 Event Types** - Memory lifecycle, quality changes, drift detection
- **12 Action Types** - Notifications, webhooks, reflections, evaluations
- **Workflow Orchestration** - Multi-step automation with dependencies
- **Rate Limiting & Cooldowns** - Prevent trigger spam

### 📱 Real-time Dashboard
- **WebSocket Updates** - Live metrics, events, and health monitoring
- **6 Visualizations** - Reflection tree, semantic graph, timelines, quality trends
- **System Health** - Component-level monitoring with recommendations
- **Activity Logs** - Real-time event feed with severity levels

### 🔌 Enhanced API Client
- **Circuit Breaker** - Prevents cascading failures (CLOSED, OPEN, HALF_OPEN states)
- **Exponential Backoff** - Intelligent retry logic with configurable parameters
- **Response Caching** - TTL-based caching for GET requests
- **Error Classification** - 6 error categories for targeted handling
- **Connection Pooling** - HTTP/2 support with configurable limits
- **Statistics Tracking** - Success rates, cache hit rates, performance metrics

### 📚 Graph Repository Enhancements
- **Temporal Graphs** - Time-based node and edge validity
- **Weighted Edges** - Confidence-based relationship strength
- **Advanced Algorithms** - Dijkstra shortest path, DFS cycle detection
- **Graph Snapshots** - Point-in-time graph state capture

## Status & Roadmap

RAE is currently in **v2.0** - Production Ready!

**Current Status:**
- ✅ Core memory layers (EM, WM, SM, LTM)
- ✅ Vector search with multiple backends
- ✅ Knowledge graph (GraphRAG)
- ✅ **Hierarchical Reflection Engine** (v2.0)
- ✅ **Semantic Memory with TTL/LTM** (v2.0)
- ✅ **Hybrid Multi-Strategy Search** (v2.0)
- ✅ **Evaluation Suite** (v2.0)
- ✅ **Event Triggers & Automation** (v2.0)
- ✅ **Real-time Dashboard** (v2.0)
- ✅ **Enhanced API Client** (v2.0)
- ✅ MCP server for IDEs
- ✅ Python SDK
- ✅ Multi-tenancy
- ✅ Docker deployment
- ✅ **184 Tests (94.6% pass rate), 57% Coverage** (v2.0)
- ✅ **CI/CD Pipeline** (lint, test, docker build - all passing ✅ 2025-11-25)

**Coming Soon:**
- 🚧 Plugin system
- 🚧 Multi-modal memories (images, audio)
- 🚧 Memory consolidation/pruning
- 🚧 Enterprise SSO/RBAC



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
