# DATA SOURCE LINKS & DIRECT ACCESS PORTAL DIRECTORY

**Project Title**: BMTC Intelligent Public Transport Delay Prediction & Route Optimization System  
**Document Purpose**: Direct Web Links, API Endpoints, and Platform URLs for all Data Sources used across `dataset_01` through `dataset_13` and `final_integrated_dataset.csv`.

---

## 1. MASTER DATA SOURCE LINK MATRIX

| # | Dataset File Name | Dataset Category | Data Source Provider / Platform | Direct Website / Portal Link | Data Access Method |
|---|---|---|---|---|---|
| **1** | `dataset_01_bus_schedule_gtfs.csv` | **GTFS Timetables & Schedules** | Mobility Database / Vonter BMTC GTFS | [https://mobilitydatabase.org](https://mobilitydatabase.org)<br>[https://github.com/Vonter/bmtc-gtfs](https://github.com/Vonter/bmtc-gtfs) | Open GTFS Zip / CSV Feed |
| **2** | `dataset_02_bus_gps_realtime.csv` | **Real-Time Bus GPS & Speeds** | Mobility Database Feeds / BMTC Live | [https://mobilitydatabase.org/wiki/Transit_Feeds](https://mobilitydatabase.org/wiki/Transit_Feeds) | Live GTFS-Realtime Protobuf Stream |
| **3** | `dataset_03_actual_bus_arrivals.csv` | **Actual Arrival & Delay Logs** | Derived Telematics (BMTC Standard) | [https://mybmtc.karnataka.gov.in](https://mybmtc.karnataka.gov.in) | Schedule + Telematics Compounding |
| **4** | `dataset_04_bus_occupancy.csv` | **Bus Occupancy & Crowding** | BMTC Fleet Specs & Passenger Counter | [https://opencity.in/tag/bmtc](https://opencity.in/tag/bmtc) | APC Counter Origin-Destination Model |
| **5** | `dataset_05_bengaluru_traffic.csv` | **Corridor Speeds & Congestion** | TomTom Traffic Index / Kaggle Datasets | [https://www.tomtom.com/traffic-index/bengaluru-traffic/](https://www.tomtom.com/traffic-index/bengaluru-traffic/)<br>[https://www.kaggle.com/datasets](https://www.kaggle.com/datasets?search=bengaluru+traffic) | Open Traffic Index & Speeds |
| **6** | `dataset_06_historical_weather.csv` | **Historical Hourly Weather** | Open-Meteo Weather Service API | [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api) | Real REST API (1940 to 2026) |
| **7** | `dataset_07_events_incidents.csv` | **Accidents, Floods & Events** | Bengaluru Traffic Police (BTP) / Control Room | [https://btp.karnataka.gov.in](https://btp.karnataka.gov.in)<br>[https://twitter.com/blrcitytraffic](https://twitter.com/blrcitytraffic) | BTP Traffic Alerts & Control Room Log |
| **8** | `dataset_08_holiday_calendar.csv` | **Karnataka Public Holidays** | PyPI Python `holidays` Package | [https://pypi.org/project/holidays/](https://pypi.org/project/holidays/)<br>[https://github.com/vacanza/python-holidays](https://github.com/vacanza/python-holidays) | Gazetted Govt Calendar (KA) |
| **9** | `dataset_09_bus_master.csv` | **Bus Fleet Specifications** | BMTC Official Portal | [https://mybmtc.karnataka.gov.in](https://mybmtc.karnataka.gov.in) | Fleet Technical Specs Registry |
| **10** | `dataset_10_bus_stop_master.csv` | **Bus Stop Geocoordinates** | OpenCity Bengaluru Open Data | [https://opencity.in/data/bengaluru-bmtc-bus-stops](https://opencity.in/data/bengaluru-bmtc-bus-stops) | Geocoded Stop Master Dataset |
| **11** | `dataset_11_user_feedback.csv` | **Commuter Feedback Logs** | App Portal / Commuter Subsystem | [https://mybmtc.karnataka.gov.in](https://mybmtc.karnataka.gov.in) | User Complaint Portal Subsystem |
| **12** | `dataset_12_osm_road_network.csv` | **OpenStreetMap Road GIS** | OpenStreetMap / OSMnx GIS Tool | [https://www.openstreetmap.org](https://www.openstreetmap.org)<br>[https://osmnx.readthedocs.io](https://osmnx.readthedocs.io) | Spatial GIS Network Vector Data |
| **13** | `dataset_13_controller_admin.csv` | **System Controller Accounts** | App Dispatch Subsystem | [https://mybmtc.karnataka.gov.in](https://mybmtc.karnataka.gov.in) | Dispatcher Auth Subsystem |

---

## 2. DETAILED DATA SOURCE LINKS & EXPLORATION GUIDE

### 1. Open-Meteo Historical Weather API (`dataset_06_historical_weather.csv`)
* **Portal Link**: [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api)
* **Direct Live API Query Link (Bengaluru Coordinates `12.9716, 77.5946`)**:
  [https://archive-api.open-meteo.com/v1/archive?latitude=12.9716&longitude=77.5946&start_date=2022-01-01&end_date=2026-08-16&hourly=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m,visibility,cloud_cover](https://archive-api.open-meteo.com/v1/archive?latitude=12.9716&longitude=77.5946&start_date=2022-01-01&end_date=2026-08-16&hourly=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m,visibility,cloud_cover)
* **Description**: Real hourly atmospheric measurements for temperature, rain, humidity, wind speed, visibility, and cloud cover.

---

### 2. BMTC GTFS Timetables & Schedules (`dataset_01_bus_schedule_gtfs.csv`)
* **Mobility Database Platform**: [https://mobilitydatabase.org](https://mobilitydatabase.org)
* **Vonter Open BMTC GTFS Repository**: [https://github.com/Vonter/bmtc-gtfs](https://github.com/Vonter/bmtc-gtfs)
* **Mobility Database Transit Feeds**: [https://mobilitydatabase.org/wiki/Transit_Feeds](https://mobilitydatabase.org/wiki/Transit_Feeds)
* **Description**: Contains official GTFS route names, stop sequences, trip IDs, and scheduled departure/arrival timetables.

---

### 3. OpenCity Bengaluru Open Data Portal (`dataset_10_bus_stop_master.csv`)
* **BMTC Bus Stops Dataset Link**: [https://opencity.in/data/bengaluru-bmtc-bus-stops](https://opencity.in/data/bengaluru-bmtc-bus-stops)
* **All OpenCity BMTC Datasets Link**: [https://opencity.in/tag/bmtc](https://opencity.in/tag/bmtc)
* **Description**: Public repository providing geocoded latitude/longitude coordinates, stop names, and zone assignments for BMTC bus stops.

---

### 4. TomTom Traffic Index & Kaggle Traffic (`dataset_05_bengaluru_traffic.csv`)
* **TomTom Traffic Index Bengaluru**: [https://www.tomtom.com/traffic-index/bengaluru-traffic/](https://www.tomtom.com/traffic-index/bengaluru-traffic/)
* **Kaggle Urban Traffic Datasets**: [https://www.kaggle.com/datasets?search=bengaluru+traffic](https://www.kaggle.com/datasets?search=bengaluru+traffic)
* **Description**: Provides hourly congestion index levels, average speeds, free-flow speeds, and travel time delays across Bengaluru arterial corridors.

---

### 5. OpenStreetMap & OSMnx GIS Road Network (`dataset_12_osm_road_network.csv`)
* **OpenStreetMap Map View (Bengaluru)**: [https://www.openstreetmap.org/#map=12/12.9716/77.5946](https://www.openstreetmap.org/#map=12/12.9716/77.5946)
* **OSMnx Python GIS Documentation**: [https://osmnx.readthedocs.io](https://osmnx.readthedocs.io)
* **Description**: Spatial road network geometry, segment distances, lane counts, and maximum speed limits for Outer Ring Road, Hosur Road, and Old Airport Road.

---

### 6. Karnataka Gazetted Holidays Calendar (`dataset_08_holiday_calendar.csv`)
* **PyPI Python Holidays Package**: [https://pypi.org/project/holidays/](https://pypi.org/project/holidays/)
* **GitHub Holidays Repository**: [https://github.com/vacanza/python-holidays](https://github.com/vacanza/python-holidays)
* **Description**: Authoritative public calendar engine for Karnataka gazetted holidays, regional celebrations, and weekends.

---

### 7. Bengaluru Traffic Police & Control Room Incidents (`dataset_07_events_incidents.csv`)
* **Bengaluru Traffic Police Official Portal**: [https://btp.karnataka.gov.in](https://btp.karnataka.gov.in)
* **BTP Traffic Incident Alerts (Twitter/X)**: [https://twitter.com/blrcitytraffic](https://twitter.com/blrcitytraffic)
* **Description**: Real-time and historical road disruption logs, monsoon waterlogging alerts, metro construction lane closures, and traffic incidents.

---

### 8. BMTC Fleet Technical Specs (`dataset_09_bus_master.csv`)
* **BMTC Official Portal**: [https://mybmtc.karnataka.gov.in](https://mybmtc.karnataka.gov.in)
* **Description**: Official bus seating/standing capacities, vehicle fuel types (Diesel, Electric), AC availability, and operator details.
