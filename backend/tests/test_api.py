import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_search_hardware():
    response = client.get("/api/hardware/search?q=4060")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any("4060" in item["name"] for item in data)

def test_hardware_compare():
    search_res = client.get("/api/hardware/search?limit=2")
    items = search_res.json()
    ids = f"{items[0]['id']},{items[1]['id']}"
    response = client.get(f"/api/hardware/compare?ids={ids}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_games_catalog():
    response = client.get("/api/games")
    assert response.status_code == 200
    games = response.json()
    assert len(games) > 0
    assert any(g["title"] == "Cyberpunk 2077" for g in games)

def test_calculation_endpoint():
    cpus = client.get("/api/hardware/search?category=cpu&limit=1").json()
    gpus = client.get("/api/hardware/search?category=gpu&limit=1").json()
    games = client.get("/api/games").json()

    assert len(cpus) > 0
    assert len(gpus) > 0
    assert len(games) > 0

    payload = {
        "cpu_id": cpus[0]["id"],
        "gpu_id": gpus[0]["id"],
        "game_id": games[0]["id"],
        "ram_gb": 16,
        "resolution": "1080p",
        "preset": "Ultra"
    }
    response = client.post("/api/calculate", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert "avg_fps" in res
    assert "one_percent_low_fps" in res
    assert "bottleneck_pct" in res
    assert "bottleneck_status" in res
    assert res["avg_fps"] > 0

def test_parse_raw_laptop_spec_endpoint():
    raw_sample = """
Processor : 13th Generation Intel Core i5-13420H Processor (12M Cache, up to 4.60 GHz)
Graphics : NVIDIA GeForce RTX 3050 6GB GDDR6
Memory : 16GB DDR4
Storage : 512GB PCIe NVMe M.2 SSD
Display : 15.6 inch Full HD IPS (1920 x 1080), 144Hz refresh rate
    """
    response = client.post("/api/hardware/parse-raw-spec", json={"raw_text": raw_sample})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["parsed"]["ram_gb"] == 16
    assert data["parsed"]["resolution"] == "1080p"
    assert data["parsed"]["display_hz"] == 144
    assert data["matched_cpu"] is not None
    assert "13420H" in data["matched_cpu"]["name"]
    assert data["matched_gpu"] is not None
    assert "3050" in data["matched_gpu"]["name"]

