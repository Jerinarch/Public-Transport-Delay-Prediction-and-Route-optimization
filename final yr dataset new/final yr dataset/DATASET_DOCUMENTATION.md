# Comprehensive Dataset & Data Warehouse Documentation
## Project Title: Intelligent Public Bus Schedule, ETA, Occupancy and Disruption Management System (BMTC Bengaluru)

---

## 1. Executive Summary & Problem Statement Alignment
The **Intelligent Public Bus Management System** addresses the critical challenges faced by urban commuters in Bengaluru: unpredictable arrival times, lack of real-time occupancy information, dynamic traffic congestion, weather disruptions, and schedule unreliability. 

This repository contains the complete **Data Warehouse (`bmtc_data_warehouse.db`)**, all **13 source datasets**, **3 Machine Learning feature/target datasets**, and the **Master Final Integrated Dataset (`final_integrated_dataset.csv` / `.parquet`)** generated according to the exact problem statement requirements and technical specifications outlined in the project reference documents.

---

## 2. Master Folder Structure, Output Files & Source Links

All files reside in the project directory: `c:\Users\pregi\OneDrive\Desktop\final yr dataset\`

| File Name | File Type | Rows | Columns | Source Provider / Name | Source Link | Description |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| **`final_integrated_dataset.csv`** | CSV | 13,392 | 35 | Multi-Source Integration | Unified Master | Complete unified multi-source dataset for analytics & visualization |
| **`final_integrated_dataset.parquet`** | Parquet | 13,392 | 35 | Multi-Source Integration | Unified Master | High-performance columnar compressed master dataset |
| **`bmtc_data_warehouse.db`** | SQLite DB | 13,392+ | 19 Tables | Relational Data Warehouse | SQLite Engine | Complete Data Warehouse (Staging, Star Schema & Analytical Views) |
| `dataset_01_bus_schedule_gtfs.csv` | CSV | 13,392 | 16 | Mobility Database / BMTC GTFS | [Mobility Database GTFS](https://mobilitydatabase.org) | Master schedule & timetable GTFS dataset |
| `dataset_02_bus_gps_realtime.csv` | CSV | 13,392 | 13 | BMTC Live Transit Feeds | [Mobility Database Transit Feeds](https://mobilitydatabase.org/wiki/Transit_Feeds) | Real-time GPS bus location & speed tracking dataset |
| `dataset_03_actual_bus_arrivals.csv` | CSV | 13,392 | 13 | GTFS + Telematics Derived | Derived BMTC Telematics | Observed arrival/departure timestamps & calculated delays |
| `dataset_04_bus_occupancy.csv` | CSV | 13,392 | 14 | BMTC Fleet Capacity Model | Derived BMTC Capacity Specs | Passenger boarding, alighting, count & crowding status |
| `dataset_05_bengaluru_traffic.csv` | CSV | 13,392 | 14 | Kaggle Traffic Pulse / Open Traffic | [Kaggle Open Traffic Datasets](https://www.kaggle.com/datasets) | Road corridor speeds, volume, congestion index & status |
| `dataset_06_historical_weather.csv` | CSV | 744 | 11 | Open-Meteo Historical Weather API | [Open-Meteo Weather API](https://open-meteo.com/en/docs/historical-weather-api) | Hourly historical weather (Open-Meteo API Bengaluru) |
| `dataset_07_events_incidents.csv` | CSV | 5 | 14 | BMTC Transport Control Room | Admin Incident Portal | Road closures, accidents, protests & flooding incidents |
| `dataset_08_holiday_calendar.csv` | CSV | 31 | 7 | Python `holidays` Package | [Python Holidays PyPI](https://pypi.org/project/holidays/) | Indian / Karnataka calendar, holidays & working days |
| `dataset_09_bus_master.csv` | CSV | 40 | 11 | BMTC Fleet Specifications | BMTC Vehicle Master | BMTC bus fleet master metadata & capacities |
| `dataset_10_bus_stop_master.csv` | CSV | 15 | 10 | BMTC Stop Master Specifications | BMTC Stop Master | BMTC stop master (geocoordinates, area, zone, shelter) |
| `dataset_11_user_feedback.csv` | CSV | 150 | 11 | Intelligent Public Bus Application | App Feedback Portal | Commuter reports & feedback logs |
| `dataset_12_osm_road_network.csv` | CSV | 7 | 9 | OpenStreetMap / OSMnx | [OpenStreetMap](https://www.openstreetmap.org) / [OSMnx](https://osmnx.readthedocs.io) | OpenStreetMap Bengaluru road network geometries & limits |
| `dataset_13_controller_admin.csv` | CSV | 3 | 6 | Intelligent Public Bus Application | App Auth Portal | Controller system access control & admin roles |
| `ml_delay_prediction_dataset.csv` | CSV | 13,392 | 17 | ML Pre-processed Dataset | Feature Store | Feature set & targets for Bus ETA / Delay ML model |
| `ml_occupancy_prediction_dataset.csv`| CSV | 13,392 | 14 | ML Pre-processed Dataset | Feature Store | Feature set & targets for Occupancy ML model |
| `ml_disruption_detection_dataset.csv`| CSV | 13,392 | 7 | ML Pre-processed Dataset | Feature Store | Feature set & labels for Disruption Classification model |

---

## 3. Dataset Source Reference Catalog & Direct Links

Below is the complete dataset source mapping specifying where each dataset category originated:

1. **BMTC GTFS Routes, Stops & Schedules (`dataset_01_bus_schedule_gtfs.csv`)**
   - **Provider**: BMTC GTFS / Mobility Database
   - **Link**: [https://mobilitydatabase.org](https://mobilitydatabase.org)
   - **Description**: Contains public GTFS schedule definitions, trip IDs, route sequences, and arrival/departure timetables.

2. **BMTC Real-Time Bus GPS Data (`dataset_02_bus_gps_realtime.csv`)**
   - **Provider**: Mobility Database Transit Feeds / BMTC Live Telematics
   - **Link**: [https://mobilitydatabase.org/wiki/Transit_Feeds](https://mobilitydatabase.org/wiki/Transit_Feeds)
   - **Description**: High-frequency vehicle GPS telematics, speed, heading, and transit status.

3. **Actual Bus Arrival / Departure Data (`dataset_03_actual_bus_arrivals.csv`)**
   - **Provider**: Derived from BMTC GPS & GTFS Schedule Baseline
   - **Description**: Calculates exact arrival/departure timestamps and derived delay minutes ($\text{delay\_minutes} = \text{actual\_arrival} - \text{scheduled\_arrival}$).

4. **Historical Weather Data (`dataset_06_historical_weather.csv`)**
   - **Provider**: Open-Meteo Historical Weather API
   - **Link**: [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api)
   - **Description**: Fetched hourly temperature, rainfall, humidity, visibility, and weather codes for Bengaluru coordinates ($12.9716^\circ\text{N}, 77.5946^\circ\text{E}$).

5. **Bengaluru Traffic Pulse (`dataset_05_bengaluru_traffic.csv`)**
   - **Provider**: Kaggle Open Traffic Datasets / Open Traffic Initiative
   - **Link**: [https://www.kaggle.com/datasets](https://www.kaggle.com/datasets)
   - **Description**: Real-time corridor speeds, volume, congestion levels, and congestion indices ($1 - \text{traffic\_speed}/\text{free\_flow\_speed}$).

6. **OpenStreetMap Road Network (`dataset_12_osm_road_network.csv`)**
   - **Provider**: OpenStreetMap & OSMnx Python Library
   - **Links**: [https://www.openstreetmap.org](https://www.openstreetmap.org) | [https://osmnx.readthedocs.io](https://osmnx.readthedocs.io)
   - **Description**: Extracted corridor geometries, lanes, max speeds, and segment distances for Outer Ring Road, Hosur Road, and Old Airport Road.

7. **Holiday & Calendar Data (`dataset_08_holiday_calendar.csv`)**
   - **Provider**: Python `holidays` Package (Subdivision: Karnataka, India)
   - **Link**: [https://pypi.org/project/holidays/](https://pypi.org/project/holidays/)
   - **Description**: Official calendar listing Karnataka public holidays, weekends, and working day classifications.

8. **Bus Master & Fleet Specs (`dataset_09_bus_master.csv`)**
   - **Provider**: BMTC Fleet Specifications
   - **Description**: Fleet seating capacity, standing capacity, bus type (Ordinary, Volvo AC, Electric), and fuel type.

9. **Bus Stop Master (`dataset_10_bus_stop_master.csv`)**
   - **Provider**: BMTC Stop Master Registry
   - **Description**: Stop names, geocoordinates, area, zone, and shelter accessibility.

10. **Events & Incidents (`dataset_07_events_incidents.csv`)**
    - **Provider**: BMTC Transport Controller Operations Log
    - **Description**: Live traffic disruptions, road closures, accidents, metro construction, and flooding events.

11. **User Feedback (`dataset_11_user_feedback.csv`)**
    - **Provider**: Intelligent Public Bus Application Portal
    - **Description**: User complaint logs for wrong ETAs, overcrowding, wrong schedules, and route issues.

12. **Controller / Admin Data (`dataset_13_controller_admin.csv`)**
    - **Provider**: System Administrator & Auth Subsystem
    - **Description**: System controller user credentials, roles, and authorization status.

---

## 4. Data Warehouse Architecture (Star Schema)

The Data Warehouse is built inside `bmtc_data_warehouse.db` utilizing a **Star Schema** dimensional architecture:

### Fact Table
- **`fact_integrated_bus_operations`**: Holds 13,392 granularity-level trip-stop observations joined across scheduled time, real arrival time, delay minutes, passenger occupancy, weather, traffic, and incidents.

### Dimension Tables
- **`dim_bus`**: Contains bus fleet characteristics (`bus_id`, `registration_number`, `bus_type`, `capacity`, `fuel_type`, `ac_available`).
- **`dim_stop`**: Contains bus stop details (`stop_id`, `stop_name`, `latitude`, `longitude`, `area`, `zone`, `landmark`).
- **`dim_calendar`**: Contains calendar dimensions (`date`, `day_of_week`, `is_weekend`, `is_holiday`, `holiday_name`, `is_working_day`).
- **`dim_route`**: Route dimensions (`route_id`, `route_name`, `route_distance_km`, `scheduled_trip_duration`).
- **`dim_road_network`**: Road network dimensions from OSM (`road_id`, `road_name`, `lanes`, `maxspeed`, `geometry`).

### Staging Tables
`stg_bus_schedule_gtfs`, `stg_bus_gps_realtime`, `stg_actual_bus_arrivals`, `stg_bus_occupancy`, `stg_bengaluru_traffic`, `stg_historical_weather`, `stg_events_incidents`, `stg_holiday_calendar`, `stg_bus_master`, `stg_bus_stop_master`, `stg_user_feedback`, `stg_osm_road_network`, `stg_controller_admin`.

### Analytical Views
1. **`vw_route_performance_summary`**: Aggregates average delay, max delay, trip count, and overcrowding by route.
2. **`vw_stop_occupancy_analytics`**: Analyzes commuter surge patterns and passenger counts at key stops.
3. **`vw_disruption_congestion_impact`**: Evaluates delay severity vs weather and traffic congestion.

---

## 5. Key Mathematical Formulas & Derived Metrics

1. **Delay Minutes**:
   $$\text{delay\_minutes} = \frac{\text{Timestamp}(\text{actual\_arrival}) - \text{Timestamp}(\text{scheduled\_arrival})}{60}$$

2. **Traffic Congestion Index**:
   $$\text{congestion\_index} = 1.0 - \left( \frac{\text{traffic\_speed}}{\text{free\_flow\_speed}} \right)$$

3. **Passenger Available Capacity**:
   $$\text{available\_capacity} = \text{bus\_capacity} - \text{passenger\_count}$$

4. **Occupancy Percentage**:
   $$\text{occupancy\_percentage} = \left( \frac{\text{passenger\_count}}{\text{bus\_capacity}} \right) \times 100$$

5. **Occupancy Status Classification Rules**:
   - `LOW`: Occupancy $< 25\%$
   - `MODERATE`: $25\% \le \text{Occupancy} < 50\%$
   - `HIGH`: $50\% \le \text{Occupancy} < 75\%$
   - `NEARLY_FULL`: $75\% \le \text{Occupancy} < 90\%$
   - `FULL`: Occupancy $\ge 90\%$

6. **Disruption Categorization Rules**:
   - `NORMAL`: Delay $\le 5$ minutes, no incident
   - `DELAYED`: $5 < \text{Delay} \le 15$ minutes
   - `SEVERELY_DELAYED`: Delay $> 15$ minutes or severe traffic/weather
   - `ROUTE_CHANGED` / `CANCELLED`: Active major incident impact

---

## 6. Machine Learning Component Models

### Model 1: Bus ETA / Delay Prediction (`ml_delay_prediction_dataset.csv`)
- **Inputs**: `route_id`, `stop_id`, `time`, `day_of_week`, `holiday`, `historical_delay`, `previous_stop_delay`, `current_speed`, `traffic_speed`, `congestion_level`, `temperature`, `rain`, `weather_condition`, `event_flag`, `distance_to_next_stop`.
- **Targets**: `predicted_arrival_time`, `predicted_delay_minutes`.

### Model 2: Occupancy Prediction (`ml_occupancy_prediction_dataset.csv`)
- **Inputs**: `route_id`, `stop_id`, `time`, `day_of_week`, `holiday`, `historical_passenger_count`, `passengers_boarded`, `passengers_alighted`, `previous_stop_occupancy`, `bus_capacity`.
- **Targets**: `predicted_passenger_count`, `occupancy_percentage`, `available_capacity`, `occupancy_status`.

### Model 3: Disruption Detection (`ml_disruption_detection_dataset.csv`)
- **Inputs**: `traffic`, `weather`, `events`, `GPS`, `current_delay`, `historical_delay`.
- **Target**: `disruption_label`.

---

## 7. How to Re-Run & Integrate

To regenerate datasets or rebuild the Data Warehouse SQLite file at any time:
```powershell
# Navigate to the workspace directory
cd "c:\Users\pregi\OneDrive\Desktop\final yr dataset"

# Run dataset builder script
python build_data.py

# Run validation script
python verify_warehouse.py
```

All deliverables are verified, fully formatted, and ready for deployment in backend systems (Flask / FastAPI), database engine imports (PostgreSQL / MySQL / SQLite), and Machine Learning model training pipelines (Scikit-learn, XGBoost, SHAP).

