from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class HardwareItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    brand: str
    category: str # cpu | gpu
    form_factor: str # desktop | laptop
    single_score: float
    multi_score: float
    base_clock_ghz: Optional[float] = None
    boost_clock_ghz: Optional[float] = None
    tgp_watts: Optional[int] = None
    vram_gb: Optional[int] = None
    release_year: int

class GameItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    genre: str
    engine: str
    cpu_weight: float
    gpu_weight: float
    ram_min_gb: int
    ram_rec_gb: int
    base_fps_1080p_ultra: float
    image_url: Optional[str] = None

class CalculationRequest(BaseModel):
    cpu_id: int
    gpu_id: int
    game_id: int
    ram_gb: int = Field(default=16, ge=4, le=128)
    resolution: str = Field(default="1080p", pattern="^(1080p|1440p|4K)$")
    preset: str = Field(default="Ultra", pattern="^(Low|Medium|High|Ultra)$")

class CalculationResponse(BaseModel):
    avg_fps: float
    one_percent_low_fps: float
    bottleneck_pct: float
    bottleneck_status: str # Balanced / Optimal, CPU Bottleneck, GPU Bottleneck
    bottleneck_component: str # None, CPU, GPU, RAM
    cpu_utilization_est: float
    gpu_utilization_est: float
    is_ram_limited: bool
    verdict: str
    recommendation: str
    game_title: str
    resolution: str
    preset: str
    cpu_name: str
    gpu_name: str
    ram_gb: int
