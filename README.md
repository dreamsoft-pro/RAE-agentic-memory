# 🧠 RAE - Reflective Agentic-memory Engine

> Give your AI agents human-like memory: Learn, remember, and improve over time.

*Designed for enterprise-grade use, currently in v2.1.1 "Enterprise Ready" state.*

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://docs.docker.com/get-docker/)
[![Tests](https://img.shields.io/badge/tests-197%20passing-brightgreen.svg)]()
[![Tests Total](https://img.shields.io/badge/total-238%20unit%20tests-blue.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-48%25-yellow.svg)]())
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Version](https://img.shields.io/badge/version-2.1.0--enterprise-blue.svg)](STATUS.md)

[📖 Documentation](#documentation) | [🚀 Quick Start](#quick-start-5-minutes) | [🔧 Troubleshooting](TROUBLESHOOTING.md) | [💬 Community](#community--support) | [🎯 Examples](#real-world-examples)

---

> 💡 **Reality Check**
>
> RAE has graduated to **"Enterprise Ready"** status with the release of v2.1.1.
> The critical gaps in authentication and cost control have been closed.
>
> **What works:**
> - ✅ **Full JWT Authentication**: Real signature verification and claim validation.
> - ✅ **Active Budget Enforcement**: Requests are blocked (HTTP 402) if budget is exceeded.
> - ✅ **Background Workers**: Fully operational Decay, Summarization, and Dreaming cycles.
> - ✅ **Core Features**: 4-layer memory, GraphRAG, Reflection Engine V2, Multi-tenancy.
>
> **What's maturing:** ML service (beta), dashboard (beta), test coverage (target: 75%).
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
> See [STATUS.md](STATUS.md) for implementation status, [TESTING_STATUS.md](docs/TESTING_STATUS.md) for test coverage, and **[SECURITY.md](docs/SECURITY.md) for honest security assessment**.

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
✅ **Automatic insight extraction** via Reflection Engine V2 (Actor-Evaluator-Reflector pattern)
✅ **Graph-based knowledge connections** (GraphRAG)
✅ **IDE integration** via Model Context Protocol (MCP)
✅ **Cost-aware caching** to minimize LLM API costs
✅ **Enterprise Security** with RBAC, authentication, and audit logging

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

- **Risk Management** - Comprehensive [Risk Register](docs/RAE-Risk-Register.md) with 10 identified risks, all fully mitigated
- **Data Governance** - Source trust scoring, provenance tracking, and retention policies per tenant
- **GDPR Compliance** - Full "right to be forgotten" (Article 17) with cascade deletion and audit trail
- **Roles & Responsibilities** - Clear RACI matrix for 6 organizational roles ([docs/RAE-Roles.md](docs/RAE-Roles.md))
- **Audit Trail** - Complete logging of all data operations, deletions, and trust assessments
- **Multi-Tenant Isolation** - Database-level tenant isolation with PostgreSQL Row-Level Security
- **Human Oversight** - Risk-based approval workflow for high-risk operations with multi-approver support
- **Context Provenance** - Full query → context → decision lineage tracking with quality metrics
- **Graceful Degradation** - Circuit breaker pattern for service resilience and fallback modes
- **Policy Versioning** - Version control for governance policies with enforcement engine
- **Compliance Dashboard** - Real-time ISO 42001 monitoring with **100% compliance score**, 25+ metrics, risk visualization, and certification readiness

### Compliance Documentation

- 📋 **[RAE-ISO_42001.md](docs/RAE-ISO_42001.md)** - Full ISO 42001 readiness assessment
- 🛡️ **[RAE-Risk-Register.md](docs/RAE-Risk-Register.md)** - 10 risks (RISK-001 to RISK-010) with mitigation
- 👥 **[RAE-Roles.md](docs/RAE-Roles.md)** - Organizational roles and RACI matrix
- 🔐 **[SECURITY.md](docs/SECURITY.md)** - Security assessment and controls

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

> 💡 **For Regulated Industries:** RAE provides a strong foundation for AI governance. Additional controls may be required depending on your industry (healthcare, finance, etc.). See [RAE-ISO_42001.md](docs/RAE-ISO_42001.md) for details.

---

## Quick Start (< 5 minutes)

**Choose your deployment profile:**

| Profile | Best For | Resources | Command |
|---------|----------|-----------|---------|
| 💡 **RAE Lite** | Developers, testing, small teams (1-10 users) | 4 GB RAM, 2 CPU | `docker-compose -f docker-compose.lite.yml up -d` |
| 🚀 **Full Stack** | Production, mid-size teams (10-100 users) | 8 GB RAM, 4 CPU | `./scripts/quickstart.sh` |
| ☸️ **Enterprise** | Large orgs, auto-scaling, high availability | Auto-scaling | [Kubernetes Guide](docs/deployment/kubernetes.md) |

**Not sure which to choose?** Start with RAE Lite - you can always upgrade later.

### Full Stack (Recommended for Production)
**One-line install:**

```bash
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory && cd RAE-agentic-memory && ./scripts/quickstart.sh
```

### RAE Lite (Minimal - Perfect for Getting Started)

**Who is RAE Lite for?**
- 👨‍💻 **Developers** evaluating RAE or building prototypes
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

**Requirements:** 4 GB RAM, 2 CPU cores (runs on any modern laptop)

**Quick start:**

```bash
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory
cd RAE-agentic-memory
cp .env.example .env
# Edit .env and add your LLM API key (OPENAI_API_KEY or ANTHROPIC_API_KEY)
docker-compose -f docker-compose.lite.yml up -d

# Initialize database (first time only)
./scripts/init-database.sh
```

**Access your instance:**
- API: http://localhost:8000/docs
- Health: http://localhost:8000/health

**Having issues?** See [Troubleshooting Guide](TROUBLESHOOTING.md)

See [RAE Lite Profile Documentation](docs/deployment/rae-lite-profile.md) for complete guide.

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

RAE implements a **4-layer cognitive memory system** inspired by human cognition:

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: SENSORY MEMORY                                │
│  Raw inputs, immediate observations                     │
│  "User clicked submit button"                           │
└──────────────────┬──────────────────────────────────────┘
                   │ Attention & Filtering
                   ▼
┌─────────────────────────────────────────────────────────┐
│  LAYER 2: WORKING MEMORY (WM)                           │
│  Active context for current task + reflections          │
│  "Currently debugging authentication issues"            │
│  + "Lessons Learned: auth.py frequently has bugs"       │
└──────────────────┬──────────────────────────────────────┘
                   │ Consolidation & Pattern Detection
                   ▼
┌─────────────────────────────────────────────────────────┐
│  LAYER 3: LONG-TERM MEMORY (LTM)                        │
│  Episodic: Events + Semantic: Facts + Profiles          │
│  "User fixed auth bug on Jan 5" + "auth.py bug-prone"   │
└──────────────────┬──────────────────────────────────────┘
                   │ Reflection Engine V2 (Actor-Evaluator-Reflector)
                   ▼
┌─────────────────────────────────────────────────────────┐
│  LAYER 4: REFLECTIVE MEMORY (RM)                        │
│  Meta-learnings, strategies, wisdom                     │
│  "Authentication module needs architectural refactoring" │
└─────────────────────────────────────────────────────────┘
```

**Key Components:**

### Microservices Architecture (v2.1)

```
┌──────────────────────────────────────────────────────────────────────┐
│                      RAE Memory API (Port 8000)                      │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  API Layer (FastAPI)                                          │   │
│  ├───────────────────────────────────────────────────────────────┤   │
│  │  Core Services (Business Logic)                               │   │
│  │  • HybridSearchService + Cache  • QueryAnalyzer               │   │
│  │  • ReflectionEngineV2 (NEW)  • EntityResolution              │   │
│  │  • TemporalGraph  • SemanticExtractor                         │   │
│  │  • ContextBuilder (NEW)  • MemoryScoringV2 (NEW)              │   │
│  ├───────────────────────────────────────────────────────────────┤   │
│  │  Enterprise Services                                          │   │
│  │  • RulesEngine (Event Triggers)  • EvaluationService          │   │
│  │  • DriftDetector  • PIIScrubber  • CostController             │   │
│  │  • DashboardWebSocket  • Analytics                            │   │
│  │  • Evaluator (NEW) - Actor-Evaluator-Reflector pattern        │   │
│  ├───────────────────────────────────────────────────────────────┤   │
│  │  Background Workers (NEW)                                     │   │
│  │  • DecayWorker  • SummarizationWorker  • DreamingWorker       │   │
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

See [MEMORY_MODEL.md](docs/MEMORY_MODEL.md) for complete layer mapping reference.

### 🔍 Hybrid Search 2.0 (GraphRAG)
- **Multi-Strategy Search**: Vector similarity, Semantic nodes, Graph traversal, Full-text
- **Query Analyzer**: LLM-powered intent classification and dynamic weight calculation
- **Graph Traversal**: BFS graph exploration for discovering connected concepts (GraphRAG)
- **LLM Re-ranking**: Optional re-ranking with Claude/GPT for contextual relevance
- **Intelligent Caching**: Hash-based cache with temporal windowing for performance
- **Adaptive Weighting**: Automatically adjusts search strategy weights based on query intent

### 🔄 Reflection Engine V2 (Actor-Evaluator-Reflector Pattern) *(NEW in v2.1)*
- **Automatic Evaluation**: Deterministic and threshold-based outcome assessment
- **Failure Analysis**: LLM-powered reflection on errors and failures
- **Success Patterns**: Extract learnings from successful executions
- **Context Integration**: Reflections automatically injected into Working Memory
- **Configurable Modes**: Lite mode (disabled) vs Full mode (enabled)
- **Background Workers**: Decay, Summarization, Dreaming for automated lifecycle

See [REFLECTIVE_MEMORY_V1.md](docs/REFLECTIVE_MEMORY_V1.md) for complete implementation guide.

### 🤖 Multi-Model LLM Integration (v2.0)
- **Unified Provider Interface**: Single API for all LLM providers
- **Supported Models**:
  - OpenAI (GPT-4, GPT-3.5, O1)
  - Anthropic (Claude 3.x, Claude 3.7)
  - Google (Gemini 1.5 Pro, Flash)
  - DeepSeek (Coder, Chat)
  - Qwen (Alibaba Cloud)
  - Grok (xAI)
  - Ollama (Local models: Llama, Mistral)
- **Intelligent Routing**: Automatic provider selection based on model name
- **Cost-Aware Fallbacks**: Switch providers on rate limits or failures
- **Streaming Support**: Real-time response streaming for all compatible providers
- **Tool Calling**: Unified function/tool calling interface
- **JSON Mode**: Structured output support across providers
- **Profile-Based Selection**: Use llm_profiles.yaml for smart model selection
- **Easy Extension**: Add new providers by implementing simple interface

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
- **[Security Overview](docs/SECURITY.md)** - **Honest "Almost Enterprise" assessment** with deployment patterns
- [RBAC Guide](docs/security/RBAC.md) - Role-based access control details
- [Migration Guide](CHANGELOG.md) - Upgrading to v2.0 security
- [Configuration Reference](docs/CONFIG_REFLECTIVE_MEMORY.md) - Feature flags and production recommendations

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

### Optional Modules (Beta/Experimental)

| Component | Status | Description | When to Use |
|-----------|--------|-------------|-------------|
| **ML Service** | 🟡 Beta | Heavy ML operations (entity resolution, NLP) | Advanced entity linking |
| **Dashboard** | 🟡 Beta | Web UI for visualization & monitoring | Teams needing visual insights |
| **Celery Workers** | 🟡 Beta | Async background tasks (scheduled reflections) | Automated workflows |
| **Prometheus + Grafana** | ⚠️ Optional | Metrics and monitoring | Production monitoring |

### Deployment Profiles

**RAE Lite** (Minimal):
- **Includes:** Enterprise Core only (API, PostgreSQL, Qdrant, Redis, GraphRAG, Governance)
- **Perfect for:** Development, testing, small teams (1-10 users)
- **Resources:** 4 GB RAM, 2 CPU cores
- **See:** [RAE Lite Profile Documentation](docs/deployment/rae-lite-profile.md)

**RAE Standard** (Recommended):
- **Includes:** Enterprise Core + Enterprise Extensions (MCP, Reranker, Context Watcher, Reflection V2) + ML Service + Dashboard
- **Perfect for:** Production use, mid-size teams (10-100 users)
- **Resources:** 8 GB RAM, 4 CPU cores

**RAE Enterprise** (Full Stack):
- **Includes:** Enterprise Core + All Extensions + All Optional Modules + Kubernetes + Monitoring
- **Perfect for:** Large organizations, high availability, auto-scaling
- **Resources:** Auto-scaling with HPA (starts at 16 GB RAM)
- **See:** [Kubernetes Deployment Guide](docs/deployment/kubernetes.md)

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
- 🧪 **[Testing Status](docs/TESTING_STATUS.md)** - Test coverage and quality metrics

### Getting Started
- 📖 **[Getting Started Guide](docs/getting-started/)** - Installation and first steps
- 🚀 **[Quick Start](docs/getting-started/)** - 5-minute setup guide
- 🎓 **[Tutorials](docs/guides/)** - Step-by-step guides

### Architecture & Concepts
- 🏗️ **[Architecture Overview](docs/concepts/architecture.md)** - System design and components
- 🧠 **[Memory Model](docs/MEMORY_MODEL.md)** - 4-layer memory architecture reference
- 🔄 **[Reflective Memory V1](docs/REFLECTIVE_MEMORY_V1.md)** - Actor-Evaluator-Reflector pattern
- 🏛️ **[Repository Pattern](docs/architecture/repository-pattern.md)** - Data access layer design
- 💰 **[Cost Controller](docs/concepts/cost-controller.md)** - Budget management and cost tracking
- 🔍 **[Hybrid Search](docs/concepts/)** - Multi-strategy search with GraphRAG

### Deployment
- 🐳 **[Docker Compose Setup](docs/getting-started/)** - Local development
- ☸️ **[Kubernetes Deployment](docs/deployment/kubernetes.md)** - Enterprise production deployment
- 📊 **[Helm Chart Configuration](helm/rae-memory/README.md)** - Detailed Helm values reference

### API Documentation
- 🔧 **[REST API Reference](docs/api/rest-api.md)** - Complete API documentation
- 📚 **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (when running)
- 🔌 **[IDE Integration Guide](docs/guides/IDE_INTEGRATION.md)** - Connect RAE with your IDE (Claude, Cursor, VSCode, etc.)
- 🔌 **[MCP Protocol Server](docs/integrations/mcp_protocol_server.md)** - Technical MCP implementation details

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

**Current Status (v2.1):**
- ✅ Core memory layers (4-layer architecture)
- ✅ Vector search with multiple backends
- ✅ Knowledge graph (GraphRAG)
- ✅ **Reflection Engine V2** (Actor-Evaluator-Reflector pattern)
- ✅ **Memory Scoring V2** (Unified α·relevance + β·importance + γ·recency)
- ✅ **Context Builder** (Working Memory with reflection injection)
- ✅ **Background Workers** (Decay, Summarization, Dreaming)
- ✅ **Evaluator Interface** (Deterministic, Threshold, LLM-ready)
- ✅ Hybrid Multi-Strategy Search
- ✅ Event Triggers & Automation
- ✅ Real-time Dashboard
- ✅ MCP server for IDEs
- ✅ Python SDK
- ✅ Multi-tenancy & RBAC
- ✅ Docker deployment
- ✅ **226 Tests (100% passing), 60% Coverage** (target: 75%+)
- ✅ **CI/CD Pipeline** (lint, test, docker build - all passing ✅)

**Coming Soon (v1.0):**
- 🚧 Test coverage improvement (60% → 75%+)
- 🚧 ML Service stabilization (beta → GA)
- 🚧 Dashboard enhancements (beta → GA)
- 🚧 LLM Evaluator implementation
- 🚧 Production deployment guides

**Future (Post-1.0):**
- 🚧 Plugin system
- 🚧 Multi-modal memories (images, audio)
- 🚧 Memory consolidation/pruning optimization
- 🚧 Enterprise SSO integration

See [STATUS.md](STATUS.md) for detailed implementation status.

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
