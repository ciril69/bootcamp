from fastapi.testclient import TestClient

def test_root_health(client: TestClient) -> None:
    """
    Test the root health check endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_api_v1_health(client: TestClient) -> None:
    """
    Test the API version 1 health check endpoint.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
