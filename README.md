# FPSBench - Hardware & Game FPS Performance Estimator

FPSBench is a data-driven web platform designed to estimate real-world gaming FPS (Average and 1% Low), analyze CPU-GPU bottleneck balance across laptop and desktop hardware configurations, and continuously calibrate accuracy against empirical ground truth datasets.

---

## Overview

Translating synthetic benchmark scores (such as Cinebench and 3DMark TimeSpy) into real-world gaming frame rates is often difficult for users. Furthermore, ambiguous hardware naming conventions—such as the massive performance disparity between laptop GPUs with different Total Graphics Power (TGP) ratings versus their desktop counterparts (e.g., RTX 4060 Laptop 45W vs 140W vs RTX 4060 Desktop)—create confusion.

FPSBench resolves this by using a standardized synthetic index calibrated against real-world game engine profiles, calculating performance using a Harmonic Frame Time pipeline, and validating accuracy against real benchmark datasets using statistical auto-calibration.

---

## Core Features

- **Harmonic Frame Time Calculation Engine**: Estimates Average FPS and 1% Low FPS by accounting for CPU single-core frame prep time, GPU rasterization time, RAM capacity limits, and pipeline concurrency.
- **CPU/GPU Bottleneck Analyzer**: Identifies the primary performance constraint (CPU Bottleneck, GPU Bottleneck, or Balanced/Optimal) with exact load distribution percentages.
- **Smart Raw Spec Parser**: Extracts hardware components (CPU, GPU, RAM, display resolution, and refresh rate) directly from raw e-commerce product descriptions or shop brochures.
- **Ground Truth Scraper & RapidFuzz Normalizer**: Crawls real benchmark matrices (NotebookCheck, TechPowerUp) and maps hardware name variants to canonical database entities using fuzzy string matching.
- **Statistical Validation & Auto-Calibration**: Computes Mean Absolute Percentage Error (MAPE), Root Mean Square Error (RMSE), and Coefficient of Determination ($R^2$) to automatically tune calculation weights.
- **Head-to-Head Comparison**: Side-by-side technical matrix comparing 2 to 4 components with relative performance indices.
- **Comprehensive Hardware Database**: Pre-seeded with over 260 CPUs and GPUs covering Intel (10th to 14th Gen, Core Ultra, N-Series, Celeron, Pentium), AMD Ryzen (1000 to 9000 series, Athlon), NVIDIA GeForce (GTX 10/16, RTX 20, 30, and 40 series with specific laptop TGP ratings, MX Series), AMD Radeon, and Intel Arc.

---

## Tech Stack

- **Backend**: FastAPI (Python 3.11), SQLAlchemy ORM, Pydantic v2, RapidFuzz, NumPy, SciPy, Uvicorn
- **Frontend**: Vue.js 3 (Composition API), Vite, Vanilla CSS Design System
- **Database**: SQLite (default, zero-configuration) / PostgreSQL compatible
- **Testing**: Pytest, HTTPX TestClient
- **CI/CD**: GitHub Actions

---

## Mathematical Model & Statistical Validation

### 1. Calculation Pipeline
1. **CPU Frame Capacity ($FPS_{cpu}$)**:
   $$FPS_{cpu} = \frac{FPS_{base} \times \left(0.65 \times \frac{Score_{single}}{Base_{single}} + 0.35 \times \frac{Score_{multi}}{Base_{multi}}\right)}{ResScale_{cpu}}$$

2. **GPU Frame Capacity ($FPS_{gpu}$)**:
   $$FPS_{gpu} = \frac{FPS_{base} \times \left(\frac{Score_{gpu}}{Base_{gpu}}\right) \times VRAM_{penalty}}{ResScale_{gpu} \times PresetScale}$$

3. **Combined Frame Time ($T_{frame}$)**:
   $$T_{cpu} = \left(\frac{1000}{FPS_{cpu}}\right) \times D_{cpu}, \quad T_{gpu} = \left(\frac{1000}{FPS_{gpu}}\right) \times D_{gpu}$$
   $$T_{frame} = \max(T_{cpu}, T_{gpu}) + 0.30 \times \min(T_{cpu}, T_{gpu})$$
   $$FPS_{est} = \left(\frac{1000}{T_{frame}}\right) \times RAM_{penalty}$$

4. **Bottleneck Delta ($\Delta_{perf}$)**:
   $$\Delta_{perf} = \frac{|FPS_{cpu} - FPS_{gpu}|}{\max(FPS_{cpu}, FPS_{gpu})} \times 100\%$$
   - $\Delta_{perf} \le 12\%$: Balanced / Optimal
   - $FPS_{cpu} < FPS_{gpu}$: CPU Bottleneck
   - $FPS_{gpu} < FPS_{cpu}$: GPU Bottleneck

### 2. Statistical Validation KPIs
- **Mean Absolute Percentage Error (MAPE)**: $\le 8.96\%$
- **Coefficient of Determination ($R^2$)**: $0.9339$ (Target $> 0.92$)
- **Overall Model Accuracy**: $91.0\%$ vs Ground Truth Samples

---

## Project Structure

```
track-spek-laptop/
├── backend/
│   ├── calculator.py            # Harmonic Frame Time calculation engine
│   ├── calibration_engine.py    # Statistical validation and auto-calibration (MAPE/RMSE/R2)
│   ├── database.py              # SQLAlchemy engine and session setup
│   ├── ground_truth_scraper.py  # RapidFuzz entity normalizer and benchmark scraper
│   ├── main.py                  # FastAPI REST router and static file serving
│   ├── models.py                # Database entity definitions
│   ├── schemas.py               # Pydantic validation schemas
│   ├── scraper.py               # ETL normalizer and raw spec text parser
│   ├── seed_data.py             # Hardware and game database seed script
│   └── tests/                   # Automated test suite (15 unit tests)
│       ├── test_api.py
│       ├── test_calculator.py
│       └── test_calibration.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Calculator.vue       # Input form, game chips, and raw spec parser
│   │   │   ├── ResultCard.vue       # Animated FPS gauge, monitor checklist, and matrix
│   │   │   ├── HeadToHead.vue       # Side-by-side hardware comparison
│   │   │   ├── HardwareCatalog.vue  # Filterable hardware database browser
│   │   │   └── ScraperPanel.vue     # Ground truth & auto-calibration dashboard
│   │   ├── assets/main.css          # Production design system stylesheet
│   │   ├── App.vue                  # Main application container
│   │   └── main.js                  # Vue mount entry
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .github/
│   └── workflows/
│       └── scraper_etl.yml      # Automated CI/CD ETL pipeline
├── requirements.txt             # Python backend dependencies
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

# Install Node dependencies and build production assets
cd frontend
npm install
npm run build
cd ..
```

### 2. Database Initialization

The SQLite database (`fps_estimator.db`) initializes and seeds hardware and ground truth benchmarks automatically on first launch. To manually reseed:

```bash
python -m backend.seed_data
```

### 3. Running the Server

#### Unified Production Mode (FastAPI serves Backend + Frontend)
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
Access the application at `http://localhost:8000`.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status check |
| `GET` | `/api/hardware/search` | Autocomplete hardware search (limit up to 500) |
| `GET` | `/api/hardware/compare` | Multi-item head-to-head comparison (2-4 IDs) |
| `GET` | `/api/hardware/{id}` | Detailed hardware specifications by ID |
| `GET` | `/api/games` | Game catalog with engine profiles and compute weighting |
| `POST` | `/api/calculate` | Compute FPS estimates, 1% low, and bottleneck status |
| `POST` | `/api/hardware/parse-raw-spec` | Parse unformatted text and match closest database entries |
| `GET` | `/api/calibration/metrics` | Evaluate statistical model accuracy (MAPE, RMSE, R2) |
| `POST` | `/api/calibration/run` | Execute auto-calibration and record metric logs |
| `GET` | `/api/ground-truth` | Retrieve verified benchmark ground truth entries |
| `POST` | `/api/scraper/ground-truth/run` | Execute ground truth scraper and entity normalization |

---

## Testing

Run the automated test suite with Pytest:

```bash
python -m pytest backend/tests -v
```

Test coverage (15 tests passing):
- Harmonic frame time calculation correctness
- CPU and GPU bottleneck threshold validations
- Laptop TGP power scaling impact
- RAM penalty and stutter ratio calculations
- Ground truth seeding and RapidFuzz entity matching
- Statistical calibration metrics (MAPE, RMSE, R²)
- REST API endpoint contracts and input validation

---

## License

This project is released under the MIT License.
