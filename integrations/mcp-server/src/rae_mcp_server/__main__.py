"""
RAE MCP Server - Main Entry Point

Run the server with:
    python -m rae_mcp_server

Or after installation:
    rae-mcp-server
"""

import asyncio
import sys
from .server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nRAE MCP Server stopped by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}", file=sys.stderr)
        sys.exit(1)
