# 🧠 RAE - Reflective Agentic-memory Engine

> Give your AI agents human-like memory: Learn, remember, and improve over time.

*Designed for enterprise-grade use, currently in v2.1.1 "Enterprise Ready" state.*

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://docs.docker.com/get-docker/)
[![Tests](https://img.shields.io/badge/tests-468%20passing-brightgreen.svg)]()
[![Tests Total](https://img.shields.io/badge/total-516%20unit%20tests-blue.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-69%25-green.svg)]())
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Version](https://img.shields.io/badge/version-2.1.0--enterprise-blue.svg)](docs/.auto-generated/status/STATUS.md)
[![Docs Automation](https://img.shields.io/badge/docs_automation-✓_healthy-brightgreen.svg)](docs/.auto-generated/metrics/DASHBOARD.md)

[📖 Documentation](#documentation) | [🚀 Quick Start](#quick-start-5-minutes) | [📊 Benchmarking](benchmarking/README.md) | [🔧 Troubleshooting](TROUBLESHOOTING.md) | [💬 Community](#community--support) | [🎯 Examples](#real-world-examples)

---

> 💡 **Reality Check**
>
> RAE has graduated to **"Enterprise Ready"** status with the release of v2.1.1.
> The critical gaps in authentication and cost control have been closed.
>
> **What works:**
> - ✅ **LLM Orchestrator**: Provider-agnostic architecture - use 0/1/N models with single/fallback strategies (NEW in v2.1.1)
> - ✅ **Full JWT Authentication**: Real signature verification and claim validation.
> - ✅ **Active Budget Enforcement**: Requests are blocked (HTTP 402) if budget is exceeded.
> - ✅ **Background Workers**: Fully operational Decay, Summarization, and Dreaming cycles.
> - ✅ **Core Features**: 4-layer memory, GraphRAG, Reflection Engine V2, Multi-tenancy.
> - ✅ **Optional Modules**: ML Service, Dashboard, Celery Workers (production-ready, 96+ tests, full docs)
>
> **What's maturing:** Test coverage (69% → 75% target), production deployment guides.
>
> **Production Ready For:**
> - ✅ Internal corporate tools (behind VPN/firewall)
> - ✅ Controlled cloud environments (with TLS termination at ALB/proxy)
> - ✅ Proof-of-concepts and team knowledge bases
>
> **Requires Additional Infrastructure For:**
> - ⚠️ Public internet deployment (add TLS, API gateway, WAF)
> - ⚠️ Regulated industries (additional controls needed)
>
> See [docs/.auto-generated/status/STATUS.md](docs/.auto-generated/status/STATUS.md) for implementation status, [TESTING_STATUS.md](docs/.auto-generated/status/TESTING_STATUS.md) for test coverage, and **[SECURITY.md](docs/compliance/layer-1-foundation/iso-42001/SECURITY.md) for honest security assessment**.

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
✅ **Mathematical intelligence layers** (Math-1: structure, Math-2: dynamics, Math-3: policy optimization)
✅ **Automatic insight extraction** via Reflection Engine V2 (Actor-Evaluator-Reflector pattern)
✅ **Hybrid search** - Vector similarity + Knowledge graph traversal (GraphRAG)
✅ **LLM Orchestrator** - Provider-agnostic: use any LLM (OpenAI, Claude, Gemini, local) or no LLM at all
✅ **Local-first capable** - Run entirely offline with local LLMs for complete data sovereignty
✅ **IDE integration** via Model Context Protocol (MCP)
✅ **Cost-aware caching** to minimize LLM API costs
✅ **Enterprise Security** with RBAC, authentication, and audit logging
✅ **Mathematical Foundations** - Rigorous MDP formalization for decision-making

#### How RAE Works: A Complete System

RAE is **not just a vector database** or **simple RAG system**. It's a complete cognitive architecture that combines:

**🧠 4-Layer Memory System (Cognitive Architecture)**
```
Sensory Memory → Working Memory → Long-Term Memory → Reflective Memory
   (raw)         (active task)      (facts+events)    (meta-learnings)
```
Each layer serves a distinct cognitive function, similar to human memory systems.

**🔢 3-Tier Mathematical Foundation (Decision Intelligence)**
```
Math-1: Structure Analysis    →  How memory looks (graph topology, coherence)
Math-2: Dynamics Tracking      →  How memory evolves (drift, retention, quality)
Math-3: Policy Optimization    →  What decisions to make (cost-quality tradeoffs)
```
These layers work **above** the 4 memory layers, continuously monitoring and optimizing the system.

**🔍 Hybrid Search Engine (Beyond Simple RAG)**

Traditional RAG systems use only vector similarity. RAE combines:
- **Vector search** - Semantic similarity (dense embeddings via Qdrant/pgvector)
- **Sparse vectors** - Keyword matching (BM25-style sparse embeddings)
- **Graph traversal** - Knowledge connections (BFS exploration of semantic graph)
- **Full-text search** - Exact phrase matching (PostgreSQL FTS)
- **Query analysis** - LLM-powered intent classification for adaptive weighting

**Why this matters:** A query like "authentication bug from last week" needs temporal reasoning (graph),
exact keywords ("bug"), and semantic understanding - not just vector similarity.

**🎭 LLM Orchestrator (Optional Intelligence)**

RAE can operate in multiple modes:
- **Zero-LLM Mode** - Pure mathematical/heuristic decisions (fastest, zero API cost)
- **Single-LLM Mode** - One model for all tasks (simple, cost-effective)
- **Multi-LLM Mode** - Specialized models for different tasks (optimal quality)
- **Local-First Mode** - Ollama/local models only (complete data sovereignty)

This means you can run RAE entirely **offline** with local LLMs, or use cloud models, or mix both.

**🏗️ Why This Is Not a "Simple RAG System"**

| Feature | Traditional RAG | RAE |
|---------|----------------|-----|
| **Memory Model** | Flat vector store | 4-layer cognitive architecture |
| **Search** | Vector similarity only | Hybrid: Vector + Graph + Sparse + FTS |
| **Learning** | Static (no adaptation) | Active learning via reflection + drift detection |
| **Decision Making** | Threshold-based | MDP-based with reward optimization |
| **Knowledge Graph** | None or separate | Integrated with temporal evolution tracking |
| **Cost Control** | Manual or none | Built-in budget enforcement + caching |
| **Offline Capable** | Usually cloud-only | Fully local-first with Ollama |
| **Mathematical Foundation** | Heuristics | 3-tier formal mathematical model |

**🔒 Local-First Deployment (Data Sovereignty)**

For organizations requiring complete data separation (healthcare, government, regulated industries),
RAE can run **entirely offline**:
- Local LLMs via Ollama (Llama 3, Mistral, Qwen)
- Self-hosted vector database (Qdrant)
- Local PostgreSQL database
- No external API calls

See [Local Setup Guide](docs/LOCAL_SETUP.md) for complete offline deployment.

**📊 Real-World Example**

```
User Query: "Show me architectural decisions from auth module"

Traditional RAG:
  → Vector search for "architectural decisions auth"
  → Returns: Top-k similar documents
  → Problem: Misses connected concepts, temporal context, keyword precision

RAE:
  1. Query Analyzer classifies intent: "factual + temporal + relational"
  2. Math-1 analyzes graph structure around "auth module" node
  3. Hybrid Search executes:
     - Vector search: Semantic similarity to "architectural decisions"
     - Graph traversal: BFS from "auth module" (depth=2)
     - Sparse vectors: Keyword match "architectural" AND "auth"
     - Full-text: Exact phrase "architectural decisions"
  4. Math-2 checks memory drift (are results still relevant?)
  5. Math-3 optimizes retrieval (balance quality vs. cost)
  6. Context Builder assembles working memory with reflections
  → Returns: Precise results with temporal context + related decisions
```

**Key Insight:** RAE makes intelligent decisions about **how to search**, **what to remember**, and **when to learn** -
not just "retrieve similar vectors."

---

## Mathematical Foundations

RAE is built on rigorous mathematical principles using **Markov Decision Process (MDP)** formalism:

**MDP = (S, A, T, R, γ)** where:
- **S**: State space - Complete memory system state (working context, memory layers, budget, graph)
- **A**: Action space - 12 distinct operations (retrieve, prune, reflect, update graph, etc.)
- **T**: Transition function - Deterministic state transitions
- **R**: Reward function - Quality metrics for decision evaluation
- **γ**: Discount factor - Future reward consideration

### Key Mathematical Components

**🔹 Information Bottleneck Principle**
Optimal context selection via: `Minimize: I(Z; X) - β · I(Z; Y)`
- Balances relevance (I(Z;Y)) with compression (I(Z;X))
- Adaptive β parameter for query-specific optimization

**🔹 Graph Update Operator**
Knowledge graph evolution: `G_{t+1} = T(G_t, o_t, a_t)`
- Temporal decay: `w(t) = w_0 · exp(-Δt / τ)`
- Convergence analysis with spectral gap metrics
- Entity resolution and duplicate merging

**🔹 Reward-Guided Learning**
Action evaluation: `R(s_t, a_t, s_{t+1}) = w_q · Quality(a_t) - w_c · Cost(a_t)`
- Quality metrics by action type
- Budget-aware cost penalties
- Performance tracking over episodes

📖 **[Complete Mathematical Documentation](docs/reference/architecture/rae-mathematical-formalization.md)**

**Implementation:** `apps/memory_api/core/` (126 tests, 100% pass rate)

---

## Choosing Your Deployment

RAE offers three deployment profiles to match your needs:

### 💡 RAE Lite (Start Here)
**Perfect for:**
- Developers trying RAE for the first time
- Small teams (1-10 users)
- Limited infrastructure (VPS, laptop)
- Prototypes and proof-of-concepts

**Includes:** Core API, GraphRAG, Cost Tracking (4 services, 4 GB RAM)

### 🚀 RAE Standard (Production Ready)
**Perfect for:**
- Mid-size teams (10-100 users)
- Production deployments
- Companies needing ML features

**Includes:** Everything in Lite + ML Service, Reranker, Dashboard (9 services, 8 GB RAM)

### ☸️ RAE Enterprise (High Availability)
**Perfect for:**
- Large organizations (100+ users)
- Mission-critical applications
- Auto-scaling requirements

**Includes:** Everything + Kubernetes, Monitoring, Auto-scaling (15+ services, auto-scaling)

**Recommendation:** Start with RAE Lite to evaluate, then upgrade as needed.

---

## 🔒 ISO/IEC 42001 Compliance

RAE is designed for enterprise AI governance and compliance with **ISO/IEC 42001** (AI Management System).

### Key Compliance Features ✅

- **Risk Management** - Comprehensive [Risk Register](docs/reference/iso-security/RAE-Risk-Register.md) with 10 identified risks, all fully mitigated
- **Data Governance** - Source trust scoring, provenance tracking, and retention policies per tenant
- **GDPR Compliance** - Full "right to be forgotten" (Article 17) with cascade deletion and audit trail
- **Roles & Responsibilities** - Clear RACI matrix for 6 organizational roles ([docs/reference/iso-security/RAE-Roles.md](docs/reference/iso-security/RAE-Roles.md))
- **Audit Trail** - Complete logging of all data operations, deletions, and trust assessments
- **Multi-Tenant Isolation** - Database-level tenant isolation with PostgreSQL Row-Level Security
- **Human Oversight** - Risk-based approval workflow for high-risk operations with multi-approver support
- **Context Provenance** - Full query → context → decision lineage tracking with quality metrics
- **Graceful Degradation** - Circuit breaker pattern for service resilience and fallback modes
- **Policy Versioning** - Version control for governance policies with enforcement engine
- **Compliance Dashboard** - Real-time ISO 42001 monitoring with **100% compliance score**, 25+ metrics, risk visualization, and certification readiness

### Compliance Documentation

**4-Layer Compliance Architecture:**
- 📚 **[Compliance Overview](docs/compliance/README.md)** - Complete 4-layer compliance framework
- **Layer 1** - [ISO 42001 Foundation](docs/compliance/layer-1-foundation/README.md)
- **Layer 2** - [Regulatory Mapping](docs/compliance/layer-2-mapping/README.md) (NIST, HIPAA, FedRAMP, GDPR, AI Act)
- **Layer 3** - [Policy Packs](docs/compliance/layer-3-modules/README.md) (Modular compliance modules)
- **Layer 4** - [Runtime Enforcement](docs/compliance/layer-4-enforcement/README.md) (Guardrails, cost controllers)

**Key Documents:**
- 📋 **[RAE-ISO_42001.md](docs/compliance/layer-1-foundation/iso-42001/RAE-ISO_42001.md)** - Full ISO 42001 readiness assessment
- 🛡️ **[RAE-Risk-Register.md](docs/compliance/layer-1-foundation/iso-42001/RAE-Risk-Register.md)** - 10 risks (RISK-001 to RISK-010) with mitigation
- 👥 **[RAE-Roles.md](docs/compliance/layer-1-foundation/iso-42001/RAE-Roles.md)** - Organizational roles and RACI matrix
- 🔐 **[SECURITY.md](docs/compliance/layer-1-foundation/iso-42001/SECURITY.md)** - Security assessment and controls
- 🗺️ **[NIST AI RMF Mapping](docs/compliance/layer-2-mapping/iso42001-to-nist.md)** - Complete NIST AI RMF coverage (~97%)

### Implementation Status (2025-12-01)

| Feature | Status | Description |
|---------|--------|-------------|
| Source Trust Scoring | ✅ Implemented | Automatic reliability assessment for knowledge sources |
| Data Retention & Cleanup | ✅ Implemented | Per-tenant policies with automated cleanup workers |
| GDPR Right to Erasure | ✅ Implemented | User data deletion with full cascade and audit |
| Deletion Audit Trail | ✅ Implemented | Complete tracking of who/when/why for all deletions |
| PostgreSQL Row-Level Security | ✅ Implemented | Database-level tenant isolation with RLS policies |
| Roles & Responsibilities | ✅ Documented | Full RACI matrix for 6 roles |
| Risk Register | ✅ Complete | 10 risks identified, all fully mitigated |
| Compliance Dashboard | ✅ Implemented | ISO 42001 monitoring with 5 API endpoints + Prometheus metrics |
| Telemetry (Technical) | ✅ Implemented | OpenTelemetry + structured logging |
| Telemetry (Cognitive) | ✅ Implemented | Compliance dashboard + drift detection |
| **Human Approval Workflow** | ✅ Implemented | Risk-based routing, multi-approver support, timeout management (2025-12-01) |
| **Context Provenance** | ✅ Implemented | Full decision lineage tracking (query → context → decision) (2025-12-01) |
| **Graceful Degradation** | ✅ Implemented | Circuit breaker pattern + degraded mode service (2025-12-01) |
| **Policy Versioning** | ✅ Implemented | Version control + enforcement engine for governance policies (2025-12-01) |

**Legend:** ✅ Complete | 🟡 Partial | ⏳ Planned

🎉 **Status: 100% ISO/IEC 42001 Compliance Achieved (2025-12-01)**

> 💡 **For Regulated Industries:** RAE provides a strong foundation for AI governance. Additional controls may be required depending on your industry (healthcare, finance, etc.). See [RAE-ISO_42001.md](docs/reference/iso-security/RAE-ISO_42001.md) for details.

---

## Quick Start (< 5 minutes)

**Choose your deployment profile:**

| Profile | Best For | Resources | Command |
|---------|----------|-----------|---------|
| 💡 **RAE Lite** | Developers, testing, small teams (1-10 users) | 4 GB RAM, 2 CPU | `docker-compose -f docker-compose.lite.yml up -d` |
| 🔒 **Local First** | Privacy focused, offline capable (Ollama) | 16GB+ RAM | See [docs/LOCAL_SETUP.md](docs/LOCAL_SETUP.md) |
| 🚀 **Full Stack** | Production, mid-size teams (10-100 users) | 8 GB RAM, 4 CPU | `./scripts/quickstart.sh` |
| ☸️ **Enterprise** | Large orgs, auto-scaling, high availability | Auto-scaling | [Kubernetes Guide](docs/reference/deployment/kubernetes.md) |

**Not sure which to choose?** Start with RAE Lite - you can always upgrade later.

### 📦 Docker Images & Build Information

**Image Sizes (Full Stack):**
- **Main API** (rae-api, celery-worker, celery-beat): 9.23 GB
- **ML Service** (embeddings, NLP): 8.14 GB
- **Dashboard**: 690 MB
- **Total Disk Space**: ~18 GB (actual storage after layer deduplication)

**Build Time (on laptop):**
- **Initial build**: 8-10 minutes (downloads PyTorch, CUDA, ML models)
- **Rebuild with cache**: 1-2 minutes (only changed layers)
- **Docker layer caching**: Automatically preserves downloaded packages

**Optimization Tips:**
- Use `docker-compose build --parallel` to build images concurrently
- Docker BuildKit cache persists between builds (no re-download)
- See [Makefile.dev](Makefile.dev) for smart rebuild commands

### Full Stack (Recommended for Production)
**One-line install:**

```bash
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory && cd RAE-agentic-memory && ./scripts/quickstart.sh
```

### RAE Lite (Minimal - Perfect for Getting Started)

**Who is RAE Lite for?**
- 👨‍💻 **Developers** evaluating RAE or building prototypes
- 🔒 **Privacy-conscious users** running local LLMs (Ollama)
- 🧪 **Teams testing** RAE before full deployment
- 🏢 **Small teams** (1-10 users) with limited infrastructure
- 💰 **Resource-constrained** environments (VPS, single server)
- 🎓 **Learning** and experimenting with agentic memory

**What you get:**
- ✅ Core API with 4-layer memory architecture
- ✅ GraphRAG (knowledge graph + hybrid search)
- ✅ Cost tracking and governance
- ✅ PostgreSQL, Qdrant, Redis (all essential services)
- ❌ No ML Service, Dashboard, or Celery (optional components)

**Requirements:** 4 GB RAM (8GB+ for Local LLM), 2 CPU cores

**Quick start:**

```bash
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory
cd RAE-agentic-memory
cp .env.example .env
# Edit .env: Add API keys OR configure Ollama for local privacy (see docs/LOCAL_SETUP.md)
docker-compose -f docker-compose.lite.yml up -d

# Initialize database (first time only)
./scripts/init-database.sh
```

**Access your instance:**
- API: http://localhost:8000/docs
- Health: http://localhost:8000/health

**Having issues?** See [Troubleshooting Guide](TROUBLESHOOTING.md)

See [RAE Lite Profile Documentation](docs/reference/deployment/rae-lite-profile.md) for complete guide.

### ⚙️ Environment Configuration

**For Docker deployments (recommended):**
1. Copy the example environment file: `cp .env.example .env`
2. **Database credentials are pre-configured** - no changes needed for Docker!
3. Only add your **LLM API keys** (OpenAI, Anthropic, or Gemini)
4. Optional: Configure Ollama for local/offline LLMs (see [Local Setup](docs/LOCAL_SETUP.md))

**Default credentials (already in docker-compose.yml):**
- Database: `rae` / User: `rae` / Password: `rae_password`
- These work out-of-box with Docker - only change for production deployments
- For production: Update password in both `.env` and `docker-compose.yml`

**For local development (without Docker):**
- Match credentials in `.env` to your local PostgreSQL setup
- Ensure Redis is running on `localhost:6379`
- See [Development Guide](docs/DEVELOPMENT.md) for complete setup

---

**Or step by step (Full Stack):**

```bash
# 1. Clone the repository
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory
cd RAE-agentic-memory

# 2. Run quickstart script (handles everything!)
./scripts/quickstart.sh

# 3. Initialize database (first time only)
./scripts/init-database.sh

# 4. Seed demo data (optional - recommended)
python3 scripts/seed_demo_data.py
```

**Demo Data Scenarios:**

RAE includes two comprehensive demo scenarios (86 memories total):

📦 **Project Phoenix** - Software Development (40 memories)
- Software team building a microservices platform
- Incidents, circuit breakers, security audits
- All 4 memory layers: STM, EM, LTM, RM
- GraphRAG-ready with enriched cross-references and temporal chains

🏛️ **City Hall** - Public Administration (46 memories)
- Municipal customer service department
- Citizen requests, RODO compliance, ISO 42001
- Real-world governance scenarios with enriched relationships
- Polish language content for local government use case

**Load specific scenario:**
```bash
python3 scripts/seed_demo_data.py --scenario phoenix      # Only software dev
python3 scripts/seed_demo_data.py --scenario city-hall   # Only public admin
python3 scripts/seed_demo_data.py --scenario all          # Both (default)
```

That's it! 🎉

- **API Documentation**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501
- **Health Check**: http://localhost:8000/health

**Having issues?** See [Troubleshooting Guide](TROUBLESHOOTING.md)

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

RAE implements a **complete cognitive architecture** with multiple integrated layers:

### System Overview

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    RAE COGNITIVE ARCHITECTURE                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │         MATH-3: POLICY OPTIMIZATION (Decision Layer)             │    │
│  │  • What decisions to make (retrieval strategy, reflection timing)│    │
│  │  • Cost-Quality Frontier, Optimal Retrieval Ratio               │    │
│  └────────────────┬─────────────────────────────────────────────────┘    │
│                   │ Guides system behavior                                │
│  ┌────────────────┴─────────────────────────────────────────────────┐    │
│  │         MATH-2: DYNAMICS TRACKING (Evolution Layer)              │    │
│  │  • How memory evolves (drift, retention, degradation)            │    │
│  │  • Memory Drift Index, Retention Curves, Reflection Gain         │    │
│  └────────────────┬─────────────────────────────────────────────────┘    │
│                   │ Monitors quality                                      │
│  ┌────────────────┴─────────────────────────────────────────────────┐    │
│  │         MATH-1: STRUCTURE ANALYSIS (Topology Layer)              │    │
│  │  • How memory looks (graph connectivity, semantic coherence)     │    │
│  │  • Graph Connectivity Score, Semantic Coherence, Entropy         │    │
│  └────────────────┬─────────────────────────────────────────────────┘    │
│                   │ Analyzes structure                                    │
├───────────────────┴────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────┐          │
│  │  LAYER 4: REFLECTIVE MEMORY (Meta-Learnings)                │          │
│  │  "Authentication module needs architectural refactoring"     │          │
│  └──────────────────────────┬──────────────────────────────────┘          │
│                             │ Reflection Engine V2                        │
│  ┌──────────────────────────┴──────────────────────────────────┐          │
│  │  LAYER 3: LONG-TERM MEMORY (Facts + Events + Profiles)      │          │
│  │  Episodic: "User fixed auth bug" | Semantic: "auth.py prone"│          │
│  └──────────────────────────┬──────────────────────────────────┘          │
│                             │ Consolidation                               │
│  ┌──────────────────────────┴──────────────────────────────────┐          │
│  │  LAYER 2: WORKING MEMORY (Active Task Context)              │          │
│  │  "Currently debugging auth" + "Lessons: frequent bugs"      │          │
│  └──────────────────────────┬──────────────────────────────────┘          │
│                             │ Attention & Filtering                       │
│  ┌──────────────────────────┴──────────────────────────────────┐          │
│  │  LAYER 1: SENSORY MEMORY (Raw Inputs)                       │          │
│  │  "User clicked submit button"                                │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                       HYBRID SEARCH ENGINE                                 │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐            │
│  │ Vector Search│ Graph Travers│ Sparse Vector│ Full-Text    │            │
│  │ (Qdrant)     │ (PostgreSQL) │ (BM25-style) │ (PostgreSQL) │            │
│  │ Dense emb.   │ BFS/DFS      │ Keywords     │ Exact phrases│            │
│  └──────┬───────┴──────┬───────┴──────┬───────┴──────┬───────┘            │
│         └──────────────┴──────────────┴──────────────┘                    │
│                   Query Analyzer (Intent Classification)                   │
│                   Adaptive Weighting + Cache Layer                         │
└────────────────────────────────────────────────────────────────────────────┘
```

**What Makes RAE Different:**

1. **Mathematical Layers Work ABOVE Memory Layers** - Math-1/2/3 continuously monitor and optimize the 4 memory layers
2. **Hybrid Search = 4 Search Strategies Combined** - Not just vector similarity, but graph reasoning + keywords + exact matches
3. **Vector + Relational Database Integration** - Qdrant (vectors) + PostgreSQL (relations, graph, full-text) work together
4. **Optional LLM Orchestration** - Can run with zero LLMs (pure math), local LLMs, or cloud LLMs

**Key Components:**

### Microservices Architecture (v2.1)

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                          RAE Memory API (Port 8000)                            │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  API Layer (FastAPI) - REST + WebSocket endpoints                       │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │  Mathematical Layer Controller (Math-1/2/3) *(NEW in v2.2)*             │   │
│  │  • Math-1: Structure metrics  • Math-2: Drift tracking                 │   │
│  │  • Math-3: Policy optimization  • Decision-making for retrieval         │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │  Core Services (Business Logic)                                         │   │
│  │  • HybridSearchService + Cache  • QueryAnalyzer (LLM intent)            │   │
│  │  • ReflectionEngineV2 (Actor-Evaluator-Reflector)                       │   │
│  │  • TemporalGraph  • EntityResolution  • SemanticExtractor               │   │
│  │  • ContextBuilder (Working Memory assembly)                             │   │
│  │  • MemoryScoringV2 (α·relevance + β·importance + γ·recency)             │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │  Enterprise Services                                                    │   │
│  │  • RulesEngine (Event Automation)  • EvaluationService (MRR, NDCG)     │   │
│  │  • DriftDetector  • PIIScrubber  • CostController                       │   │
│  │  • DashboardWebSocket  • Analytics  • Evaluator (Outcome Assessment)   │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │  Background Workers (Celery + Redis Queue)                              │   │
│  │  • DecayWorker (importance decay)  • SummarizationWorker                │   │
│  │  • DreamingWorker (batch reflections)                                   │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │  Repositories (Data Access Layer - DAO Pattern)                         │   │
│  │  • MemoryRepository  • GraphRepository  • ReflectionRepository          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└──────────────┬───────────────────┬─────────────────┬────────────────────────────┘
               │                   │                 │
       ┌───────┴────────┐  ┌───────┴────────┐  ┌────┴──────────────────────────┐
       │                │  │                │  │                               │
       ▼                ▼  ▼                ▼  ▼                               ▼
┌──────────────────┐  ┌────────────────┐  ┌─────────────────────────────────────────┐
│ ML Service       │  │ Reranker       │  │      Storage Layer (Hybrid)             │
│ (Port 8001)      │  │ (Port 8002)    │  │  ┌─────────────────────────────────┐    │
│ ┌──────────────┐ │  │ ┌────────────┐ │  │  │  PostgreSQL (Relational)        │    │
│ │ • Entity Res.│ │  │ │CrossEncoder│ │  │  │  • Memory metadata (id, content)│    │
│ │ • Embeddings │ │  │ │Re-ranking  │ │  │  │  • pgvector (dense vectors)     │    │
│ │ • NLP Tasks  │ │  │ │Score boost│ │  │  │  • Knowledge graph (nodes+edges)│    │
│ │ • SpaCy/BERT │ │  │ │Precision   │ │  │  │  • Full-text search (FTS)       │    │
│ └──────────────┘ │  │ └────────────┘ │  │  │  • Row-Level Security (RLS)     │    │
└──────────────────┘  └────────────────┘  │  └─────────────────────────────────┘    │
                                          │  ┌─────────────────────────────────┐    │
                                          │  │  Qdrant (Vector Database)       │    │
                                          │  │  • Dense embeddings (768/1536d) │    │
                                          │  │  • Sparse vectors (BM25-style)  │    │
                                          │  │  • HNSW index for fast ANN      │    │
                                          │  │  • Tenant isolation via payload │    │
                                          │  └─────────────────────────────────┘    │
                                          │  ┌─────────────────────────────────┐    │
                                          │  │  Redis (Cache + Queue)          │    │
                                          │  │  • Query result cache (hybrid)  │    │
                                          │  │  • Celery task queue            │    │
                                          │  │  • Session state cache          │    │
                                          │  └─────────────────────────────────┘    │
                                          └─────────────────────────────────────────┘
```

**Integration Flow Example:**

```
Query: "authentication bug"
   ↓
1. Query Analyzer (LLM) → intent: "factual + technical"
   ↓
2. Math-3 Policy → decides: hybrid search (vector=0.4, graph=0.3, sparse=0.2, fts=0.1)
   ↓
3. Hybrid Search executes IN PARALLEL:
   ├─ Qdrant: Vector search (dense embedding) → 50 results
   ├─ PostgreSQL Graph: BFS from "authentication" node → 30 results
   ├─ Qdrant: Sparse vector (keyword match) → 40 results
   └─ PostgreSQL FTS: Full-text "authentication" AND "bug" → 20 results
   ↓
4. Result Fusion: Normalize scores → weighted combination → deduplicate
   ↓
5. Math-2 Drift Check: Filter stale memories (drift > threshold)
   ↓
6. Math-1 Structure Check: Verify graph coherence of results
   ↓
7. [Optional] Reranker: CrossEncoder re-ranks top-20
   ↓
8. Context Builder: Assemble Working Memory with reflections
   ↓
Returns: Top-k results with full context
```

**Architecture Highlights:**
- **Mathematical Intelligence Layer**: Math-1/2/3 continuously monitor and optimize all operations
- **Hybrid Storage**: PostgreSQL (relations, graph, FTS) + Qdrant (vectors) work as unified system
- **Vector + Relational Integration**: Single query leverages both vector similarity AND relational reasoning
- **Local-First Capable**: Run entirely offline with Ollama + self-hosted databases (complete data sovereignty)
- **Separation of Concerns**: DAO pattern isolates database operations from business logic
- **Microservices**: Heavy ML dependencies (PyTorch, transformers) isolated in separate services
- **Lightweight Main API**: Faster startup, smaller Docker images (~500MB vs 3-5GB)
- **Scalable**: ML and Reranker services can be scaled independently based on load
- **Clean Architecture**: Repository pattern, dependency injection, testable code
- **Enterprise Ready**: Built-in PII scrubbing, drift detection, cost control, event automation

**Core Services:**
- **HybridSearchService** - Multi-strategy search (vector, semantic, graph, fulltext) with caching
- **QueryAnalyzer** - LLM-powered query intent classification and dynamic weight calculation
- **ReflectionEngineV2** - Actor-Evaluator-Reflector pattern for automatic insight extraction *(NEW in v2.1)*
- **ContextBuilder** - Working Memory (Layer 2) construction with reflection injection *(NEW in v2.1)*
- **MemoryScoringV2** - Unified scoring: α·relevance + β·importance + γ·recency *(NEW in v2.1)*
- **Evaluator** - Execution outcome assessment (Deterministic, Threshold, LLM) *(NEW in v2.1)*
- **RulesEngine** - Event-driven automation with triggers, conditions, and actions
- **EvaluationService** - Search quality metrics (MRR, NDCG, Precision@K, Recall@K)
- **TemporalGraph** - Knowledge graph evolution tracking and time-travel queries
- **PIIScrubber** - Automatic PII detection and anonymization
- **DriftDetector** - Memory quality and semantic drift monitoring
- **DashboardWebSocket** - Real-time updates for dashboard visualization

**Background Workers (NEW in v2.1):**
- **DecayWorker** - Automatic importance decay with temporal logic
- **SummarizationWorker** - Session-based memory consolidation
- **DreamingWorker** - Batch reflection generation during idle periods

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
| Auto-reflection | ✅ Actor-Evaluator-Reflector | ❌ No | ⚠️ Limited | ❌ |
| Knowledge graph | ✅ GraphRAG | ❌ No | ❌ No | ❌ |
| Hybrid search | ✅ Vector + Graph | ⚠️ Vector only | ⚠️ Vector only | ⚠️ Vector only |
| Multi-model LLM | ✅ 7 providers | ⚠️ Manual | ⚠️ Limited | ❌ |
| MCP integration | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Multi-tenancy | ✅ Built-in | ❌ No | ❌ No | ⚠️ Manual |
| RBAC & Auth | ✅ Enterprise | ❌ No | ❌ No | ⚠️ Basic |
| Audit logging | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Memory decay | ✅ Automated workers | ❌ No | ⚠️ Manual | ❌ No |
| Self-hosted | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Production-ready | ⚠️ Pre-1.0 | ⚠️ DIY | ⚠️ DIY | ✅ Yes |
| Cost optimization | ✅ Built-in cache | ❌ No | ❌ No | ❌ No |

---

## Core Features

### 🧠 Multi-Layer Memory Architecture (v2.1)
- **Layer 1 - Sensory**: Raw inputs and immediate observations (`layer=stm`, `memory_type=sensory`)
- **Layer 2 - Working**: Active task context with reflection injection (`layer=stm/em`, `memory_type=episodic`)
- **Layer 3 - Long-Term**: Episodic events + Semantic facts + User profiles (`layer=ltm/em`, `memory_type=episodic/semantic/profile`)
- **Layer 4 - Reflective**: Meta-learnings and strategies (`layer=rm`, `memory_type=reflection/strategy`)

See [MEMORY_MODEL.md](docs/reference/memory/MEMORY_MODEL.md) for complete layer mapping reference.

### 🔢 Three-Tier Mathematical Foundation

RAE's memory system is governed by three mathematical layers that work above the 4-layer memory architecture:

**Math-1: Memory Structure Mathematics** (Geometry of Information)
- **What it measures**: How memory looks - graph topology, semantic coherence, entropy
- **Key metrics**: Graph Connectivity Score, Semantic Coherence Score, Graph Entropy, Cluster Consistency
- **Purpose**: Ensures structural integrity and optimal knowledge organization

**Math-2: Memory Dynamics Mathematics** (Physics of Memory Evolution)
- **What it measures**: How memory changes - semantic drift, structural evolution, retention curves
- **Key metrics**: Memory Drift Index, Structural Drift, Retention Curve, Reflection Gain Score, Compression Fidelity
- **Purpose**: Tracks memory quality over time and prevents degradation

**Math-3: Memory Policy Mathematics** (Economics & Control Theory)
- **What it measures**: How to make decisions - which memories to strengthen, when to reflect, retrieval optimization
- **Key metrics**: Cost-Quality Frontier, Optimal Retrieval Ratio, Reflection Policy Efficiency
- **Purpose**: Optimizes decision-making while controlling costs and maintaining quality

These mathematical layers enable RAE to be stable, adaptive, predictable, and cost-efficient. See [Mathematical Layer Overview](docs/project-design/active/MATH_LAYER_OVERVIEW.md) for complete specification.

### 🔍 Hybrid Search 2.0 (GraphRAG)
- **Multi-Strategy Search**: Vector similarity, Semantic nodes, Graph traversal, Full-text
- **Query Analyzer**: LLM-powered intent classification and dynamic weight calculation
- **Graph Traversal**: BFS graph exploration for discovering connected concepts (GraphRAG)
- **LLM Re-ranking**: Optional re-ranking with Claude/GPT for contextual relevance
- **Intelligent Caching**: Hash-based cache with temporal windowing for performance
- **Adaptive Weighting**: Automatically adjusts search strategy weights based on query intent

See [Hybrid Search Documentation](docs/reference/services/HYBRID_SEARCH.md) for detailed implementation guide, architecture, and API usage examples.

### 🔄 Reflection Engine V2 (Actor-Evaluator-Reflector Pattern) *(NEW in v2.1)*
- **Automatic Evaluation**: Deterministic and threshold-based outcome assessment
- **Failure Analysis**: LLM-powered reflection on errors and failures
- **Success Patterns**: Extract learnings from successful executions
- **Context Integration**: Reflections automatically injected into Working Memory
- **Configurable Modes**: Lite mode (disabled) vs Full mode (enabled)
- **Background Workers**: Decay, Summarization, Dreaming for automated lifecycle

See [REFLECTIVE_MEMORY_V1.md](docs/project-design/rae-4layer-design/REFLECTIVE_MEMORY_V1.md) for complete implementation guide.

### 🤖 LLM Orchestrator - Multi-Model Flexibility (v2.1.1)

**Decouples RAE from any specific LLM provider** - use 0, 1, or N models simultaneously!

#### Orchestrator Modes
- **Single Mode**: One LLM per request (simple, fast, cost-effective)
- **Fallback Mode**: Primary + backup model for high availability
- **Ensemble Mode** *(coming soon)*: Multiple models collaborate for improved quality
- **No-LLM Mode**: RAE works without any LLM (rule-based fallbacks)

#### Configuration-Driven
```yaml
# apps/llm/config/llm_config.yaml
default_strategy: single

models:
  - id: openai_gpt4o
    provider: openai
    model_name: gpt-4o
    enabled: true
    roles: [general, reflection, coding]
    cost_weight: 1.0

  - id: local_llama3
    provider: ollama
    model_name: llama3
    enabled: true
    roles: [low_cost, offline]
    cost_weight: 0.0

strategies:
  default:
    mode: single
    primary: openai_gpt4o

  summaries:
    mode: fallback
    primary: openai_gpt4o_mini
    fallback: local_llama3
```

#### Supported Providers
- **OpenAI** (GPT-4, GPT-3.5, O1)
- **Anthropic** (Claude 3.x, Claude 3.7)
- **Google** (Gemini 1.5 Pro, Flash)
- **DeepSeek** (Coder, Chat)
- **Qwen** (Alibaba Cloud)
- **Grok** (xAI)
- **Ollama** (Local models: Llama, Mistral, Qwen)

#### Benefits
- ✅ **Provider Independence**: Switch models without code changes
- ✅ **Cost Optimization**: Route queries to cheaper models based on complexity
- ✅ **High Availability**: Automatic fallback on provider failures
- ✅ **Privacy Options**: Use local models (Ollama) for sensitive data
- ✅ **Testing**: Compare model quality side-by-side
- ✅ **Future-Proof**: Add new providers via simple configuration

See [LLM Orchestrator Documentation](docs/project-design/active/LLM_orchestrator/LLM_ORCHESTRATOR.md) for complete guide.

### 🔒 Enterprise Security & Access Control (v2.0)

**Production-ready security implementation with comprehensive access control:**

#### Authentication & Authorization
- **Dual Authentication**: API Key and JWT token support
- **Unified Auth System**: Consistent `verify_token()` across all endpoints
- **Flexible Configuration**: Enable/disable auth methods per deployment
- **Token Management**: JWT with expiration, refresh, and validation

#### Role-Based Access Control (RBAC)
- **5-Tier Role Hierarchy**: Owner → Admin → Developer → Analyst → Viewer
- **Granular Permissions**: Action-level control (read, write, delete, manage)
- **Permission Matrix**: 20+ distinct permissions across resources
- **Role Hierarchy**: Lower roles cannot escalate privileges
- **Time-Limited Access**: Roles can expire automatically
- **Project-Level Restrictions**: Optional fine-grained project access

#### Tenant Isolation
- **Strict Tenant Boundaries**: Query-level filtering on all operations
- **Explicit Access Required**: Users must be assigned to tenants
- **No Tenant Enumeration**: UUID-based tenant identification
- **Cross-Tenant Protection**: All access attempts validated and logged

#### Audit & Compliance
- **Comprehensive Audit Logs**: All access attempts logged with IP and user agent
- **Access Denial Tracking**: Failed attempts logged with reasons
- **Role Assignment History**: Complete audit trail of role changes
- **GDPR-Ready**: Audit logs support compliance requirements

#### Memory Lifecycle Management *(Enhanced in v2.1)*
- **Enterprise Decay Worker**: Automated importance decay with temporal logic
- **Summarization Worker**: Session-based memory consolidation
- **Dreaming Worker**: Batch reflection generation during idle periods
- **Configurable Schedules**: Cron-based scheduling for all workers
- **Multi-Tenant Support**: Processes all tenants in batch

#### Security Features
- **Database-Backed RBAC**: PostgreSQL storage with migrations
- **FastAPI Dependencies**: Easy endpoint protection patterns
- **Rate Limiting**: Configurable request limits per user/tenant
- **CORS Protection**: Restrictable origin configuration
- **Secrets Management**: Environment-based configuration

**Documentation:**
- **[Security Overview](docs/compliance/layer-1-foundation/iso-42001/SECURITY.md)** - **Honest "Almost Enterprise" assessment** with deployment patterns
- [RBAC Guide](docs/reference/iso-security/security/RBAC.md) - Role-based access control details
- [Migration Guide](CHANGELOG.md) - Upgrading to v2.0 security
- [Configuration Reference](docs/reference/deployment/CONFIG_REFLECTIVE_MEMORY.md) - Feature flags and production recommendations

**Configuration:**
```bash
# Authentication
ENABLE_API_KEY_AUTH=true
ENABLE_JWT_AUTH=false

# Reflective Memory V2.1
REFLECTIVE_MEMORY_ENABLED=true
REFLECTIVE_MEMORY_MODE=full  # "lite" or "full"

# Memory Decay Worker
MEMORY_IMPORTANCE_DECAY_ENABLED=true
MEMORY_IMPORTANCE_DECAY_RATE=0.01  # 1% per day
MEMORY_IMPORTANCE_DECAY_SCHEDULE="0 2 * * *"  # Daily at 2 AM
```

### 🏢 Enterprise Features

#### Observability & Monitoring
- **OpenTelemetry Distributed Tracing**: Deep visibility into all operations
  - Auto-instrumentation (FastAPI, PostgreSQL, Redis, Celery, HTTP)
  - Custom spans for mathematical core, services, and API endpoints
  - Multi-backend export (Jaeger, Grafana Tempo, Elastic APM, AWS X-Ray)
  - Standardized `rae.*` namespace for all trace attributes
- **Prometheus Metrics**: Comprehensive performance metrics
  - API latency and throughput (request_latency, request_duration)
  - Cache efficiency (cache_hits, cache_misses, hit_ratio)
  - LLM usage and costs (token_usage, llm_cost by model/provider)
  - System health (memory, CPU, connection pools)
- **Grafana Dashboard**: Pre-built visualization with 20+ panels
- **Trace Context Propagation**: W3C TraceContext for distributed systems
- **Zero Configuration**: Works out of the box with sensible defaults
- **Production Ready**: Sampling, filtering, multi-tenant tracking

See **[Observability Documentation](docs/reference/deployment/observability.md)** for setup and deployment guides.

#### Event Automation & Rules Engine
- **Event-Driven Triggers**: React to memory creation, reflections, threshold breaches
- **Complex Conditions**: AND/OR logic with nested condition groups
- **Rate Limiting**: Per-trigger execution limits and cooldown periods
- **Action Execution**: Webhook calls, notifications, automated reflections
- **Retry Logic**: Automatic retries with exponential backoff

See [Rules Engine Documentation](docs/reference/services/RULES_ENGINE.md) for complete API reference, use cases, and integration examples.

#### Cost Control & Budget Management
- **Real-time Cost Tracking**: Track LLM API costs across all providers (OpenAI, Anthropic, Google)
- **Budget Enforcement**: Daily and monthly limits with automatic HTTP 402 responses when exceeded
- **Multi-tenant Isolation**: Per-tenant and per-project cost tracking
- **Budget Alerts**: Configurable thresholds (default: 80%, 95%) with notifications
- **Cost Analytics**: Detailed cost logs, usage trends, and optimization recommendations
- **Model Selection**: Cost-aware model selection based on budget availability

See [Cost Controller Documentation](docs/reference/concepts/cost-controller.md) for implementation details.

#### Quality & Monitoring
- **Evaluation Service**: Industry-standard IR metrics (MRR, NDCG, Precision@K, Recall@K, MAP)
- **Drift Detection**: Automatic detection of semantic drift in memory quality
- **PII Scrubbing**: Automatic detection and anonymization of sensitive data
- **Analytics Dashboard**: Real-time metrics and performance monitoring

See [Evaluation Service Documentation](docs/reference/services/EVALUATION_SERVICE.md) for metrics specifications and [Enterprise Services Overview](docs/reference/services/ENTERPRISE_SERVICES.md) for PII scrubbing, drift detection, and analytics implementation.

#### Temporal Knowledge Graph
- **Graph Snapshots**: Point-in-time graph state capture
- **Time Travel**: Query graph state at any historical moment
- **Change Tracking**: Complete audit trail of graph evolution
- **Growth Analytics**: Track knowledge graph expansion over time

See [Temporal Graph Service Documentation](docs/reference/services/ENTERPRISE_SERVICES.md#6-temporal-graph-service) for API usage and time-travel query examples.

#### Search Quality
- **A/B Testing**: Statistical comparison of search variants
- **Query Analysis**: Automatic query intent classification
- **Dynamic Weights**: Adaptive search strategy selection
- **Result Caching**: Intelligent caching with temporal windowing

See [Evaluation Service Documentation](docs/reference/services/EVALUATION_SERVICE.md) for A/B testing guide and [Hybrid Search Documentation](docs/reference/services/HYBRID_SEARCH.md) for query analysis and caching implementation.

### 🔌 IDE Integration

RAE provides two complementary integration methods:

| Integration | Protocol | Use Case | Documentation |
|-------------|----------|----------|---------------|
| **MCP Server** (IDE) | Model Context Protocol (JSON-RPC/STDIO) | AI assistant tools in Claude Desktop, Cursor, Cline | [docs/reference/integrations/mcp_protocol_server.md](docs/reference/integrations/mcp_protocol_server.md) |
| **Context Watcher** | HTTP + File Watcher | Automatic file sync to RAE memory | [docs/reference/integrations/context_watcher_daemon.md](docs/reference/integrations/context_watcher_daemon.md) |

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

See [Cost Controller Documentation](docs/reference/concepts/cost-controller.md) for detailed usage.

### 🔒 Production-Ready
- **Enterprise Security**: RBAC, authentication, tenant isolation (see section above)
- **Multi-tenant Architecture**: Complete tenant isolation with RLS
- **API Protection**: Authentication, rate limiting, CORS
- **Audit Logging**: Comprehensive access logs with IP tracking
- **Health Checks**: Built-in health and readiness endpoints
- **Horizontal Scaling**: Stateless API design for easy scaling
- **Database Migrations**: Version-controlled schema updates

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

# Quick start with Makefile (recommended)
make start              # Start all services
make logs               # View logs
make db-init            # Initialize database (first time)

# Or use docker-compose directly
docker-compose up -d

# Services will be available at:
# - Memory API: http://localhost:8000
# - ML Service: http://localhost:8001
# - Dashboard: http://localhost:8501

# Check health
curl http://localhost:8000/health
curl http://localhost:8001/health
```

### Local Development (with hot-reload)

For active development with instant code reloading:

```bash
# 1. Install Python dependencies
make install            # Core dependencies
# or
make install-all        # All dependencies including integrations

# 2. Start infrastructure only (Postgres, Redis, Qdrant)
docker-compose up -d postgres redis qdrant

# 3. Run API locally with hot-reload
make dev                # Starts uvicorn with --reload

# 4. Run tests during development
make test-focus FILE=apps/memory_api/tests/test_my_feature.py
```

**Development Commands:**
```bash
make help               # Show all available commands
make start              # Start all Docker services
make stop               # Stop all services
make restart            # Restart services
make logs               # View all logs
make logs-api           # View API logs only
make clean              # Clean up volumes and caches

# Development
make install            # Install dependencies
make dev                # Run with hot-reload
make format             # Format code (black, isort)
make lint               # Run linters (ruff, black)
make test               # Run all tests
make test-unit          # Run unit tests only
make test-focus         # Run specific test file

# Database
make db-init            # Initialize database
make db-migrate         # Run migrations
make db-reset           # Reset database (WARNING: deletes data)
```

See [Makefile](Makefile) for complete list of commands.

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

See [Kubernetes Deployment Guide](docs/reference/deployment/kubernetes.md) for complete documentation.

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

## Enterprise Core vs Optional Modules

RAE is designed with a modular architecture. Choose the components that fit your needs:

### Enterprise Core (Required) ✅

These components are required for RAE to function.

| Component | Description | Use Case |
|-----------|-------------|----------|
| **Core API** | Main memory engine with 4-layer architecture | All deployments |
| **PostgreSQL** | Primary database with pgvector | Data persistence |
| **Qdrant** | Vector database for semantic search | Memory retrieval |
| **Redis** | Cache and rate limiting | Performance optimization |
| **GraphRAG** | Knowledge graph with hybrid search | Contextual memory |
| **Governance API** | Cost tracking & budget management | Production deployments |

### Enterprise Extensions (Optional - Production Ready - GA) ✅

Production-ready components that enhance RAE but are not required.

| Component | Version | Description | When to Use |
|-----------|---------|-------------|-------------|
| **MCP Integration** | v1.2.0 | IDE integration (Cursor, VSCode, Claude Desktop) | Developer productivity & IDE workflows |
| **Reranker Service** | v1.0.0 | CrossEncoder-based result re-ranking | Improved search quality (10-20% accuracy boost) |
| **Context Watcher** | v1.0.0 | Automatic file change detection | Auto-sync to memory, live updates |
| **Reflection Engine V2** | v2.1.0 | Actor-Evaluator-Reflector pattern | Automated learning from failures/successes |

### Optional Modules (Beta/Experimental) ✅

**All modules are fully implemented, tested, and documented!**

| Component | Status | Tests | Docs | Description | When to Use |
|-----------|--------|-------|------|-------------|-------------|
| **[ML Service](apps/ml_service/README.md)** | 🟢 Ready | ✅ 43 tests (1308 lines) | ✅ Complete | Heavy ML operations (entity resolution, embeddings, NLP, triple extraction) | Advanced entity linking, local embeddings |
| **[Dashboard](tools/memory-dashboard/README.md)** | 🟢 Ready | ✅ 43 tests (608 lines) | ✅ Complete | Streamlit web UI for visualization & monitoring | Teams needing visual insights, real-time monitoring |
| **[Celery Workers](apps/memory_api/tasks/README.md)** | 🟢 Ready | ✅ 10 tests (334 lines) | ✅ Complete | Async background tasks (graph extraction, reflections, decay, pruning) | Automated workflows, scheduled maintenance |
| **[Prometheus + Grafana](infra/README.md)** | 🟢 Ready | N/A | ✅ Complete | Metrics collection and dashboards | Production monitoring, observability |

**Test Coverage:** 96+ test functions, 2250+ lines of test code
**Documentation:** 4 comprehensive README files + API docs

### Deployment Profiles

**RAE Lite** (Minimal):
- **Includes:** Enterprise Core only (API, PostgreSQL, Qdrant, Redis, GraphRAG, Governance)
- **Perfect for:** Development, testing, small teams (1-10 users)
- **Resources:** 4 GB RAM, 2 CPU cores
- **See:** [RAE Lite Profile Documentation](docs/reference/deployment/rae-lite-profile.md)

**RAE Standard** (Recommended):
- **Includes:** Enterprise Core + Enterprise Extensions (MCP, Reranker, Context Watcher, Reflection V2) + ML Service + Dashboard
- **Perfect for:** Production use, mid-size teams (10-100 users)
- **Resources:** 8 GB RAM, 4 CPU cores

**RAE Enterprise** (Full Stack):
- **Includes:** Enterprise Core + All Extensions + All Optional Modules + Kubernetes + Monitoring
- **Perfect for:** Large organizations, high availability, auto-scaling
- **Resources:** Auto-scaling with HPA (starts at 16 GB RAM)
- **See:** [Kubernetes Deployment Guide](docs/reference/deployment/kubernetes.md)

---

## Components Overview

### Core Services
- **`apps/memory_api`** - Main FastAPI service exposing the memory engine
- **[`apps/ml_service`](apps/ml_service/README.md)** - ML microservice (embeddings, entity resolution, NLP, triples)
- **`apps/memory_api/tasks`** - [Background tasks](apps/memory_api/tasks/README.md) (Celery workers for graph extraction, reflections, decay)
- **`apps/reranker-service`** - Optional re-ranking service for improved relevance

### Client SDKs & Integrations
- **`sdk/python/rae_memory_sdk`** - Python client library
- **`integrations/mcp/`** - Model Context Protocol (MCP) server for IDE integration
- **`integrations/context-watcher/`** - HTTP daemon for automatic file watching
- **`integrations/ollama-wrapper/`** - Local LLM integration
- **`integrations/langchain/`** - LangChain RAE retriever
- **`integrations/llama_index/`** - LlamaIndex RAE integration

### Tools & Infrastructure
- **[`tools/memory-dashboard`](tools/memory-dashboard/README.md)** - Streamlit dashboard for visualization & monitoring
- **[`infra/`](infra/README.md)** - Docker infrastructure (Postgres, Qdrant, Redis, Prometheus, Grafana)
- **`examples/`** - Real-world example projects
- **`eval/`** - Evaluation harness and test suite

---

## 🔬 Academic & Enterprise Benchmarking Suite

RAE includes a comprehensive benchmarking environment designed for both academic research and enterprise quality assurance:

### Quick Start

```bash
# Run quick smoke test (<10 seconds)
make benchmark-lite

# Run comprehensive evaluation (~30 seconds)
make benchmark-extended

# Run production-like test (~2 minutes)
make benchmark-industrial
```

### What's Included

- **3 Official Benchmark Sets**:
  - `academic_lite.yaml` - Fast validation (10 memories, 7 queries)
  - `academic_extended.yaml` - Thorough testing (50 memories, 20 queries, multi-domain)
  - `industrial_small.yaml` - Real-world simulation (100+ memories, "dirty data", edge cases)

- **Research-Grade Metrics**:
  - Quality: MRR (Mean Reciprocal Rank), Hit Rate @k, Precision, Recall, Semantic Similarity
  - Performance: Latency (avg, P95, P99), Throughput, Insert time
  - System Analysis: GraphRAG impact, Reflection engine effectiveness

- **Automated Tools**:
  - `run_benchmark.py` - Execute benchmarks with JSON + Markdown reports
  - `compare_runs.py` - A/B testing and regression detection
  - CI/CD integration with automatic smoke tests on PRs

### Example Results

Recent benchmark on `academic_extended`:
- **MRR**: 0.8456 ✅ (target: >0.70)
- **Hit Rate @5**: 0.9143 ✅ (91.4% queries found in top 5)
- **Avg Latency**: 45.67ms ✅ (P95: 78.45ms)
- **Overall Quality**: 0.8234 ✅ (weighted composite score)

### Documentation

- **[Quick Start Guide](benchmarking/BENCHMARK_STARTER.md)** - Get started in 3 minutes
- **[Report Template](benchmarking/BENCHMARK_REPORT_TEMPLATE.md)** - Standardized format for papers/reports
- **[Example Report](benchmarking/results/example_report.md)** - Reference implementation
- **[YAML Schema](benchmarking/sets/)** - Create custom benchmark sets

### Use Cases

- **Academic Research**: Reproducible results for papers and publications
- **Enterprise QA**: Pre-deployment validation and regression testing
- **CI/CD Integration**: Automated quality gates on pull requests
- **Performance Tracking**: Monitor metrics over time
- **A/B Testing**: Compare configurations and model changes

### CI/CD Integration

Benchmarks run automatically on:
- All pull requests (lite benchmark, 60s timeout)
- Pushes to `main` and `develop` branches
- Manual workflow dispatch for full test suites

Quality gates enforce minimum thresholds:
- MRR > 0.50
- Hit Rate @5 > 0.60
- Overall Quality > 0.55

See `benchmarking/BENCHMARK_STARTER.md` for complete documentation.

---

## Testing & Quality Assurance

RAE maintains **strong startup/scale-up level testing practices** - comparable to companies like Stripe, GitLab, and Vercel in their growth phase.

### Current Test Suite

- **~900 tests** across unit, integration, and performance layers
- **Multi-version testing:** Python 3.10, 3.11, 3.12
- **Smart test selection:** 90% CI cost reduction on feature branches (1-2 min vs 13 min full suite)
- **65% coverage minimum** with gap analysis and trending
- **Automated quality gates:**
  - Security scanning (Bandit)
  - Code quality (Ruff linting, mypy type checking)
  - Flaky test detection and quarantine
  - Performance drift detection with baseline tracking
  - Warning detection and monitoring

### CI/CD Pipeline

- **13-minute full test suite** (feature branches: 1-2 minutes with smart selection)
- **100% test pass rate** maintained via "main always green" policy
- **Automated smoke tests** on all pull requests
- **Benchmark quality gates** (MRR >0.50, Hit Rate @5 >0.60)
- **Auto-documentation** with CI-driven updates

### What This Means

**✅ Production-ready for:**
- Startups and scale-ups (10-500 employees)
- Internal tools and controlled environments
- Proof-of-concepts with solid foundations

**⚠️ Not Yet At:**
- Big Tech level (OpenAI, Anthropic, AWS) - requires 10-50 engineer QA teams and $M budgets
- This is realistic and appropriate for our stage

### Improvement Roadmap

We have a pragmatic 3-iteration plan to enhance testing quality:
- **Iteration 1 (1-2 weeks):** Performance benchmarking, load testing, structured logging
- **Iteration 2 (4-6 weeks):** Canary deployments, SLO tracking, enhanced security, ML testing
- **Iteration 3 (8-12 weeks):** Distributed tracing, advanced ML testing, chaos engineering

**See [Testing Improvement Roadmap](docs/TESTING_IMPROVEMENT_ROADMAP.md) for detailed plan.**

---

## Documentation

### 📋 Documentation Structure (Updated 2025-12-03)

RAE documentation is organized into four main areas:

1. **[`.auto-generated/`](docs/.auto-generated/)** - Automatically updated documentation
   - Status reports, test results, API specs, compliance reports
   - Updated by CI/CD pipelines

2. **[`compliance/`](docs/compliance/)** - ISO 42001 & 4-layer compliance framework
   - Layer 1: ISO 42001 foundation
   - Layer 2: Regulatory mappings (NIST, HIPAA, FedRAMP, GDPR, AI Act)
   - Layer 3: Policy packs (modular compliance modules)
   - Layer 4: Runtime enforcement (guardrails, cost controllers)

3. **[`operations/`](docs/operations/)** - Operational documentation
   - Security policies, runbooks, monitoring, maintenance

4. **[`project-design/`](docs/project-design/)** - Development planning
   - Active projects, completed work, research ideas

### Project Status & Progress
- 📊 **[Project Status](docs/.auto-generated/status/STATUS.md)** - Current implementation status and features
- ✅ **[TODO List](TODO.md)** - Upcoming features and improvements
- 🧪 **[Testing Status](docs/.auto-generated/status/TESTING_STATUS.md)** - Test coverage and quality metrics

### Testing & Benchmarking
- 📊 **[Benchmarking Suite Complete Guide](benchmarking/README.md)** - **⭐ START HERE** - Central hub for all 11 benchmarks
  - 5 Standard Benchmarks (v1) - academic_lite, academic_extended, industrial_small, stress_memory_drift, industrial_large
  - 6 Research Benchmarks (9/5) - LECT, MMIT, GRDT, RST, MPEB, ORB
  - 1,109+ memories | 164+ queries | 10,000+ cycle temporal testing
  - Decision tree, comparison matrix, telemetry guide
- 🧪 **[Testing Kit](docs/testing/RAE_TESTING_KIT.md)** - Complete guide to running tests and benchmarks
- 🚀 **[Quick Start: test_all_benchmarks.sh](benchmarking/test_all_benchmarks.sh)** - One command to test everything
- 📝 **[Report Template](docs/testing/BENCHMARK_REPORT_TEMPLATE.md)** - Standardized benchmark reporting

### Academic & Research
- 📄 **[Executive Summary](docs/outreach/EXEC_SUMMARY.md)** - 1-page RAE overview
- 🔬 **[Technical Abstract](docs/outreach/TECHNICAL_ABSTRACT.md)** - Detailed technical description
- 📧 **[Research Invitation](docs/outreach/RESEARCH_INVITATION_LETTER.md)** - Collaboration opportunities
- 📐 **[LaTeX Description](docs/outreach/LATEX_DESCRIPTION.md)** - Academic paper-ready content
- 💼 **[R&D Pitch](docs/outreach/RD_PITCH.md)** - Enterprise evaluation opportunity
- 💬 **[Quick Messages](docs/outreach/QUICK_MESSAGE.md)** - Templates for technical outreach

### Getting Started
- 📖 **[Getting Started Guide](docs/guides/developers/getting-started/)** - Installation and first steps
- 🚀 **[Quick Start](docs/guides/developers/getting-started/quickstart.md)** - 5-minute setup guide
- 🎓 **[Tutorials](docs/guides/)** - Step-by-step guides

### Architecture & Concepts
- 🏗️ **[Architecture Overview](docs/reference/concepts/architecture.md)** - System design and components
- 🧠 **[Memory Model](docs/reference/memory/MEMORY_MODEL.md)** - 4-layer memory architecture reference
- 🔄 **[Reflective Memory V1](docs/project-design/rae-4layer-design/REFLECTIVE_MEMORY_V1.md)** - Actor-Evaluator-Reflector pattern
- 🏛️ **[Repository Pattern](docs/reference/architecture/repository-pattern.md)** - Data access layer design
- 💰 **[Cost Controller](docs/reference/concepts/cost-controller.md)** - Budget management and cost tracking
- 🔍 **[Hybrid Search](docs/reference/concepts/)** - Multi-strategy search with GraphRAG

### Deployment
- 🐳 **[Docker Compose Setup](docs/guides/developers/getting-started/)** - Local development
- ☸️ **[Kubernetes Deployment](docs/reference/deployment/kubernetes.md)** - Enterprise production deployment
- 📊 **[Helm Chart Configuration](helm/rae-memory/README.md)** - Detailed Helm values reference

### API Documentation
- 🔧 **[REST API Reference](docs/reference/api/rest-api.md)** - Complete API documentation
- 📚 **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (when running)
- 🔌 **[IDE Integration Guide](docs/guides/IDE_INTEGRATION.md)** - Connect RAE with your IDE (Claude, Cursor, VSCode, etc.)
- 🔌 **[MCP Protocol Server](docs/reference/integrations/mcp_protocol_server.md)** - Technical MCP implementation details

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

## Status & Roadmap

RAE is currently in **v2.1.0-enterprise** - Pre-1.0 with Enterprise Features!

**Current Status (v2.1.1):**
- ✅ Core memory layers (4-layer architecture)
- ✅ Vector search with multiple backends
- ✅ Knowledge graph (GraphRAG)
- ✅ **LLM Orchestrator** (Multi-model flexibility: 0/1/N LLMs, single/fallback modes)
- ✅ **Reflection Engine V2** (Actor-Evaluator-Reflector pattern)
- ✅ **Memory Scoring V2** (Unified α·relevance + β·importance + γ·recency)
- ✅ **Context Builder** (Working Memory with reflection injection)
- ✅ **Background Workers** (Decay, Summarization, Dreaming)
- ✅ **Evaluator Interface** (Deterministic, Threshold, **LLM Evaluator**)
- ✅ **ML Service** (Production Ready: 43 tests, embeddings, entity resolution, NLP, triples)
- ✅ **Dashboard** (Production Ready: 43 tests, Streamlit UI for visualization)
- ✅ **Celery Background Tasks** (Production Ready: 10 tests, async workflows)
- ✅ Hybrid Multi-Strategy Search
- ✅ Event Triggers & Automation
- ✅ MCP server for IDEs
- ✅ Python SDK
- ✅ Multi-tenancy & RBAC
- ✅ Docker deployment
- ✅ **820+ Tests (100% passing), 69% Coverage** (target: 75%+)
- ✅ **CI/CD Pipeline** (lint, test, docker build - all passing ✅)

**Coming Soon (v1.0):**
- 🚧 Test coverage improvement (69% → 75%+)
- 🚧 Production deployment guides (Kubernetes, cloud providers)
- 🚧 Performance optimization (query latency, caching improvements)
- 🚧 Advanced monitoring dashboards (Grafana templates)

**Future (Post-1.0):**
- 🚧 Plugin system
- 🚧 Multi-modal memories (images, audio)
- 🚧 Memory consolidation/pruning optimization
- 🚧 Enterprise SSO integration

See [docs/.auto-generated/status/STATUS.md](docs/.auto-generated/status/STATUS.md) for detailed implementation status.

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
