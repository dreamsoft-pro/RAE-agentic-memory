# IDE Integration Guide

Integrate RAE memory with your IDE using Model Context Protocol (MCP).

## Supported IDEs
- Cursor
- Claude Desktop  
- VSCode (with Continue)
- Windsurf

## Quick Setup

### 1. Install MCP Server
```bash
cd integrations/mcp-server
pip install -e .
```

### 2. Configure IDE

**Cursor** - Edit `~/.cursor/config.json`:
```json
{
  "mcpServers": {
    "rae": {
      "command": "python",
      "args": ["-m", "rae_mcp_server"],
      "env": {
        "RAE_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

**Claude Desktop** - Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

### 3. Restart IDE

## Usage

- `/rae-save <text>` - Save to memory
- `/rae-search <query>` - Search memories  
- `/rae-list` - List recent

Auto-context injection happens automatically based on your current work.

See [MCP Server docs](../api/mcp-server.md) for details.
