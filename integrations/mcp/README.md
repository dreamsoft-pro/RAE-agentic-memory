# RAE MCP Server

Enterprise-grade **Model Context Protocol (MCP)** server for RAE (Reflective Agentic Memory Engine).

This server implements the official MCP specification, enabling IDE integrations (Claude Desktop, Cursor, Cline) to interact with RAE memory via STDIO JSON-RPC.

## What is MCP?

**Model Context Protocol (MCP)** is a standardized protocol developed by Anthropic for connecting AI assistants with external data sources and tools. It uses JSON-RPC over STDIO for communication.

Learn more: [MCP Specification](https://modelcontextprotocol.io/)

## Features

### 🛠️ MCP Tools

1. **save_memory** - Store information in RAE memory
   - Save important decisions, code patterns, or context
   - Supports multiple memory layers (episodic, working, semantic, ltm)
   - Tagging for easy categorization

2. **search_memory** - Search RAE for relevant information
   - Semantic search across all memories
   - Configurable result count (1-20)
   - Scored results for relevance

3. **get_related_context** - Get historical context for files
   - View past changes and decisions
   - Understand file evolution
   - Access related memories

### 📚 MCP Resources

1. **rae://project/reflection** - Current project insights
   - Synthesized summary of recent activities
   - Key patterns and decisions
   - Auto-updated reflections

2. **rae://project/guidelines** - Project coding guidelines
   - Best practices and conventions
   - Team agreements
   - Semantic memory layer

### 💬 MCP Prompts

1. **project-guidelines** - Inject guidelines into context
   - Auto-loads coding standards
   - Ensures consistency
   - Continuous context awareness

2. **recent-context** - Recent project activities
   - What's been happening
   - Recent changes and updates
   - Current focus areas

## Installation

### From Source

```bash
cd integrations/mcp
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

### Verify Installation

```bash
rae-mcp-server --help
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
RAE_API_URL=http://localhost:8000
RAE_API_KEY=your-api-key-here
RAE_PROJECT_ID=my-project
RAE_TENANT_ID=my-tenant
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "rae-memory": {
      "command": "rae-mcp-server",
      "env": {
        "RAE_API_URL": "http://localhost:8000",
        "RAE_API_KEY": "your-api-key-here",
        "RAE_PROJECT_ID": "my-project",
        "RAE_TENANT_ID": "default-tenant"
      }
    }
  }
}
```

### Cursor IDE Configuration

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "rae-memory": {
      "command": "rae-mcp-server",
      "env": {
        "RAE_API_URL": "http://localhost:8000",
        "RAE_API_KEY": "your-api-key-here",
        "RAE_PROJECT_ID": "my-project",
        "RAE_TENANT_ID": "default-tenant"
      }
    }
  }
}
```

### Cline (VSCode Extension)

1. Open VSCode Settings
2. Search for "Cline: MCP Settings"
3. Add MCP server configuration:

```json
{
  "rae-memory": {
    "command": "rae-mcp-server",
    "env": {
      "RAE_API_URL": "http://localhost:8000",
      "RAE_API_KEY": "your-api-key-here",
      "RAE_PROJECT_ID": "my-project",
      "RAE_TENANT_ID": "default-tenant"
    }
  }
}
```

**Important**: Cline requires the server name (`rae-memory`) to match the `providerId` in your extension settings.

## Usage Examples

### Storing Memories

In your IDE (Claude Desktop, Cursor, etc.):

```
Please save this architectural decision to memory:

We decided to use PostgreSQL for the database because of its
excellent JSON support, ACID compliance, and proven reliability
in production environments.

Tags: architecture, database, decision, postgresql
Layer: semantic
```

The AI assistant will automatically use the `save_memory` tool.

### Searching Memory

```
What database technology decisions have we made for this project?
```

The AI will use `search_memory` to find relevant architectural decisions.

### Getting File Context

```
What changes have been made to src/auth/middleware.py recently?
Show me the historical context.
```

The AI will use `get_related_context` to show file history and related memories.

### Using Resources

```
Show me the current project reflection summary
```

The AI will read the `rae://project/reflection` resource.

### Using Prompts

The `project-guidelines` prompt can be manually invoked or automatically injected, ensuring the AI is always aware of your project's coding standards and conventions.

## Development

### Running Tests

```bash
# Unit tests
pytest

# With coverage
pytest --cov=rae_mcp --cov-report=html

# Integration tests
pytest -m integration

# End-to-end tests
pytest -m e2e
```

### Type Checking

```bash
mypy src/rae_mcp
```

### Linting and Formatting

```bash
# Check formatting
black --check src/rae_mcp

# Format code
black src/rae_mcp

# Lint
ruff check src/rae_mcp
```

## Architecture

### Communication Flow

```
┌─────────────────────────────────────┐
│ IDE (Claude Desktop, Cursor, Cline) │
└─────────────┬───────────────────────┘
              │ STDIO (JSON-RPC)
              │
┌─────────────▼───────────────────────┐
│      RAE MCP Server                 │
│  - Tools (save, search, context)    │
│  - Resources (reflection, guides)   │
│  - Prompts (auto-injection)         │
└─────────────┬───────────────────────┘
              │ HTTP REST API (/v1/...)
              │
┌─────────────▼───────────────────────┐
│      RAE Memory API                 │
│  - Memory storage & retrieval       │
│  - Semantic search                  │
│  - Reflection generation            │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│ PostgreSQL + pgvector               │
│ (Vector embeddings + metadata)      │
└─────────────────────────────────────┘
```

### Components

- **server.py** - Main MCP server implementation (JSON-RPC handlers)
- **RAEMemoryClient** - Async HTTP client for RAE API
- **PIIScrubber** - PII detection and masking for secure logging
- **Tools** - save_memory, search_memory, get_related_context
- **Resources** - project/reflection, project/guidelines
- **Prompts** - project-guidelines, recent-context

## Monitoring & Observability

### Prometheus Metrics

The server exposes the following metrics:

- `mcp_tools_called_total` - Counter of tool invocations by tool name
- `mcp_tool_errors_total` - Counter of tool errors
- `mcp_tool_duration_seconds` - Histogram of tool execution time
- `mcp_resources_read_total` - Counter of resource reads
- `mcp_prompts_requested_total` - Counter of prompt requests

### Structured Logging

Uses `structlog` for structured JSON logging:

```json
{
  "event": "tool_called",
  "tool": "save_memory",
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "info"
}
```

PII is automatically scrubbed from logs (API keys, emails, etc.).

## Troubleshooting

### Server Not Starting

1. Check environment variables are set correctly
2. Ensure RAE API is running: `curl http://localhost:8000/health`
3. Verify Python version: `python --version` (requires 3.10+)
4. Check for port conflicts

### Connection Errors

1. Verify `RAE_API_URL` points to correct endpoint
2. Check API key is valid: `X-API-Key` header
3. Ensure network connectivity between MCP server and RAE API
4. Check firewall rules

### Tool Not Working in IDE

1. Verify IDE MCP integration is enabled
2. Check server is running in IDE MCP settings
3. Review IDE logs for MCP errors
4. Restart IDE after configuration changes
5. Ensure `command` path is correct (use absolute path if needed)

### PII Appearing in Logs

The PIIScrubber should automatically mask sensitive data. If PII appears:

1. Report the issue with a sanitized example
2. Check `PIIScrubber.PATTERNS` in `server.py`
3. Add custom patterns if needed

## Performance Benchmarks

Measured on local development machine (RAE API on localhost):

- **Memory Storage**: 100-200ms per operation
- **Memory Search**: 200-500ms (depends on corpus size)
- **Resource Read**: 300-600ms (includes reflection generation)
- **Prompt Load**: 200-400ms
- **Throughput**: ~5-10 requests/second per client

## Security

- ✅ API keys transmitted securely via headers
- ✅ HTTPS recommended for production deployments
- ✅ Tenant isolation enforced at API level
- ✅ No data stored locally by MCP server (stateless)
- ✅ PII scrubbing in logs
- ✅ Input validation on all tool parameters

## Contributing

See main repository [CONTRIBUTING.md](../../CONTRIBUTING.md).

## License

Apache License 2.0 - see [LICENSE](../../LICENSE) file

## Support

- **GitHub Issues**: https://github.com/dreamsoft-pro/RAE-agentic-memory/issues
- **Documentation**: See [docs/integrations/mcp_protocol_server.md](../../docs/integrations/mcp_protocol_server.md)
- **Community**: Discussions tab on GitHub

## Related

- [Context Watcher](../context-watcher/README.md) - HTTP daemon for file watching
- [RAE Memory API](../../apps/memory_api/README.md) - Core RAE API documentation
