# GraphRAG - Knowledge Graph Integration Guide

## Overview

GraphRAG extends RAE's memory capabilities by integrating **Knowledge Graph** technology with traditional **Retrieval-Augmented Generation (RAG)**. This hybrid approach provides:

- **Semantic Search**: Vector-based similarity search for finding relevant memories
- **Structural Search**: Graph traversal for discovering relationships and dependencies
- **Context Synthesis**: Merged context from both vector and graph sources
- **Entity Extraction**: Automatic extraction of entities and relationships from episodic memories

## Architecture

```
┌─────────────────┐
│ Episodic Memory │
│   (Memories)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Graph Extraction       │
│  (LLM-based)           │
│  - Extract entities     │
│  - Identify relations   │
│  - Assign confidence    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Knowledge Graph        │
│  ┌─────┐  ┌─────┐      │
│  │Node │──│Edge │──►   │
│  └─────┘  └─────┘      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Hybrid Search          │
│  1. Vector search       │
│  2. Map to graph nodes  │
│  3. Traverse graph      │
│  4. Synthesize context  │
└─────────────────────────┘
```

## Core Concepts

### Entities and Relationships

GraphRAG automatically extracts structured knowledge from unstructured episodic memories:

**Example Memory:**
```
"User John reported bug #123 in the authentication module.
 Developer Alice fixed it by updating the password validation logic."
```

**Extracted Triples:**
```json
[
  {
    "source": "John",
    "relation": "REPORTED_BUG",
    "target": "bug #123",
    "confidence": 0.95
  },
  {
    "source": "bug #123",
    "relation": "AFFECTS",
    "target": "authentication module",
    "confidence": 0.90
  },
  {
    "source": "Alice",
    "relation": "FIXED",
    "target": "bug #123",
    "confidence": 0.95
  }
]
```

### Confidence Scoring

Each extracted triple has a confidence score (0.0 to 1.0) indicating the LLM's certainty about the relationship. You can filter triples by minimum confidence threshold.

### Graph Traversal

Two traversal strategies are supported:

- **BFS (Breadth-First Search)**: Explores all neighbors at the current depth before moving deeper. Good for finding nearby relationships.
- **DFS (Depth-First Search)**: Explores as deep as possible along each branch. Good for finding long chains of relationships.

## API Endpoints

### 1. Extract Knowledge Graph

**Endpoint:** `POST /v1/graph/extract`

Extracts knowledge graph from episodic memories.

**Request:**
```json
{
  "project_id": "my-project",
  "limit": 50,
  "min_confidence": 0.5,
  "auto_store": true
}
```

**Response:**
```json
{
  "triples": [
    {
      "source": "AuthService",
      "relation": "DEPENDS_ON",
      "target": "EncryptionService",
      "confidence": 0.92,
      "metadata": {
        "project_id": "my-project",
        "extraction_method": "llm_structured"
      }
    }
  ],
  "extracted_entities": [
    "AuthService",
    "EncryptionService",
    "bug #123",
    "Alice"
  ],
  "statistics": {
    "memories_processed": 10,
    "entities_count": 15,
    "triples_count": 23,
    "min_confidence": 0.5
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/v1/graph/extract \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: my-tenant" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "project_id": "my-project",
    "limit": 50,
    "min_confidence": 0.6,
    "auto_store": true
  }'
```

### 2. Hybrid Search (Memory Query with Graph)

**Endpoint:** `POST /v1/memory/query`

Standard memory query extended with graph traversal capabilities.

**Request:**
```json
{
  "query_text": "authentication bugs and fixes",
  "k": 10,
  "use_graph": true,
  "graph_depth": 2,
  "project": "my-project"
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "mem-123",
      "content": "Bug in authentication module...",
      "score": 0.87,
      "source": "bug-tracker",
      "tags": ["bug", "authentication"]
    }
  ],
  "synthesized_context": "# Search Query\nauthentication bugs and fixes\n\n# Relevant Memories...",
  "graph_statistics": {
    "vector_results": 5,
    "graph_nodes": 12,
    "graph_edges": 18,
    "graph_depth": 2,
    "traversal_strategy": "bfs"
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/v1/memory/query \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: my-tenant" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "query_text": "authentication module dependencies",
    "k": 5,
    "use_graph": true,
    "graph_depth": 2,
    "project": "my-project"
  }'
```

### 3. Advanced Graph Query

**Endpoint:** `POST /v1/graph/query`

Dedicated endpoint for complex graph-based searches.

**Request:**
```json
{
  "query": "authentication dependencies",
  "project_id": "my-project",
  "top_k_vector": 5,
  "graph_depth": 3,
  "traversal_strategy": "bfs"
}
```

**Response:**
```json
{
  "vector_matches": [...],
  "graph_nodes": [
    {
      "id": "node-uuid",
      "node_id": "AuthService",
      "label": "AuthService",
      "properties": {},
      "depth": 0
    }
  ],
  "graph_edges": [
    {
      "source_id": "node-1",
      "target_id": "node-2",
      "relation": "DEPENDS_ON",
      "properties": {"confidence": 0.92}
    }
  ],
  "synthesized_context": "...",
  "statistics": {
    "vector_results": 5,
    "graph_nodes": 25,
    "graph_edges": 42
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/v1/graph/query \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: my-tenant" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "query": "show me all dependencies of AuthService",
    "project_id": "my-project",
    "top_k_vector": 10,
    "graph_depth": 3,
    "traversal_strategy": "bfs"
  }'
```

### 4. Get Graph Statistics

**Endpoint:** `GET /v1/graph/stats?project_id=my-project`

Retrieve statistics about the knowledge graph.

**Response:**
```json
{
  "project_id": "my-project",
  "tenant_id": "my-tenant",
  "total_nodes": 145,
  "total_edges": 287,
  "unique_relations": [
    "DEPENDS_ON",
    "FIXED_BY",
    "REPORTED_BUG",
    "RELATED_TO"
  ],
  "statistics": {
    "avg_edges_per_node": 1.98,
    "total_relation_types": 12
  }
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/v1/graph/stats?project_id=my-project" \
  -H "X-Tenant-ID: my-tenant" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 5. Get Subgraph

**Endpoint:** `GET /v1/graph/subgraph`

Retrieve a subgraph starting from specific nodes.

**Parameters:**
- `project_id`: Project identifier
- `node_ids`: Comma-separated list of starting node IDs
- `depth`: Traversal depth (default: 1)

**Example:**
```bash
curl -X GET "http://localhost:8000/v1/graph/subgraph?project_id=my-project&node_ids=AuthService,EncryptionService&depth=2" \
  -H "X-Tenant-ID: my-tenant" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 6. Hierarchical Reflection

**Endpoint:** `POST /v1/graph/reflection/hierarchical`

Generate hierarchical (map-reduce) reflection from large episode collections.

**Request:**
```json
{
  "project_id": "my-project",
  "bucket_size": 10,
  "max_episodes": 1000
}
```

**Response:**
```json
{
  "project_id": "my-project",
  "summary": "The project has focused on improving authentication security...",
  "episodes_processed": 234
}
```

## Usage Patterns

### Pattern 1: Initial Graph Construction

When starting with a new project, build the knowledge graph from existing memories:

```python
import httpx

# 1. Store episodic memories
for event in events:
    httpx.post("http://localhost:8000/v1/memory/store", json={
        "content": event,
        "layer": "em",
        "project": "my-project"
    }, headers={"X-Tenant-ID": "tenant-123"})

# 2. Extract knowledge graph
result = httpx.post("http://localhost:8000/v1/graph/extract", json={
    "project_id": "my-project",
    "limit": 100,
    "min_confidence": 0.6,
    "auto_store": True
}, headers={"X-Tenant-ID": "tenant-123"})

print(f"Extracted {result.json()['statistics']['triples_count']} triples")
```

### Pattern 2: Incremental Updates

Periodically update the graph as new memories are added:

```python
# Run graph extraction on a schedule (e.g., every hour)
async def update_knowledge_graph():
    result = await client.post("/v1/graph/extract", json={
        "project_id": "my-project",
        "limit": 50,  # Only process recent memories
        "min_confidence": 0.5,
        "auto_store": True
    })
    return result.json()
```

### Pattern 3: Contextual AI Agent Queries

Use hybrid search to provide rich context to AI agents:

```python
# Agent receives user query
user_query = "How does authentication work in our system?"

# Perform hybrid search
response = httpx.post("http://localhost:8000/v1/memory/query", json={
    "query_text": user_query,
    "k": 10,
    "use_graph": True,
    "graph_depth": 3,
    "project": "my-project"
}, headers={"X-Tenant-ID": "tenant-123"})

# Use synthesized context with LLM
context = response.json()["synthesized_context"]
agent_response = llm.generate(
    prompt=f"Context:\n{context}\n\nQuestion: {user_query}"
)
```

### Pattern 4: Dependency Analysis

Explore dependencies and relationships in your codebase:

```python
# Find all dependencies of a specific module
result = httpx.post("http://localhost:8000/v1/graph/query", json={
    "query": "AuthService dependencies and relationships",
    "project_id": "my-project",
    "graph_depth": 3,
    "traversal_strategy": "bfs"
}, headers={"X-Tenant-ID": "tenant-123"})

# Analyze the graph structure
nodes = result.json()["graph_nodes"]
edges = result.json()["graph_edges"]

print(f"Found {len(nodes)} related entities")
for edge in edges:
    if edge["relation"] == "DEPENDS_ON":
        print(f"{edge['source_id']} depends on {edge['target_id']}")
```

## Best Practices

### 1. Confidence Thresholds

Choose appropriate confidence thresholds based on your use case:

- **High precision (0.7-1.0)**: Critical systems, production environments
- **Balanced (0.5-0.7)**: General-purpose knowledge extraction
- **High recall (0.3-0.5)**: Exploratory analysis, research

### 2. Graph Depth

Consider the trade-off between context richness and performance:

- **Depth 1-2**: Fast queries, immediate relationships
- **Depth 3-4**: Comprehensive context, slower queries
- **Depth 5+**: Deep exploration, use sparingly

### 3. Extraction Frequency

Balance freshness vs. cost:

- **Real-time**: Extract on every new memory (expensive but fresh)
- **Scheduled**: Extract hourly/daily (good balance)
- **On-demand**: Extract only when needed (cost-effective but stale)

### 4. Entity Normalization

Ensure consistent entity names in your memories:

```python
# Good: Consistent naming
"The AuthService module handles authentication"
"AuthService depends on EncryptionService"

# Bad: Inconsistent naming
"The auth service module..."
"authentication-service depends on..."
```

### 5. Memory Quality

High-quality episodic memories lead to better graph extraction:

- Use clear, descriptive language
- Include entity names explicitly
- Specify relationships clearly
- Add relevant tags and metadata

## Performance Considerations

### Indexing

The knowledge graph tables are indexed for optimal performance:

```sql
-- Indexes created by migration
CREATE INDEX idx_nodes_tenant_project ON knowledge_graph_nodes(tenant_id, project_id);
CREATE INDEX idx_nodes_node_id ON knowledge_graph_nodes(node_id);
CREATE INDEX idx_edges_tenant_project ON knowledge_graph_edges(tenant_id, project_id);
CREATE INDEX idx_edges_relation ON knowledge_graph_edges(relation);
```

### Caching

Consider caching frequently accessed subgraphs:

```python
# Cache common queries
cache_key = f"subgraph:{node_id}:depth:{depth}"
if cached := redis.get(cache_key):
    return cached

result = fetch_subgraph(node_id, depth)
redis.setex(cache_key, 3600, result)  # 1 hour TTL
```

### Batch Processing

For large-scale graph construction, use batch processing:

```python
# Process memories in batches
batch_size = 100
for i in range(0, total_memories, batch_size):
    await extract_graph(limit=batch_size, offset=i)
    await asyncio.sleep(1)  # Rate limiting
```

## Troubleshooting

### Common Issues

**1. No triples extracted**
- Check memory content quality
- Lower `min_confidence` threshold
- Verify LLM provider is configured
- Check LLM model has sufficient capability

**2. Slow graph queries**
- Reduce `graph_depth`
- Limit `top_k_vector`
- Check database indexes
- Consider result caching

**3. Duplicate entities**
- Normalize entity names in memories
- Use consistent terminology
- Implement entity resolution post-processing

**4. Low confidence scores**
- Improve memory content clarity
- Use more explicit relationship descriptions
- Try different LLM models
- Review extraction prompt engineering

## Integration Examples

### Python SDK

```python
from rae_memory_sdk import MemoryClient

client = MemoryClient(
    api_url="http://localhost:8000",
    tenant_id="my-tenant"
)

# Extract graph
result = client.extract_knowledge_graph(
    project_id="my-project",
    limit=50,
    min_confidence=0.6
)

# Hybrid search
results = client.query_with_graph(
    query="authentication bugs",
    project="my-project",
    graph_depth=2
)
```

### LangChain Integration

```python
from langchain.memory import RAEGraphMemory

memory = RAEGraphMemory(
    rae_url="http://localhost:8000",
    tenant_id="my-tenant",
    project_id="my-project",
    use_graph=True,
    graph_depth=2
)

# Use in agent
agent = create_agent(
    llm=llm,
    memory=memory,
    tools=tools
)
```

## Next Steps

- Explore the [API Reference](api_reference.md) for complete endpoint documentation
- See [Examples](examples/) for more usage patterns
- Check [Architecture](architecture.md) for system design details
- Read [Best Practices](best_practices.md) for production deployment guidance

## Support

For questions and issues:
- GitHub Issues: https://github.com/dreamsoft-pro/RAE-agentic-memory/issues
- Documentation: https://rae-docs.example.com
- Community: https://discord.gg/rae-memory
