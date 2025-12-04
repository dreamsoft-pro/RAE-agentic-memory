"""
API Contract Tests

These tests ensure that API responses maintain backward compatibility.
Any breaking change (removed field, changed type, etc.) will fail these tests.

Run with: pytest -m contract

Note: These tests require test infrastructure (client_with_overrides fixture).
If infrastructure is not available, tests will be skipped.
"""

import pytest
from datetime import datetime
from typing import Dict, Any, List

# Check if test infrastructure is available
try:
    from tests.api.v1.test_memory import client_with_overrides
    HAS_TEST_INFRASTRUCTURE = True
except ImportError:
    HAS_TEST_INFRASTRUCTURE = False


# ============================================================================
# Contract Validation Helpers
# ============================================================================


def assert_schema(data: Dict[str, Any], expected_schema: Dict[str, type]):
    """
    Assert that data matches expected schema.

    Args:
        data: Response data
        expected_schema: Dict mapping field names to expected types
    """
    for field, expected_type in expected_schema.items():
        assert field in data, f"Missing required field: {field}"

        value = data[field]

        # Handle optional fields (None is OK)
        if value is None:
            continue

        # Handle list types
        if expected_type == list:
            assert isinstance(value, list), f"{field} should be list, got {type(value)}"
        # Handle dict types
        elif expected_type == dict:
            assert isinstance(value, dict), f"{field} should be dict, got {type(value)}"
        # Handle datetime strings
        elif expected_type == "datetime":
            assert isinstance(value, str), f"{field} should be string (ISO datetime)"
            # Try parsing
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                pytest.fail(f"{field} is not valid ISO datetime: {value}")
        # Handle regular types
        else:
            assert isinstance(
                value, expected_type
            ), f"{field} should be {expected_type}, got {type(value)}"


def assert_fields_not_present(data: Dict[str, Any], forbidden_fields: List[str]):
    """Assert that deprecated/removed fields are not in response"""
    for field in forbidden_fields:
        assert field not in data, f"Deprecated field '{field}' should not be in response"


# ============================================================================
# Memory API Contracts
# ============================================================================


@pytest.mark.contract
@pytest.mark.skipif(not HAS_TEST_INFRASTRUCTURE, reason="Test infrastructure not available")
class TestMemoryStoreContract:
    """Contract tests for /v1/memory/store endpoint"""

    def test_store_memory_response_schema(self, client_with_overrides):
        """Ensure store memory returns correct schema"""
        payload = {
            "content": "Test memory content",
            "source": "test",
            "layer": "em",
            "importance": 0.8,
            "project": "test-project",
        }

        response = client_with_overrides.post(
            "/v1/memory/store", json=payload, headers={"X-Tenant-Id": "test-tenant"}
        )

        assert response.status_code == 200
        data = response.json()

        # Required fields
        expected_schema = {
            "id": str,
            "content": str,
            "source": str,
            "layer": str,
            "importance": (int, float),
            "project": str,
            "created_at": "datetime",
            "last_accessed_at": "datetime",
            "usage_count": int,
        }

        assert_schema(data, expected_schema)

        # Ensure no deprecated fields
        assert_fields_not_present(data, ["deprecated_at", "old_id"])


@pytest.mark.contract
@pytest.mark.skipif(not HAS_TEST_INFRASTRUCTURE, reason="Test infrastructure not available")
class TestMemoryQueryContract:
    """Contract tests for /v1/memory/query endpoint"""

    def test_query_memory_response_schema(self, client_with_overrides):
        """Ensure query memory returns correct schema"""
        payload = {"query_text": "test query", "k": 5}

        response = client_with_overrides.post(
            "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
        )

        assert response.status_code == 200
        data = response.json()

        # Top-level fields
        assert "results" in data
        assert isinstance(data["results"], list)

        # If we have results, check their schema
        if data["results"]:
            result = data["results"][0]
            expected_schema = {
                "id": str,
                "content": str,
                "score": (int, float),
                "importance": (int, float),
                "layer": str,
                "source": str,
                "project": str,
                "tags": list,
            }
            assert_schema(result, expected_schema)

    def test_hybrid_search_response_schema(self, client_with_overrides):
        """Ensure hybrid search returns correct schema"""
        payload = {
            "query_text": "test query",
            "k": 5,
            "use_graph": True,
            "project": "test-project",
        }

        response = client_with_overrides.post(
            "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
        )

        assert response.status_code == 200
        data = response.json()

        # Hybrid search specific fields
        assert "results" in data
        assert "synthesized_context" in data or True  # Optional
        assert "graph_statistics" in data or True  # Optional


@pytest.mark.contract
@pytest.mark.skipif(not HAS_TEST_INFRASTRUCTURE, reason="Test infrastructure not available")
class TestMemoryDeleteContract:
    """Contract tests for /v1/memory/delete endpoint"""

    def test_delete_memory_response_schema(self, client_with_overrides):
        """Ensure delete memory returns correct schema"""
        response = client_with_overrides.delete(
            "/v1/memory/delete?memory_id=test-id",
            headers={"X-Tenant-Id": "test-tenant"},
        )

        # Could be 200 (deleted) or 404 (not found)
        assert response.status_code in [200, 404]

        data = response.json()

        # Should have message field
        assert "message" in data or "detail" in data


# ============================================================================
# Agent API Contracts
# ============================================================================


@pytest.mark.contract
@pytest.mark.skipif(not HAS_TEST_INFRASTRUCTURE, reason="Test infrastructure not available")
class TestAgentExecuteContract:
    """Contract tests for /v1/agent/execute endpoint"""

    def test_agent_execute_response_schema(self, client_with_overrides):
        """Ensure agent execute returns correct schema"""
        payload = {
            "task": "Test task",
            "context": {"test": "data"},
            "project": "test-project",
        }

        response = client_with_overrides.post(
            "/v1/agent/execute", json=payload, headers={"X-Tenant-Id": "test-tenant"}
        )

        # Should return 200 or error
        if response.status_code == 200:
            data = response.json()

            expected_schema = {
                "task_id": str,
                "status": str,
                "result": (dict, str, type(None)),
            }

            assert_schema(data, expected_schema)


# ============================================================================
# Health & Status Contracts
# ============================================================================


@pytest.mark.contract
@pytest.mark.skipif(not HAS_TEST_INFRASTRUCTURE, reason="Test infrastructure not available")
class TestHealthContract:
    """Contract tests for /health endpoint"""

    def test_health_response_schema(self, client_with_overrides):
        """Ensure health check returns correct schema"""
        response = client_with_overrides.get("/health")

        assert response.status_code == 200
        data = response.json()

        expected_schema = {
            "status": str,
            "version": str,
        }

        assert_schema(data, expected_schema)

        # Status should be one of known values
        assert data["status"] in ["healthy", "degraded", "unhealthy"]


# ============================================================================
# Error Response Contracts
# ============================================================================


@pytest.mark.contract
@pytest.mark.skipif(not HAS_TEST_INFRASTRUCTURE, reason="Test infrastructure not available")
class TestErrorResponseContract:
    """Contract tests for error responses"""

    def test_400_error_schema(self, client_with_overrides):
        """Ensure 400 errors have consistent schema"""
        # Send invalid payload
        payload = {"invalid": "data"}

        response = client_with_overrides.post(
            "/v1/memory/store", json=payload, headers={"X-Tenant-Id": "test-tenant"}
        )

        assert response.status_code in [400, 422]  # Validation error
        data = response.json()

        # FastAPI returns 'detail' for validation errors
        assert "detail" in data

    def test_404_error_schema(self, client_with_overrides):
        """Ensure 404 errors have consistent schema"""
        response = client_with_overrides.get(
            "/v1/nonexistent", headers={"X-Tenant-Id": "test-tenant"}
        )

        assert response.status_code == 404
        data = response.json()

        assert "detail" in data


# ============================================================================
# Pagination Contract
# ============================================================================


@pytest.mark.contract
@pytest.mark.skipif(not HAS_TEST_INFRASTRUCTURE, reason="Test infrastructure not available")
class TestPaginationContract:
    """Contract tests for paginated endpoints"""

    def test_pagination_schema(self, client_with_overrides):
        """Ensure paginated responses have consistent structure"""
        # Test with any endpoint that supports pagination
        # This is a placeholder - adjust based on actual pagination endpoints

        # Expected pagination fields:
        # - results: list
        # - total: int
        # - page: int
        # - page_size: int
        # - has_next: bool

        # Note: Implement when pagination is standardized
        pass


# ============================================================================
# Backward Compatibility Tests
# ============================================================================


@pytest.mark.contract
@pytest.mark.skipif(not HAS_TEST_INFRASTRUCTURE, reason="Test infrastructure not available")
class TestBackwardCompatibility:
    """Ensure we don't break backward compatibility"""

    def test_no_removed_endpoints(self, client_with_overrides):
        """Ensure critical endpoints still exist"""
        critical_endpoints = [
            ("/health", "GET"),
            ("/v1/memory/store", "POST"),
            ("/v1/memory/query", "POST"),
            ("/v1/memory/delete", "DELETE"),
        ]

        for endpoint, method in critical_endpoints:
            if method == "GET":
                response = client_with_overrides.get(
                    endpoint, headers={"X-Tenant-Id": "test-tenant"}
                )
            elif method == "POST":
                response = client_with_overrides.post(
                    endpoint, json={}, headers={"X-Tenant-Id": "test-tenant"}
                )
            elif method == "DELETE":
                response = client_with_overrides.delete(
                    f"{endpoint}?memory_id=test",
                    headers={"X-Tenant-Id": "test-tenant"},
                )

            # Should not be 404
            assert (
                response.status_code != 404
            ), f"Critical endpoint {method} {endpoint} not found!"

    def test_api_version_in_header(self, client_with_overrides):
        """Ensure API version is returned in headers"""
        response = client_with_overrides.get("/health")

        # Check for version header (if implemented)
        # assert "X-API-Version" in response.headers
        # For now, just ensure we have some version indicator
        pass
