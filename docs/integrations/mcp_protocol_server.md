# Model Context Protocol (MCP) Server Integration

Enterprise-grade integration of RAE Memory Engine with the Model Context Protocol for IDE support.

## Table of Contents

- [Overview](#overview)
- [What is MCP?](#what-is-mcp)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Features](#features)
- [IDE Integration](#ide-integration)
- [Tools Reference](#tools-reference)
- [Resources Reference](#resources-reference)
- [Prompts Reference](#prompts-reference)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Performance](#performance)
- [Development](#development)

## Overview

The RAE MCP Server implements the **Model Context Protocol** specification, enabling AI assistants in IDEs (Claude Desktop, Cursor, Cline) to interact with RAE's memory engine through a standardized STDIO JSON-RPC interface.

### Key Benefits

- **Seamless IDE Integration**: Works out-of-the-box with Claude Desktop, Cursor, and Cline
- **Persistent Memory**: AI assistants can store and retrieve context across sessions
- **Project Awareness**: Automatic injection of project guidelines and recent context
- **Zero-Copy Architecture**: Direct STDIO communication (no HTTP overhead)
- **Enterprise-Grade Security**: PII scrubbing, tenant isolation, structured logging

## What is MCP?

**Model Context Protocol (MCP)** is an open standard developed by Anthropic for connecting AI assistants to external data sources and tools. It defines:

- **Tools**: Functions the AI can invoke (e.g., save_memory, search_memory)
- **Resources**: Data sources the AI can read (e.g., project reflections)
- **Prompts**: Pre-defined context that can be injected into conversations

MCP uses **JSON-RPC 2.0** over **STDIO** for communication, making it:
- Language-agnostic
- Fast (no network latency)
- Secure (no exposed ports)
- Simple to implement

**Learn More**: [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────┐
│  IDE (Claude Desktop, Cursor, Cline)                        │
│  - User writes prompt                                       │
│  - AI assistant invokes MCP tools/resources                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ STDIO (JSON-RPC 2.0)
                     │ {"method": "tool/save_memory", ...}
                     │
┌────────────────────▼────────────────────────────────────────┐
│  RAE MCP Server (rae-mcp-server)                            │
│  - Receives JSON-RPC requests                               │
│  - Validates and sanitizes inputs                           │
│  - Scrubs PII from logs                                     │
│  - Calls RAE Memory API                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP REST API
                     │ POST /v1/memory/store
                     │
┌────────────────────▼────────────────────────────────────────┐
│  RAE Memory API (port 8000)                                 │
│  - Handles memory CRUD operations                           │
│  - Generates embeddings                                     │
│  - Performs semantic search                                 │
│  - Creates reflections                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  PostgreSQL + pgvector                                      │
│  - Stores memory content                                    │
│  - Vector embeddings for semantic search                    │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### MCP Server Components

- **server.py**: Core MCP server implementation
  - JSON-RPC handlers
  - Tool/Resource/Prompt definitions
  - Request routing

- **RAEMemoryClient**: Async HTTP client
  - Connects to RAE Memory API
  - Handles authentication (API keys, tenant IDs)
  - Error handling and retries

- **PIIScrubber**: Security component
  - Detects sensitive data (API keys, emails, SSNs, etc.)
  - Masks PII in logs
  - Configurable patterns

#### Communication Protocol

The server implements MCP's JSON-RPC 2.0 protocol:

**Request Example**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tool/save_memory",
  "params": {
    "content": "We decided to use PostgreSQL",
    "source": "architecture-decision",
    "tags": ["database", "decision"],
    "layer": "semantic"
  }
}
```

**Response Example**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "✓ Memory stored successfully\nID: 550e8400-e29b-41d4-a716-446655440000\nLayer: semantic\nTags: database, decision"
      }
    ]
  }
}
```

## Installation

### Prerequisites

- Python 3.10 or higher
- RAE Memory API running on `http://localhost:8000` (or configured URL)
- API key for RAE Memory API

### Install from Source

```bash
cd integrations/mcp
pip install -e .
```

### Install with Development Tools

```bash
pip install -e ".[dev]"
```

### Verify Installation

```bash
rae-mcp-server --help
```

Expected output:
```
Usage: rae-mcp-server [OPTIONS]

Enterprise-grade MCP server for RAE Memory Engine
```

## Configuration

### Environment Variables

The MCP server reads configuration from environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `RAE_API_URL` | RAE Memory API base URL | `http://localhost:8000` |
| `RAE_API_KEY` | API key for authentication | `your-rae-api-key` |
| `RAE_PROJECT_ID` | Default project identifier | `default-project` |
| `RAE_TENANT_ID` | Tenant ID for multi-tenancy | `default-tenant` |

#### Creating `.env` File

```bash
# integrations/mcp/.env
RAE_API_URL=http://localhost:8000
RAE_API_KEY=my-secure-api-key-123
RAE_PROJECT_ID=my-awesome-project
RAE_TENANT_ID=my-company
```

The server will automatically load this file on startup.

## Features

### Tools

MCP tools are functions that the AI assistant can invoke.

#### 1. `save_memory`

Store information in RAE memory for later retrieval.

**Use Cases**:
- Save architectural decisions
- Store code patterns and best practices
- Remember user preferences
- Archive important conversations

**Parameters**:
- `content` (string, required): The content to remember
- `source` (string, required): Source identifier (e.g., file path, URL, "user-input")
- `tags` (array of strings, optional): Tags for categorization
- `layer` (string, optional): Memory layer - one of:
  - `episodic`: Recent events and activities (default)
  - `working`: Current task context
  - `semantic`: Concepts, guidelines, principles
  - `ltm`: Long-term facts and knowledge

**Example Usage** (in IDE):
```
Please save this to memory:

We decided to use FastAPI for the web framework because of its
excellent async support and automatic OpenAPI documentation.

Tags: architecture, web-framework, decision
Layer: semantic
```

#### 2. `search_memory`

Search RAE memory for relevant information using semantic search.

**Use Cases**:
- Find similar code patterns
- Recall past decisions
- Retrieve related context
- Answer "have we done this before?" questions

**Parameters**:
- `query` (string, required): Search query
- `top_k` (integer, optional): Number of results to return (1-20, default: 5)

**Example Usage**:
```
What framework decisions have we made for this project?
```

The AI will automatically use `search_memory` with an appropriate query.

#### 3. `get_related_context`

Get historical context about a specific file or module.

**Use Cases**:
- Understand file evolution
- View past changes and decisions
- Get context before modifying code
- Debug issues by reviewing history

**Parameters**:
- `file_path` (string, required): Path to the file (relative or absolute)
- `include_count` (integer, optional): Number of context items (default: 10)

**Example Usage**:
```
Show me the history of changes to src/auth/middleware.py
```

### Resources

MCP resources are data sources that the AI can read.

#### 1. `rae://project/reflection`

Current project reflection - a synthesized summary of recent activities, patterns, and key decisions.

**Content**: Auto-generated insights based on:
- Recent memories
- Activity patterns
- Recurring themes
- Key decisions

**Update Frequency**: On-demand (generated when accessed)

**Example**:
```
Show me the current project reflection
```

#### 2. `rae://project/guidelines`

Project-specific coding guidelines and conventions from semantic memory.

**Content**:
- Coding standards
- Best practices
- Team agreements
- Architecture patterns

**Storage**: Semantic memory layer

**Example**:
```
What are our project guidelines?
```

### Prompts

MCP prompts are pre-defined context that can be automatically injected into conversations.

#### 1. `project-guidelines`

Automatically injects project guidelines into the conversation context.

**Usage**: Can be manually invoked or auto-injected by IDE

**Content**: Retrieves semantic memories tagged as guidelines, conventions, or standards

#### 2. `recent-context`

Provides awareness of recent project activities and changes.

**Usage**: Helps AI understand "what's been happening"

**Content**: Recent episodic memories from the project

## IDE Integration

### Claude Desktop

Claude Desktop has native MCP support built-in.

#### Configuration (macOS)

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rae-memory": {
      "command": "rae-mcp-server",
      "env": {
        "RAE_API_URL": "http://localhost:8000",
        "RAE_API_KEY": "your-api-key-here",
        "RAE_PROJECT_ID": "my-project",
        "RAE_TENANT_ID": "my-tenant"
      }
    }
  }
}
```

#### Configuration (Windows)

Edit `%APPDATA%\Claude\claude_desktop_config.json` with the same content.

#### Verification

1. Restart Claude Desktop
2. Start a new conversation
3. Type: "Can you search my memory for database decisions?"
4. Claude should use the `search_memory` tool

#### Troubleshooting

- Check Claude Desktop logs: `~/Library/Logs/Claude/` (macOS)
- Ensure `rae-mcp-server` is in your PATH
- Verify RAE API is running: `curl http://localhost:8000/health`

### Cursor IDE

Cursor supports MCP through `.cursor/mcp.json` configuration.

#### Configuration

Create `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "rae-memory": {
      "command": "/absolute/path/to/rae-mcp-server",
      "env": {
        "RAE_API_URL": "http://localhost:8000",
        "RAE_API_KEY": "your-api-key-here",
        "RAE_PROJECT_ID": "my-project",
        "RAE_TENANT_ID": "my-tenant"
      }
    }
  }
}
```

**Important**: Cursor requires **absolute paths** for the command.

#### Finding the Absolute Path

```bash
which rae-mcp-server
# Or if using virtual environment:
which $(poetry env info --path)/bin/rae-mcp-server
```

#### Verification

1. Open Cursor in your project
2. Use Cmd+K (Mac) or Ctrl+K (Windows) to open AI chat
3. Ask: "Save this to memory: test message"
4. Cursor should invoke the MCP tool

### Cline (VSCode Extension)

Cline is a VSCode extension with MCP support.

#### Configuration

1. Open VSCode Settings (Cmd+, or Ctrl+,)
2. Search for "Cline: MCP Settings"
3. Click "Edit in settings.json"
4. Add MCP server configuration:

```json
{
  "cline.mcpServers": {
    "rae-memory": {
      "command": "rae-mcp-server",
      "env": {
        "RAE_API_URL": "http://localhost:8000",
        "RAE_API_KEY": "your-api-key-here",
        "RAE_PROJECT_ID": "my-project",
        "RAE_TENANT_ID": "my-tenant"
      }
    }
  }
}
```

**Important**: The server name (`rae-memory`) must match the `providerId` in Cline's configuration.

#### Verification

1. Open Cline panel in VSCode
2. Start a conversation
3. Ask: "Can you search my memory?"
4. Cline should show MCP tool invocation

## Tools Reference

### save_memory

**JSON-RPC Method**: `tool/save_memory`

**Parameters**:
```typescript
{
  content: string;      // Required: Content to store
  source: string;       // Required: Source identifier
  tags?: string[];      // Optional: Tags for categorization
  layer?: "episodic" | "working" | "semantic" | "ltm";  // Optional: Memory layer
}
```

**Response**:
```typescript
{
  content: [{
    type: "text";
    text: string;  // Success message with memory ID
  }]
}
```

**Errors**:
- `content` or `source` missing → validation error
- RAE API error → HTTP error message
- Network error → connection error message

### search_memory

**JSON-RPC Method**: `tool/search_memory`

**Parameters**:
```typescript
{
  query: string;   // Required: Search query
  top_k?: number;  // Optional: Number of results (1-20, default: 5)
}
```

**Response**:
```typescript
{
  content: [{
    type: "text";
    text: string;  // Formatted results with scores, sources, tags
  }]
}
```

**Result Format**:
```
Found 3 relevant memories:

1. [Score: 0.892]
   Source: architecture-decisions.md
   Tags: database, postgresql
   Content: We decided to use PostgreSQL because...

2. [Score: 0.765]
   ...
```

### get_related_context

**JSON-RPC Method**: `tool/get_related_context`

**Parameters**:
```typescript
{
  file_path: string;      // Required: Path to file
  include_count?: number; // Optional: Number of items (default: 10)
}
```

**Response**:
```typescript
{
  content: [{
    type: "text";
    text: string;  // Historical context with timestamps
  }]
}
```

## Resources Reference

### rae://project/reflection

**URI**: `rae://project/reflection`

**Type**: `text/plain`

**Content**: Synthesized project reflection

**Generation**: On-demand via RAE API `/v1/memory/reflection/hierarchical`

**Cache**: Not cached (always fresh)

### rae://project/guidelines

**URI**: `rae://project/guidelines`

**Type**: `text/plain`

**Content**: Formatted project guidelines

**Source**: Semantic memory layer, filtered by guideline-related queries

**Format**:
```
PROJECT GUIDELINES
============================================================

1. Use PostgreSQL for all new projects requiring ACID compliance
2. Follow RESTful API conventions with /v1/ versioning
3. Always include unit tests for business logic
...

============================================================
Last updated: 2025-01-15T10:30:00Z
```

## Prompts Reference

### project-guidelines

**Name**: `project-guidelines`

**Description**: Injects project guidelines into conversation context

**Arguments**: None

**Output**: User message containing formatted guidelines

**Usage**:
- Automatically invoked by IDE (if configured)
- Manually triggered by AI when discussing standards

### recent-context

**Name**: `recent-context`

**Description**: Provides recent project activities

**Arguments**: None

**Output**: User message containing recent memories

**Content**: Last 10 episodic memories with timestamps

## Security

### PII Scrubbing

The MCP server includes a **PIIScrubber** that automatically detects and masks sensitive data in logs:

**Detected Patterns**:
- API keys, tokens, secrets
- Email addresses (masked: `us***@example.com`)
- Credit card numbers (last 4 digits preserved)
- IP addresses (last two octets masked)
- Phone numbers
- Social Security Numbers (SSNs)

**Sensitive Field Names**:
Fields named `password`, `api_key`, `secret`, `token`, etc. are always masked.

**Example**:
```python
# Input log
logger.info("user_email", email="user@example.com", api_key="sk-abc123")

# Output log (scrubbed)
{"event": "user_email", "email": "us***@example.com", "api_key": "***REDACTED***"}
```

### Tenant Isolation

All RAE API calls include the `X-Tenant-Id` header, ensuring:
- Memories are isolated by tenant
- No cross-tenant data leakage
- Multi-project support within single tenant

### Input Validation

All tool parameters are validated before processing:
- Required fields checked
- Type validation (string, integer, enum)
- Range validation (e.g., `top_k` between 1-20)

### Secure Communication

- **STDIO**: No network ports exposed
- **API Keys**: Transmitted via headers, never logged
- **HTTPS**: Recommended for RAE API in production

## Troubleshooting

### Issue: MCP Server Not Starting in IDE

**Symptoms**:
- IDE shows "MCP server failed to start"
- No tools available in AI assistant

**Solutions**:
1. Check command path is correct:
   ```bash
   which rae-mcp-server
   ```
2. Verify environment variables are set:
   ```bash
   env | grep RAE_
   ```
3. Test server manually:
   ```bash
   rae-mcp-server
   ```
   Expected: Server starts and waits for input
4. Check IDE logs for specific error messages

### Issue: Tools Not Working

**Symptoms**:
- AI assistant doesn't invoke tools
- Tool calls fail silently

**Solutions**:
1. Verify RAE API is running:
   ```bash
   curl http://localhost:8000/health
   ```
2. Check API key is valid:
   ```bash
   curl -H "X-API-Key: your-key" http://localhost:8000/v1/memory/query
   ```
3. Review MCP server logs (if available via IDE)
4. Test tool manually using JSON-RPC:
   ```bash
   echo '{"jsonrpc":"2.0","id":1,"method":"tool/save_memory","params":{"content":"test","source":"test"}}' | rae-mcp-server
   ```

### Issue: PII Appearing in Logs

**Symptoms**:
- Sensitive data visible in log files
- Emails, API keys not masked

**Solutions**:
1. Verify PIIScrubber is enabled (default: always on)
2. Check scrubber patterns in `server.py`
3. Add custom patterns if needed:
   ```python
   PIIScrubber.PATTERNS['custom'] = re.compile(r'your-pattern')
   ```
4. Report issue with sanitized example

### Issue: High Latency

**Symptoms**:
- Tool calls take > 5 seconds
- IDE feels sluggish

**Solutions**:
1. Check RAE API response times:
   ```bash
   time curl -X POST http://localhost:8000/v1/memory/query \
     -H "Content-Type: application/json" \
     -d '{"query_text":"test","k":5}'
   ```
2. Optimize RAE API (see RAE documentation)
3. Reduce `top_k` in search queries
4. Check network latency if RAE API is remote

## Performance

### Benchmarks (v1.1.0)

**Test Environment**: MacBook Pro M1 (8 cores, 16GB RAM), RAE Lite Profile (docker-compose.lite.yml)

#### Latency Percentiles

| Operation | p50 | p95 | p99 | Notes |
|-----------|-----|-----|-----|-------|
| **save_memory** | 45ms | 120ms | 250ms | Includes embedding generation |
| **search_memory** (k=5) | 80ms | 200ms | 400ms | Depends on corpus size |
| **search_memory** (k=20) | 120ms | 280ms | 550ms | Linear scaling with k |
| **get_related_context** | 90ms | 220ms | 450ms | File-based filtering |
| **Resource: reflection** | 300ms | 600ms | 900ms | Includes reflection generation |
| **Resource: guidelines** | 100ms | 250ms | 500ms | Simple query |
| **Prompt: recent-context** | 110ms | 270ms | 530ms | Query + formatting |

#### Throughput

| Metric | Value | Configuration |
|--------|-------|---------------|
| **Max req/sec** | 100+ | Single MCP server instance |
| **Concurrent calls** | 50+ | With connection pooling |
| **Rate limit (default)** | 100 req/min | Per tenant, configurable |

#### Memory Usage

| Stage | Memory | Notes |
|-------|--------|-------|
| **Baseline** | 150 MB | MCP server idle |
| **Under load** | 300 MB | 50 concurrent tool calls |
| **Peak** | 450 MB | 100 concurrent with rate limiting |

### Rate Limiting (New in v1.1.0)

**Default Configuration**:
- **Enabled**: Yes (set `MCP_RATE_LIMIT_ENABLED=false` to disable)
- **Limit**: 100 requests per 60 seconds per tenant
- **Algorithm**: Sliding window

**Configuration**:
```bash
# Environment variables
MCP_RATE_LIMIT_ENABLED=true
MCP_RATE_LIMIT_REQUESTS=100
MCP_RATE_LIMIT_WINDOW=60
```

**Behavior**:
- When limit exceeded, tool calls return user-friendly error message
- Metrics recorded: `mcp_tool_errors_total{error_type="rate_limit"}`
- Per-tenant isolation ensures one tenant cannot affect others

**Example Rate Limit Error**:
```
⚠️ Rate limit exceeded

Tenant: my-tenant-id
Limit: 100 requests per 60s
Remaining: 0

Please wait a moment before trying again.
```

### Optimization Tips

1. **Reduce `top_k`**: Lower values = faster searches (5-10 is optimal)
2. **Use Appropriate Layer**:
   - `episodic`: Fastest (recent memories, no heavy processing)
   - `semantic`: Slower (requires semantic search and reasoning)
   - `ltm`: Medium (long-term storage, minimal processing)
3. **Local RAE API**: Run RAE API on localhost to minimize network latency
4. **Connection Pooling**: httpx client uses automatic connection pooling (default)
5. **Rate Limiting**: Adjust limits based on your usage patterns
6. **Caching**: RAE API caches embeddings for 1 hour (reduces latency for repeated queries)

### Load Testing Results

Tested with Apache Bench (100 requests, concurrency 10):

```bash
# save_memory benchmark
ab -n 100 -c 10 -T application/json -p payload.json http://localhost:8000/v1/memory/store

Requests per second:    23.45 [#/sec]
Time per request:       42.6ms [mean]
Transfer rate:          12.5 KB/sec
```

**Conclusion**: MCP server can handle 20+ tool calls per second on single instance.

### Scaling Recommendations

| Users | Tool Calls/min | Recommendation |
|-------|----------------|----------------|
| 1-10 | < 100 | Single MCP server (RAE Lite) |
| 10-50 | 100-500 | Single MCP server + monitoring |
| 50-100 | 500-1000 | Multiple MCP instances + load balancer |
| 100+ | 1000+ | Kubernetes deployment with HPA |

For high-scale deployments (100+ users), consider:
- Kubernetes with Horizontal Pod Autoscaler (HPA)
- Redis-based distributed rate limiting
- RAE Full Stack (not Lite) for better performance
- CDN for static resources

## Development

### Running Tests

```bash
# Unit tests
pytest tests/

# Integration tests (requires RAE API)
pytest tests/ -m integration

# Coverage report
pytest --cov=rae_mcp --cov-report=html
```

### Adding a New Tool

1. Define tool in `handle_list_tools()`:
   ```python
   types.Tool(
       name="my_new_tool",
       description="Description of what the tool does",
       inputSchema={
           "type": "object",
           "properties": {
               "param1": {"type": "string", "description": "..."}
           },
           "required": ["param1"]
       }
   )
   ```

2. Implement handler in `handle_call_tool()`:
   ```python
   elif name == "my_new_tool":
       param1 = arguments.get("param1")
       # ... implementation
       return [types.TextContent(type="text", text=result)]
   ```

3. Add tests:
   ```python
   async def test_my_new_tool():
       result = await handle_call_tool("my_new_tool", {"param1": "value"})
       assert result[0].text == "expected output"
   ```

### Adding a New Resource

1. Define resource in `handle_list_resources()`:
   ```python
   types.Resource(
       uri="rae://my/resource",
       name="My Resource",
       description="Description",
       mimeType="text/plain"
   )
   ```

2. Implement reader in `handle_read_resource()`:
   ```python
   elif uri == "rae://my/resource":
       content = await fetch_resource_content()
       return content
   ```

### Code Style

```bash
# Format code
black src/rae_mcp

# Lint
ruff check src/rae_mcp

# Type check
mypy src/rae_mcp
```

## Related Documentation

- [Context Watcher Integration](./context_watcher_daemon.md) - HTTP file-watching daemon
- [RAE Memory API](../../apps/memory_api/README.md) - Core API documentation
- [MCP Specification](https://modelcontextprotocol.io/) - Official MCP docs

## Contributing

See main repository [CONTRIBUTING.md](../../CONTRIBUTING.md).

## License

Apache License 2.0 - see [LICENSE](../../LICENSE)

## Support

- **GitHub Issues**: https://github.com/dreamsoft-pro/RAE-agentic-memory/issues
- **Discussions**: https://github.com/dreamsoft-pro/RAE-agentic-memory/discussions
- **Documentation**: https://github.com/dreamsoft-pro/RAE-agentic-memory/tree/main/docs
