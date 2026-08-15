from fastapi.testclient import TestClient
from datumbim.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "task": "006"}


def test_design_status():
    response = client.get("/design/status")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["task"] == "003"


def test_design_views():
    response = client.get("/design/views")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["id"] == "view-3d" for item in data)
