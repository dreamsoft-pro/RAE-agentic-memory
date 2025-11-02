# Agentic Memory — Starter Pack (Gemini/Jules-ready)

To repo zawiera minimalny szkielet pod pamięć agentową:
- **FastAPI** (`apps/memory-api`) z kontraktami OpenAPI/MCP
- **Qdrant** (jedna kolekcja dense+sparse)
- **PostgreSQL + RLS** (DDL w `infra/postgres/ddl`)
- **Reranker service** (stub)
- **CLI (Typer)** proxy do API
- **Eval** (goldenset + skrypt metryk)
- **Docker Compose** + CI stub

## Szybki start
```bash
make up
# otwórz http://localhost:8000/health
python cli/gemini-cli/main.py health
```

Następnie użyj promptów w `docs/PROMPTS.md`, by Gemini i Jules wygenerowały pełną implementację.
