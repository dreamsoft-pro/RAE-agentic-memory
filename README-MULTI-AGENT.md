# 🤖 Multi-Agent Collaboration with Shared RAE Memory

> **TL;DR**: Podłącz dowolną liczbę AI agentów (Claude, Gemini, Cursor, Windsurf, etc.) do wspólnej pamięci RAE. Wszyscy widzą to samo, uczą się od siebie, dzielą kontekst.

---

## 🎯 Czym jest to?

**RAE Multi-Agent System** umożliwia wielu AI agentom współpracę przez **wspólną, trwałą pamięć**.

### Bez RAE:
```
Claude          Gemini          Cursor
  🧠              🧠              🧠
  │               │               │
  └───────────────┴───────────────┘
         Każdy działa solo
         Brak wspólnej pamięci
         Duplikacja pracy
```

### Z RAE:
```
┌─────────────────────────────────────────────────┐
│              RAE Memory Engine                   │
│         🧠 Współdzielona Pamięć                 │
│                                                  │
│  • Episodic:   Co się wydarzyło                 │
│  • Semantic:   Wiedza i zasady                  │
│  • Working:    Obecny kontekst                  │
│  • Reflective: Wnioski i uczenie się           │
└────────┬──────────┬──────────┬──────────────────┘
         │          │          │
    ┌────┴────┐ ┌──┴────┐ ┌──┴─────┐
    │ Claude  │ │Gemini │ │ Cursor │  ... ∞ więcej
    │  Code   │ │  CLI  │ │   IDE  │
    └─────────┘ └───────┘ └────────┘
```

**Korzyści:**
- ✅ **Wspólny kontekst**: Każdy agent widzi pracę innych
- ✅ **Uczenie się**: Decyzje jednego agenta są dostępne dla innych
- ✅ **Ciągłość**: Pamięć przetrwa zamknięcie sesji
- ✅ **Skalowalność**: Dodaj więcej agentów bez limitu
- ✅ **Audit trail**: Pełna historia współpracy

---

## 🚀 Quick Start (1 minuta)

### Krok 1: Uruchom RAE API

```bash
docker-compose up -d rae-api

# Sprawdź czy działa
curl http://localhost:8000/health
```

### Krok 2: Uruchom automatyczny setup

```bash
# Pierwsza instalacja - skopiuj przykładowy skrypt
cp .claude/scripts/setup-rae-mcp-example.sh .local/setup-rae-mcp.sh

# Opcjonalnie: dostosuj konfigurację
nano .local/setup-rae-mcp.sh

# Uruchom setup
.local/setup-rae-mcp.sh
```

**To wszystko!** 🎉

Script automatycznie:
1. ✅ Sprawdza czy RAE API działa
2. ✅ Instaluje MCP serwery
3. ✅ Konfiguruje Claude Code
4. ✅ Konfiguruje Gemini CLI
5. ✅ Testuje połączenie

### Krok 3: Użyj agentów

**W Claude Code:**
```
"Save to RAE: Using PostgreSQL for main database"
```

**W Gemini CLI:**
```bash
gemini "Search RAE: What database are we using?"
# → Finds: "Using PostgreSQL for main database"
```

**Wspólna pamięć działa!** 🧠

---

## 📐 Architektura (Scalable)

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


    Dodaj więcej agentów:

    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │  Windsurf IDE   │  │  Cline (VSCode) │  │  Your Custom    │
    │                 │  │                 │  │  Agent          │
    └─────────────────┘  └─────────────────┘  └─────────────────┘

    Każdy nowy agent automatycznie:
    - Ma dostęp do całej historii
    - Widzi pracę poprzednich agentów
    - Może zapisywać swoją pracę
    - Uczy się od innych
```

**Im więcej agentów, tym bogatsza współdzielona pamięć!**

---

## 🔧 Konfiguracja Szczegółowa

### Zmienne Środowiskowe

```bash
# Podstawowe
export RAE_API_URL="http://localhost:8000"
export RAE_API_KEY="dev-key"

# Multi-tenancy (opcjonalne)
export RAE_TENANT_ID="my-team"           # Izolacja między zespołami
export RAE_PROJECT_ID="my-awesome-app"   # Izolacja między projektami

# Uruchom setup
.local/setup-rae-mcp.sh
```

### Struktura Tenantów

```
┌─────────────────────────────────────────────┐
│             RAE Memory API                   │
├─────────────────────────────────────────────┤
│                                              │
│  Tenant: "team-frontend"                    │
│  ├─ Project: "nextjs-app"                   │
│  │  └─ Agenty: Claude, Cursor               │
│  └─ Project: "react-native-app"             │
│     └─ Agenty: Gemini, Windsurf             │
│                                              │
│  Tenant: "team-backend"                     │
│  ├─ Project: "api-service"                  │
│  │  └─ Agenty: Claude, Cline                │
│  └─ Project: "worker-service"               │
│     └─ Agenty: Gemini                       │
│                                              │
└─────────────────────────────────────────────┘
```

**Izolacja:**
- Tenant "team-frontend" **nie widzi** pamięci tenant "team-backend"
- Project "nextjs-app" **nie widzi** pamięci "react-native-app"
- W ramach jednego projektu **wszyscy agenty widzą tę samą pamięć**

---

## 🎓 Przykłady Użycia

### Przykład 1: Współpraca przy implementacji

**Dzień 1 - Claude Code:**
```
User: "Implement user authentication"

Claude: [Searches RAE for auth patterns]
        [Implements OAuth2 with JWT]
        [Saves to RAE]:
        "Implemented OAuth2 authentication with JWT tokens.
         Access tokens expire after 1h, refresh tokens after 7 days.
         Using bcrypt for password hashing."
```

**Dzień 2 - Gemini CLI:**
```bash
gemini "Write tests for authentication"

# Gemini automatycznie:
# 1. Search RAE: "authentication implementation"
# 2. Znajduje: "OAuth2 with JWT, 1h access, 7d refresh, bcrypt"
# 3. Pisze testy pokrywające te szczegóły
# 4. Saves to RAE: "Added tests for OAuth2 flow..."
```

**Dzień 3 - Cursor IDE:**
```
User: "Fix the authentication bug"

Cursor: [Searches RAE: "authentication"]
        [Widzi: implementację, testy, historię zmian]
        [Naprawia bug z pełnym kontekstem]
```

### Przykład 2: Code Review Workflow

```
┌──────────────────────────────────────────────┐
│ 1. Claude implementuje feature              │
│    └─> Saves: "Added payment processing"    │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│ 2. Gemini robi review                        │
│    └─> Searches RAE for context             │
│    └─> Saves: "Payment code looks good,     │
│              but missing error handling"     │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│ 3. Claude dodaje error handling              │
│    └─> Reads Gemini's feedback from RAE     │
│    └─> Implements fixes                      │
│    └─> Saves: "Added comprehensive error    │
│              handling as suggested"          │
└──────────────────────────────────────────────┘
```

### Przykład 3: Długoterminowe uczenie się

**Tydzień 1:**
```
Claude: "Tried approach A for caching - didn't work well"
        [Saves to RAE with tag: "lessons-learned"]
```

**Tydzień 4:**
```
Gemini: "How should I implement caching?"
        [Searches RAE: "caching lessons"]
        [Finds: "Approach A didn't work"]
        [Suggests: "Based on past experience, let's try B"]
```

**Miesiąc później:**
```
New team member's agent:
        [Onboards with full context from RAE]
        [Knows: what works, what doesn't, why]
```

---

## 🛠️ Dodawanie Więcej Agentów

### Claude Desktop App (GUI)

**macOS:**
```bash
# Edytuj: ~/Library/Application Support/Claude/claude_desktop_config.json
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

Utwórz `.cursor/mcp.json` w projekcie:

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

Podobnie jak Cursor - utwórz config w projekcie.

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

### Sprawdź status agentów

```bash
# Claude Code
claude mcp list

# Gemini CLI
gemini mcp list
```

### Zapytaj RAE o aktywność

```bash
curl -X POST http://localhost:8000/v1/memory/query \
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

Pamięć jest **kompletnie izolowana** między tenantami:

```
Tenant A → Widzi tylko swoją pamięć
Tenant B → Widzi tylko swoją pamięć
```

**Brak leakage między zespołami!**

### API Keys

```bash
# Produkcja - użyj silnych kluczy
export RAE_API_KEY="$(openssl rand -base64 32)"

# Development - prosty klucz
export RAE_API_KEY="dev-key"
```

### PII Scrubbing

MCP Server automatycznie maskuje:
- API keys (w logach)
- Emails (częściowo)
- IP addresses (częściowo)
- Credit cards
- SSNs

---

## 🎯 Best Practices

### 1. Używaj opisowych source identifiers

```python
# ❌ ZŁE
source="agent"

# ✅ DOBRE
source="claude-code:feature-implementation"
source="gemini-cli:code-review"
source="cursor:bug-fix"
```

### 2. Taguj sensownie

```python
# ❌ ZŁE
tags=["code"]

# ✅ DOBRE
tags=["authentication", "security", "bug-fix", "lesson-learned"]
```

### 3. Używaj odpowiednich warstw

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

### 4. Ustawiaj importance

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

### Problem: Agent nie widzi memories

**Sprawdź:**
```bash
# 1. Czy używasz tego samego tenant_id?
echo $RAE_TENANT_ID

# 2. Czy używasz tego samego project_id?
echo $RAE_PROJECT_ID

# 3. Czy RAE API działa?
curl http://localhost:8000/health

# 4. Czy MCP server jest połączony?
claude mcp list
gemini mcp list
```

### Problem: "Layer validation error"

**Używaj poprawnych kodów warstw:**
- `episodic` lub `em`
- `working` lub `stm`
- `semantic` lub `ltm`
- `reflective` lub `rm`

MCP server automatycznie mapuje human-friendly names → API codes.

### Problem: Setup script fails

```bash
# Debug mode
bash -x .local/setup-rae-mcp.sh

# Check logs
docker-compose logs rae-api
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
