import re
from typing import List, Optional
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from .database import engine, Base, get_db, SessionLocal
from .models import HardwareBenchmark, Game, PresetMultiplier, GroundTruthBenchmark, ModelCalibration
from .schemas import HardwareItem, GameItem, CalculationRequest, CalculationResponse
from .calculator import calculate_fps_and_bottleneck
from .seed_data import seed_database
from .scraper import run_etl_pipeline, parse_raw_laptop_spec
from .ground_truth_scraper import seed_ground_truth_benchmarks
from .calibration_engine import evaluate_model_accuracy, run_auto_calibration
from pydantic import BaseModel

class RawSpecInput(BaseModel):
    raw_text: str

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Initialize tables & seed
Base.metadata.create_all(bind=engine)
seed_database()
db_init = SessionLocal()
seed_ground_truth_benchmarks(db_init)
db_init.close()

app = FastAPI(
    title="FPSBench - Hardware & Game FPS Performance Estimator API",
    version="2.0.0",
    description="API untuk kalkulator estimasi performa gaming FPS, deteksi bottleneck hardware, dan kalibrasi Ground Truth."
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

@app.get("/")
def read_root():
    if os.path.exists(os.path.join(frontend_dist, "index.html")):
        return FileResponse(os.path.join(frontend_dist, "index.html"))
    return {
        "status": "online",
        "service": "FPSBench Hardware & Game FPS Estimator API",
        "version": "2.0.0"
    }

@app.get("/api/health")
def api_health():
    return {
        "status": "online",
        "service": "FPSBench Hardware & Game FPS Estimator API",
        "version": "2.0.0"
    }

@app.get("/api/hardware/search", response_model=List[HardwareItem])
def search_hardware(
    q: str = Query("", min_length=0, description="Search query"),
    category: Optional[str] = Query(None, pattern="^(cpu|gpu)$"),
    form_factor: Optional[str] = Query(None, pattern="^(desktop|laptop)$"),
    limit: int = Query(20, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    FR-1.1 Autocomplete Search: Instant search hardware by model name/brand.
    """
    query = db.query(HardwareBenchmark)
    if category:
        query = query.filter(HardwareBenchmark.category == category)
    if form_factor:
        query = query.filter(HardwareBenchmark.form_factor == form_factor)
    if q.strip():
        search_pattern = f"%{q.strip()}%"
        query = query.filter(
            or_(
                HardwareBenchmark.name.ilike(search_pattern),
                HardwareBenchmark.brand.ilike(search_pattern)
            )
        )
    return query.order_by(HardwareBenchmark.multi_score.desc()).limit(limit).all()

@app.get("/api/hardware/compare", response_model=List[HardwareItem])
def compare_hardware(
    ids: str = Query(..., description="Comma-separated IDs of hardware items to compare, e.g. 1,2,5"),
    db: Session = Depends(get_db)
):
    """
    FR-1.3 Head-to-Head Comparison matrix for 2-4 components.
    """
    try:
        id_list = [int(x.strip()) for x in ids.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID list format.")

    if len(id_list) < 2 or len(id_list) > 4:
        raise HTTPException(status_code=400, detail="Harap pilih 2 hingga 4 komponen untuk dibandingkan.")

    items = db.query(HardwareBenchmark).filter(HardwareBenchmark.id.in_(id_list)).all()
    if len(items) != len(id_list):
        raise HTTPException(status_code=404, detail="Satu atau lebih komponen tidak ditemukan.")
    return items

@app.get("/api/hardware/{hardware_id}", response_model=HardwareItem)
def get_hardware_detail(hardware_id: int, db: Session = Depends(get_db)):
    """
    Mendapatkan detail spesifikasi satu komponen.
    """
    item = db.query(HardwareBenchmark).filter(HardwareBenchmark.id == hardware_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Komponen hardware tidak ditemukan.")
    return item

@app.get("/api/games", response_model=List[GameItem])
def get_games_catalog(db: Session = Depends(get_db)):
    """
    FR-2.1 Mengambil katalog game beserta bobot CPU/GPU.
    """
    return db.query(Game).all()

@app.post("/api/calculate", response_model=CalculationResponse)
def calculate_performance(req: CalculationRequest, db: Session = Depends(get_db)):
    """
    FR-2.1, FR-2.2, FR-2.3, FR-2.4 Harmonic Frame Time Calculation Engine.
    """
    cpu = db.query(HardwareBenchmark).filter(HardwareBenchmark.id == req.cpu_id).first()
    gpu = db.query(HardwareBenchmark).filter(HardwareBenchmark.id == req.gpu_id).first()
    game = db.query(Game).filter(Game.id == req.game_id).first()

    if not cpu or cpu.category != "cpu":
        raise HTTPException(status_code=400, detail="CPU yang dipilih tidak valid.")
    if not gpu or gpu.category != "gpu":
        raise HTTPException(status_code=400, detail="GPU yang dipilih tidak valid.")
    if not game:
        raise HTTPException(status_code=400, detail="Game yang dipilih tidak valid.")

    result = calculate_fps_and_bottleneck(
        cpu=cpu,
        gpu=gpu,
        game=game,
        ram_gb=req.ram_gb,
        resolution=req.resolution,
        preset=req.preset
    )
    return result

@app.post("/api/hardware/parse-raw-spec")
def parse_raw_spec_endpoint(req: RawSpecInput, db: Session = Depends(get_db)):
    """
    Ekstraksi spesifikasi teks mentah (e-commerce/brosur laptop) dan pencocokan cerdas hardware.
    """
    parsed = parse_raw_laptop_spec(req.raw_text)
    
    # 1. Pencocokan Cerdas CPU
    matched_cpu = None
    if parsed["cpu_query"]:
        raw_cpu = parsed["cpu_query"].strip()
        clean_cpu = re.sub(r"\b(Intel|AMD|Core|Processor|Prosesor|Generation|Gen|Laptop|Desktop)\b", "", raw_cpu, flags=re.I).strip()
        
        if clean_cpu:
            matched_cpu = db.query(HardwareBenchmark).filter(
                and_(
                    HardwareBenchmark.category == "cpu",
                    HardwareBenchmark.name.ilike(f"%{clean_cpu}%")
                )
            ).first()

        if not matched_cpu:
            code_m = re.search(r"\b(i[3579]-?\d{4,5}[A-Z0-9]{1,4}|N\d{2,3}|\d{4,5}[A-Z0-9]{1,4})\b", raw_cpu, re.I)
            if code_m:
                matched_cpu = db.query(HardwareBenchmark).filter(
                    and_(
                        HardwareBenchmark.category == "cpu",
                        HardwareBenchmark.name.ilike(f"%{code_m.group(0)}%")
                    )
                ).first()

        if not matched_cpu:
            words = [w for w in clean_cpu.split() if len(w) >= 3]
            for w in words:
                matched_cpu = db.query(HardwareBenchmark).filter(
                    and_(
                        HardwareBenchmark.category == "cpu",
                        HardwareBenchmark.name.ilike(f"%{w}%")
                    )
                ).first()
                if matched_cpu:
                    break

    # 2. Pencocokan Cerdas GPU
    matched_gpu = None
    if parsed["gpu_query"]:
        raw_gpu = parsed["gpu_query"].strip()
        clean_gpu = re.sub(r"\b(NVIDIA|GeForce|AMD|Radeon|Graphics|Grafis|VGA|Card|GDDR\d?)\b", "", raw_gpu, flags=re.I).strip()

        if re.search(r"\b(Intel\s+UHD|UHD\s+Graphics|Intel\s+HD)\b", raw_gpu, re.I):
            matched_gpu = db.query(HardwareBenchmark).filter(
                and_(
                    HardwareBenchmark.category == "gpu",
                    HardwareBenchmark.name.ilike("%Intel UHD%")
                )
            ).first()
        elif re.search(r"\b(Iris\s*Xe|Intel\s+Iris)\b", raw_gpu, re.I):
            matched_gpu = db.query(HardwareBenchmark).filter(
                and_(
                    HardwareBenchmark.category == "gpu",
                    HardwareBenchmark.name.ilike("%Iris Xe%")
                )
            ).first()
        elif re.search(r"\b(Radeon\s+Graphics|Vega\s*\d+|Radeon\s+Vega)\b", raw_gpu, re.I):
            matched_gpu = db.query(HardwareBenchmark).filter(
                and_(
                    HardwareBenchmark.category == "gpu",
                    HardwareBenchmark.name.ilike("%Radeon%")
                )
            ).first()
        
        if not matched_gpu:
            gpu_code = re.search(r"\b(RTX\s*\d{4}|GTX\s*\d{4}|RX\s*\d{4}|MX\d{3}|GT\s*\d{3}|\d{3,4}M|\d{4})\b", raw_gpu, re.I)
            if gpu_code:
                matched_gpu = db.query(HardwareBenchmark).filter(
                    and_(
                        HardwareBenchmark.category == "gpu",
                        HardwareBenchmark.form_factor == "laptop",
                        HardwareBenchmark.name.ilike(f"%{gpu_code.group(0)}%")
                    )
                ).first()
                if not matched_gpu:
                    matched_gpu = db.query(HardwareBenchmark).filter(
                        and_(
                            HardwareBenchmark.category == "gpu",
                            HardwareBenchmark.name.ilike(f"%{gpu_code.group(0)}%")
                        )
                    ).first()

        if not matched_gpu and clean_gpu:
            matched_gpu = db.query(HardwareBenchmark).filter(
                and_(
                    HardwareBenchmark.category == "gpu",
                    HardwareBenchmark.name.ilike(f"%{clean_gpu}%")
                )
            ).first()

    return {
        "status": "success",
        "parsed": parsed,
        "matched_cpu": matched_cpu,
        "matched_gpu": matched_gpu
    }

@app.post("/api/pipeline/run")
def trigger_etl_pipeline(raw_items: List[dict], db: Session = Depends(get_db)):
    """
    FR-3.1, FR-3.2, FR-3.3 Automated ETL Pipeline & Database Upsert.
    """
    processed = run_etl_pipeline(raw_items)
    upserted_count = 0
    for p in processed:
        existing = db.query(HardwareBenchmark).filter(
            and_(
                HardwareBenchmark.name == p["name"],
                HardwareBenchmark.form_factor == p["form_factor"]
            )
        ).first()
        if existing:
            existing.single_score = p["single_score"]
            existing.multi_score = p["multi_score"]
            existing.base_clock_ghz = p["base_clock_ghz"]
            existing.boost_clock_ghz = p["boost_clock_ghz"]
            existing.release_year = p["release_year"]
            existing.tgp_watts = p["tgp_watts"]
            existing.vram_gb = p["vram_gb"]
        else:
            new_item = HardwareBenchmark(**p)
            db.add(new_item)
        upserted_count += 1
    db.commit()
    return {"status": "success", "upserted_count": upserted_count}

@app.get("/api/calibration/metrics")
def get_calibration_metrics(db: Session = Depends(get_db)):
    """
    FR-4.1 Statistical Evaluation Engine (MAPE, RMSE, R2, Accuracy %).
    """
    return evaluate_model_accuracy(db)

@app.post("/api/calibration/run")
def run_model_calibration_endpoint(db: Session = Depends(get_db)):
    """
    FR-4.2 Automated Weight Calibration & Metric Logging.
    """
    return run_auto_calibration(db)

@app.get("/api/ground-truth")
def get_ground_truth_samples(db: Session = Depends(get_db)):
    """
    Mengambil data ground truth riil hasil scraping.
    """
    return evaluate_model_accuracy(db)

@app.post("/api/scraper/ground-truth/run")
def run_ground_truth_scraper_endpoint(db: Session = Depends(get_db)):
    """
    Menjalankan ground truth scraper & RapidFuzz entity normalizer.
    """
    count = seed_ground_truth_benchmarks(db, force_refresh=True)
    metrics = evaluate_model_accuracy(db)
    return {
        "status": "success",
        "seeded_count": count,
        "metrics": metrics
    }
