import os
import sys
import datetime
import random
import math
import requests
import urllib3
import pandas as pd
import numpy as np
import holidays
import sqlite3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OUTPUT_DIR = r"c:\Users\pregi\OneDrive\Desktop\final yr dataset"

print("Starting BMTC Multi-Year (5 Years: 2022-2026) Data Warehouse & Integrated Dataset Generation...")

# Set random seed for reproducible realistic generation
random.seed(42)
np.random.seed(42)

# ---------------------------------------------------------
# 1. BUS STOP MASTER DATASET (Dataset 10)
# ---------------------------------------------------------
stops_data = [
    {"stop_id": "BS_HEB", "stop_name": "Hebbal Bus Stop", "latitude": 13.0358, "longitude": 77.5970, "area": "Hebbal", "zone": "North", "landmark": "Hebbal Flyover", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_NAG", "stop_name": "Nagavara Junction", "latitude": 13.0407, "longitude": 77.6256, "area": "Nagavara", "zone": "North", "landmark": "Manyata Tech Park", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_HEN", "stop_name": "Hennur Cross", "latitude": 13.0253, "longitude": 77.6358, "area": "Hennur", "zone": "North-East", "landmark": "Hennur Ring Road", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_KRP", "stop_name": "KR Puram Railway Station", "latitude": 13.0012, "longitude": 77.6750, "area": "KR Puram", "zone": "East", "landmark": "Cable Bridge", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_TIN", "stop_name": "Tin Factory", "latitude": 12.9982, "longitude": 77.6692, "area": "Tin Factory", "zone": "East", "landmark": "Metro Station", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_MAR", "stop_name": "Marathahalli Bridge", "latitude": 12.9562, "longitude": 77.7019, "area": "Marathahalli", "zone": "East", "landmark": "Multiplex", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_ITP", "stop_name": "ITPL Main Gate", "latitude": 12.9863, "longitude": 77.7348, "area": "Whitefield", "zone": "East", "landmark": "International Tech Park", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_BEL", "stop_name": "Bellandur Junction", "latitude": 12.9279, "longitude": 77.6751, "area": "Bellandur", "zone": "South-East", "landmark": "Ecovorld", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_AGA", "stop_name": "Agara Lake Bus Stop", "latitude": 12.9234, "longitude": 77.6477, "area": "Agara", "zone": "South-East", "landmark": "Agara Lake", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_SIL", "stop_name": "Silk Board Junction", "latitude": 12.9177, "longitude": 77.6238, "area": "Silk Board", "zone": "South", "landmark": "Central Silk Board", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_BTM", "stop_name": "BTM Layout Bus Stand", "latitude": 12.9166, "longitude": 77.6101, "area": "BTM Layout", "zone": "South", "landmark": "Udupi Garden", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_BAN", "stop_name": "Banashankari Bus TTMC", "latitude": 12.9254, "longitude": 77.5736, "area": "Banashankari", "zone": "South", "landmark": "BNS Temple", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_ELE", "stop_name": "Electronic City Wipro Gate", "latitude": 12.8452, "longitude": 77.6602, "area": "Electronic City", "zone": "South", "landmark": "Wipro Campus", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_MAJ", "stop_name": "Kempegowda Bus Station (Majestic)", "latitude": 12.9781, "longitude": 77.5697, "area": "Majestic", "zone": "Central", "landmark": "Railway Station", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
    {"stop_id": "BS_IND", "stop_name": "Indiranagar 100ft Road", "latitude": 12.9784, "longitude": 77.6408, "area": "Indiranagar", "zone": "East", "landmark": "Metro Station", "shelter_available": True, "accessibility": True, "active_status": "ACTIVE"},
]
df_stops = pd.DataFrame(stops_data)
df_stops.to_csv(os.path.join(OUTPUT_DIR, "dataset_10_bus_stop_master.csv"), index=False)
print("Saved dataset_10_bus_stop_master.csv (15 stops)")

# ---------------------------------------------------------
# 2. BUS MASTER DATASET (Dataset 9)
# ---------------------------------------------------------
bus_types = [
    {"type": "Ordinary Non-AC", "capacity": 60, "seating": 40, "standing": 20, "fuel": "Diesel", "ac": False},
    {"type": "Vajra Volvo AC", "capacity": 50, "seating": 38, "standing": 12, "fuel": "Diesel", "ac": True},
    {"type": "Vayu Vajra Airport AC", "capacity": 45, "seating": 35, "standing": 10, "fuel": "Diesel", "ac": True},
    {"type": "Electric Bus Non-AC", "capacity": 55, "seating": 35, "standing": 20, "fuel": "Electric", "ac": False},
    {"type": "Electric Bus AC", "capacity": 50, "seating": 35, "standing": 15, "fuel": "Electric", "ac": True},
]

buses_list = []
for i in range(1, 41):
    bus_id = f"BUS_{i:03d}"
    reg_no = f"KA-01-F-{1000 + i}"
    bt = bus_types[(i - 1) % len(bus_types)]
    buses_list.append({
        "bus_id": bus_id,
        "registration_number": reg_no,
        "bus_type": bt["type"],
        "operator": "BMTC",
        "capacity": bt["capacity"],
        "seating_capacity": bt["seating"],
        "standing_capacity": bt["standing"],
        "fuel_type": bt["fuel"],
        "accessibility": True,
        "ac_available": bt["ac"],
        "status": "ACTIVE"
    })
df_buses = pd.DataFrame(buses_list)
df_buses.to_csv(os.path.join(OUTPUT_DIR, "dataset_09_bus_master.csv"), index=False)
print("Saved dataset_09_bus_master.csv (40 buses)")

# ---------------------------------------------------------
# 3. OSM ROAD NETWORK DATASET (Dataset 12)
# ---------------------------------------------------------
roads_data = [
    {"road_id": "RD_ORR_NORTH", "road_name": "Outer Ring Road (Hebbal - KR Puram)", "road_type": "Primary Trunk", "length_km": 11.2, "lanes": 6, "maxspeed": 60, "oneway": False, "intersections": 8, "geometry": "LINESTRING(77.5970 13.0358, 77.6256 13.0407, 77.6750 13.0012)"},
    {"road_id": "RD_ORR_EAST", "road_name": "Outer Ring Road (KR Puram - Marathahalli)", "road_type": "Primary Trunk", "length_km": 8.5, "lanes": 6, "maxspeed": 60, "oneway": False, "intersections": 5, "geometry": "LINESTRING(77.6750 13.0012, 77.6692 12.9982, 77.7019 12.9562)"},
    {"road_id": "RD_ORR_SOUTH", "road_name": "Outer Ring Road (Marathahalli - Silk Board)", "road_type": "Primary Trunk", "length_km": 10.4, "lanes": 6, "maxspeed": 60, "oneway": False, "intersections": 7, "geometry": "LINESTRING(77.7019 12.9562, 77.6751 12.9279, 77.6477 12.9234, 77.6238 12.9177)"},
    {"road_id": "RD_HOSUR_RD", "road_name": "Hosur Road Express Corridor (Silk Board - E-City)", "road_type": "Secondary Expressway", "length_km": 12.1, "lanes": 8, "maxspeed": 80, "oneway": False, "intersections": 4, "geometry": "LINESTRING(77.6238 12.9177, 77.6602 12.8452)"},
    {"road_id": "RD_WHITEFIELD", "road_name": "ITPL Main Road (Marathahalli - Whitefield)", "road_type": "Secondary Arterial", "length_km": 6.8, "lanes": 4, "maxspeed": 50, "oneway": False, "intersections": 6, "geometry": "LINESTRING(77.7019 12.9562, 77.7348 12.9863)"},
    {"road_id": "RD_AIRPORT_RD", "road_name": "Old Airport Road (Majestic - Indiranagar - Marathahalli)", "road_type": "Primary Arterial", "length_km": 14.3, "lanes": 4, "maxspeed": 50, "oneway": False, "intersections": 12, "geometry": "LINESTRING(77.5697 12.9781, 77.6408 12.9784, 77.7019 12.9562)"},
    {"road_id": "RD_BTM_BNS", "road_name": "Outer Ring Road (Silk Board - Banashankari)", "road_type": "Primary Trunk", "length_km": 7.6, "lanes": 6, "maxspeed": 60, "oneway": False, "intersections": 6, "geometry": "LINESTRING(77.6238 12.9177, 77.6101 12.9166, 77.5736 12.9254)"},
]
df_roads = pd.DataFrame(roads_data)
df_roads.to_csv(os.path.join(OUTPUT_DIR, "dataset_12_osm_road_network.csv"), index=False)
print("Saved dataset_12_osm_road_network.csv (7 major road corridors)")

# ---------------------------------------------------------
# 4. HOLIDAY / CALENDAR DATASET (Dataset 8 - 5 Years: 2022 to 2026)
# ---------------------------------------------------------
years_list = [2022, 2023, 2024, 2025, 2026]
ka_holidays = holidays.India(years=years_list, subdiv='KA')
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2026, 8, 16)

calendar_list = []
curr = start_date
while curr <= end_date:
    d_str = curr.strftime("%Y-%m-%d")
    dow = curr.strftime("%A")
    is_wknd = curr.weekday() in [5, 6]
    h_name = ka_holidays.get(curr, None)
    is_hol = h_name is not None
    is_work = (not is_wknd) and (not is_hol)
    h_type = "Public Holiday" if is_hol else ("Weekend" if is_wknd else "Regular Working Day")
    calendar_list.append({
        "date": d_str,
        "day_of_week": dow,
        "is_weekend": is_wknd,
        "is_holiday": is_hol,
        "holiday_name": h_name if h_name else "None",
        "holiday_type": h_type,
        "is_working_day": is_work
    })
    curr += datetime.timedelta(days=1)

df_calendar = pd.DataFrame(calendar_list)
df_calendar.to_csv(os.path.join(OUTPUT_DIR, "dataset_08_holiday_calendar.csv"), index=False)
print(f"Saved dataset_08_holiday_calendar.csv ({len(df_calendar)} days across 2022-2026)")

# ---------------------------------------------------------
# 5. HISTORICAL WEATHER DATASET (Dataset 6 - Open-Meteo API: 2022 to 2026)
# ---------------------------------------------------------
print("Fetching real historical weather data from Open-Meteo API for Bengaluru (2022 to 2026)...")

weather_list = []
for yr in years_list:
    y_start = f"{yr}-01-01"
    y_end = f"{yr}-12-31" if yr < 2026 else "2026-08-16"
    weather_url = f"https://archive-api.open-meteo.com/v1/archive?latitude=12.9716&longitude=77.5946&start_date={y_start}&end_date={y_end}&hourly=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m,visibility,cloud_cover"

    try:
        resp = requests.get(weather_url, verify=False, timeout=25)
        if resp.status_code == 200:
            w_json = resp.json()
            h_data = w_json.get("hourly", {})
            times = h_data.get("time", [])
            temps = h_data.get("temperature_2m", [])
            humi = h_data.get("relative_humidity_2m", [])
            prec = h_data.get("precipitation", [])
            rain = h_data.get("rain", [])
            wcode = h_data.get("weather_code", [])
            wspeed = h_data.get("wind_speed_10m", [])
            visib = h_data.get("visibility", [])
            cloud = h_data.get("cloud_cover", [])

            for idx, t in enumerate(times):
                weather_list.append({
                    "timestamp": t.replace("T", " ") + ":00",
                    "latitude": 12.9716,
                    "longitude": 77.5946,
                    "temperature": temps[idx] if idx < len(temps) and temps[idx] is not None else 25.0,
                    "humidity": humi[idx] if idx < len(humi) and humi[idx] is not None else 70,
                    "precipitation": prec[idx] if idx < len(prec) and prec[idx] is not None else 0.0,
                    "rain": rain[idx] if idx < len(rain) and rain[idx] is not None else 0.0,
                    "weather_code": wcode[idx] if idx < len(wcode) and wcode[idx] is not None else 0,
                    "wind_speed": wspeed[idx] if idx < len(wspeed) and wspeed[idx] is not None else 10.0,
                    "visibility": visib[idx] if idx < len(visib) and visib[idx] is not None else 10000.0,
                    "cloud_cover": cloud[idx] if idx < len(cloud) and cloud[idx] is not None else 50
                })
            print(f"  Successfully fetched {len(times)} hourly records for {yr} from Open-Meteo.")
        else:
            raise Exception(f"Open-Meteo returned status {resp.status_code}")
    except Exception as e:
        print(f"  Fallback simulation for weather in {yr}: {e}")
        # Synthetic weather fallback for that year
        dt_start = datetime.date(yr, 1, 1)
        dt_end = datetime.date(yr, 12, 31) if yr < 2026 else datetime.date(2026, 8, 16)
        curr_w = dt_start
        while curr_w <= dt_end:
            for h in range(24):
                ts_str = f"{curr_w.strftime('%Y-%m-%d')} {h:02d}:00:00"
                # Seasonal variation: Summer (Mar-May) hot, Monsoon (June-Sept) rainy, Winter (Nov-Feb) cool
                m = curr_w.month
                base_temp = 32.0 if 3 <= m <= 5 else (22.0 if 11 <= m or m <= 2 else 26.0)
                is_monsoon = 6 <= m <= 9
                rain_val = round(random.choice([0.0, 0.0, 0.0, 2.5, 8.4, 18.0]), 1) if is_monsoon else round(random.choice([0.0, 0.0, 0.0, 0.0, 1.0]), 1)
                weather_list.append({
                    "timestamp": ts_str,
                    "latitude": 12.9716,
                    "longitude": 77.5946,
                    "temperature": round(base_temp + 5.0 * math.sin(math.pi * (h - 6) / 12) + random.uniform(-1, 1), 1),
                    "humidity": random.randint(75, 98) if is_monsoon else random.randint(40, 80),
                    "precipitation": rain_val,
                    "rain": rain_val,
                    "weather_code": 61 if rain_val > 0 else 0,
                    "wind_speed": round(random.uniform(5.0, 22.0), 1),
                    "visibility": 5000.0 if rain_val > 5.0 else 10000.0,
                    "cloud_cover": random.randint(60, 95) if is_monsoon else random.randint(10, 50)
                })
            curr_w += datetime.timedelta(days=1)

df_weather = pd.DataFrame(weather_list)
df_weather.to_csv(os.path.join(OUTPUT_DIR, "dataset_06_historical_weather.csv"), index=False)
print(f"Saved dataset_06_historical_weather.csv ({len(df_weather)} records across 2022-2026)")

# Fast Weather lookup dictionary (keyed by timestamp string YYYY-MM-DD HH:00:00)
weather_lookup = {w["timestamp"]: w for w in weather_list}

# ---------------------------------------------------------
# 6. EVENTS / INCIDENTS DATASET (Dataset 7 - Multi-Year 2022-2026)
# ---------------------------------------------------------
events_data = [
    # 2022 Events
    {"event_id": "EVT_2022_01", "event_name": "Silk Board Flyover Maintenance", "event_type": "CONSTRUCTION", "description": "Lanes restricted at Silk Board junction", "start_time": "2022-03-10 00:00:00", "end_time": "2022-03-25 23:59:59", "latitude": 12.9177, "longitude": 77.6238, "affected_radius_km": 2.0, "severity": "HIGH", "affected_road": "RD_ORR_SOUTH", "affected_route": "500D, 500CA, 500K", "affected_stop": "BS_SIL", "status": "RESOLVED"},
    {"event_id": "EVT_2022_02", "event_name": "Monsoon Flooding at Bellandur Underpass", "event_type": "FLOOD", "description": "Waterlogging blocking ORR slow lane", "start_time": "2022-09-05 14:00:00", "end_time": "2022-09-08 20:00:00", "latitude": 12.9279, "longitude": 77.6751, "affected_radius_km": 2.5, "severity": "SEVERE", "affected_road": "RD_ORR_SOUTH", "affected_route": "500D, 500K, 500CA", "affected_stop": "BS_BEL", "status": "RESOLVED"},
    
    # 2023 Events
    {"event_id": "EVT_2023_01", "event_name": "KR Puram Metro Line Testing", "event_type": "CONSTRUCTION", "description": "Traffic diversion near KR Puram station", "start_time": "2023-02-15 08:00:00", "end_time": "2023-03-31 23:59:59", "latitude": 13.0012, "longitude": 77.6750, "affected_radius_km": 2.0, "severity": "HIGH", "affected_road": "RD_ORR_NORTH", "affected_route": "500D, 500CA", "affected_stop": "BS_KRP", "status": "RESOLVED"},
    {"event_id": "EVT_2023_02", "event_name": "Heavy Downpour & Flash Floods", "event_type": "FLOOD", "description": "Marathahalli ORR waterlogging", "start_time": "2023-10-18 16:00:00", "end_time": "2023-10-19 22:00:00", "latitude": 12.9562, "longitude": 77.7019, "affected_radius_km": 3.0, "severity": "SEVERE", "affected_road": "RD_ORR_EAST", "affected_route": "500D, 500K, 335E", "affected_stop": "BS_MAR", "status": "RESOLVED"},
    
    # 2024 Events
    {"event_id": "EVT_2024_01", "event_name": "Metro Extension Construction", "event_type": "CONSTRUCTION", "description": "Lanes closed near Silk Board for Metro pillar work", "start_time": "2024-07-01 00:00:00", "end_time": "2024-07-31 23:59:59", "latitude": 12.9177, "longitude": 77.6238, "affected_radius_km": 2.5, "severity": "HIGH", "affected_road": "RD_ORR_SOUTH", "affected_route": "500D, 500CA, 500K", "affected_stop": "BS_SIL", "status": "RESOLVED"},
    {"event_id": "EVT_2024_02", "event_name": "Heavy Downpour & Waterlogging", "event_type": "FLOOD", "description": "Waterlogging under Marathahalli bridge causing slow traffic", "start_time": "2024-07-12 16:00:00", "end_time": "2024-07-12 21:00:00", "latitude": 12.9562, "longitude": 77.7019, "affected_radius_km": 1.5, "severity": "SEVERE", "affected_road": "RD_ORR_EAST", "affected_route": "500D, 500K, 335E", "affected_stop": "BS_MAR", "status": "RESOLVED"},
    {"event_id": "EVT_2024_03", "event_name": "Multi-Vehicle Collision", "event_type": "ACCIDENT", "description": "Cab collision near Tin Factory Flyover blocking 2 lanes", "start_time": "2024-07-18 08:30:00", "end_time": "2024-07-18 11:00:00", "latitude": 12.9982, "longitude": 77.6692, "affected_radius_km": 1.0, "severity": "MEDIUM", "affected_road": "RD_ORR_NORTH", "affected_route": "500D, 500CA", "affected_stop": "BS_TIN", "status": "RESOLVED"},
    {"event_id": "EVT_2024_04", "event_name": "Tech Summit Convoy & Rally", "event_type": "PUBLIC_EVENT", "description": "VIP movement near ITPL Main Road", "start_time": "2024-07-24 09:00:00", "end_time": "2024-07-24 14:00:00", "latitude": 12.9863, "longitude": 77.7348, "affected_radius_km": 3.0, "severity": "MEDIUM", "affected_road": "RD_WHITEFIELD", "affected_route": "500K, 335E", "affected_stop": "BS_ITP", "status": "RESOLVED"},
    {"event_id": "EVT_2024_05", "event_name": "Protest near Dairy Circle", "event_type": "PROTEST", "description": "Traffic diversion via Koramangala", "start_time": "2024-07-29 10:00:00", "end_time": "2024-07-29 15:00:00", "latitude": 12.9350, "longitude": 77.6050, "affected_radius_km": 2.0, "severity": "MEDIUM", "affected_road": "RD_BTM_BNS", "affected_route": "201, 365", "affected_stop": "BS_BTM", "status": "RESOLVED"},
    
    # 2025 Events
    {"event_id": "EVT_2025_01", "event_name": "Electronic City Expressway Resurfacing", "event_type": "CONSTRUCTION", "description": "Lane closures on Hosur Road", "start_time": "2025-01-10 00:00:00", "end_time": "2025-01-28 23:59:59", "latitude": 12.8452, "longitude": 77.6602, "affected_radius_km": 2.0, "severity": "HIGH", "affected_road": "RD_HOSUR_RD", "affected_route": "500CA", "affected_stop": "BS_ELE", "status": "RESOLVED"},
    {"event_id": "EVT_2025_02", "event_name": "Hebbal Flyover Expansion Work", "event_type": "CONSTRUCTION", "description": "Traffic restriction on airport ramp", "start_time": "2025-05-12 00:00:00", "end_time": "2025-06-30 23:59:59", "latitude": 13.0358, "longitude": 77.5970, "affected_radius_km": 3.0, "severity": "HIGH", "affected_road": "RD_ORR_NORTH", "affected_route": "500D", "affected_stop": "BS_HEB", "status": "RESOLVED"},
    
    # 2026 Events
    {"event_id": "EVT_2026_01", "event_name": "Bengaluru Tech Summit 2026", "event_type": "PUBLIC_EVENT", "description": "Heavy VIP movement & shuttle buses at Palace Grounds & ITPL", "start_time": "2026-03-15 08:00:00", "end_time": "2026-03-18 20:00:00", "latitude": 12.9863, "longitude": 77.7348, "affected_radius_km": 4.0, "severity": "MEDIUM", "affected_road": "RD_WHITEFIELD", "affected_route": "500K, 335E", "affected_stop": "BS_ITP", "status": "RESOLVED"},
    {"event_id": "EVT_2026_02", "event_name": "Pre-Monsoon Drainage Cleaning", "event_type": "CONSTRUCTION", "description": "Slow moving traffic near Agara lake", "start_time": "2026-05-02 09:00:00", "end_time": "2026-05-10 18:00:00", "latitude": 12.9234, "longitude": 77.6477, "affected_radius_km": 1.5, "severity": "MEDIUM", "affected_road": "RD_ORR_SOUTH", "affected_route": "500D, 500K, 500CA", "affected_stop": "BS_AGA", "status": "ACTIVE"},
]
df_events = pd.DataFrame(events_data)
df_events.to_csv(os.path.join(OUTPUT_DIR, "dataset_07_events_incidents.csv"), index=False)
print(f"Saved dataset_07_events_incidents.csv ({len(df_events)} incident records across 2022-2026)")

# ---------------------------------------------------------
# 7. ROUTE DEFINITIONS & SCHEDULE MASTER DATASET (Dataset 1 - 5 Years)
# ---------------------------------------------------------
routes_definition = [
    {
        "route_id": "R_500D",
        "route_name": "500D (Hebbal to Silk Board via ORR)",
        "first_stop": "Hebbal Bus Stop",
        "last_stop": "Silk Board Junction",
        "distance_km": 28.5,
        "duration_min": 75,
        "stops": ["BS_HEB", "BS_NAG", "BS_HEN", "BS_KRP", "BS_TIN", "BS_MAR", "BS_BEL", "BS_AGA", "BS_SIL"]
    },
    {
        "route_id": "R_500K",
        "route_name": "500K (Banashankari to ITPL via Silk Board & Marathahalli)",
        "first_stop": "Banashankari Bus TTMC",
        "last_stop": "ITPL Main Gate",
        "distance_km": 32.0,
        "duration_min": 90,
        "stops": ["BS_BAN", "BS_BTM", "BS_SIL", "BS_AGA", "BS_BEL", "BS_MAR", "BS_ITP"]
    },
    {
        "route_id": "R_500CA",
        "route_name": "500CA (Tin Factory to Electronic City via ORR)",
        "first_stop": "Tin Factory",
        "last_stop": "Electronic City Wipro Gate",
        "distance_km": 30.2,
        "duration_min": 80,
        "stops": ["BS_TIN", "BS_KRP", "BS_MAR", "BS_BEL", "BS_AGA", "BS_SIL", "BS_ELE"]
    },
    {
        "route_id": "R_335E",
        "route_name": "335E (Majestic to ITPL via Indiranagar & Marathahalli)",
        "first_stop": "Kempegowda Bus Station (Majestic)",
        "last_stop": "ITPL Main Gate",
        "distance_km": 24.8,
        "duration_min": 70,
        "stops": ["BS_MAJ", "BS_IND", "BS_MAR", "BS_ITP"]
    }
]

# Quick map lookup helpers
stop_lookup = {s["stop_id"]: s for s in stops_data}
bus_lookup = {b["bus_id"]: b for b in buses_list}
calendar_lookup = {c["date"]: c for c in calendar_list}

schedule_list = []
gps_list = []
actual_arrivals_list = []
occupancy_list = []
traffic_list = []
integrated_list = []
ml_delay_list = []
ml_occ_list = []
ml_disruption_list = []

print("Simulating trip schedules, telematics, traffic & occupancy across 5 full years (2022-2026)...")

departure_hours = list(range(6, 22))
curr_date = start_date

while curr_date <= end_date:
    date_str = curr_date.strftime("%Y-%m-%d")
    cal_info = calendar_lookup[date_str]
    is_weekend = cal_info["is_weekend"]
    is_holiday = cal_info["is_holiday"]
    day_type = "HOLIDAY" if is_holiday else ("WEEKEND" if is_weekend else "WEEKDAY")

    for route in routes_definition:
        r_id = route["route_id"]
        r_name = route["route_name"]
        r_stops = route["stops"]
        tot_dist = route["distance_km"]
        tot_dur = route["duration_min"]
        
        # Select assigned buses deterministically per route
        assigned_buses = [b["bus_id"] for b in buses_list if hash(b["bus_id"] + r_id) % 4 == 0]
        if not assigned_buses:
            assigned_buses = ["BUS_001", "BUS_002"]

        for h in departure_hours:
            trip_id = f"TRIP_{r_id}_{date_str.replace('-','')}_{h:02d}00"
            bus_id = assigned_buses[(h + int(date_str.replace('-', ''))) % len(assigned_buses)]
            bus_info = bus_lookup[bus_id]

            # Base trip start time
            trip_start_dt = datetime.datetime.strptime(f"{date_str} {h:02d}:00:00", "%Y-%m-%d %H:%M:%S")

            # Route traversal simulation state
            curr_passengers = random.randint(5, 15)
            accumulated_delay_sec = 0

            # Determine traffic congestion factor for this hour & day
            is_peak = (8 <= h <= 11 or 17 <= h <= 20) and day_type == "WEEKDAY"
            base_traffic_speed = random.uniform(15.0, 25.0) if is_peak else random.uniform(35.0, 50.0)
            free_flow_speed = 60.0
            
            # Weather effect from Open-Meteo weather lookup
            w_ts_key = f"{date_str} {h:02d}:00:00"
            w_info = weather_lookup.get(w_ts_key, {
                "temperature": 25.0, "humidity": 70, "precipitation": 0.0, "rain": 0.0,
                "weather_code": 0, "wind_speed": 10.0, "visibility": 10000.0, "cloud_cover": 50
            })
            rain_val = w_info["rain"]

            # Heavy rain or incident delay boost
            if rain_val > 5.0:
                base_traffic_speed *= 0.7
                accumulated_delay_sec += random.randint(300, 900)

            # Check active incidents
            incident_active = False
            inc_description = "None"
            for evt in events_data:
                if evt["affected_stop"] in r_stops:
                    evt_start = datetime.datetime.strptime(evt["start_time"], "%Y-%m-%d %H:%M:%S")
                    evt_end = datetime.datetime.strptime(evt["end_time"], "%Y-%m-%d %H:%M:%S")
                    if evt_start <= trip_start_dt <= evt_end:
                        incident_active = True
                        inc_description = evt["event_name"]
                        base_traffic_speed *= 0.6
                        accumulated_delay_sec += random.randint(400, 1200)
                        break

            traffic_vol = int(random.randint(1500, 3000) if is_peak else random.randint(400, 1200))
            if incident_active:
                traffic_vol += 1000
            
            cong_index = round(max(0.0, min(1.0, 1.0 - (base_traffic_speed / free_flow_speed))), 2)
            if cong_index > 0.6:
                cong_level = "HEAVY"
            elif cong_index > 0.3:
                cong_level = "MODERATE"
            else:
                cong_level = "LOW"

            num_stops = len(r_stops)
            time_per_stop_sec = int((tot_dur * 60) / (num_stops - 1))

            for seq, st_id in enumerate(r_stops, start=1):
                st_info = stop_lookup[st_id]
                
                # Scheduled arrival and departure
                sch_arr_dt = trip_start_dt + datetime.timedelta(seconds=(seq - 1) * time_per_stop_sec)
                sch_dep_dt = sch_arr_dt + datetime.timedelta(seconds=45)

                sch_arr_str = sch_arr_dt.strftime("%H:%M:%S")
                sch_dep_str = sch_dep_dt.strftime("%H:%M:%S")

                # Add noise & traffic impact to actual arrival
                stop_noise = random.randint(-60, 180)
                if is_peak:
                    stop_noise += random.randint(120, 480)
                
                accumulated_delay_sec += stop_noise
                accumulated_delay_sec = max(-120, accumulated_delay_sec) # cap early arrival at -2 mins

                act_arr_dt = sch_arr_dt + datetime.timedelta(seconds=accumulated_delay_sec)
                act_dep_dt = act_arr_dt + datetime.timedelta(seconds=random.randint(45, 90))

                act_arr_str = act_arr_dt.strftime("%H:%M:%S")
                act_dep_str = act_dep_dt.strftime("%H:%M:%S")

                delay_sec = accumulated_delay_sec
                delay_min = round(delay_sec / 60.0, 2)

                # Passenger dynamics at stop
                if seq == 1:
                    boarded = random.randint(15, 30) if is_peak else random.randint(5, 12)
                    alighted = 0
                elif seq == num_stops:
                    boarded = 0
                    alighted = curr_passengers
                else:
                    boarded = random.randint(3, 15) if is_peak else random.randint(1, 6)
                    alighted = min(curr_passengers, random.randint(2, 10))

                curr_passengers = max(0, curr_passengers + boarded - alighted)
                capacity = bus_info["capacity"]
                curr_passengers = min(capacity, curr_passengers)
                avail_cap = capacity - curr_passengers
                occ_pct = round((curr_passengers / capacity) * 100.0, 1)

                if occ_pct >= 90.0:
                    occ_status = "FULL"
                elif occ_pct >= 75.0:
                    occ_status = "NEARLY_FULL"
                elif occ_pct >= 50.0:
                    occ_status = "HIGH"
                elif occ_pct >= 25.0:
                    occ_status = "MODERATE"
                else:
                    occ_status = "LOW"

                timestamp_str = f"{date_str} {sch_arr_str}"

                # 1. Schedule GTFS Record
                schedule_list.append({
                    "route_id": r_id,
                    "route_name": r_name,
                    "trip_id": trip_id,
                    "bus_id": bus_id,
                    "stop_id": st_id,
                    "stop_name": st_info["stop_name"],
                    "stop_sequence": seq,
                    "direction": "INBOUND" if seq % 2 == 1 else "OUTBOUND",
                    "scheduled_arrival": sch_arr_str,
                    "scheduled_departure": sch_dep_str,
                    "service_date": date_str,
                    "day_type": day_type,
                    "first_stop": route["first_stop"],
                    "last_stop": route["last_stop"],
                    "route_distance_km": tot_dist,
                    "scheduled_trip_duration": tot_dur
                })

                # 2. GPS Real-Time Location Record
                next_st_id = r_stops[seq] if seq < num_stops else "TERMINAL"
                gps_speed = round(max(0.0, base_traffic_speed + random.uniform(-5.0, 5.0)), 1)
                dist_to_next = round(tot_dist / num_stops, 2) if seq < num_stops else 0.0
                bus_st = "IN_TRANSIT" if seq < num_stops else "COMPLETED"

                gps_list.append({
                    "timestamp": timestamp_str,
                    "bus_id": bus_id,
                    "route_id": r_id,
                    "trip_id": trip_id,
                    "latitude": st_info["latitude"],
                    "longitude": st_info["longitude"],
                    "speed_kmph": gps_speed,
                    "heading": random.choice([45, 90, 180, 270]),
                    "current_stop_id": st_id,
                    "next_stop_id": next_st_id,
                    "distance_to_next_stop": dist_to_next,
                    "gps_accuracy": 5.0,
                    "bus_status": bus_st
                })

                # 3. Actual Arrival/Departure Record
                actual_arrivals_list.append({
                    "date": date_str,
                    "timestamp": timestamp_str,
                    "bus_id": bus_id,
                    "route_id": r_id,
                    "trip_id": trip_id,
                    "stop_id": st_id,
                    "stop_sequence": seq,
                    "scheduled_arrival": sch_arr_str,
                    "actual_arrival": act_arr_str,
                    "scheduled_departure": sch_dep_str,
                    "actual_departure": act_dep_str,
                    "delay_seconds": delay_sec,
                    "delay_minutes": delay_min
                })

                # 4. Bus Occupancy Record
                occupancy_list.append({
                    "timestamp": timestamp_str,
                    "bus_id": bus_id,
                    "route_id": r_id,
                    "trip_id": trip_id,
                    "stop_id": st_id,
                    "passengers_boarded": boarded,
                    "passengers_alighted": alighted,
                    "passenger_count": curr_passengers,
                    "capacity": capacity,
                    "seating_capacity": bus_info["seating_capacity"],
                    "standing_capacity": bus_info["standing_capacity"],
                    "available_capacity": avail_cap,
                    "occupancy_percentage": occ_pct,
                    "occupancy_status": occ_status
                })

                # 5. Traffic Record
                road_id = "RD_ORR_EAST" if "MAR" in st_id or "KRP" in st_id else "RD_ORR_SOUTH"
                traffic_list.append({
                    "timestamp": timestamp_str,
                    "road_id": road_id,
                    "route_id": r_id,
                    "latitude": st_info["latitude"],
                    "longitude": st_info["longitude"],
                    "traffic_speed": round(base_traffic_speed, 1),
                    "free_flow_speed": free_flow_speed,
                    "traffic_volume": traffic_vol,
                    "congestion_level": cong_level,
                    "travel_time": round((dist_to_next / max(1.0, base_traffic_speed)) * 60.0, 2),
                    "road_distance": dist_to_next,
                    "incident_flag": incident_active,
                    "traffic_status": "CONGESTED" if cong_index > 0.4 else "SMOOTH",
                    "congestion_index": cong_index
                })

                # Disruption label calculation
                if incident_active:
                    disruption_lbl = "ROUTE_CHANGED" if random.random() < 0.2 else "SEVERELY_DELAYED"
                elif delay_min > 15.0:
                    disruption_lbl = "SEVERELY_DELAYED"
                elif delay_min > 5.0:
                    disruption_lbl = "DELAYED"
                else:
                    disruption_lbl = "NORMAL"

                # Integrated Record (joining all entities)
                integrated_list.append({
                    "service_date": date_str,
                    "timestamp": timestamp_str,
                    "route_id": r_id,
                    "route_name": r_name,
                    "trip_id": trip_id,
                    "bus_id": bus_id,
                    "registration_number": bus_info["registration_number"],
                    "bus_type": bus_info["bus_type"],
                    "fuel_type": bus_info["fuel_type"],
                    "stop_id": st_id,
                    "stop_name": st_info["stop_name"],
                    "area": st_info["area"],
                    "zone": st_info["zone"],
                    "stop_sequence": seq,
                    "scheduled_arrival": sch_arr_str,
                    "actual_arrival": act_arr_str,
                    "delay_minutes": delay_min,
                    "passenger_count": curr_passengers,
                    "bus_capacity": capacity,
                    "occupancy_percentage": occ_pct,
                    "occupancy_status": occ_status,
                    "temperature": w_info["temperature"],
                    "humidity": w_info["humidity"],
                    "precipitation": w_info["precipitation"],
                    "rain": w_info["rain"],
                    "weather_code": w_info["weather_code"],
                    "traffic_speed": round(base_traffic_speed, 1),
                    "congestion_level": cong_level,
                    "congestion_index": cong_index,
                    "incident_flag": incident_active,
                    "day_of_week": cal_info["day_of_week"],
                    "is_weekend": is_weekend,
                    "is_holiday": is_holiday,
                    "holiday_name": cal_info["holiday_name"],
                    "disruption_label": disruption_lbl
                })

                # ML Dataset 1: Delay Prediction Features & Target
                ml_delay_list.append({
                    "route_id": r_id,
                    "stop_id": st_id,
                    "time": sch_arr_str,
                    "day_of_week": cal_info["day_of_week"],
                    "holiday": is_holiday,
                    "historical_delay": round(random.uniform(2.0, 10.0), 2),
                    "previous_stop_delay": round(max(0.0, delay_min - random.uniform(0.5, 2.0)), 2),
                    "current_speed": gps_speed,
                    "traffic_speed": round(base_traffic_speed, 1),
                    "congestion_level": cong_level,
                    "temperature": w_info["temperature"],
                    "rain": w_info["rain"],
                    "weather_condition": "RAINY" if w_info["rain"] > 0 else "CLEAR",
                    "event_flag": incident_active,
                    "distance_to_next_stop": dist_to_next,
                    "predicted_arrival_time": act_arr_str,
                    "predicted_delay_minutes": delay_min
                })

                # ML Dataset 2: Occupancy Prediction Features & Targets
                ml_occ_list.append({
                    "route_id": r_id,
                    "stop_id": st_id,
                    "time": sch_arr_str,
                    "day_of_week": cal_info["day_of_week"],
                    "holiday": is_holiday,
                    "historical_passenger_count": random.randint(10, 40),
                    "passengers_boarded": boarded,
                    "passengers_alighted": alighted,
                    "previous_stop_occupancy": max(0, curr_passengers - boarded + alighted),
                    "bus_capacity": capacity,
                    "predicted_passenger_count": curr_passengers,
                    "occupancy_percentage": occ_pct,
                    "available_capacity": avail_cap,
                    "occupancy_status": occ_status
                })

                # ML Dataset 3: Disruption Detection Features & Output
                ml_disruption_list.append({
                    "traffic": cong_level,
                    "weather": "HEAVY_RAIN" if w_info["rain"] > 5.0 else ("RAIN" if w_info["rain"] > 0 else "CLEAR"),
                    "events": inc_description,
                    "GPS": bus_st,
                    "current_delay": delay_min,
                    "historical_delay": round(random.uniform(1.0, 8.0), 2),
                    "disruption_label": disruption_lbl
                })

    curr_date += datetime.timedelta(days=1)

print(f"Generated {len(schedule_list)} trip-stop records for 5 full years!")

# Save primary source datasets
df_gtfs = pd.DataFrame(schedule_list)
df_gtfs.to_csv(os.path.join(OUTPUT_DIR, "dataset_01_bus_schedule_gtfs.csv"), index=False)
print(f"Saved dataset_01_bus_schedule_gtfs.csv ({len(df_gtfs)} records)")

df_gps = pd.DataFrame(gps_list)
df_gps.to_csv(os.path.join(OUTPUT_DIR, "dataset_02_bus_gps_realtime.csv"), index=False)
print(f"Saved dataset_02_bus_gps_realtime.csv ({len(df_gps)} records)")

df_actual = pd.DataFrame(actual_arrivals_list)
df_actual.to_csv(os.path.join(OUTPUT_DIR, "dataset_03_actual_bus_arrivals.csv"), index=False)
print(f"Saved dataset_03_actual_bus_arrivals.csv ({len(df_actual)} records)")

df_occ = pd.DataFrame(occupancy_list)
df_occ.to_csv(os.path.join(OUTPUT_DIR, "dataset_04_bus_occupancy.csv"), index=False)
print(f"Saved dataset_04_bus_occupancy.csv ({len(df_occ)} records)")

df_traffic = pd.DataFrame(traffic_list)
df_traffic.to_csv(os.path.join(OUTPUT_DIR, "dataset_05_bengaluru_traffic.csv"), index=False)
print(f"Saved dataset_05_bengaluru_traffic.csv ({len(df_traffic)} records)")

# ---------------------------------------------------------
# 8. USER FEEDBACK DATASET (Dataset 11 - Scaled over 5 Years)
# ---------------------------------------------------------
feedback_types = ["WRONG_ETA", "BUS_NOT_ARRIVED", "OVER_CROWDED", "WRONG_SCHEDULE", "ROUTE_PROBLEM", "OTHER"]
feedback_list = []
# Pick sample records across 5 years
sample_indices = np.random.choice(len(schedule_list), size=1200, replace=False)

for idx, s_idx in enumerate(sample_indices, start=1):
    f_type = random.choice(feedback_types)
    r_sample = schedule_list[s_idx]
    feedback_list.append({
        "feedback_id": f"FB_{idx:05d}",
        "user_id": f"USR_{random.randint(1000, 9999)}",
        "bus_id": r_sample["bus_id"],
        "route_id": r_sample["route_id"],
        "stop_id": r_sample["stop_id"],
        "timestamp": r_sample["service_date"] + " " + r_sample["scheduled_arrival"],
        "feedback_type": f_type,
        "rating": random.randint(1, 5),
        "description": f"User feedback report regarding {f_type.lower().replace('_', ' ')} at {r_sample['stop_name']}.",
        "status": random.choice(["PENDING", "RESOLVED", "INVESTIGATING"]),
        "admin_response": "Under review by traffic controller" if random.random() > 0.5 else "Action taken"
    })

df_feedback = pd.DataFrame(feedback_list)
df_feedback.to_csv(os.path.join(OUTPUT_DIR, "dataset_11_user_feedback.csv"), index=False)
print(f"Saved dataset_11_user_feedback.csv ({len(df_feedback)} records)")

# ---------------------------------------------------------
# 9. CONTROLLER / ADMIN USERS DATASET (Dataset 13)
# ---------------------------------------------------------
admin_list = [
    {"user_id": "ADM_001", "name": "Rajesh Kumar", "email": "rajesh.admin@bmtc.gov.in", "password_hash": "$2b$12$K8j7x9L2M1qP0...", "role": "CHIEF_CONTROLLER", "status": "ACTIVE"},
    {"user_id": "ADM_002", "name": "Priya Sharma", "email": "priya.controller@bmtc.gov.in", "password_hash": "$2b$12$R5v8w1N9P2qX4...", "role": "ZONE_CONTROLLER_EAST", "status": "ACTIVE"},
    {"user_id": "ADM_003", "name": "Anil Rao", "email": "anil.controller@bmtc.gov.in", "password_hash": "$2b$12$M3k9y2L4P1qZ8...", "role": "DISPATCHER", "status": "ACTIVE"},
]
df_admin = pd.DataFrame(admin_list)
df_admin.to_csv(os.path.join(OUTPUT_DIR, "dataset_13_controller_admin.csv"), index=False)
print("Saved dataset_13_controller_admin.csv (3 admin accounts)")

# ---------------------------------------------------------
# 10. SAVE MACHINE LEARNING COMPONENT DATASETS
# ---------------------------------------------------------
df_ml_delay = pd.DataFrame(ml_delay_list)
df_ml_delay.to_csv(os.path.join(OUTPUT_DIR, "ml_delay_prediction_dataset.csv"), index=False)
print(f"Saved ml_delay_prediction_dataset.csv ({len(df_ml_delay)} records)")

df_ml_occ = pd.DataFrame(ml_occ_list)
df_ml_occ.to_csv(os.path.join(OUTPUT_DIR, "ml_occupancy_prediction_dataset.csv"), index=False)
print(f"Saved ml_occupancy_prediction_dataset.csv ({len(df_ml_occ)} records)")

df_ml_disruption = pd.DataFrame(ml_disruption_list)
df_ml_disruption.to_csv(os.path.join(OUTPUT_DIR, "ml_disruption_detection_dataset.csv"), index=False)
print(f"Saved ml_disruption_detection_dataset.csv ({len(df_ml_disruption)} records)")

# ---------------------------------------------------------
# 11. SAVE FINAL INTEGRATED MASTER DATASET (CSV & Parquet)
# ---------------------------------------------------------
df_integrated = pd.DataFrame(integrated_list)
df_integrated.to_csv(os.path.join(OUTPUT_DIR, "final_integrated_dataset.csv"), index=False)
df_integrated.to_parquet(os.path.join(OUTPUT_DIR, "final_integrated_dataset.parquet"), index=False)
print(f"Saved final_integrated_dataset.csv & parquet ({len(df_integrated)} rows x {len(df_integrated.columns)} columns)")

# ---------------------------------------------------------
# 12. BUILD DATA WAREHOUSE (SQLite DB & Star Schema)
# ---------------------------------------------------------
db_path = os.path.join(OUTPUT_DIR, "bmtc_data_warehouse.db")
if os.path.exists(db_path):
    os.remove(db_path)

print("Exporting multi-year data into SQLite Data Warehouse (bmtc_data_warehouse.db)...")
conn = sqlite3.connect(db_path)

# Export staging tables to SQLite database
df_gtfs.to_sql("stg_bus_schedule_gtfs", conn, index=False, if_exists="replace")
df_gps.to_sql("stg_bus_gps_realtime", conn, index=False, if_exists="replace")
df_actual.to_sql("stg_actual_bus_arrivals", conn, index=False, if_exists="replace")
df_occ.to_sql("stg_bus_occupancy", conn, index=False, if_exists="replace")
df_traffic.to_sql("stg_bengaluru_traffic", conn, index=False, if_exists="replace")
df_weather.to_sql("stg_historical_weather", conn, index=False, if_exists="replace")
df_events.to_sql("stg_events_incidents", conn, index=False, if_exists="replace")
df_calendar.to_sql("stg_holiday_calendar", conn, index=False, if_exists="replace")
df_buses.to_sql("stg_bus_master", conn, index=False, if_exists="replace")
df_stops.to_sql("stg_bus_stop_master", conn, index=False, if_exists="replace")
df_feedback.to_sql("stg_user_feedback", conn, index=False, if_exists="replace")
df_roads.to_sql("stg_osm_road_network", conn, index=False, if_exists="replace")
df_admin.to_sql("stg_controller_admin", conn, index=False, if_exists="replace")
df_integrated.to_sql("fact_integrated_bus_operations", conn, index=False, if_exists="replace")

cur = conn.cursor()

# Create Star Schema Tables & Views in SQLite
cur.executescript("""
CREATE TABLE IF NOT EXISTS dim_bus (
    bus_id TEXT PRIMARY KEY,
    registration_number TEXT,
    bus_type TEXT,
    capacity INTEGER,
    seating_capacity INTEGER,
    standing_capacity INTEGER,
    fuel_type TEXT,
    ac_available BOOLEAN
);

INSERT INTO dim_bus SELECT bus_id, registration_number, bus_type, capacity, seating_capacity, standing_capacity, fuel_type, ac_available FROM stg_bus_master;

CREATE TABLE IF NOT EXISTS dim_stop (
    stop_id TEXT PRIMARY KEY,
    stop_name TEXT,
    latitude REAL,
    longitude REAL,
    area TEXT,
    zone TEXT,
    landmark TEXT
);

INSERT INTO dim_stop SELECT stop_id, stop_name, latitude, longitude, area, zone, landmark FROM stg_bus_stop_master;

CREATE TABLE IF NOT EXISTS dim_calendar (
    date TEXT PRIMARY KEY,
    day_of_week TEXT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    holiday_name TEXT,
    is_working_day BOOLEAN
);

INSERT INTO dim_calendar SELECT date, day_of_week, is_weekend, is_holiday, holiday_name, is_working_day FROM stg_holiday_calendar;

-- Analytical SQL View: Route Performance Summary
CREATE VIEW IF NOT EXISTS vw_route_performance_summary AS
SELECT 
    route_id,
    route_name,
    COUNT(trip_id) AS total_trips,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(MAX(delay_minutes), 2) AS max_delay_minutes,
    ROUND(AVG(occupancy_percentage), 1) AS avg_occupancy_pct,
    SUM(CASE WHEN delay_minutes > 10 THEN 1 ELSE 0 END) AS severe_delay_trips
FROM fact_integrated_bus_operations
GROUP BY route_id, route_name;

-- Analytical SQL View: Stop Occupancy & ETA Metrics
CREATE VIEW IF NOT EXISTS vw_stop_occupancy_analytics AS
SELECT 
    stop_name,
    area,
    zone,
    ROUND(AVG(passenger_count), 1) AS avg_passenger_count,
    ROUND(AVG(occupancy_percentage), 1) AS avg_occupancy_pct,
    COUNT(CASE WHEN occupancy_status IN ('HIGH', 'NEARLY_FULL', 'FULL') THEN 1 END) AS high_crowd_instances
FROM fact_integrated_bus_operations
GROUP BY stop_name, area, zone;
""")

conn.commit()
conn.close()
print("Data warehouse bmtc_data_warehouse.db successfully built with Star Schema and analytical views!")

print("\n--- BMTC MULTI-YEAR DATASET GENERATION COMPLETE ---")
print(f"Directory: {OUTPUT_DIR}")
print("Generated Files:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    if f.endswith(".csv") or f.endswith(".parquet") or f.endswith(".db"):
        sz_mb = round(os.path.getsize(os.path.join(OUTPUT_DIR, f)) / (1024 * 1024), 2)
        print(f" - {f} ({sz_mb} MB)")

print("\nAll datasets and data warehouse created successfully for 5-year horizon!")
