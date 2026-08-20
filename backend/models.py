from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from datetime import datetime
from .database import Base

class HardwareBenchmark(Base):
    __tablename__ = "hardware_benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    brand = Column(String(50), nullable=False, index=True) # Intel, AMD, NVIDIA
    category = Column(String(20), nullable=False, index=True) # cpu, gpu
    form_factor = Column(String(20), nullable=False, index=True) # desktop, laptop
    single_score = Column(Float, default=0.0) # Single-core (CPU) or Compute unit score (GPU)
    multi_score = Column(Float, default=0.0) # Multi-core (CPU) or 3D TimeSpy/FireStrike score (GPU)
    base_clock_ghz = Column(Float, nullable=True)
    boost_clock_ghz = Column(Float, nullable=True)
    tgp_watts = Column(Integer, nullable=True) # TGP for laptops
    vram_gb = Column(Integer, nullable=True) # VRAM for GPUs
    release_year = Column(Integer, default=2023)

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False, index=True)
    genre = Column(String(50), nullable=False) # eSports, AAA Action, Simulation, Open World
    engine = Column(String(50), default="Custom Engine")
    cpu_weight = Column(Float, default=0.35) # D_cpu
    gpu_weight = Column(Float, default=0.65) # D_gpu
    ram_min_gb = Column(Integer, default=8)
    ram_rec_gb = Column(Integer, default=16)
    base_fps_1080p_ultra = Column(Float, default=60.0) # baseline target benchmark reference
    image_url = Column(String(255), nullable=True)

class PresetMultiplier(Base):
    __tablename__ = "benchmark_presets"

    id = Column(Integer, primary_key=True, index=True)
    resolution = Column(String(20), nullable=False) # 1080p, 1440p, 4K
    preset = Column(String(20), nullable=False) # Low, Medium, High, Ultra
    res_gpu_scale = Column(Float, default=1.0) # Scale load on GPU for resolution
    res_cpu_scale = Column(Float, default=1.0) # Scale load on CPU for resolution
    preset_scale = Column(Float, default=1.0) # Graphic quality multiplier

class GroundTruthBenchmark(Base):
    """
    Tabel data benchmark riil hasil scraping (NotebookCheck, TechPowerUp, pengujian fisik).
    Digunakan sebagai acuan kalibrasi statistik (MAPE / RMSE).
    """
    __tablename__ = "ground_truth_benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    cpu_id = Column(Integer, ForeignKey("hardware_benchmarks.id"), nullable=False)
    gpu_id = Column(Integer, ForeignKey("hardware_benchmarks.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    resolution = Column(String(20), default="1080p")
    preset = Column(String(20), default="Ultra")
    real_avg_fps = Column(Float, nullable=False)
    real_low_fps = Column(Float, nullable=True)
    source_url = Column(String(255), default="NotebookCheck / TechPowerUp Ground Truth")
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelCalibration(Base):
    """
    Log hasil kalibrasi model statistik (MAPE, RMSE, R²).
    """
    __tablename__ = "model_calibrations"

    id = Column(Integer, primary_key=True, index=True)
    calibrated_at = Column(DateTime, default=datetime.utcnow)
    mape_score = Column(Float, nullable=False) # e.g. 5.4%
    rmse_score = Column(Float, nullable=False) # e.g. 4.2 FPS
    r2_score = Column(Float, nullable=False) # e.g. 0.94
    sample_count = Column(Integer, default=0)
    coefficient_payload = Column(Text, nullable=True) # JSON of calibrated multipliers
