import re
from typing import List, Optional
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from .database import engine, Base, get_db
from .models import HardwareBenchmark, Game, PresetMultiplier
from .schemas import HardwareItem, GameItem, CalculationRequest, CalculationResponse
from .calculator import calculate_fps_and_bottleneck
from .seed_data import seed_database
from .scraper import run_etl_pipeline, parse_raw_laptop_spec
from pydantic import BaseModel

class RawSpecInput(BaseModel):
    raw_text: str

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Initialize tables & seed
Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(
    title="FPSBench - Hardware & Game FPS Performance Estimator API",
    version="1.0.0",
    description="API untuk kalkulator estimasi performa gaming FPS & deteksi bottleneck hardware."
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
        "service": "Hardware & Game FPS Estimator API",
        "version": "1.0.0"
    }

@app.get("/api/health")
def api_health():
    return {
        "status": "online",
        "service": "Hardware & Game FPS Estimator API",
        "version": "1.0.0"
    }

@app.get("/api/hardware/search", response_model=List[HardwareItem])
def search_hardware(
    q: str = Query("", min_length=0, description="Search query"),
    category: Optional[str] = Query(None, pattern="^(cpu|gpu)$"),
    form_factor: Optional[str] = Query(None, pattern="^(desktop|laptop)$"),
    limit: int = Query(20, ge=1, le=100),
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
    ids: str = Query(..., description="Comma-separated IDs, e.g. 1,2,3"),
    db: Session = Depends(get_db)
):
    """
    FR-1.4 Komparasi Head-to-Head 2-4 komponen berdampingan.
    """
    try:
        id_list = [int(i.strip()) for i in ids.split(",") if i.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IDs format")

    if len(id_list) < 1 or len(id_list) > 4:
        raise HTTPException(status_code=400, detail="Pilih antara 1 hingga 4 komponen untuk dibandingkan.")

    items = db.query(HardwareBenchmark).filter(HardwareBenchmark.id.in_(id_list)).all()
    # Sort in requested order
    item_map = {item.id: item for item in items}
    return [item_map[i] for i in id_list if i in item_map]

@app.get("/api/hardware/{hardware_id}", response_model=HardwareItem)
def get_hardware_detail(hardware_id: int, db: Session = Depends(get_db)):
    """
    FR-1.3 Spesifikasi Detail hardware.
    """
    item = db.query(HardwareBenchmark).filter(HardwareBenchmark.id == hardware_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Komponen hardware tidak ditemukan.")
    return item

@app.get("/api/games", response_model=List[GameItem])
def get_games(
    genre: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Katalog game beserta profil bobot komputasi CPU/GPU.
    """
    query = db.query(Game)
    if genre:
        query = query.filter(Game.genre.ilike(f"%{genre}%"))
    return query.order_by(Game.title.asc()).all()

@app.post("/api/calculate", response_model=CalculationResponse)
def calculate_fps(
    req: CalculationRequest,
    db: Session = Depends(get_db)
):
    """
    FR-2.1, FR-2.2, FR-2.3: Kalkulasi Estimasi Average & 1% Low FPS serta Bottleneck.
    """
    cpu = db.query(HardwareBenchmark).filter(
        and_(HardwareBenchmark.id == req.cpu_id, HardwareBenchmark.category == "cpu")
    ).first()
    if not cpu:
        raise HTTPException(status_code=404, detail="CPU dengan ID tersebut tidak ditemukan.")

    gpu = db.query(HardwareBenchmark).filter(
        and_(HardwareBenchmark.id == req.gpu_id, HardwareBenchmark.category == "gpu")
    ).first()
    if not gpu:
        raise HTTPException(status_code=404, detail="GPU dengan ID tersebut tidak ditemukan.")

    game = db.query(Game).filter(Game.id == req.game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game dengan ID tersebut tidak ditemukan.")

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
    Ekstraksi spesifikasi teks mentah (e-commerce/brosur laptop) dan pencocokan otomatis hardware.
    """
    parsed = parse_raw_laptop_spec(req.raw_text)
    
    # 1. Cari CPU yang cocok (prefer form_factor laptop)
    matched_cpu = None
    if parsed["cpu_query"]:
        # Coba exact search atau contains
        clean_q = parsed["cpu_query"].strip()
        matched_cpu = db.query(HardwareBenchmark).filter(
            and_(
                HardwareBenchmark.category == "cpu",
                HardwareBenchmark.name.ilike(f"%{clean_q}%")
            )
        ).first()
        if not matched_cpu:
            # Cari core code e.g. "13420H"
            core_code = re.search(r"\b\d{4,5}[A-Z]{1,2}\b", clean_q)
            if core_code:
                matched_cpu = db.query(HardwareBenchmark).filter(
                    and_(
                        HardwareBenchmark.category == "cpu",
                        HardwareBenchmark.name.ilike(f"%{core_code.group(0)}%")
                    )
                ).first()

    # 2. Cari GPU yang cocok (prefer form_factor laptop)
    matched_gpu = None
    if parsed["gpu_query"]:
        clean_g = parsed["gpu_query"].strip()
        # Prefer laptop GPU
        matched_gpu = db.query(HardwareBenchmark).filter(
            and_(
                HardwareBenchmark.category == "gpu",
                HardwareBenchmark.form_factor == "laptop",
                HardwareBenchmark.name.ilike(f"%{clean_g}%")
            )
        ).first()
        if not matched_gpu:
            # Coba number code e.g. "3050"
            gpu_code = re.search(r"\b\d{4}\b", clean_g)
            if gpu_code:
                matched_gpu = db.query(HardwareBenchmark).filter(
                    and_(
                        HardwareBenchmark.category == "gpu",
                        HardwareBenchmark.form_factor == "laptop",
                        HardwareBenchmark.name.ilike(f"%{gpu_code.group(0)}%")
                    )
                ).first()
        if not matched_gpu:
            # Fallback ke GPU umum
            matched_gpu = db.query(HardwareBenchmark).filter(
                and_(
                    HardwareBenchmark.category == "gpu",
                    HardwareBenchmark.name.ilike(f"%{clean_g}%")
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
