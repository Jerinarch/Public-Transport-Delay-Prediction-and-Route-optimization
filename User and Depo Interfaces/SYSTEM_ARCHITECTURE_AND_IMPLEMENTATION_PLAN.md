# Comprehensive System Architecture & Implementation Plan
## Native Android APK (Commuter App) + Desktop Web Application (Depot Manager)

**Project:** An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning (BMTC Bengaluru)  
**Milestone:** Final Capstone Defense & Live System Demonstration  
**Author:** Jerin Philip Mathew  

---

## 1. System Overview & Dual-Perspective Architecture

The goal is to deliver an end-to-end, real-time transportation intelligence platform consisting of:
1. **A Native Android APK (`app-debug.apk`)** running on an Android smartphone for commuters.
2. **A Desktop Web Application** running on a laptop/desktop browser for the Depot Manager.
3. **A High-Performance Asynchronous Python Backend (FastAPI)** connecting both applications via REST and WebSockets, hosting the trained ML models and in-memory live simulation engine.

```
                                  ==================================================
                                    INTELLIGENT TRANSIT SYSTEM RUNTIME ARCHITECTURE
                                  ==================================================

    [ REVIEWER'S ANDROID PHONE ]                                              [ YOUR LAPTOP / DESKTOP ]
    ╔════════════════════════════════════╗                  ╔═══════════════════════════════════════════════════════╗
    ║       COMMUTER MOBILE APK          ║                  ║              DEPOT MANAGER WEB PORTAL                 ║
    ║   (Capacitor + Leaflet Map)        ║                  ║         (Vanilla JS + Chart.js + Heatmaps)            ║
    ║                                    ║                  ║                                                       ║
    ║  • GTA Radius Spatial Culling      ║                  ║  • System-Wide Corridor Health Overview               ║
    ║  • Real-Time Bus GPS Tracking      ║                  ║  • Live DBSCAN Congestion Hotspot Heatmap             ║
    ║  • Dynamic ETA & Delay Badges      ║                  ║  • Incident Injection Control (Monsoon / Breakdown)   ║
    ║  • Natural-Language SHAP Cards     ║                  ║  • Dynamic A* Detour Approval & Dispatch Alert        ║
    ╚════════════════════════════════════╝                  ╚═══════════════════════════════════════════════════════╝
                      ▲                                                                ▲
                      │                                                                │
                      │  WebSocket Broadcast & REST APIs                               │  WebSocket Broadcast & REST APIs
                      │  (Local Hotspot / 192.168.x.x:8000)                            │  (http://localhost:8000)
                      ▼                                                                ▼
    ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
    ║                                      FASTAPI CENTRAL BACKEND ENGINE (api_server.py)                              ║
    ║                                                                                                                   ║
    ║   ┌───────────────────────────────┐  ┌────────────────────────────────┐  ┌────────────────────────────────────┐   ║
    ║   │  In-Memory Telemetry Engine   │  │   Real-Time ML Inference       │  │   Spatial Radius Culling Engine    │   ║
    ║   │  • 1-Sec Bus GPS Simulation   │  │   • XGBoost Delay Regressor    │  │   • Haversine Bounding Box Filter  │   ║
    ║   │  • Zero-Locking State Dict    │  │   • Disruption Classifier      │  │   • <15 MB Mobile RAM Footprint    │   ║
    ║   └───────────────────────────────┘  └────────────────────────────────┘  └────────────────────────────────────┘   ║
    ║   ┌───────────────────────────────┐  ┌────────────────────────────────┐  ┌────────────────────────────────────┐   ║
    ║   │ Dynamic A* & Dijkstra Routing │  │ DBSCAN Spatial Clustering      │  │ Read-Only Star Schema Warehouse    │   ║
    ║   │ • Live Graph Edge Cost Update │  │ • Pre-computed Hotspot Clusters│  │ • bmtc_data_warehouse.db (WAL Mode)│   ║
    ║   │ • Alternative Detour Generator│  │ • GeoJSON Lat/Lon Feed         │  │ • Fast OLAP SQL Aggregations       │   ║
    ║   └───────────────────────────────┘  └────────────────────────────────┘  └────────────────────────────────────┘   ║
    ╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 2. The 5 Zero-Crash Engineering Constraints

To guarantee that the system **never crashes, never hangs, and requires zero cloud payments ($0.00)** during the presentation, every component is governed by strict technical constraints:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE 5 ZERO-CRASH ENGINEERING CONSTRAINTS                                  │
├──────────────────────┬──────────────────────────────────────────┬──────────────────────────────────────┤
│ CONSTRAINT DOMAIN    │ POTENTIAL CRASH OR FAILURE POINT         │ GUARANTEED ENGINEERING SOLUTION      │
├──────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ 1. Android Security  │ Android 9-15 blocks unencrypted http://  │ Configure usesCleartextTraffic="true"│
│    & Connectivity    │ calls, crashing app with Network Error.  │ in AndroidManifest.xml and provide a │
│                      │ College Wi-Fi blocks peer communication. │ Settings Modal to dynamically set IP.│
│                      │                                          │ Use phone's Personal Hotspot.        │
├──────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ 2. Mobile Memory     │ Streaming all 6,000 buses to mobile      │ Server-Side GTA Radius Culling:      │
│    (Spatial Culling) │ exhausts phone RAM, causing Android to   │ Server only transmits buses within a │
│                      │ terminate the app (Low Memory Killer).   │ 2.5 km bounding box (3-6 buses max). │
│                      │                                          │ Mobile RAM stays under 15 MB.        │
├──────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ 3. Database Write    │ Concurrent writes to the 742 MB SQLite   │ SQLite opened strictly in Read-Only  │
│    Locking           │ database throw "OperationalError:        │ WAL mode. Active live simulation     │
│                      │ database is locked".                     │ runs in FastAPI in-memory RAM state. │
├──────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ 4. Build Toolchain   │ System Java 23 crashes Gradle with       │ Set JAVA_HOME to Android Studio's    │
│    Compatibility     │ "Unsupported class file major version 67"│ bundled OpenJDK 21 (jbr directory),  │
│                      │ during APK generation.                   │ guaranteeing flawless Gradle builds. │
├──────────────────────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ 5. Latency & Budget  │ Heavy re-computation causes UI freeze    │ Pre-load XGBoost (.joblib) once at   │
│    Management        │ when clicking "Simulate Incident".       │ startup. Inference latency is <2ms.  │
│                      │                                          │ A* runs on corridor subgraph (<1ms). │
└──────────────────────┴──────────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 3. End-to-End User Experience & Interaction Workflow

### Phase A: Normal Operations (Initial State)
1. **Depot Manager Screen:**
   - Displays all 4 arterial corridors: `R_500D` (Outer Ring Road), `R_500K` (Banashankari $\leftrightarrow$ ITPL), `R_500CA` (Tin Factory $\leftrightarrow$ Electronic City), `R_335E` (Majestic $\leftrightarrow$ ITPL).
   - Real-time KPI cards show: Fleet Punctuality ($94.2\%$), Average Corridor Delay ($1.4\text{ min}$), Active Disruption Level (**NORMAL**).
   - Buses appear on the live map as smooth-gliding green icons.
2. **Commuter Mobile App (Phone):**
   - The user opens the installed BMTC Commuter APK.
   - The map centers on the commuter's selected stop (e.g., Bellandur EcoSpace).
   - Only buses within a 2.5 km radius are rendered.
   - The commuter selects their route (`R_500D`) and destination (Silk Board).
   - Live Card displays: **Bus KA-01-F-4502 | ETA: 12 mins | Status: ON TIME**.

### Phase B: The Incident Injection (Demonstrating ML Delay Prediction)
1. **Depot Manager Action:**
   - The manager opens the **Disruption Simulator Drawer** on the dashboard.
   - Selects Corridor: `R_500D` (Outer Ring Road).
   - Injects Scenario: **Monsoon Flash Flood + Bellandur Gridlock**.
   - Sliders update: Rain $= 45.0\text{ mm/hr}$, Traffic Speed drops from $38\text{ km/h}$ to $8\text{ km/h}$.
2. **Instant System Response:**
   - FastAPI feeds the new features into the trained **XGBoost Delay Regressor** and **Disruption Classifier**.
   - Model outputs: Predicted Delay $= \mathbf{+32.4\text{ minutes}}$, Severity $= \mathbf{SEVERELY\_DELAYED}$.
   - The bus icon turns flashing **RED** on the Depot Manager screen.
   - An alert appears in the Depot Portal: *"Warning: Headway irregular on R_500D. Predicted bunching risk at Marathahalli."*

### Phase C: Dynamic Route Optimization & Real-Time Detour Approval
1. **The Optimization Engine Fires:**
   - The dynamic $A^*$ routing algorithm evaluates the road network graph.
   - Cost on Outer Ring Road edge exceeds threshold due to $W(e) = T_{\text{base}} + \hat{\text{Delay}}_{\text{ML}} + \text{Cost}_{\text{incident}}$.
   - $A^*$ generates an optimized detour path: Detouring via Old Airport Road / Indiranagar Inner Ring Road $\rightarrow$ Silk Board.
   - Travel Time Savings: **Saved 24.8 minutes** compared to waiting in gridlock.
2. **Depot Manager Dispatches Detour:**
   - Manager clicks **"Authorize Dynamic Detour"**.
   - The event is published across the WebSocket channel.

### Phase D: Instant Mobile Commuter Synchronization & Explainable AI (SHAP)
1. **Mobile App Updates (Zero Refresh Needed):**
   - The phone vibrates subtly.
   - The bus trajectory on the phone's map dynamically recalculates, drawing a dashed purple detour line.
   - A modal slide-up card appears:
     ```
     ┌─────────────────────────────────────────────────────────────┐
     │ ⚠️ DYNAMIC DETOUR IN EFFECT: BUS R_500D                     │
     ├─────────────────────────────────────────────────────────────┤
     │ New Route: Rerouted via Indiranagar / Koramangala           │
     │ New ETA: 18 mins (Saved ~25 mins vs standard route)         │
     ├─────────────────────────────────────────────────────────────┤
     │ 💡 WHY THIS ROUTE? (Explainable AI / SHAP):                 │
     │ • Severe Waterlogging at Bellandur (+18.2 min delay impact) │
     │ • Traffic Gridlock at Marathahalli (+14.2 min delay impact) │
     │ • Alternate Corridor Speed: 32 km/h (Smooth Flow)           │
     └─────────────────────────────────────────────────────────────┘
     ```

---

## 4. Technical Implementation Specifications

### 4.1 Backend Engine (`api_server.py`)
- **Framework:** FastAPI + Uvicorn (ASGI asynchronous event loop).
- **In-Memory State Store:**
  - `active_buses`: Dictionary containing vehicle ID, lat, lon, heading, route ID, delay minutes, status.
  - `active_scenarios`: Current weather/traffic overrides per corridor.
- **Background Tasks:**
  - `simulate_telemetry_loop()`: Asynchronous task sleeping 1000ms, incrementally interpolating bus GPS coordinates along the corridor polyline so vehicles visibly move on screen.
- **REST & WebSocket Endpoints:**
  - `GET /api/health`: Server heartbeat and active connections.
  - `GET /api/manager/corridors`: Returns GeoJSON polyline and stops for all 4 corridors.
  - `GET /api/manager/hotspots`: Returns pre-calculated DBSCAN cluster centers from the warehouse.
  - `POST /api/manager/inject-incident`: Accepts weather/traffic overrides, triggers ML inference and $A^*$ reroute.
  - `POST /api/manager/approve-detour`: Broadcasts reroute to all listening mobile clients.
  - `GET /api/commuter/nearby-buses`: Accepts `lat`, `lon`, and `radius_km` (implements the GTA radius bounding box).
  - `WebSocket /ws/stream`: Unified pub/sub stream sending JSON state diffs every second.

### 4.2 Depot Manager Web Application (`depot_manager/`)
- **Technology:** Pure HTML5, Vanilla CSS3 (custom dark glassmorphism design system), and JavaScript (ES6+).
- **Libraries:**
  - `Leaflet.js` (for interactive street mapping and smooth marker transitions).
  - `Chart.js` (for live corridor delay distributions and punctuality gauges).
- **Interface Layout:**
  - **Header:** Live system clock, active buses count, websocket status indicator, and corridor selector.
  - **Left Sidebar:** Incident simulator drawer with interactive sliders (Rain, Congestion, Incident Flag) and ML prediction breakdown.
  - **Center Map:** Full-screen Leaflet map displaying active corridors, live buses, DBSCAN bottleneck heatmap layer toggle, and detour polylines.
  - **Right Panel:** Live dispatch log, delay alerts, and "Approve Reroute" action cards.

### 4.3 Commuter Mobile App (`commuter_mobile/`)
- **Technology:** Mobile-first responsive HTML5/CSS3 interface packaged into a Native Android Studio project via **Capacitor**.
- **Mobile-Specific Features:**
  - Native Touch Gestures & Pull-to-Refresh.
  - Fixed-ratio smartphone viewport with modern bottom navigation sheet.
  - **Radius Selector:** Commuters can adjust their radius (1.0 km, 2.5 km, 5.0 km).
  - **Connection Settings Modal:** Accessible via a subtle gear icon in the top header. Allows setting the laptop server IP (`http://192.168.x.x:8000`) without recompiling the APK.
  - **SHAP Explanation Drawer:** Expands to show local feature attribution waterfall bars explaining delay root causes in plain English.

---

## 5. Step-by-Step Build & Verification Roadmap

```
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 1: FASTAPI BACKEND & SIMULATION ENGINE                                            │
  │ - Create `api_server.py` loading XGBoost regressor and corridor graphs.                │
  │ - Implement in-memory 1-second GPS step simulator and GTA radius filter.               │
  │ - Verify endpoints with curl / browser.                                                │
  └────────────────────────────────────────┬───────────────────────────────────────────────┘
                                           │
                                           ▼
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 2: DEPOT MANAGER WEB APPLICATION                                                  │
  │ - Build high-res control dashboard (`depot_manager/index.html`, `style.css`, `app.js`). │
  │ - Connect Leaflet map to WebSocket stream and render live moving buses.                │
  │ - Connect Incident Simulation panel to ML prediction and A* detour endpoints.          │
  └────────────────────────────────────────┬───────────────────────────────────────────────┘
                                           │
                                           ▼
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 3: COMMUTER MOBILE FRONTEND                                                       │
  │ - Build mobile-first commuter UI (`commuter_mobile/www/index.html`, `style.css`, etc). │
  │ - Integrate localized radius filtering, ETA calculations, and SHAP detour cards.       │
  │ - Test in browser responsive mobile mode.                                              │
  └────────────────────────────────────────┬───────────────────────────────────────────────┘
                                           │
                                           ▼
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 4: CAPACITOR INTEGRATION & NATIVE ANDROID CONFIGURATION                           │
  │ - Initialize Capacitor: `npx @capacitor/cli create` or `cap add android`.             │
  │ - Configure `AndroidManifest.xml` with `android:usesCleartextTraffic="true"`.          │
  │ - Configure `network_security_config.xml` for local subnet communication.              │
  └────────────────────────────────────────┬───────────────────────────────────────────────┘
                                           │
                                           ▼
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ STEP 5: GRADLE COMPILATION & APK VERIFICATION                                          │
  │ - Point `JAVA_HOME` to `C:\Program Files\Android\Android Studio\jbr` (OpenJDK 21).     │
  │ - Execute `gradlew assembleDebug` to compile `app-debug.apk`.                          │
  │ - Install via `adb install` on phone and verify real-time hotspot communication.       │
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Verification Checklist Before Project Review

- [ ] **Laptop & Phone on Same Hotspot:** Phone Hotspot is turned on, laptop connected. Both on `192.168.x.x`.
- [ ] **FastAPI Running:** `python api_server.py` starts cleanly, loads models in <2 seconds, WebSockets open on port 8000.
- [ ] **Depot Web App Operational:** Accessible at `http://localhost:8000/manager`.
- [ ] **APK Installed & Permitted:** `app-debug.apk` launches on phone with cleartext network access enabled.
- [ ] **Incident Reroute Flow Verified:** Triggering monsoon rain on laptop instantly displays the detour and SHAP explanation card on the phone screen within 500 milliseconds.
