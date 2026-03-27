.PHONY: help start stop restart logs clean install lint test format db-init demo dev docs benchmark-lite benchmark-extended benchmark-industrial benchmark-large benchmark-drift benchmark-profile benchmark-plot benchmark-full benchmark-all benchmark-compare benchmark-gate

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

start:  ## Start all services with Universal GPU Detection
	@echo "🚀 Starting RAE..."
	./scripts/start_rae.sh up -d
	@echo "✅ RAE is running!"
	@echo "📖 API Documentation: http://localhost:8000/docs"
	@echo "📊 Dashboard: http://localhost:8501"
	@echo "🔍 Health check: curl http://localhost:8000/health"

stop:  ## Stop all services
	@echo "🛑 Stopping RAE..."
	docker compose down
	@echo "✅ Services stopped"

restart:  ## Restart all services
	@echo "🔄 Restarting RAE..."
	docker compose restart
	@echo "✅ Services restarted"

logs:  ## Show logs from all services
	docker compose logs -f

logs-api:  ## Show API logs only
	docker compose logs -f rae-api

logs-worker:  ## Show Celery worker logs
	docker compose logs -f celery-worker

clean:  ## Clean up volumes and containers
	@echo "🧹 Cleaning up..."
	docker compose down -v
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
	@$(VENV_PIP) install -r apps/reranker_service/requirements.txt || true
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

dev-full:  ## Start full development environment (infra, API, Reranker, MCP)
	@echo "🔧 Starting full development environment..."
	./scripts/dev_mode.sh

install-mcp-service:  ## Install MCP systemd service for auto-start
	@echo "🔧 Installing MCP systemd service..."
	./scripts/install_mcp_service.sh

demo:  ## Run interactive quickstart demo
	@echo "🎬 Running interactive demo..."
	@$(VENV_PYTHON) examples/quickstart.py

# ==============================================================================
# CODE QUALITY
# ==============================================================================



lint:  ## Run linters (ruff, black, isort, mypy)
	@echo "🔍 Running linters..."
	@$(VENV_ACTIVATE) && ruff check apps/ sdk/ integrations/ rae-core/ benchmarking/ eval/
	@$(VENV_ACTIVATE) && black --check apps/ sdk/ integrations/ rae-core/ benchmarking/ eval/
	@$(VENV_ACTIVATE) && isort --check apps/ sdk/ integrations/ rae-core/ benchmarking/ eval/
	@$(VENV_ACTIVATE) && mypy apps/ sdk/ rae-core/ integrations/ benchmarking/ eval/
	@echo "✅ Linting complete"

security:  ## Run security scans (safety, bandit)
	@echo "🔒 Running security scans..."
	@$(VENV_ACTIVATE) && pip install safety bandit > /dev/null
	@$(VENV_ACTIVATE) && safety check --file requirements-dev.txt || true
	@$(VENV_ACTIVATE) && bandit -c pyproject.toml -r apps/ sdk/ rae-core/ -ll || true
	@echo "✅ Security scan complete"

security-check:  ## [ISO 27001] Strict security check (fails on error)
	@echo "🔒 Running strict ISO 27001 security compliance check..."
	@$(VENV_ACTIVATE) && pip install safety bandit > /dev/null
	@$(VENV_ACTIVATE) && safety check --file requirements-dev.txt
	@$(VENV_ACTIVATE) && bandit -c pyproject.toml -r apps/ sdk/ rae-core/ -ll
	@echo "✅ Security compliance verified"

format:  ## Format code with black, isort, and ruff
	@echo "🎨 Formatting code..."
	@$(VENV_ACTIVATE) && black apps/ sdk/ integrations/ rae-core/ benchmarking/ eval/
	@$(VENV_ACTIVATE) && isort apps/ sdk/ integrations/ rae-core/ benchmarking/ eval/
	@$(VENV_ACTIVATE) && ruff check --fix apps/ sdk/ integrations/ rae-core/ benchmarking/ eval/
	@echo "✅ Code formatted"

# ==============================================================================
# TESTING (PROFILES)
# ==============================================================================

test:  ## Run tests using LITE profile (default)
	@echo "🧪 Running tests (LITE PROFILE)..."
	@$(MAKE) test-lite

test-lite:  ## [PROFILE: LITE] Run unit tests (CI/CPU safe)
	@echo "🧪 Running LITE tests (Unit + No-GPU)..."
	@RAE_PROFILE=lite PYTHONPATH=. $(VENV_PYTHON) -m pytest -m "not slow and not gpu and not integration and not llm" -v $(ARGS)

test-core:  ## [PROFILE: CORE] Run rae-core unit tests with coverage
	@echo "🧪 Running RAE-CORE tests..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest rae-core/tests/ --cov=rae-core/rae_core --cov-report=term-missing -v $(ARGS)

test-fast: ## Run tests and stop on first failure (Fail Fast)
	@echo "🏃 Running tests in FAIL-FAST mode..."
	@ARGS="-x $(ARGS)" $(MAKE) test-lite

test-fix: ## Run ONLY tests that failed in the last run
	@echo "🛠️  Running only LAST FAILED tests..."
	@ARGS="--lf $(ARGS)" $(MAKE) test-lite

test-failed: ## Alias for test-fix
	@$(MAKE) test-fix

test-int:  ## [PROFILE: INTEGRATION] Run integration tests (Requires Docker Stack)
	@echo "🧪 Running INTEGRATION tests (API/DB Contracts)..."
	@RAE_PROFILE=standard RAE_DB_MODE=migrate OTEL_TRACES_ENABLED=false PYTHONPATH=. $(VENV_PYTHON) -m pytest -m "integration" -v

test-gpu:  ## [PROFILE: FULL_GPU] Run GPU/LLM tests (Requires Local LLM)
	@echo "🧪 Running FULL_GPU tests (Reranking/Benchmarks)..."
	@RAE_PROFILE=research RAE_RERANKER_MODE=llm PYTHONPATH=. $(VENV_PYTHON) -m pytest -m "gpu or benchmark" -v

test-smoke: ## Run quick E2E smoke tests to verify critical paths
	@echo "🧪 Running smoke tests..."
	@RAE_DB_MODE=migrate PYTHONPATH=. $(VENV_PYTHON) -m pytest -m "smoke" -v

test-full-stack: ## Run all collected tests (Unit + Integration + LLM + OTEL)
	@echo "🧪 Running absolute full stack verification (970+ tests)..."
	@OTEL_TRACES_ENABLED=true RAE_DB_MODE=migrate PYTHONPATH=. $(VENV_PYTHON) -m pytest -v

test-compliance: ## Run ISO 42001 Compliance tests
	@echo "🛡️ Running ISO 42001 compliance tests..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest -m "iso42001" --no-cov -v

test-iso: ## Alias for test-compliance
	@$(MAKE) test-compliance


test-local-llm: ## Run tests using local Ollama LLM
	@echo "🧪 Running tests with Local LLM (Ollama)..."
	@RAE_LLM_BACKEND=ollama OLLAMA_API_URL=http://localhost:11434 RAE_DB_MODE=migrate PYTHONPATH=. $(VENV_PYTHON) -m pytest -m "llm" -v

test-architecture: ## Run architectural and dependency tests
	@echo "🧪 Running architectural tests..."
	@PYTHONPATH=. $(VENV_PYTHON) -m pytest -m "architecture" -v

mcp-test-integration:  ## Run MCP integration tests (requires RAE API running)

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

# Remote Node1 (KUBUS) configuration
KUBUS_IP = 100.66.252.117

benchmark-kubus: ## Run all benchmarks on Kubus (Node1)
	@echo "🚀 Redirecting benchmarks to KUBUS (Node1) @ $(KUBUS_IP)..."
	@POSTGRES_HOST=$(KUBUS_IP) \
	 REDIS_URL=redis://$(KUBUS_IP):6379/0 \
	 QDRANT_URL=http://$(KUBUS_IP):6333 \
	 RAE_API_URL=http://$(KUBUS_IP):8000 \
	 $(MAKE) benchmark-all

benchmark-kubus-full: ## Run FULL heavy benchmarks on Kubus (Node1)
	@echo "🚀 Redirecting HEAVY benchmarks to KUBUS (Node1) @ $(KUBUS_IP)..."
	@POSTGRES_HOST=$(KUBUS_IP) \
	 REDIS_URL=redis://$(KUBUS_IP):6379/0 \
	 QDRANT_URL=http://$(KUBUS_IP):6333 \
	 RAE_API_URL=http://$(KUBUS_IP):8000 \
	 $(MAKE) benchmark-full

benchmark-local-lite: ## Run quick benchmark locally against dev infra
	@echo "🔬 Running lite benchmark locally..."
	@export $$(cat .env.benchmark | xargs) && PYTHONPATH=.:rae-core:apps $(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set academic_lite.yaml

benchmark-local-extended: ## Run extended benchmark locally against dev infra
	@echo "🔬 Running extended benchmark locally..."
	@export $$(cat .env.benchmark | xargs) && PYTHONPATH=.:rae-core:apps $(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set academic_extended.yaml

benchmark-local-industrial: ## Run industrial benchmark locally against dev infra
	@echo "🔬 Running industrial benchmark locally..."
	@export $$(cat .env.benchmark | xargs) && PYTHONPATH=.:rae-core:apps $(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set industrial_small.yaml

benchmark-local-large: ## Run large-scale benchmark locally against dev infra
	@echo "🔬 Running large-scale benchmark locally..."
	@export $$(cat .env.benchmark | xargs) && PYTHONPATH=.:rae-core:apps $(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set industrial_large.yaml

benchmark-local-nine-five: ## Run specialized 9/5 benchmarks locally
	@echo "🚦 Running specialized 9/5 benchmarks locally..."
	@export $$(cat .env.benchmark | xargs) && PYTHONPATH=.:rae-core:apps $(VENV_PYTHON) -m benchmarking.nine_five_benchmarks.runner --benchmark all

benchmark-lite:  ## Run quick benchmark (academic_lite, <10s)
	@echo "🔬 Running lite benchmark..."
	@$(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set benchmarking/sets/academic_lite.yaml
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

benchmark-gate:  ## Run nine_five benchmarks and check thresholds (CI gate)
	@echo "🚦 Running benchmark gate (CI threshold check)..."
	@echo "Running nine_five benchmark suite..."
	@$(VENV_PYTHON) -m benchmarking.nine_five_benchmarks.runner --benchmark all
	@echo "Checking thresholds..."
	@$(VENV_PYTHON) benchmarking/scripts/check_thresholds.py
	@echo "✅ Benchmark gate passed!"

benchmark-large:  ## Run large-scale stress benchmark (industrial_large, ~15min)
	@echo "🔬 Running large-scale benchmark..."
	@$(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set industrial_large.yaml
	@echo "✅ Large-scale benchmark complete"

benchmark-drift:  ## Run memory drift stress test (stress_memory_drift, ~2min)
	@echo "🔬 Running memory drift benchmark..."
	@$(VENV_PYTHON) benchmarking/scripts/run_benchmark.py --set stress_memory_drift.yaml
	@echo "✅ Memory drift benchmark complete"

benchmark-profile:  ## Profile query latency (Usage: make benchmark-profile BENCHMARK=academic_lite.yaml RUNS=100)
	@if [ -z "$(BENCHMARK)" ]; then \
		echo "❌ Error: BENCHMARK argument required."; \
		echo "Usage: make benchmark-profile BENCHMARK=academic_lite.yaml RUNS=100"; \
		exit 1; \
	fi
	@RUNS=$${RUNS:-100}; \
	echo "🔬 Profiling latency ($$RUNS runs per query)..."; \
	$(VENV_PYTHON) benchmarking/scripts/profile_latency.py --benchmark $(BENCHMARK) --runs $$RUNS --output latency_profile.json

benchmark-plot:  ## Generate plots from benchmark results (Usage: make benchmark-plot RESULTS=results/*.json)
	@if [ -z "$(RESULTS)" ]; then \
		echo "❌ Error: RESULTS argument required."; \
		echo "Usage: make benchmark-plot RESULTS='results/academic_*.json'"; \
		exit 1; \
	fi
	@echo "📊 Generating plots..."
	@mkdir -p benchmarking/plots
	@$(VENV_PYTHON) benchmarking/scripts/generate_plots.py --results $(RESULTS) --output benchmarking/plots/

benchmark-full:  ## Run complete benchmark suite (all benchmarks + profiling)
	@echo "🔬 Running FULL benchmark suite..."
	@$(MAKE) benchmark-lite
	@$(MAKE) benchmark-extended
	@$(MAKE) benchmark-industrial
	@$(MAKE) benchmark-large
	@$(MAKE) benchmark-drift
	@echo "✅ Full benchmark suite complete"

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
		docker compose down -v; \
		docker compose up -d postgres redis qdrant; \
		sleep 5; \
		$(VENV_ACTIVATE) && alembic upgrade head; \
		echo "✅ Database reset complete"; \
	else \
		echo "❌ Cancelled"; \
	fi

db-shell:  ## Open PostgreSQL shell
	@docker compose exec postgres psql -U rae -d rae

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
	docker compose build
	@echo "✅ Build complete"

ps:  ## Show running containers
	@docker compose ps

shell-api:  ## Open shell in API container
	@docker compose exec rae-api /bin/bash

shell-postgres:  ## Open shell in Postgres container
	@docker compose exec postgres /bin/bash

secure-shell:  ## [HARD FRAMES] Open Developer Shell inside Secure Container (No Internet, Code Access, Kernel Access)
	@echo "🛡️  Entering HARD FRAMES Environment..."
	@docker compose -f docker-compose.secure.yml up -d --build rae-agent-secure
	@docker exec -it rae-agentic-memory-agnostic-core-rae-agent-secure-1 /bin/bash
	@echo "👋 Exited Secure Shell."

# ==============================================================================
# DEPLOYMENT
# ==============================================================================

pre-push:  ## [ZERO DRIFT] Run BEFORE pushing: Format -> Docs -> Lint -> Test
	@echo "🚀 Starting Pre-Push Protocol (Zero Drift)..."
	@echo "1️⃣  Formatting Code..."
	@$(MAKE) format
	@echo "2️⃣  Generating Documentation & Metrics (Prevents CI Commits)..."
	@$(MAKE) docs
	@echo "3️⃣  Linting (Strict)..."
	@$(MAKE) lint
	@echo "4️⃣  Running Unit Tests..."
	@$(MAKE) test-lite
	@echo "✅ READY TO PUSH! (Remember to commit any modified docs/metrics files)"

deploy-prod:  ## Deploy to production (placeholder)
	@echo "🚀 Deploying to production..."
	@echo "⚠️  Not implemented yet. See docs/guides/production-deployment.md"

health:  ## Check health of all services
	@echo "🏥 Checking service health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ API not responding"
	@curl -s http://localhost:6333/ | python -m json.tool || echo "❌ Qdrant not responding"
	@docker compose exec -T postgres pg_isready -U rae || echo "❌ Postgres not responding"
	@docker compose exec -T redis redis-cli ping || echo "❌ Redis not responding"

# ==============================================================================
# UTILITIES
# ==============================================================================



version:  ## Show version information
	@echo "RAE - Reflective Agentic Memory Engine"
	@echo "Version: 3.0.2"
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

run-research:
	@./scripts/run_research_mode.sh
