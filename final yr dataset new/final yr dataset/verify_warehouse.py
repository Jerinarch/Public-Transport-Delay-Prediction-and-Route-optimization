import os
import sqlite3
import pandas as pd

DIR_PATH = r"c:\Users\pregi\OneDrive\Desktop\final yr dataset"

files = [
    "dataset_01_bus_schedule_gtfs.csv",
    "dataset_02_bus_gps_realtime.csv",
    "dataset_03_actual_bus_arrivals.csv",
    "dataset_04_bus_occupancy.csv",
    "dataset_05_bengaluru_traffic.csv",
    "dataset_06_historical_weather.csv",
    "dataset_07_events_incidents.csv",
    "dataset_08_holiday_calendar.csv",
    "dataset_09_bus_master.csv",
    "dataset_10_bus_stop_master.csv",
    "dataset_11_user_feedback.csv",
    "dataset_12_osm_road_network.csv",
    "dataset_13_controller_admin.csv",
    "ml_delay_prediction_dataset.csv",
    "ml_occupancy_prediction_dataset.csv",
    "ml_disruption_detection_dataset.csv",
    "final_integrated_dataset.csv",
    "final_integrated_dataset.parquet",
    "bmtc_data_warehouse.db"
]

print("=== BMTC DATAWAREHOUSE & INTEGRATED DATASET INTEGRITY CHECK ===")

for f in files:
    full_path = os.path.join(DIR_PATH, f)
    if os.path.exists(full_path):
        size_kb = round(os.path.getsize(full_path) / 1024, 1)
        if f.endswith(".csv"):
            df = pd.read_csv(full_path)
            print(f"[OK] {f:38s} | Size: {size_kb:7.1f} KB | Rows: {len(df):6d} | Cols: {len(df.columns):2d}")
        elif f.endswith(".parquet"):
            df = pd.read_parquet(full_path)
            print(f"[OK] {f:38s} | Size: {size_kb:7.1f} KB | Rows: {len(df):6d} | Cols: {len(df.columns):2d}")
        elif f.endswith(".db"):
            conn = sqlite3.connect(full_path)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view');")
            tables = [row[0] for row in cur.fetchall()]
            conn.close()
            print(f"[OK] {f:38s} | Size: {size_kb:7.1f} KB | Tables/Views: {len(tables)} -> {', '.join(tables)}")
    else:
        print(f"[MISSING] {f}")

print("\nVerification Complete.")
