import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal
from backend.ground_truth_scraper import seed_ground_truth_benchmarks, match_canonical_entity
from backend.calibration_engine import evaluate_model_accuracy, run_auto_calibration
from backend.models import HardwareBenchmark, Game

client = TestClient(app)

def test_ground_truth_seeding():
    db = SessionLocal()
    count = seed_ground_truth_benchmarks(db, force_refresh=True)
    assert count >= 20
    db.close()

def test_rapidfuzz_canonical_matcher():
    db = SessionLocal()
    cpus = db.query(HardwareBenchmark).filter(HardwareBenchmark.category == "cpu").all()
    matched = match_canonical_entity("Core i5 13400F Desktop", cpus)
    assert matched is not None
    assert "13400F" in matched.name
    db.close()

def test_statistical_calibration_engine():
    db = SessionLocal()
    metrics = evaluate_model_accuracy(db)
    assert metrics["status"] == "success"
    assert metrics["sample_count"] >= 20
    assert metrics["accuracy_pct"] >= 80.0
    assert metrics["r2_score"] >= 0.85
    
    calib = run_auto_calibration(db)
    assert calib["status"] == "calibrated"
    assert calib["calibration_id"] is not None
    db.close()

def test_calibration_api_endpoints():
    res_metrics = client.get("/api/calibration/metrics")
    assert res_metrics.status_code == 200
    data = res_metrics.json()
    assert "accuracy_pct" in data
    assert "mape_pct" in data
    assert "r2_score" in data

    res_calib = client.post("/api/calibration/run")
    assert res_calib.status_code == 200
    assert res_calib.json()["status"] == "calibrated"

    res_gt_run = client.post("/api/scraper/ground-truth/run")
    assert res_gt_run.status_code == 200
    assert res_gt_run.json()["status"] == "success"
