# DEVELOPER CHEAT SHEET (ScreenWatcher + RAE)

## 🚀 Startup
1. **Connect to RAE**: `python3 scripts/connect_rae_mcp.py`
2. **Start Stack**: `docker compose up -d`
3. **Check Logs**: `docker compose logs -f web`

## 🛠️ Testing & Quality
- **Unit Tests**: `docker compose exec web pytest`
- **Linting**: `docker compose exec web make lint` (or `black .`, `isort .`)
- **Shell Access**: `docker compose exec web bash`

## 🔌 MCP & RAE
- **RAE API**: `http://localhost:8001`
- **ScreenWatcher MCP**: `http://localhost:9001`
- **Bridge Script**: `scripts/connect_rae_mcp.py` (Use this for agent context)

## 📊 Infrastructure (Ports)
- **Web App**: `9000` -> `8000`
- **MCP**: `9001` -> `8001`
- **Postgres**: `5433` -> `5432`
- **Redis**: `6380` -> `6379`
- **Qdrant**: `6335` -> `6333`

## 📂 Project Structure
- `apps/`: Django apps (core logic)
- `scripts/`: Utility scripts & data importers
- `docker-compose.yml`: Main infra config

## 📝 Rules
- **Non-Interactive Only**: No `vim`/`nano`.
- **Zero Warnings**: Fix linter errors immediately.
- **Cluster-First**: Heavy tasks on external nodes (if configured).
