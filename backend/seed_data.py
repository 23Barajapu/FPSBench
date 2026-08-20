"""
Database Seeding Script.
Memasukkan katalog lengkap CPU & GPU (Entry Level, Office, Mid-Range, High-End, Desktop & Laptop).
"""
from .database import engine, Base, SessionLocal
from .models import HardwareBenchmark, Game, PresetMultiplier

def seed_database(force_refresh: bool = False):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if force_refresh:
        print("Refreshing database records...")
        db.query(HardwareBenchmark).delete()
        db.query(Game).delete()
        db.query(PresetMultiplier).delete()
        db.commit()
    elif db.query(HardwareBenchmark).count() >= 180:
        print(f"Database already populated with {db.query(HardwareBenchmark).count()} hardware items.")
        db.close()
        return

    print("Populating complete CPU and GPU hardware database from Entry Level to Enthusiast...")

    # ==========================================
    # 1. PROCESSORS (CPUs)
    # ==========================================
    cpus = [
        # --- Intel Entry Level & Office (Celeron, Pentium, N-Series, U-Series) ---
        HardwareBenchmark(name="Intel Processor N100", brand="Intel", category="cpu", form_factor="laptop", single_score=950, multi_score=3800, base_clock_ghz=0.8, boost_clock_ghz=3.4, tgp_watts=6, release_year=2023),
        HardwareBenchmark(name="Intel Processor N95", brand="Intel", category="cpu", form_factor="laptop", single_score=920, multi_score=3600, base_clock_ghz=1.7, boost_clock_ghz=3.4, tgp_watts=15, release_year=2023),
        HardwareBenchmark(name="Intel Processor N200", brand="Intel", category="cpu", form_factor="laptop", single_score=1050, multi_score=4200, base_clock_ghz=1.0, boost_clock_ghz=3.7, tgp_watts=6, release_year=2023),
        HardwareBenchmark(name="Celeron N4020", brand="Intel", category="cpu", form_factor="laptop", single_score=420, multi_score=850, base_clock_ghz=1.1, boost_clock_ghz=2.8, tgp_watts=6, release_year=2019),
        HardwareBenchmark(name="Celeron N4500", brand="Intel", category="cpu", form_factor="laptop", single_score=580, multi_score=1250, base_clock_ghz=1.1, boost_clock_ghz=2.8, tgp_watts=6, release_year=2021),
        HardwareBenchmark(name="Pentium Silver N5030", brand="Intel", category="cpu", form_factor="laptop", single_score=490, multi_score=1600, base_clock_ghz=1.1, boost_clock_ghz=3.1, tgp_watts=6, release_year=2019),
        HardwareBenchmark(name="Pentium Gold 7505", brand="Intel", category="cpu", form_factor="laptop", single_score=1050, multi_score=3100, base_clock_ghz=2.0, boost_clock_ghz=3.5, tgp_watts=15, release_year=2020),
        HardwareBenchmark(name="Pentium Gold 8505", brand="Intel", category="cpu", form_factor="laptop", single_score=1350, multi_score=5600, base_clock_ghz=1.2, boost_clock_ghz=4.4, tgp_watts=15, release_year=2022),

        # --- Intel Core i3 / i5 / i7 U-Series & G-Series (Office / Ultrabook) ---
        HardwareBenchmark(name="Core i3-1005G1", brand="Intel", category="cpu", form_factor="laptop", single_score=950, multi_score=2900, base_clock_ghz=1.2, boost_clock_ghz=3.4, tgp_watts=15, release_year=2019),
        HardwareBenchmark(name="Core i3-1115G4", brand="Intel", category="cpu", form_factor="laptop", single_score=1180, multi_score=3600, base_clock_ghz=3.0, boost_clock_ghz=4.1, tgp_watts=15, release_year=2020),
        HardwareBenchmark(name="Core i3-1125G4", brand="Intel", category="cpu", form_factor="laptop", single_score=1200, multi_score=5200, base_clock_ghz=2.0, boost_clock_ghz=3.7, tgp_watts=15, release_year=2020),
        HardwareBenchmark(name="Core i5-1135G7", brand="Intel", category="cpu", form_factor="laptop", single_score=1320, multi_score=6200, base_clock_ghz=2.4, boost_clock_ghz=4.2, tgp_watts=28, release_year=2020),
        HardwareBenchmark(name="Core i5-1155G7", brand="Intel", category="cpu", form_factor="laptop", single_score=1380, multi_score=6800, base_clock_ghz=2.5, boost_clock_ghz=4.5, tgp_watts=28, release_year=2021),
        HardwareBenchmark(name="Core i7-1165G7", brand="Intel", category="cpu", form_factor="laptop", single_score=1420, multi_score=7200, base_clock_ghz=2.8, boost_clock_ghz=4.7, tgp_watts=28, release_year=2020),
        HardwareBenchmark(name="Core i3-1215U", brand="Intel", category="cpu", form_factor="laptop", single_score=1450, multi_score=7200, base_clock_ghz=1.2, boost_clock_ghz=4.4, tgp_watts=15, release_year=2022),
        HardwareBenchmark(name="Core i5-1235U", brand="Intel", category="cpu", form_factor="laptop", single_score=1520, multi_score=9400, base_clock_ghz=1.3, boost_clock_ghz=4.4, tgp_watts=15, release_year=2022),
        HardwareBenchmark(name="Core i7-1255U", brand="Intel", category="cpu", form_factor="laptop", single_score=1580, multi_score=10200, base_clock_ghz=1.7, boost_clock_ghz=4.7, tgp_watts=15, release_year=2022),
        HardwareBenchmark(name="Core i3-1315U", brand="Intel", category="cpu", form_factor="laptop", single_score=1500, multi_score=7800, base_clock_ghz=1.2, boost_clock_ghz=4.5, tgp_watts=15, release_year=2023),
        HardwareBenchmark(name="Core i5-1335U", brand="Intel", category="cpu", form_factor="laptop", single_score=1600, multi_score=10200, base_clock_ghz=1.3, boost_clock_ghz=4.6, tgp_watts=15, release_year=2023),
        HardwareBenchmark(name="Core i7-1355U", brand="Intel", category="cpu", form_factor="laptop", single_score=1680, multi_score=11200, base_clock_ghz=1.7, boost_clock_ghz=5.0, tgp_watts=15, release_year=2023),
        HardwareBenchmark(name="Core i5-8250U", brand="Intel", category="cpu", form_factor="laptop", single_score=780, multi_score=3200, base_clock_ghz=1.6, boost_clock_ghz=3.4, tgp_watts=15, release_year=2017),
        HardwareBenchmark(name="Core i5-10210U", brand="Intel", category="cpu", form_factor="laptop", single_score=920, multi_score=3800, base_clock_ghz=1.6, boost_clock_ghz=4.2, tgp_watts=15, release_year=2019),

        # --- Intel Laptop High Performance (Core Ultra, HX, H Series) ---
        HardwareBenchmark(name="Core Ultra 9 185H", brand="Intel", category="cpu", form_factor="laptop", single_score=2100, multi_score=21500, base_clock_ghz=2.3, boost_clock_ghz=5.1, tgp_watts=45, release_year=2024),
        HardwareBenchmark(name="Core Ultra 7 155H", brand="Intel", category="cpu", form_factor="laptop", single_score=1980, multi_score=18500, base_clock_ghz=1.4, boost_clock_ghz=4.8, tgp_watts=28, release_year=2024),
        HardwareBenchmark(name="Core Ultra 5 125H", brand="Intel", category="cpu", form_factor="laptop", single_score=1820, multi_score=15200, base_clock_ghz=1.2, boost_clock_ghz=4.5, tgp_watts=28, release_year=2024),
        HardwareBenchmark(name="Core i9-14900HX", brand="Intel", category="cpu", form_factor="laptop", single_score=2200, multi_score=25000, base_clock_ghz=2.2, boost_clock_ghz=5.8, tgp_watts=55, release_year=2024),
        HardwareBenchmark(name="Core i7-14700HX", brand="Intel", category="cpu", form_factor="laptop", single_score=2080, multi_score=22500, base_clock_ghz=2.1, boost_clock_ghz=5.5, tgp_watts=55, release_year=2024),
        HardwareBenchmark(name="Core i7-14650HX", brand="Intel", category="cpu", form_factor="laptop", single_score=2020, multi_score=21000, base_clock_ghz=2.2, boost_clock_ghz=5.2, tgp_watts=55, release_year=2024),
        HardwareBenchmark(name="Core i5-14500HX", brand="Intel", category="cpu", form_factor="laptop", single_score=1880, multi_score=16800, base_clock_ghz=2.6, boost_clock_ghz=4.9, tgp_watts=55, release_year=2024),
        HardwareBenchmark(name="Core i9-13980HX", brand="Intel", category="cpu", form_factor="laptop", single_score=2180, multi_score=24500, base_clock_ghz=2.2, boost_clock_ghz=5.6, tgp_watts=55, release_year=2023),
        HardwareBenchmark(name="Core i7-13700HX", brand="Intel", category="cpu", form_factor="laptop", single_score=2000, multi_score=20500, base_clock_ghz=2.1, boost_clock_ghz=5.0, tgp_watts=55, release_year=2023),
        HardwareBenchmark(name="Core i7-13620H", brand="Intel", category="cpu", form_factor="laptop", single_score=1850, multi_score=15500, base_clock_ghz=2.4, boost_clock_ghz=4.9, tgp_watts=45, release_year=2023),
        HardwareBenchmark(name="Core i5-13500H", brand="Intel", category="cpu", form_factor="laptop", single_score=1750, multi_score=13800, base_clock_ghz=2.6, boost_clock_ghz=4.7, tgp_watts=45, release_year=2023),
        HardwareBenchmark(name="Core i5-13420H", brand="Intel", category="cpu", form_factor="laptop", single_score=1680, multi_score=11500, base_clock_ghz=2.1, boost_clock_ghz=4.6, tgp_watts=45, release_year=2023),
        HardwareBenchmark(name="Core i7-12700H", brand="Intel", category="cpu", form_factor="laptop", single_score=1780, multi_score=14500, base_clock_ghz=2.3, boost_clock_ghz=4.7, tgp_watts=45, release_year=2022),
        HardwareBenchmark(name="Core i5-12500H", brand="Intel", category="cpu", form_factor="laptop", single_score=1650, multi_score=12200, base_clock_ghz=2.5, boost_clock_ghz=4.5, tgp_watts=45, release_year=2022),
        HardwareBenchmark(name="Core i5-12450H", brand="Intel", category="cpu", form_factor="laptop", single_score=1520, multi_score=10200, base_clock_ghz=2.0, boost_clock_ghz=4.4, tgp_watts=45, release_year=2022),
        HardwareBenchmark(name="Core i7-11800H", brand="Intel", category="cpu", form_factor="laptop", single_score=1450, multi_score=11000, base_clock_ghz=2.3, boost_clock_ghz=4.6, tgp_watts=45, release_year=2021),
        HardwareBenchmark(name="Core i5-11400H", brand="Intel", category="cpu", form_factor="laptop", single_score=1350, multi_score=8900, base_clock_ghz=2.7, boost_clock_ghz=4.5, tgp_watts=45, release_year=2021),
        HardwareBenchmark(name="Core i7-10750H", brand="Intel", category="cpu", form_factor="laptop", single_score=1180, multi_score=7800, base_clock_ghz=2.6, boost_clock_ghz=5.0, tgp_watts=45, release_year=2020),
        HardwareBenchmark(name="Core i5-10300H", brand="Intel", category="cpu", form_factor="laptop", single_score=1050, multi_score=5100, base_clock_ghz=2.5, boost_clock_ghz=4.5, tgp_watts=45, release_year=2020),

        # --- Intel Desktop (Gen 6 to 14) ---
        HardwareBenchmark(name="Core i9-14900KS", brand="Intel", category="cpu", form_factor="desktop", single_score=2450, multi_score=31000, base_clock_ghz=3.2, boost_clock_ghz=6.2, release_year=2024),
        HardwareBenchmark(name="Core i9-14900K", brand="Intel", category="cpu", form_factor="desktop", single_score=2350, multi_score=29500, base_clock_ghz=3.2, boost_clock_ghz=6.0, release_year=2023),
        HardwareBenchmark(name="Core i7-14700K", brand="Intel", category="cpu", form_factor="desktop", single_score=2250, multi_score=24500, base_clock_ghz=3.4, boost_clock_ghz=5.6, release_year=2023),
        HardwareBenchmark(name="Core i5-14600K", brand="Intel", category="cpu", form_factor="desktop", single_score=2100, multi_score=18500, base_clock_ghz=3.5, boost_clock_ghz=5.3, release_year=2023),
        HardwareBenchmark(name="Core i5-14400F", brand="Intel", category="cpu", form_factor="desktop", single_score=1850, multi_score=14200, base_clock_ghz=2.5, boost_clock_ghz=4.7, release_year=2024),
        HardwareBenchmark(name="Core i9-13900K", brand="Intel", category="cpu", form_factor="desktop", single_score=2300, multi_score=28500, base_clock_ghz=3.0, boost_clock_ghz=5.8, release_year=2022),
        HardwareBenchmark(name="Core i7-13700K", brand="Intel", category="cpu", form_factor="desktop", single_score=2180, multi_score=23500, base_clock_ghz=3.4, boost_clock_ghz=5.4, release_year=2022),
        HardwareBenchmark(name="Core i5-13600K", brand="Intel", category="cpu", form_factor="desktop", single_score=2050, multi_score=17800, base_clock_ghz=3.5, boost_clock_ghz=5.1, release_year=2022),
        HardwareBenchmark(name="Core i5-13500", brand="Intel", category="cpu", form_factor="desktop", single_score=1820, multi_score=15000, base_clock_ghz=2.5, boost_clock_ghz=4.8, release_year=2023),
        HardwareBenchmark(name="Core i5-13400F", brand="Intel", category="cpu", form_factor="desktop", single_score=1780, multi_score=13500, base_clock_ghz=2.5, boost_clock_ghz=4.6, release_year=2023),
        HardwareBenchmark(name="Core i3-13100F", brand="Intel", category="cpu", form_factor="desktop", single_score=1620, multi_score=8800, base_clock_ghz=3.4, boost_clock_ghz=4.5, release_year=2023),
        HardwareBenchmark(name="Core i9-12900K", brand="Intel", category="cpu", form_factor="desktop", single_score=2050, multi_score=22000, base_clock_ghz=3.2, boost_clock_ghz=5.2, release_year=2021),
        HardwareBenchmark(name="Core i7-12700K", brand="Intel", category="cpu", form_factor="desktop", single_score=1950, multi_score=18500, base_clock_ghz=3.6, boost_clock_ghz=5.0, release_year=2021),
        HardwareBenchmark(name="Core i5-12600K", brand="Intel", category="cpu", form_factor="desktop", single_score=1850, multi_score=14500, base_clock_ghz=3.7, boost_clock_ghz=4.9, release_year=2021),
        HardwareBenchmark(name="Core i5-12400F", brand="Intel", category="cpu", form_factor="desktop", single_score=1600, multi_score=12000, base_clock_ghz=2.5, boost_clock_ghz=4.4, release_year=2022),
        HardwareBenchmark(name="Core i3-12100F", brand="Intel", category="cpu", form_factor="desktop", single_score=1500, multi_score=7800, base_clock_ghz=3.3, boost_clock_ghz=4.3, release_year=2022),
        HardwareBenchmark(name="Core i9-11900K", brand="Intel", category="cpu", form_factor="desktop", single_score=1650, multi_score=13500, base_clock_ghz=3.5, boost_clock_ghz=5.3, release_year=2021),
        HardwareBenchmark(name="Core i7-11700K", brand="Intel", category="cpu", form_factor="desktop", single_score=1550, multi_score=12500, base_clock_ghz=3.6, boost_clock_ghz=5.0, release_year=2021),
        HardwareBenchmark(name="Core i5-11400F", brand="Intel", category="cpu", form_factor="desktop", single_score=1400, multi_score=9800, base_clock_ghz=2.6, boost_clock_ghz=4.4, release_year=2021),
        HardwareBenchmark(name="Core i9-10900K", brand="Intel", category="cpu", form_factor="desktop", single_score=1420, multi_score=13000, base_clock_ghz=3.7, boost_clock_ghz=5.3, release_year=2020),
        HardwareBenchmark(name="Core i7-10700K", brand="Intel", category="cpu", form_factor="desktop", single_score=1320, multi_score=10500, base_clock_ghz=3.8, boost_clock_ghz=5.1, release_year=2020),
        HardwareBenchmark(name="Core i5-10400F", brand="Intel", category="cpu", form_factor="desktop", single_score=1180, multi_score=7500, base_clock_ghz=2.9, boost_clock_ghz=4.3, release_year=2020),
        HardwareBenchmark(name="Core i3-10100F", brand="Intel", category="cpu", form_factor="desktop", single_score=1100, multi_score=5200, base_clock_ghz=3.6, boost_clock_ghz=4.3, release_year=2020),
        HardwareBenchmark(name="Core i7-9700K", brand="Intel", category="cpu", form_factor="desktop", single_score=1240, multi_score=8400, base_clock_ghz=3.6, boost_clock_ghz=4.9, release_year=2018),
        HardwareBenchmark(name="Core i5-9400F", brand="Intel", category="cpu", form_factor="desktop", single_score=1080, multi_score=5600, base_clock_ghz=2.9, boost_clock_ghz=4.1, release_year=2019),
        HardwareBenchmark(name="Core i3-9100F", brand="Intel", category="cpu", form_factor="desktop", single_score=1000, multi_score=3900, base_clock_ghz=3.6, boost_clock_ghz=4.2, release_year=2019),
        HardwareBenchmark(name="Core i7-8700K", brand="Intel", category="cpu", form_factor="desktop", single_score=1180, multi_score=7600, base_clock_ghz=3.7, boost_clock_ghz=4.7, release_year=2017),
        HardwareBenchmark(name="Core i5-8400", brand="Intel", category="cpu", form_factor="desktop", single_score=980, multi_score=4800, base_clock_ghz=2.8, boost_clock_ghz=4.0, release_year=2017),
        HardwareBenchmark(name="Core i7-7700K", brand="Intel", category="cpu", form_factor="desktop", single_score=1050, multi_score=5100, base_clock_ghz=4.2, boost_clock_ghz=4.5, release_year=2017),

        # --- AMD Entry Level & Office (Athlon, Ryzen 3/5/7 U-Series) ---
        HardwareBenchmark(name="Athlon Silver 3050U", brand="AMD", category="cpu", form_factor="laptop", single_score=680, multi_score=1450, base_clock_ghz=2.3, boost_clock_ghz=3.2, tgp_watts=15, release_year=2020),
        HardwareBenchmark(name="Athlon Gold 3150U", brand="AMD", category="cpu", form_factor="laptop", single_score=820, multi_score=2600, base_clock_ghz=2.4, boost_clock_ghz=3.3, tgp_watts=15, release_year=2020),
        HardwareBenchmark(name="Athlon 3000G", brand="AMD", category="cpu", form_factor="desktop", single_score=750, multi_score=2200, base_clock_ghz=3.5, boost_clock_ghz=3.5, release_year=2019),
        HardwareBenchmark(name="Ryzen 3 3200U", brand="AMD", category="cpu", form_factor="laptop", single_score=820, multi_score=2700, base_clock_ghz=2.6, boost_clock_ghz=3.5, tgp_watts=15, release_year=2019),
        HardwareBenchmark(name="Ryzen 3 3250U", brand="AMD", category="cpu", form_factor="laptop", single_score=840, multi_score=2800, base_clock_ghz=2.6, boost_clock_ghz=3.5, tgp_watts=15, release_year=2020),
        HardwareBenchmark(name="Ryzen 3 4300U", brand="AMD", category="cpu", form_factor="laptop", single_score=1080, multi_score=4500, base_clock_ghz=2.7, boost_clock_ghz=3.7, tgp_watts=15, release_year=2020),
        HardwareBenchmark(name="Ryzen 3 5300U", brand="AMD", category="cpu", form_factor="laptop", single_score=1150, multi_score=5800, base_clock_ghz=2.6, boost_clock_ghz=3.8, tgp_watts=15, release_year=2021),
        HardwareBenchmark(name="Ryzen 3 7320U", brand="AMD", category="cpu", form_factor="laptop", single_score=1100, multi_score=5200, base_clock_ghz=2.4, boost_clock_ghz=4.1, tgp_watts=15, release_year=2022),
        HardwareBenchmark(name="Ryzen 5 3500U", brand="AMD", category="cpu", form_factor="laptop", single_score=880, multi_score=3800, base_clock_ghz=2.1, boost_clock_ghz=3.7, tgp_watts=15, release_year=2019),
        HardwareBenchmark(name="Ryzen 5 4500U", brand="AMD", category="cpu", form_factor="laptop", single_score=1120, multi_score=6200, base_clock_ghz=2.3, boost_clock_ghz=4.0, tgp_watts=15, release_year=2020),
        HardwareBenchmark(name="Ryzen 5 5500U", brand="AMD", category="cpu", form_factor="laptop", single_score=1220, multi_score=8200, base_clock_ghz=2.1, boost_clock_ghz=4.0, tgp_watts=15, release_year=2021),
        HardwareBenchmark(name="Ryzen 5 7520U", brand="AMD", category="cpu", form_factor="laptop", single_score=1180, multi_score=6200, base_clock_ghz=2.8, boost_clock_ghz=4.3, tgp_watts=15, release_year=2022),
        HardwareBenchmark(name="Ryzen 5 7530U", brand="AMD", category="cpu", form_factor="laptop", single_score=1350, multi_score=9500, base_clock_ghz=2.0, boost_clock_ghz=4.5, tgp_watts=15, release_year=2023),
        HardwareBenchmark(name="Ryzen 7 3700U", brand="AMD", category="cpu", form_factor="laptop", single_score=950, multi_score=4200, base_clock_ghz=2.3, boost_clock_ghz=4.0, tgp_watts=15, release_year=2019),
        HardwareBenchmark(name="Ryzen 7 4700U", brand="AMD", category="cpu", form_factor="laptop", single_score=1180, multi_score=7400, base_clock_ghz=2.0, boost_clock_ghz=4.1, tgp_watts=15, release_year=2020),
        HardwareBenchmark(name="Ryzen 7 5700U", brand="AMD", category="cpu", form_factor="laptop", single_score=1280, multi_score=10200, base_clock_ghz=1.8, boost_clock_ghz=4.3, tgp_watts=15, release_year=2021),
        HardwareBenchmark(name="Ryzen 7 7730U", brand="AMD", category="cpu", form_factor="laptop", single_score=1420, multi_score=11500, base_clock_ghz=2.0, boost_clock_ghz=4.5, tgp_watts=15, release_year=2023),

        # --- AMD Laptop High Performance (HX, HS, H Series) ---
        HardwareBenchmark(name="Ryzen 9 8945HS", brand="AMD", category="cpu", form_factor="laptop", single_score=2020, multi_score=18500, base_clock_ghz=4.0, boost_clock_ghz=5.2, tgp_watts=45, release_year=2024),
        HardwareBenchmark(name="Ryzen 7 8845HS", brand="AMD", category="cpu", form_factor="laptop", single_score=1950, multi_score=17200, base_clock_ghz=3.8, boost_clock_ghz=5.1, tgp_watts=45, release_year=2024),
        HardwareBenchmark(name="Ryzen 5 8645HS", brand="AMD", category="cpu", form_factor="laptop", single_score=1850, multi_score=14200, base_clock_ghz=4.3, boost_clock_ghz=5.0, tgp_watts=45, release_year=2024),
        HardwareBenchmark(name="Ryzen 9 7945HX", brand="AMD", category="cpu", form_factor="laptop", single_score=2100, multi_score=26500, base_clock_ghz=2.5, boost_clock_ghz=5.4, tgp_watts=55, release_year=2023),
        HardwareBenchmark(name="Ryzen 7 7840HS", brand="AMD", category="cpu", form_factor="laptop", single_score=1900, multi_score=16500, base_clock_ghz=3.8, boost_clock_ghz=5.1, tgp_watts=35, release_year=2023),
        HardwareBenchmark(name="Ryzen 7 7735HS", brand="AMD", category="cpu", form_factor="laptop", single_score=1580, multi_score=13500, base_clock_ghz=3.2, boost_clock_ghz=4.75, tgp_watts=35, release_year=2023),
        HardwareBenchmark(name="Ryzen 5 7640HS", brand="AMD", category="cpu", form_factor="laptop", single_score=1800, multi_score=13000, base_clock_ghz=4.3, boost_clock_ghz=5.0, tgp_watts=35, release_year=2023),
        HardwareBenchmark(name="Ryzen 5 7535HS", brand="AMD", category="cpu", form_factor="laptop", single_score=1420, multi_score=10800, base_clock_ghz=3.3, boost_clock_ghz=4.55, tgp_watts=35, release_year=2023),
        HardwareBenchmark(name="Ryzen 9 6900HX", brand="AMD", category="cpu", form_factor="laptop", single_score=1620, multi_score=14200, base_clock_ghz=3.3, boost_clock_ghz=4.9, tgp_watts=45, release_year=2022),
        HardwareBenchmark(name="Ryzen 7 6800H", brand="AMD", category="cpu", form_factor="laptop", single_score=1550, multi_score=12500, base_clock_ghz=3.2, boost_clock_ghz=4.7, tgp_watts=45, release_year=2022),
        HardwareBenchmark(name="Ryzen 5 6600H", brand="AMD", category="cpu", form_factor="laptop", single_score=1450, multi_score=10200, base_clock_ghz=3.3, boost_clock_ghz=4.5, tgp_watts=45, release_year=2022),
        HardwareBenchmark(name="Ryzen 7 5800H", brand="AMD", category="cpu", form_factor="laptop", single_score=1420, multi_score=11200, base_clock_ghz=3.2, boost_clock_ghz=4.4, tgp_watts=45, release_year=2021),
        HardwareBenchmark(name="Ryzen 5 5600H", brand="AMD", category="cpu", form_factor="laptop", single_score=1350, multi_score=9800, base_clock_ghz=3.3, boost_clock_ghz=4.2, tgp_watts=45, release_year=2021),
        HardwareBenchmark(name="Ryzen 7 4800H", brand="AMD", category="cpu", form_factor="laptop", single_score=1180, multi_score=8500, base_clock_ghz=2.9, boost_clock_ghz=4.2, tgp_watts=45, release_year=2020),
        HardwareBenchmark(name="Ryzen 5 4600H", brand="AMD", category="cpu", form_factor="laptop", single_score=1100, multi_score=7200, base_clock_ghz=3.0, boost_clock_ghz=4.0, tgp_watts=45, release_year=2020),

        # --- AMD Desktop (Ryzen 1000 to 9000) ---
        HardwareBenchmark(name="Ryzen 9 9950X", brand="AMD", category="cpu", form_factor="desktop", single_score=2480, multi_score=33000, base_clock_ghz=4.3, boost_clock_ghz=5.7, release_year=2024),
        HardwareBenchmark(name="Ryzen 7 9700X", brand="AMD", category="cpu", form_factor="desktop", single_score=2380, multi_score=22500, base_clock_ghz=3.8, boost_clock_ghz=5.5, release_year=2024),
        HardwareBenchmark(name="Ryzen 5 9600X", brand="AMD", category="cpu", form_factor="desktop", single_score=2300, multi_score=17800, base_clock_ghz=3.9, boost_clock_ghz=5.4, release_year=2024),
        HardwareBenchmark(name="Ryzen 7 7800X3D", brand="AMD", category="cpu", form_factor="desktop", single_score=2150, multi_score=19500, base_clock_ghz=4.2, boost_clock_ghz=5.0, release_year=2023),
        HardwareBenchmark(name="Ryzen 9 7950X3D", brand="AMD", category="cpu", form_factor="desktop", single_score=2250, multi_score=29000, base_clock_ghz=4.2, boost_clock_ghz=5.7, release_year=2023),
        HardwareBenchmark(name="Ryzen 9 7950X", brand="AMD", category="cpu", form_factor="desktop", single_score=2280, multi_score=28000, base_clock_ghz=4.5, boost_clock_ghz=5.7, release_year=2022),
        HardwareBenchmark(name="Ryzen 9 7900X", brand="AMD", category="cpu", form_factor="desktop", single_score=2200, multi_score=24000, base_clock_ghz=4.7, boost_clock_ghz=5.6, release_year=2022),
        HardwareBenchmark(name="Ryzen 7 7700X", brand="AMD", category="cpu", form_factor="desktop", single_score=2120, multi_score=18800, base_clock_ghz=4.5, boost_clock_ghz=5.4, release_year=2022),
        HardwareBenchmark(name="Ryzen 5 7600X", brand="AMD", category="cpu", form_factor="desktop", single_score=2050, multi_score=15000, base_clock_ghz=4.7, boost_clock_ghz=5.3, release_year=2022),
        HardwareBenchmark(name="Ryzen 5 7500F", brand="AMD", category="cpu", form_factor="desktop", single_score=1950, multi_score=14200, base_clock_ghz=3.7, boost_clock_ghz=5.0, release_year=2023),
        HardwareBenchmark(name="Ryzen 7 5800X3D", brand="AMD", category="cpu", form_factor="desktop", single_score=1680, multi_score=14500, base_clock_ghz=3.4, boost_clock_ghz=4.5, release_year=2022),
        HardwareBenchmark(name="Ryzen 7 5700X3D", brand="AMD", category="cpu", form_factor="desktop", single_score=1600, multi_score=13800, base_clock_ghz=3.0, boost_clock_ghz=4.1, release_year=2024),
        HardwareBenchmark(name="Ryzen 9 5950X", brand="AMD", category="cpu", form_factor="desktop", single_score=1700, multi_score=21000, base_clock_ghz=3.4, boost_clock_ghz=4.9, release_year=2020),
        HardwareBenchmark(name="Ryzen 9 5900X", brand="AMD", category="cpu", form_factor="desktop", single_score=1680, multi_score=18500, base_clock_ghz=3.7, boost_clock_ghz=4.8, release_year=2020),
        HardwareBenchmark(name="Ryzen 7 5800X", brand="AMD", category="cpu", form_factor="desktop", single_score=1640, multi_score=14800, base_clock_ghz=3.8, boost_clock_ghz=4.7, release_year=2020),
        HardwareBenchmark(name="Ryzen 7 5700X", brand="AMD", category="cpu", form_factor="desktop", single_score=1580, multi_score=13600, base_clock_ghz=3.4, boost_clock_ghz=4.6, release_year=2022),
        HardwareBenchmark(name="Ryzen 5 5600X", brand="AMD", category="cpu", form_factor="desktop", single_score=1600, multi_score=11800, base_clock_ghz=3.7, boost_clock_ghz=4.6, release_year=2020),
        HardwareBenchmark(name="Ryzen 5 5600", brand="AMD", category="cpu", form_factor="desktop", single_score=1550, multi_score=11400, base_clock_ghz=3.5, boost_clock_ghz=4.4, release_year=2022),
        HardwareBenchmark(name="Ryzen 5 5500", brand="AMD", category="cpu", form_factor="desktop", single_score=1420, multi_score=9800, base_clock_ghz=3.6, boost_clock_ghz=4.2, release_year=2022),
        HardwareBenchmark(name="Ryzen 3 3300X", brand="AMD", category="cpu", form_factor="desktop", single_score=1350, multi_score=7200, base_clock_ghz=3.8, boost_clock_ghz=4.3, release_year=2020),
        HardwareBenchmark(name="Ryzen 3 3100", brand="AMD", category="cpu", form_factor="desktop", single_score=1200, multi_score=6100, base_clock_ghz=3.6, boost_clock_ghz=3.9, release_year=2020),
        HardwareBenchmark(name="Ryzen 5 3600", brand="AMD", category="cpu", form_factor="desktop", single_score=1250, multi_score=9200, base_clock_ghz=3.6, boost_clock_ghz=4.2, release_year=2019),
        HardwareBenchmark(name="Ryzen 7 2700X", brand="AMD", category="cpu", form_factor="desktop", single_score=1050, multi_score=7500, base_clock_ghz=3.7, boost_clock_ghz=4.3, release_year=2018),
        HardwareBenchmark(name="Ryzen 5 2600", brand="AMD", category="cpu", form_factor="desktop", single_score=980, multi_score=5800, base_clock_ghz=3.4, boost_clock_ghz=3.9, release_year=2018),
        HardwareBenchmark(name="Ryzen 5 1600", brand="AMD", category="cpu", form_factor="desktop", single_score=850, multi_score=4600, base_clock_ghz=3.2, boost_clock_ghz=3.6, release_year=2017),
    ]

    # ==========================================
    # 2. GRAPHICS CARDS (GPUs)
    # ==========================================
    gpus = [
        # --- Integrated GPUs (Intel UHD / Iris Xe / AMD Radeon Vega / 600M / 700M) ---
        HardwareBenchmark(name="Intel UHD Graphics (Laptop)", brand="Intel", category="gpu", form_factor="laptop", single_score=1200, multi_score=1200, vram_gb=2, release_year=2020),
        HardwareBenchmark(name="Intel UHD Graphics 770", brand="Intel", category="gpu", form_factor="desktop", single_score=1850, multi_score=1850, vram_gb=2, release_year=2021),
        HardwareBenchmark(name="Intel UHD Graphics 730", brand="Intel", category="gpu", form_factor="desktop", single_score=1450, multi_score=1450, vram_gb=2, release_year=2021),
        HardwareBenchmark(name="Intel UHD Graphics 630", brand="Intel", category="gpu", form_factor="desktop", single_score=1150, multi_score=1150, vram_gb=2, release_year=2017),
        HardwareBenchmark(name="Intel UHD Graphics 600", brand="Intel", category="gpu", form_factor="laptop", single_score=650, multi_score=650, vram_gb=1, release_year=2017),
        HardwareBenchmark(name="Intel Iris Xe Graphics (96EU)", brand="Intel", category="gpu", form_factor="laptop", single_score=3200, multi_score=3200, vram_gb=4, release_year=2020),
        HardwareBenchmark(name="Intel Iris Xe Graphics (80EU)", brand="Intel", category="gpu", form_factor="laptop", single_score=2600, multi_score=2600, vram_gb=4, release_year=2020),
        HardwareBenchmark(name="Intel HD Graphics 620", brand="Intel", category="gpu", form_factor="laptop", single_score=950, multi_score=950, vram_gb=2, release_year=2016),
        HardwareBenchmark(name="Intel HD Graphics 520", brand="Intel", category="gpu", form_factor="laptop", single_score=850, multi_score=850, vram_gb=2, release_year=2015),

        HardwareBenchmark(name="AMD Radeon 780M (Laptop)", brand="AMD", category="gpu", form_factor="laptop", single_score=4800, multi_score=4800, vram_gb=4, release_year=2023),
        HardwareBenchmark(name="AMD Radeon 680M (Laptop)", brand="AMD", category="gpu", form_factor="laptop", single_score=3900, multi_score=3900, vram_gb=4, release_year=2022),
        HardwareBenchmark(name="AMD Radeon 660M (Laptop)", brand="AMD", category="gpu", form_factor="laptop", single_score=2400, multi_score=2400, vram_gb=2, release_year=2022),
        HardwareBenchmark(name="AMD Radeon 610M (Laptop)", brand="AMD", category="gpu", form_factor="laptop", single_score=1150, multi_score=1150, vram_gb=2, release_year=2022),
        HardwareBenchmark(name="AMD Radeon Graphics (Laptop)", brand="AMD", category="gpu", form_factor="laptop", single_score=1600, multi_score=1600, vram_gb=2, release_year=2020),
        HardwareBenchmark(name="AMD Radeon Vega 8 (Laptop)", brand="AMD", category="gpu", form_factor="laptop", single_score=2100, multi_score=2100, vram_gb=2, release_year=2019),
        HardwareBenchmark(name="AMD Radeon Vega 7 (Laptop)", brand="AMD", category="gpu", form_factor="laptop", single_score=1800, multi_score=1800, vram_gb=2, release_year=2020),
        HardwareBenchmark(name="AMD Radeon Vega 6 (Laptop)", brand="AMD", category="gpu", form_factor="laptop", single_score=1450, multi_score=1450, vram_gb=2, release_year=2020),
        HardwareBenchmark(name="AMD Radeon Vega 3 (Laptop)", brand="AMD", category="gpu", form_factor="laptop", single_score=980, multi_score=980, vram_gb=2, release_year=2019),

        # --- NVIDIA Entry / MX Series & Legacy GT Series ---
        HardwareBenchmark(name="GeForce MX550 (Laptop 30W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=3600, multi_score=3600, tgp_watts=30, vram_gb=2, release_year=2022),
        HardwareBenchmark(name="GeForce MX450 (Laptop 25W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=3200, multi_score=3200, tgp_watts=25, vram_gb=2, release_year=2020),
        HardwareBenchmark(name="GeForce MX350 (Laptop 25W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=2500, multi_score=2500, tgp_watts=25, vram_gb=2, release_year=2020),
        HardwareBenchmark(name="GeForce MX330 (Laptop 25W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=1800, multi_score=1800, tgp_watts=25, vram_gb=2, release_year=2020),
        HardwareBenchmark(name="GeForce MX250 (Laptop)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=1700, multi_score=1700, tgp_watts=25, vram_gb=2, release_year=2019),
        HardwareBenchmark(name="GeForce MX150 (Laptop)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=1600, multi_score=1600, tgp_watts=25, vram_gb=2, release_year=2017),
        HardwareBenchmark(name="GeForce MX130 (Laptop)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=1200, multi_score=1200, tgp_watts=25, vram_gb=2, release_year=2017),
        HardwareBenchmark(name="GeForce GT 1030 (2GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=1650, multi_score=1650, vram_gb=2, release_year=2017),
        HardwareBenchmark(name="GeForce GT 730 (2GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=750, multi_score=750, vram_gb=2, release_year=2014),
        HardwareBenchmark(name="GeForce GT 710 (2GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=500, multi_score=500, vram_gb=2, release_year=2016),

        # --- NVIDIA Desktop GTX Series (Legacy to Modern) ---
        HardwareBenchmark(name="GeForce GTX 750 Ti (2GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=2500, multi_score=2500, vram_gb=2, release_year=2014),
        HardwareBenchmark(name="GeForce GTX 960 (4GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=3900, multi_score=3900, vram_gb=4, release_year=2015),
        HardwareBenchmark(name="GeForce GTX 970 (4GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=6100, multi_score=6100, vram_gb=4, release_year=2014),
        HardwareBenchmark(name="GeForce GTX 980 Ti (6GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=8500, multi_score=8500, vram_gb=6, release_year=2015),
        HardwareBenchmark(name="GeForce GTX 1050 (2GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=3500, multi_score=3500, vram_gb=2, release_year=2016),
        HardwareBenchmark(name="GeForce GTX 1050 Ti (4GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=4400, multi_score=4400, vram_gb=4, release_year=2016),
        HardwareBenchmark(name="GeForce GTX 1060 (3GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=5900, multi_score=5900, vram_gb=3, release_year=2016),
        HardwareBenchmark(name="GeForce GTX 1060 (6GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=6800, multi_score=6800, vram_gb=6, release_year=2016),
        HardwareBenchmark(name="GeForce GTX 1070 (8GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=8600, multi_score=8600, vram_gb=8, release_year=2016),
        HardwareBenchmark(name="GeForce GTX 1070 Ti (8GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=9800, multi_score=9800, vram_gb=8, release_year=2017),
        HardwareBenchmark(name="GeForce GTX 1080 (8GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=10400, multi_score=10400, vram_gb=8, release_year=2016),
        HardwareBenchmark(name="GeForce GTX 1080 Ti (11GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=12800, multi_score=12800, vram_gb=11, release_year=2017),
        HardwareBenchmark(name="GeForce GTX 1650", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=3500, multi_score=3500, vram_gb=4, release_year=2019),
        HardwareBenchmark(name="GeForce GTX 1650 Super", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=4800, multi_score=4800, vram_gb=4, release_year=2019),
        HardwareBenchmark(name="GeForce GTX 1660", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=5500, multi_score=5500, vram_gb=6, release_year=2019),
        HardwareBenchmark(name="GeForce GTX 1660 Super", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=6000, multi_score=6000, vram_gb=6, release_year=2019),
        HardwareBenchmark(name="GeForce GTX 1660 Ti", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=6200, multi_score=6200, vram_gb=6, release_year=2019),

        # --- NVIDIA Desktop RTX Series ---
        HardwareBenchmark(name="GeForce RTX 2060 (6GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=7500, multi_score=7500, vram_gb=6, release_year=2019),
        HardwareBenchmark(name="GeForce RTX 2060 Super (8GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=8700, multi_score=8700, vram_gb=8, release_year=2019),
        HardwareBenchmark(name="GeForce RTX 2070 (8GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=9200, multi_score=9200, vram_gb=8, release_year=2018),
        HardwareBenchmark(name="GeForce RTX 2070 Super (8GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=10200, multi_score=10200, vram_gb=8, release_year=2019),
        HardwareBenchmark(name="GeForce RTX 2080 Super (8GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=11800, multi_score=11800, vram_gb=8, release_year=2019),
        HardwareBenchmark(name="GeForce RTX 2080 Ti (11GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=14200, multi_score=14200, vram_gb=11, release_year=2018),
        HardwareBenchmark(name="GeForce RTX 3050 (6GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=4900, multi_score=4900, vram_gb=6, release_year=2024),
        HardwareBenchmark(name="GeForce RTX 3050 (8GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=5800, multi_score=5800, vram_gb=8, release_year=2022),
        HardwareBenchmark(name="GeForce RTX 3060 (12GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=8800, multi_score=8800, vram_gb=12, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3060 Ti", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=11800, multi_score=11800, vram_gb=8, release_year=2020),
        HardwareBenchmark(name="GeForce RTX 3070", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=13600, multi_score=13600, vram_gb=8, release_year=2020),
        HardwareBenchmark(name="GeForce RTX 3070 Ti", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=14800, multi_score=14800, vram_gb=8, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3080 (10GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=17800, multi_score=17800, vram_gb=10, release_year=2020),
        HardwareBenchmark(name="GeForce RTX 3080 Ti", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=19200, multi_score=19200, vram_gb=12, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3090", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=19800, multi_score=19800, vram_gb=24, release_year=2020),
        HardwareBenchmark(name="GeForce RTX 3090 Ti", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=21800, multi_score=21800, vram_gb=24, release_year=2022),
        HardwareBenchmark(name="GeForce RTX 4060", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=10500, multi_score=10500, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4060 Ti (8GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=13500, multi_score=13500, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4060 Ti (16GB)", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=13600, multi_score=13600, vram_gb=16, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4070", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=17800, multi_score=17800, vram_gb=12, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4070 Super", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=21000, multi_score=21000, vram_gb=12, release_year=2024),
        HardwareBenchmark(name="GeForce RTX 4070 Ti", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=22800, multi_score=22800, vram_gb=12, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4070 Ti Super", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=24500, multi_score=24500, vram_gb=16, release_year=2024),
        HardwareBenchmark(name="GeForce RTX 4080", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=27500, multi_score=27500, vram_gb=16, release_year=2022),
        HardwareBenchmark(name="GeForce RTX 4080 Super", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=28500, multi_score=28500, vram_gb=16, release_year=2024),
        HardwareBenchmark(name="GeForce RTX 4090", brand="NVIDIA", category="gpu", form_factor="desktop", single_score=36000, multi_score=36000, vram_gb=24, release_year=2022),

        # --- NVIDIA Laptop GPUs (with specific TGP) ---
        HardwareBenchmark(name="GeForce GTX 1050 Laptop", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=3200, multi_score=3200, tgp_watts=50, vram_gb=4, release_year=2017),
        HardwareBenchmark(name="GeForce GTX 1050 Ti Laptop", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=4100, multi_score=4100, tgp_watts=55, vram_gb=4, release_year=2017),
        HardwareBenchmark(name="GeForce GTX 1060 Laptop (80W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=6200, multi_score=6200, tgp_watts=80, vram_gb=6, release_year=2016),
        HardwareBenchmark(name="GeForce GTX 1650 Laptop (50W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=3200, multi_score=3200, tgp_watts=50, vram_gb=4, release_year=2019),
        HardwareBenchmark(name="GeForce GTX 1650 Ti Laptop (55W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=3800, multi_score=3800, tgp_watts=55, vram_gb=4, release_year=2020),
        HardwareBenchmark(name="GeForce GTX 1660 Ti Laptop (80W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=5800, multi_score=5800, tgp_watts=80, vram_gb=6, release_year=2019),
        HardwareBenchmark(name="GeForce RTX 2060 Laptop (115W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=6900, multi_score=6900, tgp_watts=115, vram_gb=6, release_year=2019),
        HardwareBenchmark(name="GeForce RTX 2070 Laptop (115W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=8500, multi_score=8500, tgp_watts=115, vram_gb=8, release_year=2019),
        HardwareBenchmark(name="GeForce RTX 3050 Laptop (35W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=3600, multi_score=3600, tgp_watts=35, vram_gb=4, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3050 Laptop (60W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=4200, multi_score=4200, tgp_watts=60, vram_gb=4, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3050 Laptop (75W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=4800, multi_score=4800, tgp_watts=75, vram_gb=4, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3050 6GB Laptop (60W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=4600, multi_score=4600, tgp_watts=60, vram_gb=6, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 3050 6GB Laptop (95W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=5600, multi_score=5600, tgp_watts=95, vram_gb=6, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 3050 Ti Laptop (80W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=5400, multi_score=5400, tgp_watts=80, vram_gb=4, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3060 Laptop (80W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=7100, multi_score=7100, tgp_watts=80, vram_gb=6, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3060 Laptop (95W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=7800, multi_score=7800, tgp_watts=95, vram_gb=6, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3060 Laptop (130W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=8600, multi_score=8600, tgp_watts=130, vram_gb=6, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3060 Laptop (140W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=8900, multi_score=8900, tgp_watts=140, vram_gb=6, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3070 Laptop (100W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=9500, multi_score=9500, tgp_watts=100, vram_gb=8, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3070 Laptop (140W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=10800, multi_score=10800, tgp_watts=140, vram_gb=8, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3070 Ti Laptop (150W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=11800, multi_score=11800, tgp_watts=150, vram_gb=8, release_year=2022),
        HardwareBenchmark(name="GeForce RTX 3080 Laptop (165W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=13200, multi_score=13200, tgp_watts=165, vram_gb=16, release_year=2021),
        HardwareBenchmark(name="GeForce RTX 3080 Ti Laptop (175W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=14500, multi_score=14500, tgp_watts=175, vram_gb=16, release_year=2022),
        HardwareBenchmark(name="GeForce RTX 4050 Laptop (45W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=5900, multi_score=5900, tgp_watts=45, vram_gb=6, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4050 Laptop (95W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=8500, multi_score=8500, tgp_watts=95, vram_gb=6, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4050 Laptop (140W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=8800, multi_score=8800, tgp_watts=140, vram_gb=6, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4060 Laptop (45W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=7200, multi_score=7200, tgp_watts=45, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4060 Laptop (75W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=8900, multi_score=8900, tgp_watts=75, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4060 Laptop (105W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=9800, multi_score=9800, tgp_watts=105, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4060 Laptop (140W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=10400, multi_score=10400, tgp_watts=140, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4070 Laptop (60W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=9200, multi_score=9200, tgp_watts=60, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4070 Laptop (105W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=11400, multi_score=11400, tgp_watts=105, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4070 Laptop (140W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=12200, multi_score=12200, tgp_watts=140, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4080 Laptop (150W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=17200, multi_score=17200, tgp_watts=150, vram_gb=12, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4080 Laptop (175W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=18500, multi_score=18500, tgp_watts=175, vram_gb=12, release_year=2023),
        HardwareBenchmark(name="GeForce RTX 4090 Laptop (175W)", brand="NVIDIA", category="gpu", form_factor="laptop", single_score=21500, multi_score=21500, tgp_watts=175, vram_gb=16, release_year=2023),

        # --- AMD Desktop Radeon Series ---
        HardwareBenchmark(name="Radeon RX 550 (4GB)", brand="AMD", category="gpu", form_factor="desktop", single_score=1700, multi_score=1700, vram_gb=4, release_year=2017),
        HardwareBenchmark(name="Radeon RX 560 (4GB)", brand="AMD", category="gpu", form_factor="desktop", single_score=2600, multi_score=2600, vram_gb=4, release_year=2017),
        HardwareBenchmark(name="Radeon RX 570 (4GB)", brand="AMD", category="gpu", form_factor="desktop", single_score=4200, multi_score=4200, vram_gb=4, release_year=2017),
        HardwareBenchmark(name="Radeon RX 580 (8GB)", brand="AMD", category="gpu", form_factor="desktop", single_score=4900, multi_score=4900, vram_gb=8, release_year=2017),
        HardwareBenchmark(name="Radeon RX 590 (8GB)", brand="AMD", category="gpu", form_factor="desktop", single_score=5600, multi_score=5600, vram_gb=8, release_year=2018),
        HardwareBenchmark(name="Radeon RX 5500 XT (8GB)", brand="AMD", category="gpu", form_factor="desktop", single_score=5200, multi_score=5200, vram_gb=8, release_year=2019),
        HardwareBenchmark(name="Radeon RX 5600 XT (6GB)", brand="AMD", category="gpu", form_factor="desktop", single_score=7800, multi_score=7800, vram_gb=6, release_year=2020),
        HardwareBenchmark(name="Radeon RX 5700 XT (8GB)", brand="AMD", category="gpu", form_factor="desktop", single_score=9200, multi_score=9200, vram_gb=8, release_year=2019),
        HardwareBenchmark(name="Radeon RX 6500 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=4800, multi_score=4800, vram_gb=4, release_year=2022),
        HardwareBenchmark(name="Radeon RX 6600", brand="AMD", category="gpu", form_factor="desktop", single_score=8100, multi_score=8100, vram_gb=8, release_year=2021),
        HardwareBenchmark(name="Radeon RX 6600 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=9400, multi_score=9400, vram_gb=8, release_year=2021),
        HardwareBenchmark(name="Radeon RX 6650 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=9800, multi_score=9800, vram_gb=8, release_year=2022),
        HardwareBenchmark(name="Radeon RX 6700 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=12500, multi_score=12500, vram_gb=12, release_year=2021),
        HardwareBenchmark(name="Radeon RX 6750 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=13500, multi_score=13500, vram_gb=12, release_year=2022),
        HardwareBenchmark(name="Radeon RX 6800", brand="AMD", category="gpu", form_factor="desktop", single_score=15500, multi_score=15500, vram_gb=16, release_year=2020),
        HardwareBenchmark(name="Radeon RX 6800 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=18500, multi_score=18500, vram_gb=16, release_year=2020),
        HardwareBenchmark(name="Radeon RX 6900 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=20000, multi_score=20000, vram_gb=16, release_year=2020),
        HardwareBenchmark(name="Radeon RX 6950 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=21000, multi_score=21000, vram_gb=16, release_year=2022),
        HardwareBenchmark(name="Radeon RX 7600", brand="AMD", category="gpu", form_factor="desktop", single_score=10200, multi_score=10200, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="Radeon RX 7600 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=11500, multi_score=11500, vram_gb=16, release_year=2024),
        HardwareBenchmark(name="Radeon RX 7700 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=16800, multi_score=16800, vram_gb=12, release_year=2023),
        HardwareBenchmark(name="Radeon RX 7800 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=19200, multi_score=19200, vram_gb=16, release_year=2023),
        HardwareBenchmark(name="Radeon RX 7900 GRE", brand="AMD", category="gpu", form_factor="desktop", single_score=21500, multi_score=21500, vram_gb=16, release_year=2023),
        HardwareBenchmark(name="Radeon RX 7900 XT", brand="AMD", category="gpu", form_factor="desktop", single_score=25500, multi_score=25500, vram_gb=20, release_year=2022),
        HardwareBenchmark(name="Radeon RX 7900 XTX", brand="AMD", category="gpu", form_factor="desktop", single_score=29000, multi_score=29000, vram_gb=24, release_year=2022),

        # --- AMD Laptop GPUs ---
        HardwareBenchmark(name="Radeon RX 6600M (100W)", brand="AMD", category="gpu", form_factor="laptop", single_score=7600, multi_score=7600, tgp_watts=100, vram_gb=8, release_year=2021),
        HardwareBenchmark(name="Radeon RX 6700M (135W)", brand="AMD", category="gpu", form_factor="laptop", single_score=9400, multi_score=9400, tgp_watts=135, vram_gb=10, release_year=2021),
        HardwareBenchmark(name="Radeon RX 6800M (145W)", brand="AMD", category="gpu", form_factor="laptop", single_score=11200, multi_score=11200, tgp_watts=145, vram_gb=12, release_year=2021),
        HardwareBenchmark(name="Radeon RX 7600S (75W)", brand="AMD", category="gpu", form_factor="laptop", single_score=7800, multi_score=7800, tgp_watts=75, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="Radeon RX 7600M XT (120W)", brand="AMD", category="gpu", form_factor="laptop", single_score=9200, multi_score=9200, tgp_watts=120, vram_gb=8, release_year=2023),

        # --- Intel Arc GPUs ---
        HardwareBenchmark(name="Intel Arc A380 (6GB)", brand="Intel", category="gpu", form_factor="desktop", single_score=4200, multi_score=4200, vram_gb=6, release_year=2022),
        HardwareBenchmark(name="Intel Arc A580 (8GB)", brand="Intel", category="gpu", form_factor="desktop", single_score=9100, multi_score=9100, vram_gb=8, release_year=2023),
        HardwareBenchmark(name="Intel Arc A750 (8GB)", brand="Intel", category="gpu", form_factor="desktop", single_score=11000, multi_score=11000, vram_gb=8, release_year=2022),
        HardwareBenchmark(name="Intel Arc A770 (16GB)", brand="Intel", category="gpu", form_factor="desktop", single_score=12400, multi_score=12400, vram_gb=16, release_year=2022),
    ]

    # ==========================================
    # 3. GAMES CATALOG
    # ==========================================
    games = [
        Game(title="Cyberpunk 2077", genre="AAA Action", engine="REDengine 4", cpu_weight=0.25, gpu_weight=0.75, ram_min_gb=12, ram_rec_gb=16, base_fps_1080p_ultra=62.0),
        Game(title="Black Myth: Wukong", genre="AAA Action", engine="Unreal Engine 5", cpu_weight=0.20, gpu_weight=0.80, ram_min_gb=16, ram_rec_gb=32, base_fps_1080p_ultra=55.0),
        Game(title="Valorant", genre="eSports", engine="Unreal Engine 4", cpu_weight=0.55, gpu_weight=0.45, ram_min_gb=4, ram_rec_gb=8, base_fps_1080p_ultra=280.0),
        Game(title="Counter-Strike 2", genre="eSports", engine="Source 2", cpu_weight=0.45, gpu_weight=0.55, ram_min_gb=8, ram_rec_gb=16, base_fps_1080p_ultra=185.0),
        Game(title="Grand Theft Auto V", genre="Open World", engine="RAGE", cpu_weight=0.35, gpu_weight=0.65, ram_min_gb=8, ram_rec_gb=16, base_fps_1080p_ultra=115.0),
        Game(title="Red Dead Redemption 2", genre="Open World", engine="RAGE", cpu_weight=0.25, gpu_weight=0.75, ram_min_gb=8, ram_rec_gb=16, base_fps_1080p_ultra=68.0),
        Game(title="Elden Ring", genre="RPG / Action", engine="FromSoftware Engine", cpu_weight=0.30, gpu_weight=0.70, ram_min_gb=12, ram_rec_gb=16, base_fps_1080p_ultra=60.0),
        Game(title="Forza Horizon 5", genre="Racing / Simulation", engine="ForzaTech", cpu_weight=0.30, gpu_weight=0.70, ram_min_gb=8, ram_rec_gb=16, base_fps_1080p_ultra=95.0),
        Game(title="Dota 2", genre="eSports", engine="Source 2", cpu_weight=0.50, gpu_weight=0.50, ram_min_gb=4, ram_rec_gb=8, base_fps_1080p_ultra=160.0),
        Game(title="Hogwarts Legacy", genre="RPG / Open World", engine="Unreal Engine 4", cpu_weight=0.30, gpu_weight=0.70, ram_min_gb=16, ram_rec_gb=16, base_fps_1080p_ultra=58.0),
        Game(title="Microsoft Flight Simulator 2024", genre="Simulation", engine="Asobo Engine", cpu_weight=0.45, gpu_weight=0.55, ram_min_gb=16, ram_rec_gb=32, base_fps_1080p_ultra=45.0),
    ]

    # ==========================================
    # 4. PRESETS
    # ==========================================
    presets = [
        PresetMultiplier(resolution="1080p", preset="Low", res_gpu_scale=1.0, res_cpu_scale=1.0, preset_scale=0.65),
        PresetMultiplier(resolution="1080p", preset="Medium", res_gpu_scale=1.0, res_cpu_scale=1.0, preset_scale=0.80),
        PresetMultiplier(resolution="1080p", preset="High", res_gpu_scale=1.0, res_cpu_scale=1.0, preset_scale=0.92),
        PresetMultiplier(resolution="1080p", preset="Ultra", res_gpu_scale=1.0, res_cpu_scale=1.0, preset_scale=1.00),
        PresetMultiplier(resolution="1440p", preset="Ultra", res_gpu_scale=1.45, res_cpu_scale=0.92, preset_scale=1.00),
        PresetMultiplier(resolution="4K", preset="Ultra", res_gpu_scale=2.25, res_cpu_scale=0.85, preset_scale=1.00),
    ]

    db.add_all(cpus)
    db.add_all(gpus)
    db.add_all(games)
    db.add_all(presets)
    db.commit()
    count_cpus = db.query(HardwareBenchmark).filter(HardwareBenchmark.category == "cpu").count()
    count_gpus = db.query(HardwareBenchmark).filter(HardwareBenchmark.category == "gpu").count()
    db.close()
    print(f"Database seeded: {count_cpus} CPUs, {count_gpus} GPUs, {len(games)} Games.")

if __name__ == "__main__":
    seed_database(force_refresh=True)
