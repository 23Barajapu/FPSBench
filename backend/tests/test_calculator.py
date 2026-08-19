import pytest
from backend.models import HardwareBenchmark, Game
from backend.calculator import calculate_fps_and_bottleneck

def test_harmonic_frame_time_balanced():
    cpu = HardwareBenchmark(name="i5-13400F", brand="Intel", category="cpu", form_factor="desktop", single_score=1780, multi_score=13500)
    gpu = HardwareBenchmark(name="RTX 4060", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=10500, multi_score=10500, vram_gb=8)
    game = Game(title="Cyberpunk 2077", genre="AAA Action", cpu_weight=0.25, gpu_weight=0.75, ram_min_gb=12, ram_rec_gb=16, base_fps_1080p_ultra=62.0)

    result = calculate_fps_and_bottleneck(cpu, gpu, game, ram_gb=16, resolution="1080p", preset="Ultra")
    
    assert result["avg_fps"] > 50
    assert result["one_percent_low_fps"] < result["avg_fps"]
    assert result["one_percent_low_fps"] > 30
    assert result["is_ram_limited"] is False

def test_cpu_bottleneck_scenario():
    # Weak CPU with powerful GPU on 1080p
    cpu = HardwareBenchmark(name="Core i3-10100F", brand="Intel", category="cpu", form_factor="desktop", single_score=1100, multi_score=5200)
    gpu = HardwareBenchmark(name="GeForce RTX 4090", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=36000, multi_score=36000, vram_gb=24)
    game = Game(title="Valorant", genre="eSports", cpu_weight=0.55, gpu_weight=0.45, ram_min_gb=4, ram_rec_gb=8, base_fps_1080p_ultra=280.0)

    result = calculate_fps_and_bottleneck(cpu, gpu, game, ram_gb=16, resolution="1080p", preset="Low")
    assert result["bottleneck_status"] == "CPU Bottleneck"
    assert result["bottleneck_component"] == "CPU"
    assert result["bottleneck_pct"] > 30.0

def test_laptop_tgp_impact():
    # RTX 4060 Laptop 140W vs 45W
    cpu = HardwareBenchmark(name="Core i7-13700HX", brand="Intel", category="cpu", form_factor="laptop", single_score=2000, multi_score=20500)
    gpu_140w = HardwareBenchmark(name="RTX 4060 Laptop 140W", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=10400, multi_score=10400, tgp_watts=140, vram_gb=8)
    gpu_45w = HardwareBenchmark(name="RTX 4060 Laptop 45W", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=7200, multi_score=7200, tgp_watts=45, vram_gb=8)
    game = Game(title="Black Myth: Wukong", genre="AAA Action", cpu_weight=0.20, gpu_weight=0.80, ram_min_gb=16, ram_rec_gb=32, base_fps_1080p_ultra=55.0)

    res_140w = calculate_fps_and_bottleneck(cpu, gpu_140w, game, ram_gb=16, resolution="1080p", preset="Ultra")
    res_45w = calculate_fps_and_bottleneck(cpu, gpu_45w, game, ram_gb=16, resolution="1080p", preset="Ultra")

    assert res_140w["avg_fps"] > res_45w["avg_fps"]

def test_ram_penalty():
    cpu = HardwareBenchmark(name="i5-12400F", brand="Intel", category="cpu", form_factor="desktop", single_score=1600, multi_score=12000)
    gpu = HardwareBenchmark(name="RTX 3060", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=8800, multi_score=8800, vram_gb=12)
    game = Game(title="Hogwarts Legacy", genre="RPG", cpu_weight=0.30, gpu_weight=0.70, ram_min_gb=16, ram_rec_gb=16, base_fps_1080p_ultra=58.0)

    res_8gb = calculate_fps_and_bottleneck(cpu, gpu, game, ram_gb=8, resolution="1080p", preset="Ultra")
    res_16gb = calculate_fps_and_bottleneck(cpu, gpu, game, ram_gb=16, resolution="1080p", preset="Ultra")

    assert res_8gb["is_ram_limited"] is True
    assert res_8gb["avg_fps"] < res_16gb["avg_fps"]
