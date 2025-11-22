# Changelog

All notable changes to RAE (Reflective Agentic Memory Engine) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- v2.0: Multi-modal memory support (images, audio)
- Memory consolidation and pruning strategies
- Advanced analytics dashboard
- Plugin system for custom integrations

---

## [1.2.0-enterprise] - 2025-11-22

### Added - Enterprise Architecture
- **Full Dependency Injection Implementation**
  - GraphExtractionService now uses constructor injection for repositories
  - HybridSearchService now uses constructor injection for repositories
  - Composition Root pattern in `dependencies.py` with factory functions
  - Factory functions: `get_graph_extraction_service()`, `get_hybrid_search_service()`
  - Repository factories: `get_memory_repository()`, `get_graph_repository()`
  - 100% testable services with mock repositories
  - Zero hidden dependencies

- **Enterprise Logging Configuration**
  - `LOG_LEVEL` environment variable for external libraries (uvicorn, asyncpg, httpx, celery)
  - `RAE_APP_LOG_LEVEL` environment variable for RAE application logs
  - Separate log levels for cleaner production logs
  - JSON output for log aggregation tools
  - Comprehensive documentation in `logging_config.py`

- **Security Enhancements**
  - Hidden API key input in `quickstart.sh` using `read -s`
  - Secure `.env` file permissions (chmod 600)
  - API keys never appear in terminal history
  - Clear user feedback during setup

- **Test Suite Improvements**
  - Updated all DI tests to use new constructor injection pattern
  - 244 total tests (213 passing - 87%)
  - Core DI services at 100% test coverage
  - Comprehensive test documentation in `TESTING.md`

### Changed
- **Service Layer Refactoring**
  - `GraphExtractionService.__init__()` now accepts `memory_repo` and `graph_repo` parameters
  - `HybridSearchService.__init__()` now accepts `graph_repo` parameter
  - Removed direct repository instantiation from services
  - All API endpoints updated to use DI factories

- **Configuration Files**
  - `.env.example` updated with `LOG_LEVEL` and `RAE_APP_LOG_LEVEL`
  - `apps/memory_api/config.py` updated with log level settings
  - `apps/memory_api/logging_config.py` completely rewritten with multi-level configuration

- **API Endpoints**
  - `/v1/graph/query` now uses `get_hybrid_search_service()` dependency
  - `/v1/graph/subgraph` now uses `get_hybrid_search_service()` dependency
  - `/v1/memory/query` now uses `get_hybrid_search_service()` dependency

### Fixed
- Test fixtures updated to match new DI constructor signatures
- Mock repository setup in all service tests
- Import statements in test files for DI pattern

### Documentation
- Updated `TESTING.md` with v1.2.0 test results and DI improvements
- Updated `RELEASE_NOTES.md` with comprehensive v1.2.0-enterprise section
- Added extensive inline documentation to `dependencies.py`
- Added logging configuration guide in `logging_config.py`

### Technical Debt Addressed
- Eliminated service-level repository instantiation
- Removed hidden dependencies from service constructors
- Improved testability through constructor injection
- Separated application logs from library logs

---

## [1.1.0-mcp] - 2025-01-15

### Added - MCP Integration
- Comprehensive Model Context Protocol (MCP) integration
- Context Watcher HTTP daemon for file synchronization
- IDE integration configs for Claude Desktop, Cursor, and Cline
- Prometheus metrics for MCP server (12 new metrics)
- End-to-end testing suite (20+ tests)
- 10,000+ lines of integration documentation

### Changed
- Module renamed: `rae_mcp_server` → `rae_mcp`
- API endpoints standardized to `/v1/memory/*` pattern
- Architectural separation: `integrations/mcp/` vs `integrations/context-watcher/`

### Documentation
- `docs/integrations/mcp_protocol_server.md` (6,400+ lines)
- `docs/integrations/context_watcher_daemon.md` (3,800+ lines)
- Updated READMEs for both integrations

---

## [1.0.0-rc.1] - 2024-11-22

### Added - Production Readiness
- **MLServiceClient Resilience Layer**
  - Automatic retry logic with exponential backoff (200ms/400ms/800ms)
  - Circuit breaker pattern (opens after 5 failures, resets after 30s)
  - Structured logging for all ML service calls
  - Health check with automatic circuit breaker reset

- **Complete ML Service Endpoints**
  - `/embeddings` - Local embedding generation (SentenceTransformers)
  - `/resolve-entities` - Entity deduplication and clustering
  - `/extract-keywords` - NLP keyword extraction (spaCy)
  - `/extract-triples` - Knowledge triple extraction (dependency parsing)

- **GraphExtractionService Repository Pattern**
  - Complete refactoring to use MemoryRepository and GraphRepository
  - Removed all direct SQL queries from service layer
  - Added `GraphRepository.create_node()`, `create_edge()`, `store_graph_triples()` methods
  - Added `get_node_internal_id()` for internal ID lookups
  - 7 integration tests using testcontainers (100% passing)

- **Docker Enhancements**
  - Parameterized PostgreSQL credentials via environment variables
  - Health checks for all services (postgres, redis, qdrant, ml-service, rae-api)
  - Proper restart policies (`unless-stopped`) for production
  - Network isolation with `rae-network`

- **Repository Hygiene**
  - Updated `.gitignore` with coverage files, test artifacts
  - Removed accidental coverage artifacts from repository
  - Clean project structure

### Changed
- Database credentials now configurable via `.env` file
- MLServiceClient now enterprise-grade with fault tolerance
- All ML operations use resilience layer with automatic retries
- GraphExtractionService now follows clean Repository/DAO pattern
- MemoryRepository.get_episodic_memories() now includes `source` field

### Fixed
- JSON serialization for JSONB PostgreSQL columns in all repositories
- Circuit breaker state management
- Health check bypasses circuit breaker for recovery detection
- Knowledge graph edges now have proper UNIQUE constraint for duplicate prevention

---

## [0.9.0] - 2024-11-22

### Added - Microservices Architecture
- **ML Service Separation**
  - Heavy ML dependencies isolated in separate microservice
  - Docker image size reduction: 3-5GB → 500MB (memory-api)
  - Horizontal scalability for ML operations
  - Independent deployment and scaling

- **Repository/DAO Pattern**
  - `GraphRepository` - All knowledge graph operations
  - `MemoryRepository` - Memory CRUD operations
  - Clean separation of data access from business logic
  - Improved testability and maintainability

- **Testcontainers Integration**
  - 4 integration tests with real PostgreSQL (ankane/pgvector)
  - BFS/DFS graph traversal tests on real database
  - Recursive CTE validation
  - No mocks for database operations

### Changed
- Refactored `HybridSearchService` to use repositories
- Split requirements: `requirements-base.txt` (lightweight) vs `requirements-ml.txt` (heavy)
- Database operations isolated in repository layer

### Technical Debt Addressed
- Removed direct SQL queries from service layer
- Eliminated tight coupling between API and ML operations
- Improved error handling and logging

---

## [0.8.0] - 2024-11-15

### Added - Core Features
- Multi-layer memory architecture (Episodic, Working, Semantic, Long-term)
- Hybrid search combining vector similarity and knowledge graph traversal
- GraphRAG implementation with BFS/DFS traversal strategies
- Entity resolution and deduplication
- Reflection engine for automatic insight extraction
- Multi-tenancy with Row Level Security (RLS)

### Infrastructure
- Docker Compose setup with all services
- PostgreSQL with pgvector extension
- Qdrant vector store integration
- Redis caching layer
- Prometheus metrics and monitoring

---

## Release Naming Convention

- **v0.x.x** - Alpha/Beta releases (feature development)
- **v1.0.0-rc.x** - Release candidates (production-ready, final testing)
- **v1.0.0** - First stable public release
- **v1.x.x** - Stable releases with backward compatibility
- **v2.0.0** - Major version with breaking changes

---

## Links

- [Repository](https://github.com/dreamsoft-pro/RAE-agentic-memory)
- [Issue Tracker](https://github.com/dreamsoft-pro/RAE-agentic-memory/issues)
- [Documentation](./docs/)

---

## Contributors

- Grzegorz Leśniowski - [@dreamsoft-pro](https://github.com/dreamsoft-pro)
- Community contributors welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md)
