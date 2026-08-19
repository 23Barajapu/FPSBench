"""
Scraper & Data Pipeline Normalizer.
Memproses raw benchmark feeds dan mengekstrak metrik hardware terstandar.
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
    if re.search(r"\b(Intel|Core|i[3579])\b", clean_name, re.I):
        brand = "Intel"
    elif re.search(r"\b(AMD|Ryzen|Radeon)\b", clean_name, re.I):
        brand = "AMD"
    elif re.search(r"\b(NVIDIA|GeForce|RTX|GTX)\b", clean_name, re.I):
        brand = "NVIDIA"

    # Deteksi Kategori
    if re.search(r"\b(RTX|GTX|Radeon RX|GeForce|Intel Arc|GPU)\b", clean_name, re.I):
        category = "gpu"
    else:
        category = "cpu"

    # Deteksi Form Factor & Suffix
    laptop_cpu_patterns = r"(HX|H|HS|U|P|HK|G[1-7]|Max-Q|Laptop|Mobile)\b"
    if category == "cpu":
        if re.search(laptop_cpu_patterns, clean_name, re.I):
            form_factor = "laptop"
    elif category == "gpu":
        if re.search(r"\b(Laptop|Mobile|Max-Q|Max-P)\b", clean_name, re.I):
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
    Mengekstrak spesifikasi laptop dari teks mentah (format toko/spesifikasi e-commerce).
    Mengembalikan dict spesifikasi terstruktur untuk pencocokan ke database hardware.
    """
    extracted = {
        "raw_text": raw_text,
        "cpu_query": "",
        "gpu_query": "",
        "ram_gb": 16,
        "resolution": "1080p",
        "display_hz": 60,
        "storage": "",
        "battery": "",
        "display_desc": "",
        "os": ""
    }

    lines = raw_text.splitlines()
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue

        # 1. Processor / CPU
        if re.search(r"^(Processor|CPU)\s*[:\-]/i", line_clean, re.I) or re.search(r"\b(i[3579]-?\d{4,5}[A-Z]{1,2}|Ryzen\s+[3579]\s+\d{4}[A-Z]{1,2})\b", line_clean, re.I):
            cpu_match = re.search(r"(i[3579]-?\d{4,5}[A-Z]{1,2}|Ryzen\s+[3579]\s+\d{4}[A-Z]{1,2}|Core\s+Ultra\s+\d{1,3}[A-Z]?)", line_clean, re.I)
            if cpu_match:
                extracted["cpu_query"] = cpu_match.group(1)
            else:
                val = re.sub(r"^(Processor|CPU)\s*[:\-]\s*", "", line_clean, flags=re.I)
                extracted["cpu_query"] = val.split("(")[0].strip()

        # 2. Graphics / GPU
        if re.search(r"^(Graphics|GPU|VGA|Graphic Card)\s*[:\-]/i", line_clean, re.I) or re.search(r"\b(RTX|GTX|Radeon|Iris|GeForce)\b", line_clean, re.I):
            gpu_match = re.search(r"(RTX\s*\d{4}(\s*Ti)?|GTX\s*\d{4}(\s*Ti)?|Radeon\s*RX\s*\d{4}[A-Z]?)", line_clean, re.I)
            if gpu_match:
                extracted["gpu_query"] = gpu_match.group(0)
            else:
                val = re.sub(r"^(Graphics|GPU|VGA|Graphic Card)\s*[:\-]\s*", "", line_clean, flags=re.I)
                extracted["gpu_query"] = val.strip()

        # 3. Memory / RAM
        if re.search(r"^(Memory|RAM)\s*[:\-]/i", line_clean, re.I) or re.search(r"\b\d{1,3}\s*GB\s*(DDR|RAM|Memory)\b", line_clean, re.I):
            ram_match = re.search(r"(\d{1,3})\s*GB", line_clean, re.I)
            if ram_match:
                extracted["ram_gb"] = int(ram_match.group(1))

        # 4. Display & Resolution
        if re.search(r"^(Display|Layar|Screen)\s*[:\-]/i", line_clean, re.I) or re.search(r"(1920\s*x\s*1080|2560\s*x\s*1440|3840\s*x\s*2160|Full HD|QHD|4K|144Hz|165Hz|240Hz)", line_clean, re.I):
            extracted["display_desc"] = re.sub(r"^(Display|Layar|Screen)\s*[:\-]\s*", "", line_clean, flags=re.I)
            if re.search(r"(3840\s*x\s*2160|4K|UHD)", line_clean, re.I):
                extracted["resolution"] = "4K"
            elif re.search(r"(2560\s*x\s*1440|1440p|QHD|2K)", line_clean, re.I):
                extracted["resolution"] = "1440p"
            elif re.search(r"(1920\s*x\s*1080|1080p|Full HD|FHD)", line_clean, re.I):
                extracted["resolution"] = "1080p"

            hz_match = re.search(r"(\d{2,3})\s*Hz", line_clean, re.I)
            if hz_match:
                extracted["display_hz"] = int(hz_match.group(1))

        # 5. Storage
        if re.search(r"^(Storage|Penyimpanan|SSD|HDD)\s*[:\-]/i", line_clean, re.I):
            extracted["storage"] = re.sub(r"^(Storage|Penyimpanan|SSD|HDD)\s*[:\-]\s*", "", line_clean, flags=re.I)

        # 6. Battery & OS
        if re.search(r"^(Baterry|Battery|Baterai)\s*[:\-]/i", line_clean, re.I):
            extracted["battery"] = re.sub(r"^(Baterry|Battery|Baterai)\s*[:\-]\s*", "", line_clean, flags=re.I)
        if re.search(r"^(Operating System|OS)\s*[:\-]/i", line_clean, re.I):
            extracted["os"] = re.sub(r"^(Operating System|OS)\s*[:\-]\s*", "", line_clean, flags=re.I)

    return extracted

