from fastapi.testclient import TestClient

from apps.memory_api.main import app

client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "RAE Memory API"
    assert "Memory" in [tag["name"] for tag in schema["tags"]]
    assert "/v1/memory/store" in schema["paths"]
