# RAE Memory Python SDK

This is the Python client for RAE (Reflective Agentic Memory Engine).

## Install from source

```bash
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory.git
cd RAE-agentic-memory/sdk/python/rae_memory_sdk
pip install .
```

## Basic Usage

```python
from rae_memory_sdk import RAEClient

client = RAEClient(
    base_url="http://localhost:8000",
    tenant_id="demo-tenant",  # or get from env
)

# Store memory
client.store_memory(
    layer="episodic",
    type="event",
    content="User asked the agent to refactor a legacy PHP service.",
    tags=["refactor", "legacy"]
)

# Query memory
response = client.query_memory(
    query="What legacy refactor tasks did the user ask about recently?",
    top_k=5
)

print(response)
```

## Advanced Usage

The client also supports:
- Storing memories in different layers (`semantic`, `reflective`).
- Passing custom headers for authentication or other purposes.
- An asynchronous client (`AsyncRAEClient`) for use with `asyncio`.