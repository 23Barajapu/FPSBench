# FPSBench - Hardware & Game FPS Performance Estimator

FPSBench is a data-driven web platform designed to estimate real-world gaming FPS (Average and 1% Low) and analyze CPU-GPU bottleneck balance across laptop and desktop hardware configurations.

---

## Overview

Translating synthetic benchmark scores (such as Cinebench and 3DMark TimeSpy) into real-world gaming frame rates is often difficult for users. Furthermore, ambiguous hardware naming conventions—such as the massive performance disparity between laptop GPUs with different Total Graphics Power (TGP) ratings versus their desktop counterparts (e.g., RTX 4060 Laptop 45W vs 140W vs RTX 4060 Desktop)—create confusion.

FPSBench resolves this by using a standardized synthetic index calibrated against real-world game engine profiles and calculating performance using a Harmonic Frame Time pipeline.

---

## Core Features

- **Harmonic Frame Time Calculation Engine**: Estimates Average FPS and 1% Low FPS by accounting for CPU single-core frame prep time, GPU rasterization time, RAM capacity limits, and pipeline concurrency.
- **CPU/GPU Bottleneck Analyzer**: Identifies the primary performance constraint (CPU Bottleneck, GPU Bottleneck, or Balanced/Optimal) with exact load distribution percentages.
- **Smart Raw Spec Parser**: Extracts hardware components (CPU, GPU, RAM, display resolution, and refresh rate) directly from raw e-commerce product descriptions or shop brochures.
- **Head-to-Head Comparison**: Side-by-side technical matrix comparing 2 to 4 components with relative performance indices.
- **Comprehensive Hardware Database**: Pre-seeded with over 150 CPUs and GPUs covering Intel (10th to 14th Gen, Core Ultra), AMD Ryzen (3000 to 9000 series), NVIDIA GeForce (GTX 16, RTX 20, 30, and 40 series with specific laptop TGP ratings), AMD Radeon, and Intel Arc.
- **Automated Scraper & ETL Pipeline**: Automated data normalization script and GitHub Actions cron workflow for periodic benchmark synchronization.

---

## Tech Stack

- **Backend**: FastAPI (Python 3.11), SQLAlchemy ORM, Pydantic v2, Uvicorn
- **Frontend**: Vue.js 3 (Composition API), Vite, Vanilla CSS
- **Database**: SQLite (default, zero-configuration) / PostgreSQL compatible
- **Testing**: Pytest, HTTPX TestClient
- **CI/CD**: GitHub Actions

---

## Mathematical Model

The calculation engine models frame delivery using a pipelined frame time approach:

1. **CPU Frame Capacity ($FPS_{cpu}$)**:
   $$FPS_{cpu} = \frac{FPS_{base} \times \left(0.65 \times \frac{Score_{single}}{Base_{single}} + 0.35 \times \frac{Score_{multi}}{Base_{multi}}\right)}{D_{cpu} \times ResScale_{cpu}}$$

2. **GPU Frame Capacity ($FPS_{gpu}$)**:
   $$FPS_{gpu} = \frac{FPS_{base} \times \left(\frac{Score_{gpu}}{Base_{gpu}}\right) \times VRAM_{penalty}}{D_{gpu} \times ResScale_{gpu} \times PresetScale}$$

3. **Combined Frame Time ($T_{frame}$)**:
   $$T_{frame} = \max(T_{cpu}, T_{gpu}) + 0.25 \times \min(T_{cpu}, T_{gpu})$$
   $$FPS_{est} = \left(\frac{1000}{T_{frame}}\right) \times RAM_{penalty}$$

4. **Bottleneck Delta ($\Delta_{perf}$)**:
   $$\Delta_{perf} = \frac{|FPS_{cpu} - FPS_{gpu}|}{\max(FPS_{cpu}, FPS_{gpu})} \times 100\%$$
   - $\Delta_{perf} \le 12\%$: Balanced / Optimal
   - $FPS_{cpu} < FPS_{gpu}$: CPU Bottleneck
   - $FPS_{gpu} < FPS_{cpu}$: GPU Bottleneck

---

## Project Structure

```
track-spek-laptop/
├── backend/
│   ├── calculator.py       # Harmonic Frame Time calculation engine
│   ├── database.py         # SQLAlchemy engine and session setup
│   ├── main.py             # FastAPI REST router and static file serving
│   ├── models.py           # Database entity definitions
│   ├── schemas.py          # Pydantic validation schemas
│   ├── scraper.py          # ETL normalizer and raw spec text parser
│   ├── seed_data.py        # Hardware and game database seed script
│   └── tests/              # Automated test suite
│       ├── test_api.py
│       └── test_calculator.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Calculator.vue       # Input form and raw spec parser UI
│   │   │   ├── ResultCard.vue       # FPS gauge, bottleneck bar, and matrix
│   │   │   ├── HeadToHead.vue       # Side-by-side hardware comparison
│   │   │   ├── HardwareCatalog.vue  # Filterable hardware database browser
│   │   │   └── ScraperPanel.vue     # ETL worker control panel
│   │   ├── assets/main.css          # Production design system stylesheet
│   │   ├── App.vue                  # Main application container
│   │   └── main.js                  # Vue mount entry
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .github/
│   └── workflows/
│       └── scraper_etl.yml # Automated CI/CD ETL pipeline
├── PRD.md                  # Product Requirement Document
├── requirements.txt        # Python backend dependencies
└── README.md
```

---

## Installation & Setup

### Prerequisites

- Python 3.10+
- Node.js 18+ (for building frontend assets)

### 1. Clone & Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies (if compiling frontend from source)
cd frontend
npm install
npm run build
cd ..
```

### 2. Database Initialization

The SQLite database (`fps_estimator.db`) initializes and seeds automatically on first launch. To manually reseed:

```bash
python -m backend.seed_data
```

### 3. Running the Server

#### Option A: Unified Production Mode (FastAPI serves Backend + Frontend)
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
Access the application at `http://localhost:8000`.

#### Option B: Development Mode (Hot-Reload)
Terminal 1 (Backend API):
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Terminal 2 (Frontend Dev Server):
```bash
cd frontend
npm run dev
```
Access the frontend development server at `http://localhost:5173`.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status check |
| `GET` | `/api/hardware/search` | Autocomplete hardware search with category and form factor filters |
| `GET` | `/api/hardware/compare` | Multi-item head-to-head comparison (accepts comma-separated IDs) |
| `GET` | `/api/hardware/{id}` | Detailed hardware specifications by ID |
| `GET` | `/api/games` | Game catalog with engine profiles and compute weighting |
| `POST` | `/api/calculate` | Compute FPS estimates, 1% low, and bottleneck status |
| `POST` | `/api/hardware/parse-raw-spec` | Parse unformatted text and match closest database entries |
| `POST` | `/api/pipeline/run` | Execute ETL batch upsert into database |

---

## Testing

Run the automated test suite with Pytest:

```bash
python -m pytest backend/tests -v
```

Test coverage includes:
- Harmonic frame time calculation correctness
- CPU and GPU bottleneck threshold validations
- Laptop TGP power scaling impact
- RAM penalty and stutter ratio calculations
- REST API endpoint contracts and input validation
- Raw spec text parsing and fuzzy entity matching

---

## License

This project is released under the MIT License.
