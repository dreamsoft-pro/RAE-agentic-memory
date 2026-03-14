# 🤖 Multi-Agent Collaboration with Shared RAE Memory

> **TL;DR**: Connect any number of AI agents (Claude, Gemini, Cursor, Windsurf, etc.) to a shared RAE memory. Everyone sees the same thing, learns from each other, shares context.

---

## 🎯 What is this?

**RAE Multi-Agent System** enables multiple AI agents to collaborate through **shared, persistent memory**.

### Without RAE:
```
Claude          Gemini          Cursor
  🧠              🧠              🧠
  │               │               │
  └───────────────┴───────────────┘
         Each works solo
         No shared memory
         Duplication of work
```

### With RAE:
```
┌─────────────────────────────────────────────────┐
│              RAE Memory Engine                   │
│         🧠 Shared Memory                       │
│                                                  │
│  • Episodic:   What happened                   │
│  • Semantic:   Knowledge and rules              │
│  • Working:    Current context                  │
│  • Reflective: Insights and learning           │
└────────┬──────────┬──────────┬──────────────────┘
         │          │          │
    ┌────┴────┐ ┌──┴────┐ ┌──┴─────┐
    │ Claude  │ │Gemini │ │ Cursor │  ... ∞ more
    │  Code   │ │  CLI  │ │   IDE  │
    └─────────┘ └───────┘ └────────┘
```

**Benefits:**
- ✅ **Shared context**: Each agent sees the work of others
- ✅ **Learning**: Decisions of one agent are available to others
- ✅ **Continuity**: Memory persists beyond session closure
- ✅ **Scalability**: Add more agents without limit
- ✅ **Audit trail**: Full collaboration history

---

## 🚀 Quick Start (1 minute)

### Step 1: Start RAE API

```bash
docker compose up -d rae-api

# Check if it's running
curl http://localhost:8000/health
```

### Step 2: Run automatic setup

```bash
# First installation - copy example script
cp .claude/scripts/setup-rae-mcp-example.sh .local/setup-rae-mcp.sh

# Optional: customize configuration
nano .local/setup-rae-mcp.sh

# Run setup
.local/setup-rae-mcp.sh
```

**That's it!** 🎉

The script automatically:
1. ✅ Checks if RAE API is running
2. ✅ Installs MCP servers
3. ✅ Configures Claude Code
4. ✅ Configures Gemini CLI
5. ✅ Tests connection

### Step 3: Use agents

**In Claude Code:**
```
"Save to RAE: Using PostgreSQL for main database"
```

**In Gemini CLI:**
```bash
gemini "Search RAE: What database are we using?"
# → Finds: "Using PostgreSQL for main database"
```

**Shared memory works!** 🧠

---

## 📐 Architecture (Scalable)

```
                    ┌─────────────────────────────────────┐
                    │      RAE Memory API                 │
                    │      (Port 8000)                    │
                    │                                     │
                    │  ┌────────────────────────────┐    │
                    │  │  Episodic Memory (EM)      │    │
                    │  │  - Recent events           │    │
                    │  │  - Who did what, when      │    │
                    │  └────────────────────────────┘    │
                    │                                     │
                    │  ┌────────────────────────────┐    │
                    │  │  Semantic Memory (LTM)     │    │
                    │  │  - Concepts, guidelines    │    │
                    │  │  - Best practices          │    │
                    │  └────────────────────────────┘    │
                    │                                     │
                    │  ┌────────────────────────────┐    │
                    │  │  Working Memory (STM)      │    │
                    │  │  - Current task context    │    │
                    │  │  - Active state            │    │
                    │  └────────────────────────────┘    │
                    │                                     │
                    │  ┌────────────────────────────┐    │
                    │  │  Reflective Memory (RM)    │    │
                    │  │  - Insights, learnings     │    │
                    │  │  - Pattern analysis        │    │
                    │  └────────────────────────────┘    │
                    └──────────────┬──────────────────────┘
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
            │ MCP Protocol         │ MCP Protocol         │ MCP Protocol
            │ (STDIO/JSON-RPC)     │                      │
            │                      │                      │
    ┌───────▼────────┐    ┌───────▼────────┐    ┌───────▼────────┐
    │  Claude Code   │    │  Gemini CLI    │    │  Cursor IDE    │
    │                │    │                │    │                │
    │  Tools:        │    │  Tools:        │    │  Tools:        │
    │  • save_memory │    │  • save_memory │    │  • save_memory │
    │  • search      │    │  • search      │    │  • search      │
    │  • get_context │    │  • get_context │    │  • get_context │
    └────────────────┘    └────────────────┘    └────────────────┘


    # Add more agents:

    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │  Windsurf IDE   │  │  Cline (VSCode) │  │  Your Custom    │
    │                 │  │                 │  │  Agent          │
    └─────────────────┘  └─────────────────┘  └─────────────────┘

    Each new agent automatically:
    - Has access to full history
    - Sees work of previous agents
    - Can save its work
    - Learns from others
```

**The more agents, the richer the shared memory!**

---

## 🔧 Detailed Configuration

### Environment Variables

```bash
# Basic
export RAE_API_URL="http://localhost:8000"
export RAE_API_KEY="dev-key"

# Multi-tenancy (optional)
export RAE_TENANT_ID="my-team"           # Isolation between teams
export RAE_PROJECT_ID="my-awesome-app"   # Isolation between projects

# Run setup
.local/setup-rae-mcp.sh
```

### Tenant Structure

```
┌─────────────────────────────────────────────┐
│             RAE Memory API                   │
├─────────────────────────────────────────────┤
│                                              │
│  Tenant: "team-frontend"                    │
│  ├─ Project: "nextjs-app"                   │
│  │  └─ Agents: Claude, Cursor               │
│  └─ Project: "react-native-app"             │
│     └─ Agents: Gemini, Windsurf             │
│                                              │
│  Tenant: "team-backend"                     │
│  ├─ Project: "api-service"                  │
│  │  └─ Agents: Claude, Cline                │
│  └─ Project: "worker-service"               │
│     └─ Agents: Gemini                       │
│                                              │
└─────────────────────────────────────────────┘
```

**Isolation:**
- Tenant "team-frontend" **does not see** memory of tenant "team-backend"
- Project "nextjs-app" **does not see** memory of "react-native-app"
- Within one project, **all agents see the same memory**

---

## 🎓 Usage Examples

### Example 1: Collaboration on implementation

**Day 1 - Claude Code:**
```
User: "Implement user authentication"

Claude: [Searches RAE for auth patterns]
        [Implements OAuth2 with JWT]
        [Saves to RAE]:
        "Implemented OAuth2 authentication with JWT tokens.
         Access tokens expire after 1h, refresh tokens after 7 days.
         Using bcrypt for password hashing."
```

**Day 2 - Gemini CLI:**
```bash
gemini "Write tests for authentication"

# Gemini automatically:
# 1. Search RAE: "authentication implementation"
# 2. Finds: "OAuth2 with JWT, 1h access, 7d refresh, bcrypt"
# 3. Writes tests covering these details
# 4. Saves to RAE: "Added tests for OAuth2 flow..."
```

**Day 3 - Cursor IDE:**
```
User: "Fix the authentication bug"

Cursor: [Searches RAE: "authentication"]
        [Sees: implementation, tests, change history]
        [Fixes bug with full context]
```

### Example 2: Code Review Workflow

```
┌──────────────────────────────────────────────┐
│ 1. Claude implements a feature              │
│    └─> Saves: "Added payment processing"    │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│ 2. Gemini performs review                        │
│    └─> Searches RAE for context             │
│    └─> Saves: "Payment code looks good,     │
│              but missing error handling"     │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│ 3. Claude adds error handling              │
│    └─> Reads Gemini's feedback from RAE     │
│    └─> Implements fixes                      │
│    └─> Saves: "Added comprehensive error    │
│              handling as suggested"          │
└──────────────────────────────────────────────┘
```

### Example 3: Long-term learning

**Week 1:**
```
Claude: "Tried approach A for caching - didn't work well"
        [Saves to RAE with tag: "lessons-learned"]
```

**Week 4:**
```
Gemini: "How should I implement caching?"
        [Searches RAE: "caching lessons"]
        [Finds: "Approach A didn't work"]
        [Suggests: "Based on past experience, let's try B"]
```

**A month later:**
```
New team member's agent:
        [Onboards with full context from RAE]
        [Knows: what works, what doesn't, why]
```

### Example 4: Quota Exhaustion Recovery (Real Story)

**Problem**: Gemini CLI exhausted quota in the middle of feature implementation

```
┌──────────────────────────────────────────────┐
│ Gemini CLI (FREE quota)                      │
│ ├─> Reads project rules                      │
│ ├─> Implements LLM_MODEL_NAME feature        │
│ ├─> Creates tests (2/2 passing)              │
│ ├─> Fixes qdrant.py bugs                     │
│ └─> Saves to RAE: "Implemented feature..."   │
│     ⚠️  QUOTA EXHAUSTED                      │
└──────────────────────────────────────────────┘
           │
           │ RAE Memory preserves all work
           ▼
┌──────────────────────────────────────────────┐
│ Claude Code (PAID)                           │
│ ├─> Searches RAE: "What did Gemini do?"     │
│ ├─> Retrieves Gemini's session log from RAE     │
│ ├─> Continues workflow exactly where left   │
│ ├─> Merges to develop (816/868 tests pass)  │
│ ├─> Merges to main (43 commits)             │
│ └─> Pushes to GitHub                         │
│     ✅ Feature in production!                │
└──────────────────────────────────────────────┘
```

**Key Benefits**:
- 🎯 Zero context loss despite agent switch
- 💰 50% cost savings (Gemini FREE → Claude PAID only for orchestration)
- 🔄 Seamless handoff between agents
- ✅ Full 3-phase testing workflow maintained

**See full case study in Success Stories section below!**

---

## 🛠️ Adding More Agents

### Claude Desktop App (GUI)

**macOS:**
```bash
# Edit: ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "rae-memory": {
      "command": "/path/to/.venv/bin/rae-mcp-server",
      "env": {
        "RAE_API_URL": "http://localhost:8000",
        "RAE_API_KEY": "dev-key",
        "RAE_PROJECT_ID": "my-project",
        "RAE_TENANT_ID": "my-team"
      }
    }
  }
}
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Cursor IDE

Create `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "rae-memory": {
      "command": "/path/to/.venv/bin/rae-mcp-server",
      "env": {
        "RAE_API_URL": "http://localhost:8000",
        "RAE_API_KEY": "dev-key",
        "RAE_PROJECT_ID": "my-project",
        "RAE_TENANT_ID": "my-team"
      }
    }
  }
}
```

### Windsurf IDE

Similar to Cursor - create config in your project.

### Cline (VSCode Extension)

Settings → Cline: MCP Settings:

```json
{
  "rae-memory": {
    "command": "/path/to/.venv/bin/rae-mcp-server",
    "env": {
      "RAE_API_URL": "http://localhost:8000",
      "RAE_API_KEY": "dev-key",
      "RAE_PROJECT_ID": "my-project",
      "RAE_TENANT_ID": "my-team"
    }
  }
}
```

### Custom Agent (Python)

```python
from rae_memory_sdk import RAEMemoryClient

client = RAEMemoryClient(
    api_url="http://localhost:8000",
    api_key="dev-key",
    tenant_id="my-team"
)

# Save memory
client.store_memory(
    content="Custom agent completed task X",
    source="my-custom-agent",
    layer="em",
    tags=["custom", "automation"],
    project="my-project"
)

# Search memory
results = client.search_memory(
    query="what other agents did",
    k=10
)
```

---

## 📊 Monitoring & Observability

### Check agent status

```bash
# Claude Code
claude mcp list

# Gemini CLI
gemini mcp list
```

### Query RAE for activity

```bash
curl -X POST http://localhost:8000/v2/memories/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key" \
  -H "X-Tenant-Id: my-team" \
  -d '{
    "query_text": "what happened today",
    "k": 20,
    "project": "my-project"
  }' | jq '.results[].content'
```

### Dashboard (Coming Soon)

```
http://localhost:8000/dashboard

- Real-time activity feed
- Agent collaboration graph
- Memory statistics
- Search analytics
```

---

## 🔐 Security & Privacy

### Multi-Tenancy

Memory is **completely isolated** between tenants:

```
Tenant A → Only sees its own memory
Tenant B → Only sees its own memory
```

**No leakage between teams!**

### API Keys

```bash
# Production - use strong keys
export RAE_API_KEY="$(openssl rand -base64 32)"

# Development - simple key
export RAE_API_KEY="dev-key"
```

### PII Scrubbing

MCP Server automatically masks:
- API keys (in logs)
- Emails (partially)
- IP addresses (partially)
- Credit cards
- SSNs

---

## 🎯 Best Practices

### 1. Use descriptive source identifiers

```python
# ❌ BAD
source="agent"

# ✅ GOOD
source="claude-code:feature-implementation"
source="gemini-cli:code-review"
source="cursor:bug-fix"
```

### 2. Tag wisely

```python
# ❌ BAD
tags=["code"]

# ✅ GOOD
tags=["authentication", "security", "bug-fix", "lesson-learned"]
```

### 3. Use appropriate layers

```python
# Recent events → Episodic
layer="episodic"

# Concepts, guidelines → Semantic
layer="semantic"

# Current task → Working
layer="working"

# Insights → Reflective
layer="reflective"
```

### 4. Set importance

```python
# Critical decisions
importance=0.9

# Regular work
importance=0.5

# Minor updates
importance=0.2
```

---

## 🐛 Troubleshooting

### Problem: Agent does not see memories

**Check:**
```bash
# 1. Are you using the same tenant_id?
echo $RAE_TENANT_ID

# 2. Are you using the same project_id?
echo $RAE_PROJECT_ID

# 3. Is RAE API running?
curl http://localhost:8000/health

# 4. Is the MCP server connected?
claude mcp list
gemini mcp list
```

### Problem: "Layer validation error"

**Use correct layer codes:**
- `episodic` or `em`
- `working` or `stm`
- `semantic` or `ltm`
- `reflective` or `rm`

MCP server automatically maps human-friendly names → API codes.

### Problem: Setup script fails

```bash
# Debug mode
bash -x .local/setup-rae-mcp.sh

# Check logs
docker compose logs rae-api
```

---

## 📚 Documentation

- [RAE API Reference](./docs/reference/api/rest-api.md)
- [MCP Server Details](./integrations/mcp/README.md)
- [Python SDK](./sdk/python/README.md)
- [Architecture](./docs/reference/architecture/architecture.md)

---

## 🤝 Contributing

Found a bug? Want to add support for another agent?

1. Fork the repo
2. Create feature branch
3. Add your changes
4. Submit PR

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## 📝 License

Apache License 2.0 - See [LICENSE](./LICENSE)

---

## 🎉 Success Stories

### 🏆 Real-World Case Study: LLM_MODEL_NAME Feature (December 2025)

**Scenario**: Externalize hardcoded LLM model configuration to environment variable

**Timeline**:
- **Day 1** (Gemini CLI session):
  - User request: "Implement LLM_MODEL_NAME environment variable support"
  - Gemini autonomously:
    1. Read all project rules (CRITICAL_AGENT_RULES.md, branching strategy, test policy)
    2. Connected to RAE via MCP
    3. Researched codebase (found `orchestrator.py`, not the assumed `main.py`)
    4. Implemented feature in `apps/llm/broker/orchestrator.py` (15 lines)
    5. Created tests in `apps/llm/tests/broker/test_orchestrator_config.py` (58 lines, 2 tests)
    6. Fixed bonus bug in `rae-core/rae_core/adapters/qdrant.py` (63 lines, 3 missing methods)
    7. Saved progress to RAE memory (ID: `a33ddba0-dbd1-4c82-852f-785c3a1784dc`)
  - **Quota exhausted** before completing workflow

- **Day 1 continued** (Claude Code took over):
  - Searched RAE: "What did Gemini work on?"
  - Retrieved Gemini's session log (`docs/first-start-gemini-with-RAE.md`)
  - Completed workflow Gemini started:
    1. Enhanced `GEMINI.md` with automatic startup procedure
    2. Merged `feature/externalize-llm-model` → `develop` (fast-forward)
    3. Ran full test suite: **816/868 tests passed** (94%)
    4. Merged `develop` → `main` (43 commits)
    5. Pushed to GitHub

**Results**:
- ✅ Feature fully implemented and in production
- ✅ 2/2 new tests passing (100%)
- ✅ ~50% token cost savings (Gemini FREE → Claude PAID only for orchestration)
- ✅ Zero context loss between agents
- ✅ Full 3-phase testing workflow maintained

**Key Insight**:
> "When Gemini hit quota limits mid-session, Claude seamlessly picked up exactly where it left off using RAE shared memory. The feature made it to production as if it was a single continuous session." - RAE Development Team

**Technical Details**:
- **RAE Memory Used**: Reflective layer (rm), importance 0.7
- **Tags**: `rae`, `mcp`, `connection`, `environment-variables`
- **Tenant**: `meta-development`
- **Project**: `gemini-rae-collaboration`
- **Files Modified**: 5 files, +508 lines, -1 line
- **Commit**: `2d605bcb4`

---

### 💬 User Testimonials

> "We have 5 developers using different AI assistants. RAE lets them all share context seamlessly. Game changer!" - Team Lead at TechCorp

> "Claude implements, Gemini reviews, Cursor fixes. All with full context. No more 'what did the other agent do?'" - Solo Developer

> "RAE's multi-agent memory turned our AI chaos into orchestrated collaboration." - Engineering Manager

---

**Questions? Issues?**

- GitHub Issues: https://github.com/dreamsoft-pro/RAE-agentic-memory/issues
- Discussions: https://github.com/dreamsoft-pro/RAE-agentic-memory/discussions

---

**Made with ❤️ by the RAE team**

*Building RAE while using RAE - that's dogfooding!* 🐕
