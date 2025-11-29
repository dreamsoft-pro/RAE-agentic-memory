"""
Integration tests for RAE Lite Profile deployment.

These tests verify that the docker-compose.lite.yml configuration works correctly
and all core services are operational.

Requirements:
- Docker and docker-compose installed
- .env file configured with LLM API key
- Ports 8000, 5432, 6333, 6379 available

Usage:
    pytest tests/integration/test_lite_profile.py -v
"""

import subprocess
import time

import httpx
import pytest

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def lite_profile_services():
    """
    Start docker-compose.lite.yml services for integration testing.

    This fixture:
    1. Starts all RAE Lite services
    2. Waits for services to be healthy
    3. Yields control to tests
    4. Tears down services after tests complete
    """
    # Check if docker-compose is available and if not in CI
    docker_compose_missing = subprocess.run(["which", "docker-compose"], capture_output=True).returncode != 0
    in_ci = "CI" in os.environ

    if docker_compose_missing or in_ci:
        pytest.skip("Skipping lite profile tests: docker-compose not available or running in CI (services pre-provisioned)")

    # Start services
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.lite.yml", "up", "-d"],
        check=True,
        capture_output=True,
    )

    # Wait for services to be ready (up to 60 seconds)
    max_retries = 30
    retry_count = 0
    api_ready = False

    while retry_count < max_retries and not api_ready:
        try:
            response = httpx.get("http://localhost:8000/health", timeout=5.0)
            if response.status_code == 200:
                api_ready = True
                break
        except (httpx.ConnectError, httpx.TimeoutException):
            pass

        retry_count += 1
        time.sleep(2)

    if not api_ready:
        # Cleanup on failure
        subprocess.run(
            ["docker-compose", "-f", "docker-compose.lite.yml", "down"],
            capture_output=True,
        )
        pytest.fail("RAE API failed to start within 60 seconds")

    # Services are ready
    yield

    # Teardown: Stop services
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.lite.yml", "down", "-v"],
        capture_output=True,
    )


def test_lite_profile_health_check(lite_profile_services):
    """Test that API health endpoint is accessible"""
    response = httpx.get("http://localhost:8000/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["healthy", "degraded"]


def test_lite_profile_api_docs(lite_profile_services):
    """Test that API documentation is accessible"""
    response = httpx.get("http://localhost:8000/docs")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_lite_profile_store_memory(lite_profile_services):
    """Test storing a memory via API"""
    payload = {
        "content": "Integration test memory for RAE Lite Profile",
        "source": "integration-test",
        "layer": "em",
        "importance": 0.5,
        "tags": ["test", "integration"],
    }

    response = httpx.post(
        "http://localhost:8000/v1/memory/store",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"},
        timeout=10.0,
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert len(data["id"]) > 0


def test_lite_profile_query_memory(lite_profile_services):
    """Test querying memories via API"""
    # First, store a memory
    store_payload = {
        "content": "Test memory for query operation",
        "source": "integration-test",
        "layer": "em",
        "importance": 0.7,
        "tags": ["querytest"],
    }

    store_response = httpx.post(
        "http://localhost:8000/v1/memory/store",
        json=store_payload,
        headers={"X-Tenant-Id": "test-tenant"},
        timeout=10.0,
    )
    assert store_response.status_code == 200

    # Wait a moment for indexing
    time.sleep(1)

    # Query for the memory
    query_payload = {"query_text": "test memory query", "k": 5}

    response = httpx.post(
        "http://localhost:8000/v1/memory/query",
        json=query_payload,
        headers={"X-Tenant-Id": "test-tenant"},
        timeout=10.0,
    )

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)


def test_lite_profile_services_running():
    """Test that all required Lite Profile services are running"""
    # Check services via docker-compose
    result = subprocess.run(
        ["docker-compose", "-f", "docker-compose.lite.yml", "ps", "--services"],
        capture_output=True,
        text=True,
    )

    services = result.stdout.strip().split("\n")

    # Expected services in Lite Profile
    expected_services = ["rae-api", "postgres", "qdrant", "redis"]

    for service in expected_services:
        assert service in services, f"Service {service} not found in running services"


def test_lite_profile_postgres_accessible():
    """Test that PostgreSQL is accessible"""
    # This is a basic check that postgres container is running
    result = subprocess.run(
        ["docker-compose", "-f", "docker-compose.lite.yml", "ps", "postgres"],
        capture_output=True,
        text=True,
    )

    assert "Up" in result.stdout or "running" in result.stdout.lower()


def test_lite_profile_qdrant_accessible():
    """Test that Qdrant vector database is accessible"""
    try:
        response = httpx.get("http://localhost:6333/", timeout=5.0)
        assert response.status_code == 200
    except httpx.ConnectError:
        pytest.fail("Qdrant is not accessible on port 6333")


def test_lite_profile_redis_accessible():
    """Test that Redis cache is accessible"""
    result = subprocess.run(
        ["docker-compose", "-f", "docker-compose.lite.yml", "ps", "redis"],
        capture_output=True,
        text=True,
    )

    assert "Up" in result.stdout or "running" in result.stdout.lower()


def test_lite_profile_no_ml_service():
    """Verify that ML service is NOT running in Lite Profile"""
    result = subprocess.run(
        ["docker-compose", "-f", "docker-compose.lite.yml", "ps", "--services"],
        capture_output=True,
        text=True,
    )

    services = result.stdout.strip().split("\n")

    # These services should NOT be present in Lite Profile
    unwanted_services = ["ml-service", "celery-worker", "celery-beat", "rae-dashboard"]

    for service in unwanted_services:
        assert (
            service not in services
        ), f"Service {service} should not be in Lite Profile"


def test_lite_profile_resource_efficiency():
    """Verify that Lite Profile uses less resources than full stack"""
    # Check container count
    result = subprocess.run(
        ["docker-compose", "-f", "docker-compose.lite.yml", "ps", "--services"],
        capture_output=True,
        text=True,
    )

    service_count = len(result.stdout.strip().split("\n"))

    # Lite Profile should have exactly 4 services (API, PostgreSQL, Qdrant, Redis)
    assert service_count == 4, f"Expected 4 services, found {service_count}"


@pytest.mark.skipif(
    subprocess.run(["which", "docker-compose"], capture_output=True).returncode != 0,
    reason="docker-compose not available",
)
def test_lite_profile_config_valid():
    """Test that docker-compose.lite.yml is valid"""
    result = subprocess.run(
        ["docker-compose", "-f", "docker-compose.lite.yml", "config"],
        capture_output=True,
    )

    assert result.returncode == 0, "docker-compose.lite.yml has invalid syntax"
