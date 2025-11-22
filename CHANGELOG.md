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
