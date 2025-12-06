.PHONY: help start stop restart logs clean install lint test format db-init demo dev docs benchmark-lite benchmark-extended benchmark-industrial benchmark-all benchmark-compare

# ==============================================================================
# HELP
# ==============================================================================

help:  ## Show this help message
	@echo "RAE - Reflective Agentic Memory Engine"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# ==============================================================================
# QUICK START
# ==============================================================================

start:  ## Start all services with Docker Compose
	@echo "🚀 Starting RAE..."
	docker-compose up -d
	@echo "✅ RAE is running!"
	@echo "📖 API Documentation: http://localhost:8000/docs"
	@echo "📊 Dashboard: http://localhost:8501"
	@echo "🔍 Health check: curl http://localhost:8000/health"

stop:  ## Stop all services
	@echo "🛑 Stopping RAE..."
	docker-compose down
	@echo "✅ Services stopped"

restart:  ## Restart all services
	@echo "🔄 Restarting RAE..."
	docker-compose restart
	@echo "✅ Services restarted"

logs:  ## Show logs from all services
	docker-compose logs -f

logs-api:  ## Show API logs only
	docker-compose logs -f rae-api

logs-worker:  ## Show Celery worker logs
	docker-compose logs -f celery-worker

clean:  ## Clean up volumes and containers
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup complete"

# ==============================================================================
# DEVELOPMENT
# ==============================================================================

VENV_PYTHON = .venv/bin/python
VENV_PIP = .venv/bin/pip
VENV_ACTIVATE = . .venv/bin/activate

install:  ## Install all Python dependencies
	@echo "📦 Installing dependencies..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	@$(VENV_PIP) install --upgrade pip
	@$(VENV_PIP) install -r requirements-dev.txt
	@$(VENV_PIP) install -r apps/memory_api/requirements.txt
	@$(VENV_PIP) install -e sdk/python/rae_memory_sdk
	@echo "✅ Installation complete"

install-all:  ## Install all dependencies (including integrations)
	@echo "📦 Installing all dependencies..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	@$(VENV_PIP) install --upgrade pip
	@$(VENV_PIP) install -r requirements-dev.txt
	@$(VENV_PIP) install -r apps/memory_api/requirements.txt
	@$(VENV_PIP) install -r apps/reranker-service/requirements.txt || true
	@$(VENV_PIP) install -r apps/ml_service/requirements.txt || true # New ML Service requirements
	@$(VENV_PIP) install -r cli/agent-cli/requirements.txt || true
	@$(VENV_PIP) install -r eval/requirements.txt || true
	@$(VENV_PIP) install -r integrations/langchain/requirements.txt || true
	@$(VENV_PIP) install -r integrations/llama_index/requirements.txt || true
	@$(VENV_PIP) install -e integrations/mcp || true
	@$(VENV_PIP) install -r integrations/ollama-wrapper/requirements.txt || true
	@$(VENV_PIP) install -e sdk/python/rae_memory_sdk
	@echo "✅ All dependencies installed"

ml-install:  ## Install ML service dependencies
	@echo "📦 Installing ML service dependencies..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	@$(VENV_PIP) install --upgrade pip
	@$(VENV_PIP) install -r apps/ml_service/requirements.txt
	@echo "✅ ML service dependencies installed"

dev:  ## Start API in development mode (with auto-reload)
	@echo "🔧 Starting development server..."
	@$(VENV_ACTIVATE) && uvicorn apps.memory_api.main:app --reload --host 0.0.0.0 --port 8000

demo:  ## Run interactive quickstart demo
	@echo "🎬 Running interactive demo..."
	@$(VENV_PYTHON) examples/quickstart.py

# ==============================================================================
# CODE QUALITY
# ==============================================================================

format:  ## Format code with black and isort
	@echo "🎨 Formatting code..."
	@$(VENV_ACTIVATE) && black apps/ sdk/ integrations/
	@$(VENV_ACTIVATE) && isort apps/ sdk/ integrations/
	@echo "✅ Code formatted"

lint:  ## Run linters (ruff, black, isort, mypy)
	@echo "🔍 Running linters..."
	@$(VENV_ACTIVATE) && ruff check apps/ sdk/ integrations/
	@$(VENV_ACTIVATE) && black --check apps/ sdk/ integrations/
	@$(VENV_ACTIVATE) && isort --check apps/ sdk/ integrations/
	@$(VENV_ACTIVATE) && mypy apps/ sdk/ || true
	@echo "✅ Linting complete"

security:  ## Run security scans (safety, bandit)
	@echo "🔒 Running security scans..."
	@$(VENV_ACTIVATE) && pip install safety bandit > /dev/null
	@$(VENV_ACTIVATE) && safety check --file requirements-dev.txt || true
	@$(VENV_ACTIVATE) && bandit -r apps/ sdk/ -ll || true
	@echo "✅ Security scan complete"

format:  ## Format code with black, isort, and ruff
	@echo "🎨 Formatting code..."
	@$(VENV_ACTIVATE) && black apps/ sdk/ integrations/
	@$(VENV_ACTIVATE) && isort apps/ sdk/ integrations/
	@$(VENV_ACTIVATE) && ruff check --fix apps/ sdk/ integrations/
	@echo "✅ Code formatted"

# ==============================================================================
# TESTING
# ==============================================================================

test:  ## Run all tests
	@echo "🧪 Running tests..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest

test-unit:  ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest -m "not integration and not llm and not contract and not performance" -v

test-integration:  ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest -m "integration" -v

test-cov:  ## Run tests with coverage report
	@echo "🧪 Running tests with coverage..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest --cov=apps --cov=sdk --cov-report=html --cov-report=term-missing
	@echo "📊 Coverage report generated at htmlcov/index.html"

test-focus:  ## Run a specific test file without coverage checks (Usage: make test-focus FILE=tests/foo.py)
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Error: FILE argument is required. Usage: make test-focus FILE=path/to/test.py"; \
		exit 1; \
	fi
	@echo "🧪 Running focused test on $(FILE) (skipping coverage)..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest --no-cov $(FILE) -v

test-watch:  ## Run tests in watch mode
	@echo "🧪 Running tests in watch mode..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest-watch

# ==============================================================================
# BENCHMARKING
# ==============================================================================

benchmark-lite:  ## Run quick benchmark (academic_lite, <10s)
	@echo "🔬 Running lite benchmark..."
	@$(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set academic_lite.yaml
	@echo "✅ Lite benchmark complete"

benchmark-extended:  ## Run extended benchmark (academic_extended, ~30s)
	@echo "🔬 Running extended benchmark..."
	@$(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set academic_extended.yaml
	@echo "✅ Extended benchmark complete"

benchmark-industrial:  ## Run industrial benchmark (industrial_small, ~2min)
	@echo "🔬 Running industrial benchmark..."
	@$(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set industrial_small.yaml
	@echo "✅ Industrial benchmark complete"

benchmark-all:  ## Run all benchmarks sequentially
	@echo "🔬 Running all benchmarks..."
	@$(MAKE) benchmark-lite
	@$(MAKE) benchmark-extended
	@$(MAKE) benchmark-industrial
	@echo "✅ All benchmarks complete"

benchmark-compare:  ## Compare two benchmark runs (Usage: make benchmark-compare BASE=run1.json COMP=run2.json)
	@if [ -z "$(BASE)" ] || [ -z "$(COMP)" ]; then \
		echo "❌ Error: BASE and COMP arguments required."; \
		echo "Usage: make benchmark-compare BASE=benchmarking/results/run1.json COMP=benchmarking/results/run2.json"; \
		exit 1; \
	fi
	@echo "🔍 Comparing benchmark results..."
	@$(VENV_PYTHON) benchmarking/scripts/compare_runs.py $(BASE) $(COMP) --output comparison_report.md
	@echo "✅ Comparison complete: comparison_report.md"

# ==============================================================================
# DATABASE
# ==============================================================================

db-init:  ## Initialize database with migrations
	@echo "🗄️  Initializing database..."
	@$(VENV_ACTIVATE) && alembic upgrade head
	@echo "✅ Database initialized"

db-migrate:  ## Create a new migration
	@echo "🗄️  Creating migration..."
	@read -p "Migration name: " name; \
	$(VENV_ACTIVATE) && alembic revision --autogenerate -m "$$name"

db-reset:  ## Reset database (WARNING: deletes all data)
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		docker-compose down -v; \
		docker-compose up -d postgres redis qdrant; \
		sleep 5; \
		$(VENV_ACTIVATE) && alembic upgrade head; \
		echo "✅ Database reset complete"; \
	else \
		echo "❌ Cancelled"; \
	fi

db-shell:  ## Open PostgreSQL shell
	@docker-compose exec postgres psql -U rae -d rae

# ==============================================================================
# PRE-COMMIT
# ==============================================================================

pre-commit-install:  ## Install pre-commit hooks
	@echo "🪝 Installing pre-commit hooks..."
	@$(VENV_ACTIVATE) && pre-commit install
	@echo "✅ Pre-commit hooks installed"

pre-commit-run:  ## Run pre-commit on all files
	@echo "🪝 Running pre-commit..."
	@$(VENV_ACTIVATE) && pre-commit run --all-files

# ==============================================================================
# DOCKER SHORTCUTS
# ==============================================================================

build:  ## Build Docker images
	@echo "🏗️  Building Docker images..."
	docker-compose build
	@echo "✅ Build complete"

ps:  ## Show running containers
	@docker-compose ps

shell-api:  ## Open shell in API container
	@docker-compose exec rae-api /bin/bash

shell-postgres:  ## Open shell in Postgres container
	@docker-compose exec postgres /bin/bash

# ==============================================================================
# DEPLOYMENT
# ==============================================================================

deploy-prod:  ## Deploy to production (placeholder)
	@echo "🚀 Deploying to production..."
	@echo "⚠️  Not implemented yet. See docs/guides/production-deployment.md"

health:  ## Check health of all services
	@echo "🏥 Checking service health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ API not responding"
	@curl -s http://localhost:6333/ | python -m json.tool || echo "❌ Qdrant not responding"
	@docker-compose exec -T postgres pg_isready -U rae || echo "❌ Postgres not responding"
	@docker-compose exec -T redis redis-cli ping || echo "❌ Redis not responding"

# ==============================================================================
# UTILITIES
# ==============================================================================

docs:  ## Auto-generate documentation (Changelog, TODOs, Status)
	@echo "📚 Generating documentation..."
	@python3 scripts/docs_automator.py
	@echo "✅ Documentation updated"

version:  ## Show version information
	@echo "RAE - Reflective Agentic Memory Engine"
	@echo "Version: 1.0.0"
	@echo "Python: $(shell python --version)"
	@echo "Docker: $(shell docker --version)"

env-example:  ## Create .env from .env.example
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env from .env.example"; \
		echo "⚠️  Please edit .env and add your API keys"; \
	else \
		echo "⚠️  .env already exists"; \
	fi

# ==============================================================================
# MCP INTEGRATION
# ==============================================================================

mcp-dev-install:  ## Install MCP server in development mode
	@echo "📦 Installing MCP server (development mode)..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	@$(VENV_PIP) install --upgrade pip
	@cd integrations/mcp && ../../$(VENV_PIP) install -e ".[dev]"
	@echo "✅ MCP server installed"
	@echo "🔍 Verify: $(VENV_ACTIVATE) && rae-mcp-server --help"

mcp-install:  ## Install MCP server (production mode)
	@echo "📦 Installing MCP server..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	@$(VENV_PIP) install --upgrade pip
	@cd integrations/mcp && ../../$(VENV_PIP) install -e .
	@echo "✅ MCP server installed"

mcp-test:  ## Run MCP server tests
	@echo "🧪 Running MCP server tests..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest integrations/mcp/tests/ -v
	@echo "✅ MCP tests complete"

mcp-test-integration:  ## Run MCP integration tests (requires RAE API running)
	@echo "🧪 Running MCP integration tests..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest integrations/mcp/tests/test_mcp_integration.py -v
	@echo "✅ MCP integration tests complete"

mcp-test-load:  ## Run MCP load tests (requires RAE API running)
	@echo "🧪 Running MCP load tests..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest integrations/mcp/tests/test_mcp_load.py -v -m load
	@echo "✅ MCP load tests complete"

mcp-lint:  ## Lint MCP server code
	@echo "🔍 Linting MCP server..."
	@$(VENV_ACTIVATE) && ruff check integrations/mcp/
	@$(VENV_ACTIVATE) && black --check integrations/mcp/
	@$(VENV_ACTIVATE) && isort --check integrations/mcp/
	@echo "✅ MCP linting complete"

mcp-format:  ## Format MCP server code
	@echo "🎨 Formatting MCP server..."
	@$(VENV_ACTIVATE) && black integrations/mcp/
	@$(VENV_ACTIVATE) && isort integrations/mcp/
	@echo "✅ MCP code formatted"

mcp-verify:  ## Verify MCP installation and health
	@echo "🔍 Verifying MCP installation..."
	@$(VENV_ACTIVATE) && rae-mcp-server --help || echo "❌ rae-mcp-server not found"
	@echo ""
	@echo "✅ Verification complete"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Configure your IDE using examples/ide-config/<YOUR-IDE>/"
	@echo "  2. Read docs/guides/IDE_INTEGRATION.md for full setup guide"
	@echo "  3. Restart your IDE to load MCP configuration"

# Documentation
.PHONY: docs
docs:
	@echo "🤖 Updating auto-generated documentation..."
	python3 scripts/docs_automator.py
	@echo "✅ Documentation updated. See docs/.auto-generated/metrics/DASHBOARD.md for health status."

docs-validate:  ## Validate documentation (check broken links, placeholders)
	@echo "🔍 Validating documentation..."
	@python3 scripts/validate_docs.py

docs-validate-fix:  ## Validate and auto-fix documentation issues
	@echo "🔍 Validating and fixing documentation..."
	@python3 scripts/validate_docs.py --fix
