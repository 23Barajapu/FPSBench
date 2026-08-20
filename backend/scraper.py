"""
Scraper & Data Pipeline Normalizer.
Memproses raw benchmark feeds, normalisasi form factor, dan ekstraksi spesifikasi teks mentah.
"""
import re
from typing import Dict, Any, List

def normalize_hardware_name(raw_name: str) -> Dict[str, Any]:
    """
    Normalisasi nama komponen, klasifikasi Desktop vs Laptop,
    serta ekstraksi perkiraan daya (TGP/TDP) jika ada.
    """
    clean_name = raw_name.strip()
    brand = "Unknown"
    category = "cpu"
    form_factor = "desktop"
    tgp = None
    vram = None

    # Deteksi Brand
    if re.search(r"\b(Intel|Core|i[3579]|Celeron|Pentium|Xeon)\b", clean_name, re.I):
        brand = "Intel"
    elif re.search(r"\b(AMD|Ryzen|Radeon|Athlon)\b", clean_name, re.I):
        brand = "AMD"
    elif re.search(r"\b(NVIDIA|GeForce|RTX|GTX|MX\d{3}|GT\s*\d{3})\b", clean_name, re.I):
        brand = "NVIDIA"
    elif re.search(r"\b(Apple|M[1234])\b", clean_name, re.I):
        brand = "Apple"

    # Deteksi Kategori
    if re.search(r"\b(RTX|GTX|Radeon RX|GeForce|Intel Arc|GPU|Iris|UHD Graphics|HD Graphics|Radeon \d{3}M|Radeon Vega|Vega \d+|MX\d{3}|GT\s*\d{3})\b", clean_name, re.I):
        category = "gpu"
    else:
        category = "cpu"

    # Deteksi Form Factor & Suffix
    laptop_cpu_patterns = r"(HX|H|HS|U|P|HK|G[1-7]|Max-Q|Laptop|Mobile|Celeron|Pentium|N\d{2,3}|Athlon Silver)\b"
    if category == "cpu":
        if re.search(laptop_cpu_patterns, clean_name, re.I):
            form_factor = "laptop"
    elif category == "gpu":
        if re.search(r"\b(Laptop|Mobile|Max-Q|Max-P|Iris|UHD|Vega|M\b|\d{3}M\b|MX\d{3})\b", clean_name, re.I):
            form_factor = "laptop"

    # Ekstraksi TGP jika ada (misal: "RTX 4060 Laptop 140W")
    tgp_match = re.search(r"(\d{2,3})\s*W\b", clean_name, re.I)
    if tgp_match:
        tgp = int(tgp_match.group(1))

    # Ekstraksi VRAM jika ada (misal: "8GB", "12GB", "16GB")
    vram_match = re.search(r"(\d{1,2})\s*GB\b", clean_name, re.I)
    if vram_match:
        vram = int(vram_match.group(1))

    return {
        "name": clean_name,
        "brand": brand,
        "category": category,
        "form_factor": form_factor,
        "tgp_watts": tgp,
        "vram_gb": vram
    }

def run_etl_pipeline(raw_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Eksekusi ETL normalisasi data sebelum disimpan ke database.
    """
    normalized_list = []
    for record in raw_records:
        meta = normalize_hardware_name(record.get("name", ""))
        meta["single_score"] = float(record.get("single_score", 0.0))
        meta["multi_score"] = float(record.get("multi_score", 0.0))
        meta["base_clock_ghz"] = float(record.get("base_clock_ghz", 2.5))
        meta["boost_clock_ghz"] = float(record.get("boost_clock_ghz", 4.5))
        meta["release_year"] = int(record.get("release_year", 2023))
        if record.get("tgp_watts"):
            meta["tgp_watts"] = int(record.get("tgp_watts"))
        if record.get("vram_gb"):
            meta["vram_gb"] = int(record.get("vram_gb"))
        normalized_list.append(meta)
    return normalized_list

def parse_raw_laptop_spec(raw_text: str) -> Dict[str, Any]:
    """
    Mengekstrak spesifikasi laptop dari teks mentah (format toko, e-commerce, bullet list atau paragraf koma).
    """
    extracted = {
        "raw_text": raw_text,
        "cpu_query": "",
        "gpu_query": "",
        "ram_gb": 8,
        "resolution": "1080p",
        "display_hz": 60,
        "storage": "",
        "battery": "",
        "display_desc": "",
        "os": ""
    }

    if not raw_text or not raw_text.strip():
        return extracted

    # Pecah berdasarkan newline, titik-koma, atau koma yang diikuti kata kunci spesifikasi
    chunks = re.split(r"[\r\n;]+|,\s*(?=(?:prosesor|processor|cpu|ram|memory|penyimpanan|storage|ssd|grafis|vga|graphics|gpu|layar|display|sistem operasi|os|baterai|battery)\b)", raw_text, flags=re.I)

    # 1. Ekstraksi RAM terlebih dahulu (cari pola RAM/Memory X GB)
    ram_match = re.search(r"(?:RAM|Memory|Memori)\s*[:\s=–-]*\s*(\d{1,3})\s*GB", raw_text, re.I)
    if not ram_match:
        ram_match = re.search(r"\b(\d{1,3})\s*GB\s*(?:DDR[345]|LPDDR[45]|RAM|Memory)\b", raw_text, re.I)
    if ram_match:
        extracted["ram_gb"] = int(ram_match.group(1))

    # 2. Ekstraksi Resolusi & Refresh rate (hindari pencocokan kata 'UHD' dari 'Intel UHD')
    if re.search(r"(?:3840\s*x\s*2160|\b4K\b|UHD\s+(?:screen|display|layar|monitor|panel|res))", raw_text, re.I):
        extracted["resolution"] = "4K"
    elif re.search(r"(?:2560\s*x\s*1440|1440p|QHD|2K|WQXGA|2.8K|2880\s*x\s*1800)", raw_text, re.I):
        extracted["resolution"] = "1440p"
    elif re.search(r"(?:1920\s*x\s*1080|1080p|Full\s*HD|FHD|1920\s*x\s*1200|WUXGA)", raw_text, re.I):
        extracted["resolution"] = "1080p"
    else:
        extracted["resolution"] = "1080p" # Default standard gaming base

    hz_match = re.search(r"(\d{2,3})\s*Hz\b", raw_text, re.I)
    if hz_match:
        extracted["display_hz"] = int(hz_match.group(1))

    # 3. Ekstraksi CPU
    # Coba cari pola eksplisit prosesor
    cpu_explicit = re.search(r"(?:prosesor|processor|cpu)\s*[:\s=–-]*\s*([^,\n;]+)", raw_text, re.I)
    if cpu_explicit:
        raw_cpu = cpu_explicit.group(1).strip()
        # Ambil model code jika ada
        model_m = re.search(r"\b(i[3579]-?\d{4,5}[A-Z0-9]{1,4}|Core\s+Ultra\s+\d+\s*\w*|Ryzen\s+[3579]\s+\d{4}[A-Z0-9]*|Celeron\s+[A-Z0-9]+|Pentium\s+[A-Z0-9]+|Athlon\s+[A-Z0-9]+|Intel\s+Processor\s+N\d{2,3})\b", raw_cpu, re.I)
        if model_m:
            extracted["cpu_query"] = model_m.group(0).strip()
        else:
            extracted["cpu_query"] = raw_cpu.split("(")[0].strip()
    else:
        # Cari pola model langsung di seluruh teks
        model_direct = re.search(r"\b(i[3579]-?\d{4,5}[A-Z0-9]{1,4}|Core\s+Ultra\s+\d+\s*\w*|Ryzen\s+[3579]\s+\d{4}[A-Z0-9]*|Celeron\s+[A-Z0-9]+|Pentium\s+[A-Z0-9]+|Intel\s+Processor\s+N\d{2,3})\b", raw_text, re.I)
        if model_direct:
            extracted["cpu_query"] = model_direct.group(0).strip()

    # 4. Ekstraksi GPU
    # Coba cari pola eksplisit grafis / GPU / VGA
    gpu_explicit = re.search(r"(?:grafis|graphics|gpu|vga|kartu grafis)\s*[:\s=–-]*\s*([^,\n;]+)", raw_text, re.I)
    if gpu_explicit:
        raw_gpu = gpu_explicit.group(1).strip()
        # Cari model spesifik
        gpu_m = re.search(r"\b(RTX\s*\d{4}(?:\s*Ti)?(?:\s*\d+GB)?|GTX\s*\d{4}(?:\s*Ti)?|Radeon\s*RX\s*\d{4}[A-Z]?|Intel\s+(?:Iris\s*Xe|UHD|HD\s*Graphics)|Radeon\s+(?:Vega\s*\d+|Graphics|\d{3}M)|GeForce\s+MX\d{3}|GeForce\s+GT\s*\d{3})\b", raw_gpu, re.I)
        if gpu_m:
            extracted["gpu_query"] = gpu_m.group(0).strip()
        else:
            extracted["gpu_query"] = raw_gpu.strip()
    else:
        # Cari pola GPU langsung di seluruh teks
        gpu_direct = re.search(r"\b(RTX\s*\d{4}(?:\s*Ti)?|GTX\s*\d{4}(?:\s*Ti)?|Radeon\s*RX\s*\d{4}[A-Z]?|Intel\s+Iris\s*Xe|Intel\s+UHD|Intel\s+HD\s*Graphics|Radeon\s+Vega\s*\d+|Radeon\s+Graphics|GeForce\s+MX\d{3})\b", raw_text, re.I)
        if gpu_direct:
            extracted["gpu_query"] = gpu_direct.group(0).strip()

    # 5. Storage & Battery
    storage_m = re.search(r"(?:penyimpanan|storage|ssd|hdd)\s*[:\s=–-]*\s*([^,\n;]+)", raw_text, re.I)
    if storage_m:
        extracted["storage"] = storage_m.group(1).strip()
    elif re.search(r"(\d{3,4}\s*GB\s*(?:SSD|NVMe|HDD)|\d\s*TB\s*(?:SSD|NVMe|HDD))", raw_text, re.I):
        st_m = re.search(r"(\d{3,4}\s*GB\s*(?:SSD|NVMe|HDD)|\d\s*TB\s*(?:SSD|NVMe|HDD))", raw_text, re.I)
        extracted["storage"] = st_m.group(1).strip()

    battery_m = re.search(r"(?:baterai|baterry|battery)\s*[:\s=–-]*\s*([^,\n;]+)", raw_text, re.I)
    if battery_m:
        extracted["battery"] = battery_m.group(1).strip()

    return extracted
