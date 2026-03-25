# RAE Enterprise Services Documentation

Complete documentation for RAE's enterprise-grade services and features.

## 📚 Documentation Index

### Core Search & Retrieval

- **[Hybrid Search 2.0 (GraphRAG)](./HYBRID_SEARCH.md)** - Multi-strategy search with query analysis, graph traversal, and intelligent caching
  - Query Analyzer with intent classification
  - Vector + Semantic + Graph + Fulltext search
  - LLM re-ranking
  - Hash-based cache with temporal windowing

### Automation & Events

- **[Rules Engine](./RULES_ENGINE.md)** - Event-driven automation with triggers, conditions, and actions
  - 10+ event types
  - Complex AND/OR condition logic
  - Rate limiting and cooldowns
  - Webhook integrations
  - Retry with exponential backoff

### Quality & Evaluation

- **[Evaluation Service](./EVALUATION_SERVICE.md)** - Search quality metrics and A/B testing
  - MRR, NDCG, Precision@K, Recall@K, MAP
  - A/B testing with statistical significance
  - Continuous evaluation pipelines

### All Enterprise Services

- **[Enterprise Services Overview](./ENTERPRISE_SERVICES.md)** - Quick reference for all enterprise services
  - PII Scrubber
  - Drift Detector
  - Temporal Graph
  - Analytics Service
  - Cost Controller
  - Dashboard WebSocket
  - Complete integration examples

## 🚀 Quick Links

### By Use Case

**Search & Retrieval**
- Multi-strategy search → [Hybrid Search](./HYBRID_SEARCH.md#api-usage)
- GraphRAG exploration → [Hybrid Search](./HYBRID_SEARCH.md#graph-search-graphrag)
- Query intent analysis → [Hybrid Search](./HYBRID_SEARCH.md#1-query-analyzer)
- Result caching → [Hybrid Search](./HYBRID_SEARCH.md#3-hybrid-cache)

**Automation**
- Event triggers → [Rules Engine](./RULES_ENGINE.md#2-triggers)
- Webhook integration → [Rules Engine](./RULES_ENGINE.md#4-actions)
- Scheduled tasks → [Rules Engine](./RULES_ENGINE.md#common-use-cases)
- Condition logic → [Rules Engine](./RULES_ENGINE.md#3-conditions)

**Quality & Monitoring**
- Search metrics → [Evaluation Service](./EVALUATION_SERVICE.md#supported-metrics)
- A/B testing → [Evaluation Service](./EVALUATION_SERVICE.md#ab-testing)
- Drift detection → [Enterprise Services](./ENTERPRISE_SERVICES.md#5-drift-detector)
- PII protection → [Enterprise Services](./ENTERPRISE_SERVICES.md#4-pii-scrubber)

**Analytics & Monitoring**
- Real-time updates → [Enterprise Services](./ENTERPRISE_SERVICES.md#7-dashboard-websocket-service)
- Cost tracking → [Enterprise Services](./ENTERPRISE_SERVICES.md#9-cost-controller)
- Memory analytics → [Enterprise Services](./ENTERPRISE_SERVICES.md#8-analytics-service)
- Graph evolution → [Enterprise Services](./ENTERPRISE_SERVICES.md#6-temporal-graph-service)

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    RAE Enterprise Stack                       │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Search & Retrieval                                          │
│  ├─ Hybrid Search 2.0 (GraphRAG)                            │
│  ├─ Query Analyzer                                           │
│  └─ Result Cache                                             │
│                                                               │
│  Automation & Events                                          │
│  ├─ Rules Engine                                             │
│  ├─ Event Bus                                                │
│  └─ Action Executors                                         │
│                                                               │
│  Quality & Security                                           │
│  ├─ Evaluation Service                                       │
│  ├─ Drift Detector                                           │
│  └─ PII Scrubber                                             │
│                                                               │
│  Analytics & Monitoring                                       │
│  ├─ Analytics Service                                        │
│  ├─ Cost Controller                                          │
│  ├─ Dashboard WebSocket                                      │
│  └─ Temporal Graph                                           │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## 📖 Reading Guide

### For Developers

1. Start with [Hybrid Search](./HYBRID_SEARCH.md) to understand core search functionality
2. Read [Rules Engine](./RULES_ENGINE.md) for automation capabilities
3. Review [Enterprise Services](./ENTERPRISE_SERVICES.md) for quick reference

### For DevOps/SRE

1. Review [Enterprise Services](./ENTERPRISE_SERVICES.md#configuration) for configuration
2. Check [Hybrid Search Performance](./HYBRID_SEARCH.md#performance-optimization)
3. Study [Rules Engine Monitoring](./RULES_ENGINE.md#monitoring)

### For Product Managers

1. Overview in [Enterprise Services](./ENTERPRISE_SERVICES.md#core-services)
2. Use cases in [Rules Engine](./RULES_ENGINE.md#common-use-cases)
3. Metrics in [Evaluation Service](./EVALUATION_SERVICE.md#interpreting-results)

## 🔧 Common Tasks

### Setup Multi-Strategy Search

```python
from apps.memory_api.services.hybrid_search_service import HybridSearchService

search = HybridSearchService(pool=db_pool, enable_cache=True)

results = await search.search(
    tenant_id="my-tenant",
    project="my-project",
    query="authentication best practices",
    k=10,
    enable_graph=True,
    enable_reranking=True
)
```

**Documentation**: [Hybrid Search - API Usage](./HYBRID_SEARCH.md#api-usage)

### Create Automation Rule

```python
from apps.memory_api.models.event_models import TriggerRule, ActionConfig

trigger = TriggerRule(
    name="Alert on High Importance",
    event_type=EventType.MEMORY_CREATED,
    condition=...,
    actions=[
        ActionConfig(
            action_type=ActionType.SEND_WEBHOOK,
            config={"url": "https://..."}
        )
    ]
)
```

**Documentation**: [Rules Engine - API Usage](./RULES_ENGINE.md#api-usage)

### Run Search Evaluation

```python
from apps.memory_api.services.evaluation_service import EvaluationService

eval_service = EvaluationService()

result = await eval_service.evaluate_search_results(
    relevance_judgments=judgments,
    search_results=results,
    metrics_to_compute=[MetricType.MRR, MetricType.NDCG]
)
```

**Documentation**: [Evaluation Service - API Usage](./EVALUATION_SERVICE.md#api-usage)

## 🔐 Security Features

- **PII Scrubbing**: Automatic detection and anonymization ([docs](./ENTERPRISE_SERVICES.md#4-pii-scrubber))
- **Multi-tenancy**: Complete tenant isolation across all services
- **Audit Trail**: Temporal graph provides complete change history
- **Cost Limits**: Prevent runaway API costs ([docs](./ENTERPRISE_SERVICES.md#9-cost-controller))
- **Rate Limiting**: Rules Engine prevents automation abuse

## 📊 Monitoring & Metrics

All services provide structured logging and metrics:

- **Search Latency**: Hybrid search breakdown (analysis, search, reranking)
- **Cache Hit Rate**: Track cache performance
- **Automation Execution**: Trigger fire rate, action success/failure
- **Quality Metrics**: MRR, NDCG, Precision@K tracking
- **Cost Tracking**: LLM API usage and costs
- **Drift Detection**: Semantic drift scores

## 🤝 Contributing

Found an issue or want to improve documentation?

1. Open an issue on GitHub
2. Submit a pull request
3. Join discussions in GitHub Discussions

## 📞 Support

- **Documentation**: `/docs`
- **API Reference**: `/docs` (Swagger UI)
- **GitHub Issues**: Report bugs and feature requests
- **GitHub Discussions**: Community support
