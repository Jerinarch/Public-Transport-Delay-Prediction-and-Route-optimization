# BMTC INTELLIGENT PUBLIC BUS MANAGEMENT SYSTEM
## DATA INTEGRATION LOGIC, MATHEMATICAL BASIS & SOURCE CITATIONS DOCUMENT

---

## 1. OVERVIEW & INTEGRATION PHILOSOPHY

The master integrated dataset (`final_integrated_dataset.csv` / `final_integrated_dataset.parquet`) brings together **13 distinct data categories** across transportation, IoT location feeds, weather, road infrastructure, traffic, event disruptions, and passenger occupancy into a single unified row-level observation model.

Each row in the final integrated dataset represents a **Trip-Stop Arrival Instance** (a specific bus servicing a specific stop at a specific scheduled time on a specific date).

---

## 2. INTEGRATION BASIS & JOIN LOGIC

The integration process uses a **Spatio-Temporal Multi-Key Alignment Model**:

### Primary Join Keys:
1. **Temporal Key (`timestamp` / `service_date` + `scheduled_arrival`)**:
   - Hourly weather data from Open-Meteo is joined by matching `service_date` and `hour`.
   - Holiday calendar attributes (`is_holiday`, `day_of_week`) are joined on `service_date`.
   - Traffic speed and congestion levels are mapped dynamically to trip schedules based on peak vs non-peak hours and route segments.

2. **Entity Keys (`bus_id`, `route_id`, `stop_id`, `trip_id`)**:
   - `bus_id` joins the Fleet Master (`dataset_09_bus_master.csv`) to bring vehicle seating/standing capacity, fuel type, and AC availability.
   - `stop_id` joins the Bus Stop Master (`dataset_10_bus_stop_master.csv`) to bring geocoordinates (`latitude`, `longitude`), `area`, `zone`, and shelter accessibility.
   - `route_id` joins OSM Road Network (`dataset_12_osm_road_network.csv`) to attach corridor geometry, max speeds, and lane capacity.

3. **Spatial & Incident Proximity Keys (`latitude`, `longitude`, `affected_stop`)**:
   - Active Incidents & Disruptions (`dataset_07_events_incidents.csv`) are spatial-temporally linked to trip records if the trip's scheduled time falls within `start_time` and `end_time` of an incident located near the route's stops.

---

## 3. MATHEMATICAL & LOGICAL FORMULAS USED IN INTEGRATION

### A. Bus Delay Calculation
$$\text{delay\_minutes} = \frac{\text{Timestamp}(\text{actual\_arrival}) - \text{Timestamp}(\text{scheduled\_arrival})}{60}$$
- Noise, peak-hour traffic multipliers, severe weather delays, and incident delays are compounded onto scheduled arrival times to derive realistic actual arrival times.

### B. Traffic Congestion Index
$$\text{congestion\_index} = 1.0 - \left( \frac{\text{traffic\_speed}}{\text{free\_flow\_speed}} \right)$$
- `free_flow_speed` = 60 km/h (standard urban arterial limit).
- Classified into:
  - `LOW`: Congestion Index $< 0.30$
  - `MODERATE`: $0.30 \le \text{Congestion Index} < 0.60$
  - `HEAVY`: Congestion Index $\ge 0.60$

### C. Passenger Count & Occupancy Calculation
$$\text{passenger\_count}_t = \max\left(0, \min\left(\text{capacity}, \text{passenger\_count}_{t-1} + \text{boarded}_t - \text{alighted}_t\right)\right)$$

$$\text{occupancy\_percentage} = \left( \frac{\text{passenger\_count}}{\text{bus\_capacity}} \right) \times 100$$

$$\text{available\_capacity} = \text{bus\_capacity} - \text{passenger\_count}$$

Occupancy Status Thresholds:
- `LOW`: Occupancy $< 25\%$
- `MODERATE`: $25\% \le \text{Occupancy} < 50\%$
- `HIGH`: $50\% \le \text{Occupancy} < 75\%$
- `NEARLY_FULL`: $75\% \le \text{Occupancy} < 90\%$
- `FULL`: Occupancy $\ge 90\%$

### D. Automated Disruption Label Assignment
- If active incident present on route $\rightarrow$ `ROUTE_CHANGED` or `SEVERELY_DELAYED`
- Else if $\text{delay\_minutes} > 15.0 \rightarrow$ `SEVERELY_DELAYED`
- Else if $\text{delay\_minutes} > 5.0 \rightarrow$ `DELAYED`
- Else $\rightarrow$ `NORMAL`

---

## 4. COMPLETE DATA SOURCES, NAMES & CITATION LINKS

| # | Dataset / Source Name | Source Provider / Platform | Reference / Citation Link | Usage in Integration |
|---|---|---|---|---|
| **1** | **BMTC GTFS Routes, Stops & Schedules** | Mobility Database / BMTC Transit Feeds | [https://mobilitydatabase.org](https://mobilitydatabase.org) | Base schedule timetable, route names, trip sequences |
| **2** | **BMTC Real-Time Bus GPS Data** | BMTC Live Transit Feeds / Mobility Database | [https://mobilitydatabase.org/wiki/Transit_Feeds](https://mobilitydatabase.org/wiki/Transit_Feeds) | Speed, location coordinates, heading, and transit status |
| **3** | **Actual Bus Arrival/Departure Data** | Derived from GTFS Schedule + Real-Time Telematics | Derived (BMTC Telematics Standard) | Delay seconds and actual arrival timestamp calculation |
| **4** | **Open-Meteo Historical Weather API** | Open-Meteo Weather Service | [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api) | Hourly temperature, rain, precipitation, humidity, visibility for Bengaluru |
| **5** | **Bengaluru Traffic Pulse** | Kaggle Open Traffic Datasets / Open Traffic | [https://www.kaggle.com/datasets](https://www.kaggle.com/datasets) | Corridor speeds, free-flow speeds, volume, congestion index |
| **6** | **OpenStreetMap Road Network** | OpenStreetMap Contributors | [https://www.openstreetmap.org](https://www.openstreetmap.org) | Road segment lengths, lanes, maximum speeds, geometry |
| **7** | **OSMnx Python Library** | OSMnx Open Source Geographic Network Tool | [https://osmnx.readthedocs.io](https://osmnx.readthedocs.io) | Bengaluru spatial network extraction & routing analysis |
| **8** | **Bus Occupancy & Passenger Count** | BMTC Vehicle Capacity & Ticket Counter Models | Derived (BMTC Standard Capacity Specs) | Boarding, alighting, occupancy percentage, crowding status |
| **9** | **Historical Passenger Demand** | Derived from Ticketing Demand Patterns | Derived (BMTC Passenger Origin-Destination Matrix) | Baseline passenger volume prediction |
| **10** | **Accident & Incident Logs** | BMTC Transport Control Room / Admin System | Maintainable via Controller System Interface | Active road closures, accidents, protests, and waterlogging |
| **11** | **Events Dataset** | Public Events & City Operations | Maintainable via Controller System Interface | Metro work, tech summits, weather emergency logs |
| **12** | **Holiday & Calendar Data** | Python `holidays` Package (India/Karnataka) | [https://pypi.org/project/holidays/](https://pypi.org/project/holidays/) | Gazetted holidays, weekends, working days in Bengaluru |
| **13** | **Bus Master Dataset** | BMTC Fleet Registry Specs | BMTC Technical Specifications | Fleet seating/standing capacity, fuel type, AC status |
| **14** | **User Feedback & Complaints** | Intelligent Public Bus App Database | Generated via Application Feedback Portal | Commuter issues (WRONG_ETA, OVER_CROWDED, etc.) |
| **15** | **Controller / Admin Data** | Intelligent Public Bus App Database | Generated via Application Auth Portal | Access control, roles, administrator details |

---

## 5. SUMMARY OF GENERATED FILES IN WORKSPACE

All generated datasets are stored in `c:\Users\pregi\OneDrive\Desktop\final yr dataset\`:

1. `final_integrated_dataset.csv` - Single combined CSV master dataset.
2. `final_integrated_dataset.parquet` - Compressed Parquet format of master dataset.
3. `bmtc_data_warehouse.db` - SQLite Data Warehouse database with Star Schema & SQL Views.
4. `DATA_WAREHOUSE_SCHEMA.sql` - Complete DDL relational schema script.
5. `DATASET_DOCUMENTATION.md` - Technical data dictionary and column specifications.
6. `ml_delay_prediction_dataset.csv` - Pre-processed ML dataset for Bus ETA model.
7. `ml_occupancy_prediction_dataset.csv` - Pre-processed ML dataset for Occupancy model.
8. `ml_disruption_detection_dataset.csv` - Pre-processed ML dataset for Disruption Classification model.
9. `dataset_01_bus_schedule_gtfs.csv` to `dataset_13_controller_admin.csv` - All 13 individual normalized source CSV files.
