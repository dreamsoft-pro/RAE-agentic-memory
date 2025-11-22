# RAE Testing Guide

Comprehensive guide for testing the RAE (Reflective Agentic Memory Engine) system.

## Test Coverage

### Current Test Suite

| Module | Test File | Coverage | Tests |
|--------|-----------|----------|-------|
| **Reflection Engine** | `test_reflection_engine.py` | ✅ Comprehensive | 20+ |
| **Semantic Memory** | `test_semantic_memory.py` | ✅ Core Features | 10+ |
| **Graph Repository** | `test_graph_algorithms.py`, `test_temporal_graph.py` | ✅ Algorithms | 15+ |
| **Hybrid Search** | `test_hybrid_search.py` | ✅ Multi-strategy | 12+ |
| **Evaluation Suite** | `test_evaluation_suite.py` | ✅ IR Metrics | 10+ |
| **Event Triggers** | `test_event_triggers.py` | ✅ Rules Engine | 15+ |
| **Dashboard** | `test_dashboard_websocket.py` | ✅ Real-time | 12+ |
| **API Client** | `test_api_client.py` | ✅ Resilience | 20+ |

**Total:** 100+ tests across 8 enterprise modules

---

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Ensure database is running
docker-compose up -d postgres
```

### Run All Tests

```bash
# Run all tests
pytest apps/memory_api/tests/

# Run with coverage
pytest --cov=apps/memory_api --cov-report=html apps/memory_api/tests/

# Run specific module
pytest apps/memory_api/tests/test_reflection_engine.py

# Run with verbose output
pytest -v apps/memory_api/tests/
```

### Run Tests by Category

```bash
# Unit tests only
pytest -m "not integration" apps/memory_api/tests/

# Integration tests only
pytest -m integration apps/memory_api/tests/

# Async tests
pytest -m asyncio apps/memory_api/tests/
```

### Run Tests in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run with 4 workers
pytest -n 4 apps/memory_api/tests/
```

---

## Test Structure

### Directory Layout

```
apps/memory_api/tests/
├── __init__.py
├── conftest.py                           # Shared fixtures
├── test_reflection_engine.py             # Reflection tests
├── test_semantic_memory.py               # Semantic memory tests
├── test_graph_algorithms.py              # Graph algorithm tests
├── test_temporal_graph.py                # Temporal graph tests
├── test_hybrid_search.py                 # Hybrid search tests
├── test_evaluation_suite.py              # Evaluation tests
├── test_event_triggers.py                # Event trigger tests
├── test_dashboard_websocket.py           # Dashboard tests
├── test_api_client.py                    # API client tests
├── test_background_tasks.py              # Background tasks
├── test_analytics.py                     # Analytics tests
└── test_api_e2e.py                       # End-to-end tests
```

### Test Naming Convention

```python
# Pattern: test_<functionality>_<scenario>
def test_generate_reflection_from_memories()
def test_clustering_hdbscan()
def test_circuit_breaker_opens_on_failures()
```

---

## Test Categories

### 1. Reflection Engine Tests

**File:** `test_reflection_engine.py`

**Covers:**
- ✅ Reflection generation from memories
- ✅ HDBSCAN clustering with fallback to K-means
- ✅ Hierarchical reflection creation
- ✅ Meta-insight generation
- ✅ Cycle detection in reflection relationships
- ✅ Reflection scoring (novelty, importance, utility)
- ✅ Repository operations (CRUD)

**Key Tests:**
```python
test_generate_reflection_from_memories()
test_clustering_hdbscan()
test_create_hierarchical_reflection()
test_generate_meta_insight()
test_cycle_detection_with_cycle()
test_reflection_scoring()
```

### 2. Semantic Memory Tests

**File:** `test_semantic_memory.py`

**Covers:**
- ✅ Semantic node extraction from memories
- ✅ Term canonicalization
- ✅ 3-stage semantic search (topic → canonicalization → re-ranking)
- ✅ TTL/LTM decay model
- ✅ Reinforcement learning

**Key Tests:**
```python
test_extract_semantic_nodes()
test_canonicalization()
test_semantic_search_3_stages()
test_ttl_ltm_decay()
test_node_reinforcement()
```

### 3. Evaluation Suite Tests

**File:** `test_evaluation_suite.py`

**Covers:**
- ✅ IR metrics: MRR, NDCG, Precision, Recall, MAP
- ✅ Kolmogorov-Smirnov test
- ✅ Population Stability Index (PSI)
- ✅ Drift severity classification
- ✅ A/B testing traffic allocation

**Key Tests:**
```python
test_mrr_calculation()
test_ndcg_calculation()
test_precision_recall()
test_kolmogorov_smirnov_test()
test_psi_calculation()
test_drift_severity_classification()
```

### 4. Event Triggers Tests

**File:** `test_event_triggers.py`

**Covers:**
- ✅ Event emission and processing
- ✅ Condition evaluation (simple, AND, OR, nested)
- ✅ All 12 condition operators
- ✅ Rate limiting
- ✅ Cooldown periods
- ✅ Action execution
- ✅ Workflow orchestration

**Key Tests:**
```python
test_process_event()
test_evaluate_simple_condition()
test_evaluate_condition_group_and()
test_nested_condition_groups()
test_condition_operators()
test_rate_limiting()
test_cooldown_period()
```

### 5. Dashboard WebSocket Tests

**File:** `test_dashboard_websocket.py`

**Covers:**
- ✅ WebSocket connection lifecycle
- ✅ Event broadcasting to tenants
- ✅ Subscription filtering
- ✅ Metrics collection
- ✅ Health monitoring
- ✅ Significant change detection

**Key Tests:**
```python
test_websocket_connect()
test_broadcast_to_tenant()
test_subscription_filtering()
test_collect_system_metrics()
test_check_system_health()
test_broadcast_quality_alert()
```

### 6. API Client Tests

**File:** `test_api_client.py`

**Covers:**
- ✅ Error classification (6 categories)
- ✅ Circuit breaker (CLOSED, OPEN, HALF_OPEN)
- ✅ Retry logic with exponential backoff
- ✅ Response caching with TTL
- ✅ Cache invalidation
- ✅ Statistics tracking

**Key Tests:**
```python
test_classify_network_error()
test_circuit_breaker_opens_on_failures()
test_circuit_breaker_half_open_recovery()
test_cache_set_and_get()
test_retry_on_network_error()
test_exponential_backoff()
```

---

## Writing New Tests

### Test Template

```python
"""
Tests for <Module Name> - <Brief Description>

Tests cover:
- Feature 1
- Feature 2
- Feature 3
"""

import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, Mock

from apps.memory_api.services.my_service import MyService


@pytest.fixture
def mock_pool():
    """Mock database connection pool"""
    return AsyncMock()


@pytest.fixture
def my_service(mock_pool):
    """Service instance"""
    return MyService(mock_pool)


@pytest.mark.asyncio
async def test_my_feature(my_service, mock_pool):
    """Test my feature description"""
    # Arrange
    mock_pool.fetchrow = AsyncMock(return_value={"id": uuid4()})

    # Act
    result = await my_service.my_method()

    # Assert
    assert result is not None
```

### Best Practices

1. **Use Fixtures** - Share common setup via pytest fixtures
2. **Mock External Dependencies** - Database, LLM, HTTP calls
3. **Test Edge Cases** - Empty inputs, errors, boundary conditions
4. **Async Tests** - Use `@pytest.mark.asyncio` for async functions
5. **Clear Names** - Descriptive test names explain what's being tested
6. **AAA Pattern** - Arrange, Act, Assert
7. **Isolation** - Tests should not depend on each other

---

## Mocking Guidelines

### Database Mocking

```python
@pytest.fixture
def mock_pool():
    pool = AsyncMock()
    pool.fetchrow = AsyncMock(return_value={"id": uuid4()})
    pool.fetch = AsyncMock(return_value=[{"data": "test"}])
    pool.execute = AsyncMock()
    return pool
```

### LLM Provider Mocking

```python
@pytest.fixture
def mock_llm():
    llm = AsyncMock()
    llm.generate = AsyncMock(return_value="Generated content")
    llm.generate_structured = AsyncMock(return_value={"score": 0.85})
    return llm
```

### HTTP Client Mocking

```python
@pytest.fixture
def mock_http_response():
    response = Mock()
    response.json.return_value = {"success": True}
    response.status_code = 200
    response.raise_for_status = Mock()
    return response
```

---

## Integration Tests

### Database Integration

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_reflection_workflow(real_pool):
    """Test with real database"""
    # Use real database connection
    # Test end-to-end workflow
    pass
```

### API Integration

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_e2e():
    """Test full API workflow"""
    # Test actual HTTP requests
    # Verify database changes
    pass
```

---

## Coverage Reports

### Generate HTML Report

```bash
pytest --cov=apps/memory_api \
       --cov-report=html \
       --cov-report=term \
       apps/memory_api/tests/

# View report
open htmlcov/index.html
```

### Coverage Targets

| Category | Target | Current |
|----------|--------|---------|
| Overall | 80%+ | ✅ 85%+ |
| Services | 90%+ | ✅ 92% |
| Routes | 75%+ | ✅ 78% |
| Models | 95%+ | ✅ 98% |
| Repositories | 85%+ | ✅ 88% |

---

## Continuous Integration

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov

      - name: Run tests
        run: pytest --cov=apps/memory_api apps/memory_api/tests/

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Debugging Tests

### Run Single Test

```bash
pytest apps/memory_api/tests/test_reflection_engine.py::test_generate_reflection_from_memories -v
```

### Print Debug Output

```bash
pytest -s apps/memory_api/tests/test_reflection_engine.py
```

### Use PDB Debugger

```python
def test_my_feature():
    # Add breakpoint
    import pdb; pdb.set_trace()

    result = my_function()
    assert result is not None
```

### Show Fixtures

```bash
pytest --fixtures apps/memory_api/tests/
```

---

## Performance Testing

### Load Testing

```python
@pytest.mark.performance
@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test system under load"""
    tasks = [
        create_memory(f"Memory {i}")
        for i in range(1000)
    ]

    results = await asyncio.gather(*tasks)
    assert len(results) == 1000
```

### Benchmark Tests

```bash
pip install pytest-benchmark

# Run benchmark
pytest apps/memory_api/tests/test_benchmarks.py --benchmark-only
```

---

## Test Data Fixtures

### Sample Memories

```python
@pytest.fixture
def sample_memories():
    return [
        {
            "id": uuid4(),
            "content": "Test memory content",
            "importance": 0.8,
            "embedding": np.random.rand(1536).tolist()
        }
    ]
```

### Sample Events

```python
@pytest.fixture
def sample_event():
    return Event(
        event_id=uuid4(),
        event_type=EventType.MEMORY_CREATED,
        tenant_id="test",
        project_id="test",
        payload={"importance": 0.9}
    )
```

---

## Troubleshooting

### Common Issues

**Issue:** Tests fail with database connection error
```bash
# Solution: Ensure PostgreSQL is running
docker-compose up -d postgres
```

**Issue:** Async tests not running
```bash
# Solution: Install pytest-asyncio
pip install pytest-asyncio
```

**Issue:** Import errors
```bash
# Solution: Install package in editable mode
pip install -e .
```

**Issue:** Slow tests
```bash
# Solution: Run in parallel
pip install pytest-xdist
pytest -n auto apps/memory_api/tests/
```

---

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

---

## Contributing Tests

When adding new features:

1. **Write tests first** (TDD approach)
2. **Aim for 80%+ coverage** of new code
3. **Include edge cases** and error scenarios
4. **Update this guide** with new test patterns
5. **Run full test suite** before committing

```bash
# Pre-commit checklist
pytest apps/memory_api/tests/                    # All tests pass
pytest --cov=apps/memory_api apps/memory_api/tests/  # Coverage check
black apps/memory_api/                           # Code formatting
mypy apps/memory_api/                            # Type checking
```

---

**Test Coverage Status:** ✅ 100+ tests | ✅ 85%+ coverage | ✅ All modules covered
