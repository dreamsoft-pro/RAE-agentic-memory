# RAE MCP Server - Installation Guide

## Quick Start (5 Minutes)

### Prerequisites

- Python 3.10 or higher
- RAE Memory API running (http://localhost:8000)
- One of: Claude Desktop, Cursor, or Cline (VSCode)

### Step 1: Install MCP Server

```bash
# Navigate to MCP server directory
cd integrations/mcp-server

# Install the package
pip install -e .

# Verify installation
python -m rae_mcp_server --help
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp examples/.env.example .env

# Edit .env file
nano .env

# Set your values:
# RAE_API_URL=http://localhost:8000
# RAE_API_KEY=your-api-key
# RAE_PROJECT_ID=my-project
# RAE_TENANT_ID=default-tenant
```

### Step 3: Configure Your IDE

Choose your IDE and follow the instructions:

#### Option A: Claude Desktop

**macOS:**
```bash
# Create config directory if it doesn't exist
mkdir -p ~/Library/Application\ Support/Claude

# Copy config file
cp examples/configs/claude-desktop-config.json \
   ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Edit the config file to update paths and environment variables
```

**Windows:**
```bash
# Config location:
# %APPDATA%\Claude\claude_desktop_config.json

# Copy and edit the example config
```

**Linux:**
```bash
# Config location:
# ~/.config/Claude/claude_desktop_config.json

# Copy and edit the example config
```

#### Option B: Cursor

```bash
# Create .cursor directory in your project
mkdir -p .cursor

# Copy config
cp examples/configs/cursor-config.json .cursor/config.json

# Edit to update environment variables
```

#### Option C: Cline (VSCode)

1. Install Cline extension from VSCode marketplace
2. Open Cline settings (Cmd+Shift+P → "Cline: Open Settings")
3. Paste configuration from `examples/configs/cline-config.json`
4. Update environment variables

### Step 4: Restart IDE

Close and reopen your IDE to load the MCP server.

### Step 5: Verify Installation

In your IDE, try asking:

```
Search our memory for "test"
```

The AI should use the `search_memory` tool. If it works, you're all set! 🎉

---

## Detailed Installation

### System Requirements

**Operating System:**
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 11+)
- Windows 10+

**Python:**
- Python 3.10, 3.11, or 3.12
- pip 21.0+
- virtualenv (recommended)

**Network:**
- Access to RAE Memory API (default: http://localhost:8000)
- Internet for package downloads

### Virtual Environment Setup (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Installation from Source

```bash
# Clone repository (if not already done)
git clone https://github.com/your-org/rae-agentic-memory.git
cd rae-agentic-memory/integrations/mcp-server

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Check installation
pip list | grep rae-mcp-server

# Test import
python -c "from rae_mcp_server import server; print('✓ Import successful')"

# Check version
python -c "import rae_mcp_server; print(rae_mcp_server.__version__)"
```

---

## Configuration

### Environment Variables

Create `.env` file in `integrations/mcp-server/`:

```bash
# RAE API Configuration
RAE_API_URL=http://localhost:8000
RAE_API_KEY=your-rae-api-key
RAE_PROJECT_ID=my-project
RAE_TENANT_ID=default-tenant

# Optional: Logging
LOG_LEVEL=INFO
```

### IDE-Specific Configuration

#### Claude Desktop - Detailed Setup

**macOS Configuration:**

1. Open Terminal
2. Edit config file:
   ```bash
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. Add MCP server configuration:
   ```json
   {
     "mcpServers": {
       "rae-memory": {
         "command": "python",
         "args": ["-m", "rae_mcp_server"],
         "env": {
           "RAE_API_URL": "http://localhost:8000",
           "RAE_API_KEY": "your-actual-api-key",
           "RAE_PROJECT_ID": "my-actual-project",
           "RAE_TENANT_ID": "default-tenant"
         }
       }
     }
   }
   ```

4. Save and close (Ctrl+X, Y, Enter)
5. Restart Claude Desktop

**Windows Configuration:**

1. Navigate to: `%APPDATA%\Claude`
2. Create or edit `claude_desktop_config.json`
3. Add configuration (same JSON as above)
4. Save and restart Claude Desktop

**Linux Configuration:**

1. Navigate to: `~/.config/Claude`
2. Create or edit `claude_desktop_config.json`
3. Add configuration (same JSON as above)
4. Save and restart Claude Desktop

#### Cursor - Detailed Setup

1. Open your project in Cursor
2. Create `.cursor` directory:
   ```bash
   mkdir -p .cursor
   ```

3. Create `config.json`:
   ```bash
   nano .cursor/config.json
   ```

4. Add configuration:
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

5. Save and reload Cursor (Cmd+R or Ctrl+R)

#### Cline - Detailed Setup

1. Install Cline extension from VSCode marketplace
2. Open Command Palette (Cmd+Shift+P or Ctrl+Shift+P)
3. Type "Cline: Open Settings"
4. Find "MCP Servers" section
5. Click "Edit in settings.json"
6. Add configuration:
   ```json
   {
     "cline.mcpServers": {
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
   ```
7. Save and reload VSCode

---

## Troubleshooting

### Installation Issues

**Problem: `pip install` fails**

```bash
# Solution 1: Upgrade pip
pip install --upgrade pip setuptools wheel

# Solution 2: Install dependencies manually
pip install mcp httpx structlog pydantic python-dotenv

# Solution 3: Use Python 3.11 if you have 3.12+
python3.11 -m pip install -e .
```

**Problem: Import error for `mcp` module**

```bash
# Install mcp directly
pip install mcp>=0.9.0

# Or install from requirements
pip install -r requirements.txt
```

**Problem: Permission denied**

```bash
# On macOS/Linux: Use user install
pip install --user -e .

# Or fix permissions
sudo chown -R $USER:$USER .
```

### Configuration Issues

**Problem: Server not starting in IDE**

1. Check if RAE API is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Test MCP server directly:
   ```bash
   python -m rae_mcp_server
   ```

3. Check environment variables:
   ```bash
   python -c "import os; print(os.getenv('RAE_API_URL'))"
   ```

**Problem: Tools not available**

1. Verify IDE MCP integration is enabled
2. Check IDE logs for errors
3. Restart IDE completely
4. Try Claude Desktop (most reliable MCP support)

**Problem: Authentication errors**

1. Verify API key:
   ```bash
   curl -H "X-API-Key: your-key" http://localhost:8000/health
   ```

2. Check tenant ID matches
3. Verify project ID exists

### Runtime Issues

**Problem: Slow responses**

1. Check network latency:
   ```bash
   ping localhost
   ```

2. Check RAE API performance:
   ```bash
   time curl http://localhost:8000/health
   ```

3. Monitor RAE API logs

**Problem: Connection refused**

1. Verify RAE API is running:
   ```bash
   docker ps | grep memory-api
   ```

2. Check port availability:
   ```bash
   lsof -i :8000
   ```

3. Check firewall settings

---

## Testing Installation

### Manual Tests

**Test 1: Direct Server Test**

```bash
# Start server directly
python -m rae_mcp_server

# Should show: "Starting RAE MCP Server..."
# Press Ctrl+C to stop
```

**Test 2: API Connectivity**

```python
# Test script: test_connection.py
import asyncio
from rae_mcp_server.server import rae_client

async def test():
    try:
        result = await rae_client.search_memory("test", top_k=1)
        print(f"✓ Connection successful: {len(result)} results")
    except Exception as e:
        print(f"✗ Connection failed: {e}")

asyncio.run(test())
```

**Test 3: IDE Integration**

In your IDE, ask:

```
Please save this to memory: "Installation test successful"
```

Expected: AI uses `save_memory` tool and returns success message.

### Automated Tests

```bash
# Run test suite
cd integrations/mcp-server
pytest

# With verbose output
pytest -v

# With coverage
pytest --cov=rae_mcp_server
```

---

## Uninstallation

### Remove Package

```bash
pip uninstall rae-mcp-server
```

### Remove Configuration

**Claude Desktop:**
```bash
rm ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Cursor:**
```bash
rm .cursor/config.json
```

**Cline:**
Remove MCP server configuration from VSCode settings.

---

## Getting Help

### Documentation

- **README.md** - Main documentation
- **USAGE_EXAMPLES.md** - Detailed usage examples
- **KIERUNEK_3_SUMMARY.md** - Implementation details

### Support Channels

- GitHub Issues: https://github.com/your-org/rae-agentic-memory/issues
- Documentation: https://docs.rae-memory.dev
- Email: support@rae-memory.dev

### Common Questions

**Q: Which IDE should I use?**
A: Claude Desktop has the most mature MCP support. Cursor and Cline are also good options.

**Q: Can I use multiple projects?**
A: Yes, set different `RAE_PROJECT_ID` for each project's configuration.

**Q: How do I update?**
A: Run `git pull && pip install -e .` in the mcp-server directory.

**Q: Is Windows fully supported?**
A: Yes, but some path configurations differ. Follow Windows-specific instructions above.

---

## Next Steps

After successful installation:

1. Read **USAGE_EXAMPLES.md** for detailed usage patterns
2. Try the examples with your own project
3. Configure project-specific guidelines in semantic memory
4. Integrate with your team's workflow

Enjoy your AI-powered memory system! 🎉
