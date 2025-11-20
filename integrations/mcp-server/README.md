# RAE MCP Server

Enterprise-grade Model Context Protocol (MCP) server for RAE (Reflective Agentic-memory Engine).

## Features

### 🛠️ MCP Tools

1. **save_memory** - Store information in RAE memory
   - Save important decisions, code patterns, or context
   - Supports multiple memory layers (episodic, working, semantic, ltm)
   - Tagging for easy categorization

2. **search_memory** - Search RAE for relevant information
   - Semantic search across all memories
   - Configurable result count
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
   - Best practices
   - Conventions and standards
   - Team agreements

### 💬 MCP Prompts

1. **project-guidelines** - Inject guidelines into context
   - Auto-loads coding standards
   - Ensures consistency
   - Continuous context awareness

2. **recent-context** - Recent project activities
   - What's been happening
   - Recent changes
   - Current focus areas

## Installation

### From Source

```bash
cd integrations/mcp-server
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
RAE_API_URL=http://localhost:8000
RAE_API_KEY=your-api-key
RAE_PROJECT_ID=my-project
RAE_TENANT_ID=my-tenant
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "rae-memory": {
      "command": "python",
      "args": ["-m", "rae_mcp_server"],
      "env": {
        "RAE_API_URL": "http://localhost:8000",
        "RAE_API_KEY": "your-api-key",
        "RAE_PROJECT_ID": "my-project",
        "RAE_TENANT_ID": "default-tenant"
      }
    }
  }
}
```

### Cursor Configuration

Add to your Cursor settings (`.cursor/config.json`):

```json
{
  "mcp": {
    "servers": {
      "rae-memory": {
        "command": "python",
        "args": ["-m", "rae_mcp_server"],
        "env": {
          "RAE_API_URL": "http://localhost:8000",
          "RAE_API_KEY": "your-api-key",
          "RAE_PROJECT_ID": "my-project"
        }
      }
    }
  }
}
```

### Cline (VSCode Extension)

Add to Cline MCP settings:

```json
{
  "rae-memory": {
    "command": "python",
    "args": ["-m", "rae_mcp_server"],
    "env": {
      "RAE_API_URL": "http://localhost:8000",
      "RAE_API_KEY": "your-api-key",
      "RAE_PROJECT_ID": "my-project"
    }
  }
}
```

## Usage Examples

### Storing Memories

In your IDE (Claude Desktop, Cursor, etc.):

```
Please save this decision to memory:
We decided to use PostgreSQL for the database because of its excellent JSON support and reliability.

Tags: architecture, database, decision
Layer: semantic
```

The AI will use the `save_memory` tool automatically.

### Searching Memory

```
What database decisions have we made?
```

The AI will use `search_memory` to find relevant information.

### Getting File Context

```
What changes have been made to auth.py recently?
```

The AI will use `get_related_context` to show file history.

### Using Resources

```
Show me the current project reflection
```

The AI will read the `rae://project/reflection` resource.

### Using Prompts

The `project-guidelines` prompt is automatically injected into context, ensuring the AI is always aware of your project's coding standards.

## Development

### Running Tests

```bash
pytest
```

### With Coverage

```bash
pytest --cov=rae_mcp_server --cov-report=html
```

### Type Checking

```bash
mypy src/rae_mcp_server
```

### Linting

```bash
ruff check src/rae_mcp_server
black src/rae_mcp_server
```

## Architecture

### Communication Flow

```
IDE (Claude Desktop, Cursor, etc.)
    ↓ STDIO (JSON-RPC)
RAE MCP Server
    ↓ HTTP REST API
RAE Memory API
    ↓
PostgreSQL + Vector Store
```

### Components

- **server.py** - Main MCP server implementation
- **RAEMemoryClient** - Async client for RAE API
- **MCP Tools** - save_memory, search_memory, get_related_context
- **MCP Resources** - project/reflection, project/guidelines
- **MCP Prompts** - project-guidelines, recent-context

## Troubleshooting

### Server Not Starting

1. Check environment variables are set
2. Ensure RAE API is running: `curl http://localhost:8000/health`
3. Check Python version: `python --version` (requires 3.10+)

### Connection Errors

1. Verify RAE_API_URL is correct
2. Check API key is valid
3. Ensure network connectivity

### Tool Not Working

1. Check IDE MCP integration is enabled
2. Verify server is running in IDE settings
3. Check IDE logs for errors

## Performance

- **Memory Storage**: ~100-200ms per operation
- **Memory Search**: ~200-500ms depending on corpus size
- **Resource Read**: ~300-600ms (includes reflection generation)
- **Prompt Load**: ~200-400ms

## Security

- API keys transmitted in headers
- HTTPS recommended for production
- Tenant isolation enforced
- No data stored locally by MCP server

## License

Apache License 2.0 - see LICENSE file

## Support

- GitHub Issues: https://github.com/your-org/rae-agentic-memory/issues
- Documentation: https://docs.rae-memory.dev
- Email: support@rae-memory.dev
