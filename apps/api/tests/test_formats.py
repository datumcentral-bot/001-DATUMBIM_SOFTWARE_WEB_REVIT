from fastapi.testclient import TestClient
from datumbim.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "task": "005"}


def test_design_status():
    response = client.get("/design/status")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_design_views():
    response = client.get("/design/views")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_format_formats():
    response = client.get("/format/formats")
    assert response.status_code == 200
    data = response.json()
    assert "formats" in data
    assert len(data["formats"]) > 0
    format_names = {f["format"] for f in data["formats"]}
    assert "ifc" in format_names
    assert "rvt" in format_names
    assert "dwg" in format_names


def test_format_detect_ifc():
    response = client.get("/format/detect", params={"filename": "model.ifc"})
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "ifc"
    assert data["category"] == "bim"
    assert data["confidence"] > 0.9


def test_format_detect_rvt():
    response = client.get("/format/detect", params={"filename": "project.rvt"})
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "rvt"
    assert data["category"] == "bim"


def test_format_detect_dwg():
    response = client.get("/format/detect", params={"filename": "drawing.dwg"})
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "dwg"
    assert data["category"] == "cad"


def test_format_detect_unknown():
    response = client.get("/format/detect", params={"filename": "unknown.xyz"})
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "generic"
