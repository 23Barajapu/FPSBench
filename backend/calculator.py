from typing import Dict, Any
from .models import HardwareBenchmark, Game

# Baseline standard references:
# CPU Baseline: Intel Core i5-12400 / Ryzen 5 5600 (Single Score ~1600, Multi Score ~12000)
CPU_BASELINE_SINGLE = 1600.0
CPU_BASELINE_MULTI = 12000.0

# GPU Baseline: RTX 3060 12GB (3D Graphic Score ~8800)
GPU_BASELINE_SCORE = 8800.0

# Resolution Scaling Factors (GPU load scales heavily with resolution, CPU load slightly decreases or stays flat)
RESOLUTION_SCALING = {
    "1080p": {"gpu_load": 1.00, "cpu_load": 1.00},
    "1440p": {"gpu_load": 1.45, "cpu_load": 0.92},
    "4K": {"gpu_load": 2.25, "cpu_load": 0.85},
}

# Quality Preset Scaling Factors (Affects GPU render cost)
PRESET_SCALING = {
    "Low": 0.65,
    "Medium": 0.80,
    "High": 0.92,
    "Ultra": 1.00,
}

def calculate_fps_and_bottleneck(
    cpu: HardwareBenchmark,
    gpu: HardwareBenchmark,
    game: Game,
    ram_gb: int = 16,
    resolution: str = "1080p",
    preset: str = "Ultra"
) -> Dict[str, Any]:
    """
    Kalkulator estimasi FPS & Bottleneck berbasis Harmonic Frame Time.
    Formula:
    1. FPS_cpu = Baseline_FPS * ( (SingleScore/BaseSingle)*0.65 + (MultiScore/BaseMulti)*0.35 ) / (D_cpu * ResCpuScale)
    2. FPS_gpu = Baseline_FPS * (GpuScore / BaseGpu) / (D_gpu * ResGpuScale * PresetScale)
    3. T_frame = (D_cpu / FPS_cpu) + (D_gpu / FPS_gpu)
    4. FPS_est = 1 / T_frame
    """
    res_factor = RESOLUTION_SCALING.get(resolution, RESOLUTION_SCALING["1080p"])
    preset_factor = PRESET_SCALING.get(preset, 1.0)

    # 1. Hitung Kapasitas Teoretis CPU (Frame budget CPU)
    # Single-core menyumbang 65% untuk game, multi-core 35%
    cpu_power_index = (
        (cpu.single_score / CPU_BASELINE_SINGLE) * 0.65 +
        (cpu.multi_score / CPU_BASELINE_MULTI) * 0.35
    )
    # CPU bottleneck lebih terasa di resolusi rendah (1080p) dan game CPU-heavy
    fps_cpu_capacity = (game.base_fps_1080p_ultra * cpu_power_index) / (game.cpu_weight * res_factor["cpu_load"])

    # 2. Hitung Kapasitas Teoretis GPU (Frame budget GPU)
    gpu_power_index = gpu.multi_score / GPU_BASELINE_SCORE
    
    # Laptop TGP modifier jika ada (e.g. RTX 4060 Laptop 45W vs 140W)
    if gpu.form_factor == "laptop" and gpu.tgp_watts:
        # Standar TGP reference 100W, kurva efisiensi logaritmik
        tgp_ratio = min(1.3, max(0.6, gpu.tgp_watts / 100.0))
        # multi_score sudah merefleksikan pengujian riil, tapi berikan fine-tuning jika VRAM terbatas
    
    # VRAM check penalty
    vram_penalty = 1.0
    if resolution == "4K" and (gpu.vram_gb or 8) < 10:
        vram_penalty = 0.82 # VRAM swapping stutter
    elif resolution == "1440p" and (gpu.vram_gb or 8) < 8:
        vram_penalty = 0.90

    gpu_load_multiplier = game.gpu_weight * res_factor["gpu_load"] * preset_factor
    fps_gpu_capacity = (game.base_fps_1080p_ultra * gpu_power_index * vram_penalty) / gpu_load_multiplier

    # 3. Efek Kapasitas RAM
    ram_penalty = 1.0
    is_ram_limited = False
    if ram_gb < game.ram_min_gb:
        ram_penalty = 0.70 # Severe stutter & FPS drop
        is_ram_limited = True
    elif ram_gb < game.ram_rec_gb:
        ram_penalty = 0.90 # Mild frame drop
        is_ram_limited = True

    # 4. Harmonic Frame Time Calculation
    # Waktu render total gabungan CPU frame preparation time + GPU rasterization time
    t_cpu_ms = (game.cpu_weight / fps_cpu_capacity) * 1000.0
    t_gpu_ms = (game.gpu_weight / fps_gpu_capacity) * 1000.0
    
    # Overlap komputasi CPU & GPU pipeline (pipelining efisiensi ~75%)
    t_frame_total_ms = max(t_cpu_ms, t_gpu_ms) + 0.25 * min(t_cpu_ms, t_gpu_ms)
    
    raw_avg_fps = (1000.0 / t_frame_total_ms) * ram_penalty
    avg_fps = round(max(5.0, raw_avg_fps), 1)

    # 5. 1% Low FPS Estimation
    # 1% low sangat dipengaruhi single-core CPU, kestabilan RAM, dan bottleneck
    cpu_stability = min(1.15, max(0.65, cpu.single_score / CPU_BASELINE_SINGLE))
    low_ratio = 0.72 * cpu_stability * (0.85 if is_ram_limited else 1.0)
    # Batasi rasio wajar 1% low (antara 55% - 85% dari avg FPS)
    low_ratio = min(0.85, max(0.50, low_ratio))
    one_percent_low_fps = round(avg_fps * low_ratio, 1)

    # 6. Bottleneck Calculation & Status
    # Menghitung ketimpangan antara CPU capacity vs GPU capacity
    delta_perf = abs(fps_cpu_capacity - fps_gpu_capacity) / max(fps_cpu_capacity, fps_gpu_capacity)
    bottleneck_pct = round(min(100.0, delta_perf * 100.0), 1)

    if delta_perf < 0.12:
        bottleneck_status = "Balanced / Optimal"
        bottleneck_component = "None"
        cpu_util = min(98.0, round((raw_avg_fps / fps_cpu_capacity) * 90.0, 1))
        gpu_util = min(99.0, round((raw_avg_fps / fps_gpu_capacity) * 95.0, 1))
        verdict = "Konfigurasi seimbang. CPU dan GPU bekerja pada efisiensi optimal tanpa hambatan signifikan."
        recommendation = "Sistem sudah ideal untuk kombinasi resolusi dan game ini."
    elif fps_cpu_capacity < fps_gpu_capacity:
        bottleneck_status = "CPU Bottleneck"
        bottleneck_component = "CPU"
        cpu_util = 99.0
        gpu_util = max(40.0, round((fps_cpu_capacity / fps_gpu_capacity) * 95.0, 1))
        verdict = f"CPU membatasi performa kartu grafis sebesar {bottleneck_pct}%. GPU tidak terutilisasi penuh."
        if resolution == "1080p":
            recommendation = "Coba naikkan resolusi ke 1440p/4K atau tingkatkan preset grafis untuk memindahkan beban ke GPU, atau pertimbangkan upgrade CPU."
        else:
            recommendation = "Pertimbangkan upgrade prosesor dengan performa single-core/multi-core lebih tinggi."
    else:
        bottleneck_status = "GPU Bottleneck"
        bottleneck_component = "GPU"
        gpu_util = 99.0
        cpu_util = max(35.0, round((fps_gpu_capacity / fps_cpu_capacity) * 90.0, 1))
        verdict = f"GPU mencapai beban maksimal (Bottleneck {bottleneck_pct}%). CPU masih memiliki ruang performa tersisa."
        recommendation = "Ini adalah kondisi normal pada gaming resolusi tinggi. Turunkan preset grafis/resolusi atau gunakan fitur upscaler (DLSS/FSR) untuk FPS lebih tinggi."

    if is_ram_limited:
        recommendation += f" PERINGATAN: RAM {ram_gb}GB di bawah rekomendasi ({game.ram_rec_gb}GB). Upgrade RAM ke {game.ram_rec_gb}GB untuk menghilangkan stuttering."

    return {
        "avg_fps": avg_fps,
        "one_percent_low_fps": one_percent_low_fps,
        "bottleneck_pct": bottleneck_pct,
        "bottleneck_status": bottleneck_status,
        "bottleneck_component": bottleneck_component,
        "cpu_utilization_est": cpu_util,
        "gpu_utilization_est": gpu_util,
        "is_ram_limited": is_ram_limited,
        "verdict": verdict,
        "recommendation": recommendation,
        "game_title": game.title,
        "resolution": resolution,
        "preset": preset,
        "cpu_name": f"{cpu.brand} {cpu.name} ({cpu.form_factor.title()})",
        "gpu_name": f"{gpu.brand} {gpu.name} ({gpu.form_factor.title()}{f' {gpu.tgp_watts}W' if gpu.tgp_watts else ''})",
        "ram_gb": ram_gb,
    }
