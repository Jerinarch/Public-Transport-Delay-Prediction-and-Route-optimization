# BMTC INTELLIGENT PUBLIC BUS MANAGEMENT SYSTEM
## SYSTEM ARCHITECTURE, DATAWAREHOUSE OPERATIONAL GUIDE & RECOMMENDATIONS

---

## 1. DATASET USAGE RECOMMENDATIONS: MERGED VS. SEPARATE DATASETS

For an engineering & academic project, a **Hybrid Integration Strategy** is strongly recommended:

### Table 1: Recommended Dataset Format Mapping per System Component

| System Component & Module | Recommended Dataset Format | Technical & Operational Rationale |
| :--- | :--- | :--- |
| **Machine Learning Models** *(ETA Prediction, Occupancy, Disruption Classifier)* | **Merged Master Dataset** (`final_integrated_dataset.csv` / `final_integrated_dataset.parquet`) | Machine Learning algorithms (XGBoost, Random Forest, Scikit-learn, PyTorch) require a single flattened tabular row per sample where **all features** (Weather + Traffic + Schedule + GPS + Delay) are pre-joined. |
| **Web App Backend APIs** *(FastAPI / Flask / Node.js)* | **Database Data Warehouse** (`bmtc_data_warehouse.db`) | Relational databases store separate normalized tables (`dim_bus`, `dim_stop`, `dim_route`). Updating a bus specification updates 1 record in `dim_bus` without altering thousands of duplicated CSV rows. |
| **Passenger Front-End Dashboard** | **Analytical SQL Views** (`vw_stop_occupancy_analytics`) | Pre-computed SQL views execute queries instantly without requiring heavy client-side joins. |

---

## 2. REAL-TIME DATASET FORMATS & FEASIBILITY ANALYSIS

### Real-World Industry Standard:
- In production systems (BMTC, Uber, Transport for London), real-time bus locations arrive as live streaming JSON payloads over **WebSockets** or **MQTT** every 5–10 seconds:
```json
{
  "bus_id": "BUS_007",
  "route_id": "R_500D",
  "latitude": 12.9562,
  "longitude": 77.7019,
  "speed_kmph": 19.6,
  "timestamp": "2024-07-01 06:46:50"
}
```
- Public transit authorities also publish real-time feeds using **GTFS-Realtime (GTFS-RT)** Protobuf binary streams.

### Project Evaluation Usage:
- **Using CSV / Parquet for your project is 100% Valid & Industry-Standard for Offline Analysis.**
- In academic evaluation, real-time streams are represented as **historical time-series logs** (`dataset_02_bus_gps_realtime.csv`).
- In Python / FastAPI, you can simulate a live stream by iterating through `dataset_02_bus_gps_realtime.csv` row-by-row on a timer loop.

---

## 3. HOW THE DATA WAREHOUSE (`bmtc_data_warehouse.db`) WORKS

The Data Warehouse functions as the central analytical engine connecting all data streams:

```
+-----------------------------------------------------------------------+
|                       1. INGESTION LAYER                              |
|  GTFS Schedule | Real-Time GPS | Weather API | Traffic | Incident Logs |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|             2. DATA WAREHOUSE (bmtc_data_warehouse.db)                |
|  - Staging Layer (stg_bus_schedule, stg_bus_gps, stg_weather, etc.)   |
|  - ETL Transformation Engine (Calculates delay_minutes & congestion)  |
|  - Star Schema Fact Table (fact_integrated_bus_operations)            |
|  - Dimension Tables (dim_bus, dim_stop, dim_calendar, dim_route)      |
|  - Analytical Views (vw_route_performance, vw_stop_occupancy)         |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                    3. APPLICATION SERVING LAYER                       |
|  - Machine Learning Models (Delay & Occupancy Prediction)             |
|  - Passenger Web Portal (Upcoming ETAs, Delays, Occupancy Gauge)      |
|  - Transport Controller Dashboard (Monitoring, Alerts & Incidents)    |
+-----------------------------------------------------------------------+
```

---

## 4. TOP RECOMMENDATIONS & PROJECT IMPROVEMENTS

1. **Machine Learning Explainability with SHAP (Section 10 Requirement)**:
   - Provide passengers and controllers with the reason behind predicted delays:
     - *Predicted Delay*: **+14 minutes**
     - *Factors*: Heavy Traffic (+7 min), Rain (+4 min), Previous Stop Delay (+2 min), Peak Hour (+1 min).

2. **Interactive Live Bus Tracking Map (Leaflet.js / OpenStreetMap)**:
   - Render bus positions using `dataset_10_bus_stop_master.csv` and `dataset_12_osm_road_network.csv` with color coding (Green = On Time, Yellow = Delayed, Red = Severely Delayed).

3. **Commuter Crowding Indicator (Occupancy Gauge)**:
   - Visual progress bar showing live bus capacity (e.g. 45% LOW, 72% HIGH, 91% NEARLY FULL).

4. **Automated Incident & Service Disruption Alerts**:
   - Push notification banners whenever `disruption_label != 'NORMAL'` (e.g., *"Route 500D diverted due to road closure near Marathahalli"*).

5. **FastAPI REST API Backend**:
   - Serve clean endpoints to the front-end interface:
     - `GET /api/v1/stops/{stop_id}/upcoming-buses`
     - `GET /api/v1/routes/{route_id}/delays`
     - `POST /api/v1/admin/incidents`
