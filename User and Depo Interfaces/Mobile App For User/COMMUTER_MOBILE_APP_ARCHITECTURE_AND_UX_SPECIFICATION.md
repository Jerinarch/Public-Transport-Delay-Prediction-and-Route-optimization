# BMTC SmartCommute: Mobile App Architecture & UX Specification
## Production-Grade Engineering Blueprint for Commuter Mobile Application (Native Android APK)

**System:** Intelligent Public Transport Delay Prediction and Route Optimization System  
**Role:** Senior Mobile Software Architect & Lead Product Designer  
**Platform:** Native Android Application (via Capacitor Engine + OpenStreetMap / Leaflet)  
**Target:** Final Capstone Defense & Live Review Demonstration  
**Author:** Jerin Philip Mathew  

---

## 1. Executive Product Vision & Identity

### 1.1 The Product Concept
**BMTC SmartCommute** is an enterprise-grade, real-time public transit companion designed with the smooth responsiveness and visual elegance of modern ride-hailing applications (**Uber, Ola, Citymapper**), tailored specifically for municipal bus fleets.

Unlike static transit timetable apps that merely print schedules, **BMTC SmartCommute** is an **active intelligence client**:
1. It connects directly to the local transit intelligence engine (FastAPI) via bi-directional WebSockets.
2. It visually streams buses moving smoothly along city streets with bearing-aligned vehicle icons.
3. It implements **Server-Side Spatial Radius Culling (The GTA Technique)**, streaming only vehicles within a localized bubble (default $2.5\text{ km}$), ensuring that mobile memory footprint stays below **$15\text{ MB RAM}$** and runs at a locked **$60\text{ FPS}$** without overheating or crashing.
4. It features **Explainable AI (SHAP) Detour Cards**, providing commuters with clear, human-readable explanations whenever a dynamic route optimization is executed by the central depot.

---

## 2. The 6-Stage User Journey & Screen Flows (Uber/Ola Pattern)

```
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │                           BMTC SMARTCOMMUTE USER FLOW PIPELINE                         │
  └────────────────────────────────────────────────────────────────────────────────────────┘
          │
          ▼
  ┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐
  │   STAGE 1: BOOT &     │ ───►  │  STAGE 2: DISCOVERY   │ ───►  │  STAGE 3: ROUTE &     │
  │   HANDSHAKE           │       │  (GTA Radius Map)     │       │  ETA COMPARISON       │
  │ • Fast Splash (<1s)   │       │ • Nearby stops list   │       │ • Multi-corridor card │
  │ • Server handshake    │       │ • Nearby buses moving │       │ • Predicted delay tag │
  │ • Fallback IP config  │       │ • "Where to?" sheet   │       │ • Occupancy indicator │
  └───────────────────────┘       └───────────────────────┘       └───────────────────────┘
                                                                              │
                                                                              ▼
  ┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐
  │  STAGE 6: DIAGNOSTICS │       │  STAGE 5: DYNAMIC     │       │  STAGE 4: LIVE TRIP   │
  │  & SERVER SETTINGS    │ ◄───  │  DETOUR & SHAP ALERT  │ ◄───  │  TRACKING (EN ROUTE)  │
  │ • Dynamic IP switch   │       │ • Instant WebSocket   │       │ • Bus camera lock     │
  │ • Latency ping check  │       │ • Dashed detour line  │       │ • Stop-by-stop bar    │
  │ • Reconnect trigger   │       │ • Natural reason card │       │ • Real-time countdown │
  └───────────────────────┘       └───────────────────────┘       └───────────────────────┘
```

---

### Detailed Screen Specifications & ASCII Wireframes

#### Screen 1: Instant Handshake & Splash Screen
- **UX Goal:** Boot in under $800\text{ ms}$, verify backend connectivity, and smoothly transition to the live map.
- **Fail-Safe Mechanism:** If the mobile phone cannot reach the default backend address (`http://192.168.x.x:8000`), a clean slide-up dialog prompts the user to enter their laptop's current IP address, avoiding a hard crash.

```
┌──────────────────────────────────────────┐
│ [●●● WiFi               10:30 AM  98%]   │
│                                          │
│                                          │
│              🚌 BMTC                     │
│           SmartCommute                   │
│                                          │
│   Intelligent Delay Prediction System    │
│                                          │
│             [ ⟳ Connecting ]             │
│        Target: 192.168.43.12:8000        │
│                                          │
│                                          │
│     ⚙️ Change Server Connection          │
└──────────────────────────────────────────┘
```

---

#### Screen 2: Discovery & Localized Radius Map (Home Screen)
- **UX Goal:** The core home screen. Mimics Uber's dark/light modern UI with full-screen vector mapping.
- **The "GTA Radius" Experience:** The user’s location is displayed as a pulsing blue dot surrounded by a translucent radius ring ($2.5\text{ km}$). Only buses currently inside this ring are displayed and animated.
- **Bottom Sheet (Collapsed State):** Displays a search bar ("Where are you heading?") and fast-pill buttons for primary transit nodes (`Silk Board`, `Majestic`, `ITPL`, `Hebbal`).

```
┌──────────────────────────────────────────┐
│ [≡] Search or filter routes    [⚙️ Server]│
│──────────────────────────────────────────│
│                                          │
│             ( Outer Ring Road )          │
│                    │                     │
│                [🚌 500D] -> 4 min        │
│                    │                     │
│            ┌───────┴───────┐             │
│            │   (●) You     │             │
│            │  (Bellandur)  │             │
│            └───────┬───────┘             │
│                    │                     │
│                [🚌 500K] -> 11 min       │
│                                          │
│  [🎯 Recenter]              [🔍 2.5 km]  │
│                                          │
│┌────────────────────────────────────────┐│
││ 🔍 Where are you heading?              ││
││ [ Silk Board ] [ ITPL ] [ Majestic ]   ││
││                                        ││
││ 📍 Nearest Stop: Bellandur EcoSpace    ││
││    • Next: Bus 500D (Silk Board) in 4m ││
│└────────────────────────────────────────┘│
└──────────────────────────────────────────┘
```

---

#### Screen 3: Route Search & Options Matrix
- **UX Goal:** When the user selects a destination, the bottom sheet expands to display all available buses serving that corridor.
- **Predictive ML Badge:** Rather than showing only scheduled times, each bus card displays:
  - **Live ETA:** Computed dynamically taking traffic into account.
  - **Delay Classification Badge:**
    - 🟢 `ON TIME` (Delay $\le 3\text{ min}$)
    - 🟡 `DELAYED` (Delay $4\text{ to }12\text{ min}$)
    - 🔴 `SEVERELY DELAYED` (Delay $> 12\text{ min}$)
  - **Live Occupancy:** Derived from the warehouse's optical passenger counter integration (`Seats Available`, `Standing Only`, `Crowded`).

```
┌──────────────────────────────────────────┐
│ [←] Select Transit Option                │
│──────────────────────────────────────────│
│ From: Bellandur EcoSpace                 │
│ To:   Central Silk Board                 │
│──────────────────────────────────────────│
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │ 🚌 ROUTE 500D (Outer Ring Road AC)   │ │
│ │ Arrival: 10:34 AM (in 4 mins)        │ │
│ │ Status:  🟢 ON TIME (+1.2 min delay) │ │
│ │ Crowd:   💺 Plenty of Seats (42%)    │ │
│ │ Fare:    ₹25 • Non-Stop Express      │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │ 🚌 ROUTE 500K (Via Marathahalli)     │ │
│ │ Arrival: 10:41 AM (in 11 mins)       │ │
│ │ Status:  🟡 DELAYED (+8.5 min delay) │ │
│ │ Crowd:   👥 Standing Available (78%) │ │
│ │ Fare:    ₹20 • Regular Ordinary      │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ [  TRACK THIS BUS ON LIVE MAP  ]         │
└──────────────────────────────────────────┘
```

---

#### Screen 4: Live Trip Tracker (En-Route View)
- **UX Goal:** Commuter selects a bus and follows its journey.
- **Camera Auto-Lock:** Map smooth-pans to keep the tracked bus in the viewport.
- **Stop Sequence Bar:** Shows upcoming stops with countdown clocks.

```
┌──────────────────────────────────────────┐
│ [←] Tracking Bus KA-01-F-4502 (500D)     │
│──────────────────────────────────────────│
│                                          │
│                 [🚌 Bus]                 │
│                    │                     │
│                    ▼ (Moving 34 km/h)    │
│              == Agara Junction ==        │
│                    │                     │
│              == Silk Board ==            │
│                                          │
│┌────────────────────────────────────────┐│
││ ⏱️ ETA at Central Silk Board: 14 mins  ││
││ Current Speed: 34 km/h • Green Traffic ││
││────────────────────────────────────────││
││ Next:  Agara Junction (in 5 mins)      ││
││ Final: Central Silk Board (in 14 mins) ││
│└────────────────────────────────────────┘│
└──────────────────────────────────────────┘
```

---

#### Screen 5: Dynamic Disruption & Explainable AI (SHAP) Detour Card
- **UX Goal:** The signature presentation moment.
- **The Event:** When the Depot Manager injects an incident (rain, accident, or gridlock) on their laptop and authorizes a detour:
  1. The mobile phone receives a high-priority WebSocket broadcast.
  2. The phone vibrates (haptic feedback).
  3. The active trajectory line on the map splits: the congested standard corridor turns red/blocked, and a dashed purple line redraws the dynamic detour.
  4. A **SHAP Detour Explanation Card** slides up, providing the exact root-cause metrics.

```
┌──────────────────────────────────────────┐
│ [●●●] ⚠️ ROUTE UPDATE IN PROGRESS         │
│──────────────────────────────────────────│
│                                          │
│               [⛔ BLOCKED] Bellandur     │
│              ············                │
│             :            :               │
│      ======(Detour via Inner Ring)====== │
│             :            :               │
│              ····►[🚌 500D]              │
│                                          │
│┌────────────────────────────────────────┐│
││ ⚠️ ROUTE DETOUR ACTIVE: BUS 500D       ││
││ New ETA: 18 min (Saved ~25 min delay)  ││
││────────────────────────────────────────││
││ 💡 WHY WAS THIS ROUTE CHANGED? (XAI)   ││
││                                        ││
││ • Monsoon Flood: Bellandur (+18.2m)    ││
││   ████████████████████                 ││
││ • Traffic Gridlock: ORR (+14.2m)       ││
││   ██████████████                       ││
││ • Alternate Path Speed: 32 km/h        ││
││   ██████                               ││
││                                        ││
││ "A* dynamic routing rerouted this      ││
││  vehicle to bypass severe bottleneck." ││
││                                        ││
││ [  ACKNOWLEDGE & CONTINUE  ]           ││
│└────────────────────────────────────────┘│
└──────────────────────────────────────────┘
```

---

#### Screen 6: Diagnostics & Dynamic IP Settings Modal
- **UX Goal:** Zero-friction IP switching during your viva.
- **The Problem It Solves:** If your laptop moves from home Wi-Fi to college Wi-Fi or phone hotspot, you never need to recompile the app. Tap the gear icon, type `192.168.43.12:8000`, tap **Save & Reconnect**, and you are live instantly.

```
┌──────────────────────────────────────────┐
│ ⚙️ Connection Diagnostics                │
│──────────────────────────────────────────│
│                                          │
│ Backend Server Address:                  │
│ ┌──────────────────────────────────────┐ │
│ │ http://192.168.43.12:8000            │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ WebSocket Connection Status:             │
│ 🟢 CONNECTED (Ping: 4ms)                 │
│                                          │
│ Active Corridor: Outer Ring Road (500D)  │
│ Local Culling Radius: 2.5 km             │
│ Nearby Buses Tracked: 4 vehicles         │
│                                          │
│ [ TEST CONNECTION ]  [ SAVE & RECONNECT ]│
│                                          │
│ [ Close ]                                │
└──────────────────────────────────────────┘
```

---

## 3. Technical Architecture & Client-Side Engineering

```
┌────────────────────────────────────────────────────────────────────────┐
│               CAPACITOR NATIVE ANDROID WRAPPER (JAVA 21)               │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    COMMUTER APP CORE (SPA)                       │  │
│  │                                                                  │  │
│  │  ┌───────────────────┐  ┌───────────────────┐  ┌──────────────┐  │  │
│  │  │  State Store      │  │  WebSocket Engine │  │ Leaflet Map  │  │  │
│  │  │  (Reactive JS)    │  │  (Auto-Reconnect) │  │  (Hardware)  │  │  │
│  │  └─────────┬─────────┘  └─────────┬─────────┘  └──────┬───────┘  │  │
│  │            │                      │                   │          │  │
│  │            ▼                      ▼                   ▼          │  │
│  │  ┌────────────────────────────────────────────────────────────┐  │  │
│  │  │               SPATIAL CULLING & SLERP ENGINE               │  │  │
│  │  │  • Filters bus markers by radius: |ΔLat| & |ΔLon| <= R     │  │  │
│  │  │  • Smooth 60 FPS marker interpolation between pings        │  │  │
│  │  │  • Prunes off-screen Leaflet DOM elements                  │  │  │
│  │  └────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
│                                     │                                  │
│  ┌──────────────────────────────────▼───────────────────────────────┐  │
│  │              NATIVE BRIDGE (Capacitor Android Core)              │  │
│  │  • Haptics Plugin (vibrates on detour)                           │  │
│  │  • Geolocation Plugin (gets true or simulated user GPS)         │  │
│  │  • AndroidManifest with android:usesCleartextTraffic="true"      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Smooth Marker Animation (SLERP Interpolation)
Bus GPS updates arrive over the WebSocket once per second. Rather than teleporting markers across the map (which looks jarring and amateur), the app uses a **Linear/Spherical Interpolation Loop**:
```javascript
// Updates marker position smoothly across 60 frames between 1-second pings
function animateMarker(marker, startLatLng, endLatLng, durationMs = 1000) {
    const startTime = performance.now();
    function step(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / durationMs, 1.0);
        
        // Linear interpolation
        const currentLat = startLatLng.lat + (endLatLng.lat - startLatLng.lat) * progress;
        const currentLng = startLatLng.lng + (endLatLng.lng - startLatLng.lng) * progress;
        
        marker.setLatLng([currentLat, currentLng]);
        
        if (progress < 1.0) {
            requestAnimationFrame(step);
        }
    }
    requestAnimationFrame(step);
}
```

### 3.2 WebSocket Auto-Reconnection Strategy
In presentation halls, Wi-Fi connections can glitch for a second. The WebSocket engine implements **Exponential Backoff Reconnect**:
```javascript
class TransitSocket {
    constructor(url) {
        this.url = url;
        this.delay = 1000;
        this.maxDelay = 8000;
        this.connect();
    }
    
    connect() {
        this.ws = new WebSocket(this.url);
        this.ws.onopen = () => {
            console.log("Connected to Transit Engine");
            this.delay = 1000; // Reset backoff
            updateStatusBadge(true);
        };
        this.ws.onclose = () => {
            updateStatusBadge(false);
            setTimeout(() => this.connect(), this.delay);
            this.delay = Math.min(this.delay * 1.5, this.maxDelay);
        };
    }
}
```

---

## 4. API & WebSocket Data Contracts

### 4.1 Nearby Buses Request (`GET /api/commuter/nearby-buses`)
**Request Query Parameters:**
- `lat`: `12.9279` (User Latitude)
- `lon`: `77.6271` (User Longitude)
- `radius_km`: `2.5` (Spatial Culling Radius)

**Response Payload (JSON):**
```json
{
  "user_location": {"lat": 12.9279, "lon": 77.6271},
  "culling_radius_km": 2.5,
  "buses_found_count": 3,
  "buses": [
    {
      "trip_id": "TRIP_500D_UP_0845",
      "route_id": "R_500D",
      "route_name": "Hebbal to Silk Board via ORR",
      "bus_registration": "KA-01-F-4502",
      "current_lat": 12.9345,
      "current_lon": 77.6312,
      "bearing": 172.5,
      "speed_kmph": 34.0,
      "next_stop_id": "BS_AGR",
      "next_stop_name": "Agara Junction",
      "predicted_delay_minutes": 1.2,
      "disruption_severity": "NORMAL",
      "occupancy_percentage": 42.0,
      "occupancy_status": "SEATS_AVAILABLE",
      "detour_active": false
    }
  ]
}
```

---

### 4.2 Dynamic Detour & Disruption Push Packet (`WebSocket /ws/stream`)
Broadcasted by the server when the Depot Manager authorizes a dynamic reroute:
```json
{
  "event_type": "DYNAMIC_DETOUR_TRIGGERED",
  "timestamp": "2026-11-02T10:35:12Z",
  "route_id": "R_500D",
  "affected_segment": "Bellandur EcoSpace to Silk Board",
  "disruption_cause": "Severe Monsoon Waterlogging + Intersection Gridlock",
  "predicted_delay_without_detour_min": 32.4,
  "predicted_delay_with_detour_min": 7.6,
  "time_saved_minutes": 24.8,
  "detour_path_coordinates": [
    [12.9345, 77.6312],
    [12.9410, 77.6280],
    [12.9290, 77.6220],
    [12.9176, 77.6234]
  ],
  "shap_explainability": {
    "primary_factor": "Precipitation (45.0 mm/hr)",
    "primary_impact_minutes": 18.2,
    "secondary_factor": "Congestion Index (9.2 / 10.0)",
    "secondary_impact_minutes": 14.2,
    "human_explanation": "Severe waterlogging at Bellandur caused a 32-minute gridlock. Dynamic A* search rerouted this bus via the Inner Ring corridor, saving 25 minutes."
  }
}
```

---

## 5. File Structure for the Implementation

The mobile project will be placed in the requested directory:
```
D:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning\User and Depo Interfaces\Mobile App For User\
│
├── www/                                       # Core Mobile Web Application
│   ├── index.html                             # Single Page Architecture (Uber-style layout)
│   ├── css/
│   │   ├── style.css                          # Modern Dark Theme & Glassmorphism styles
│   │   └── leaflet.css                        # Leaflet vector map styling
│   ├── js/
│   │   ├── app.js                             # Master State Machine & UI Controllers
│   │   ├── socket.js                          # Auto-reconnecting WebSocket Manager
│   │   ├── map_engine.js                      # Leaflet Map, Culling & SLERP Interpolator
│   │   └── config.js                          # Dynamic IP storage & default routes
│   └── assets/
│       ├── bus_icon_green.png                 # Normal bus map pin
│       ├── bus_icon_yellow.png                # Delayed bus map pin
│       ├── bus_icon_red.png                   # Severely delayed bus pin
│       └── logo.png                           # BMTC SmartCommute branding
│
├── capacitor.config.json                      # Native Android Bridge Configuration
├── package.json                               # npm dependencies (@capacitor/core, @capacitor/android)
│
└── android/                                   # Native Android Studio Project (Generated)
    ├── app/
    │   ├── build.gradle                       # Android SDK 34 / 35 dependencies
    │   └── src/main/
    │       ├── AndroidManifest.xml            # Cleartext HTTP & Network Security declarations
    │       └── res/xml/
    │           └── network_security_config.xml # Permitted subnets (192.168.x.x, 10.x.x.x)
    └── gradlew.bat                            # Local Gradle wrapper execution script
```

---

## 6. Native Android Safety Declarations (`AndroidManifest.xml`)

To permanently prevent the Android OS from rejecting local server calls:
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.VIBRATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="BMTC SmartCommute"
        android:usesCleartextTraffic="true"
        android:networkSecurityConfig="@xml/network_security_config"
        android:theme="@style/AppTheme">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|locale|smallestScreenSize|screenLayout|uiMode"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

And `network_security_config.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
</network-security-config>
```

---

## 7. Reviewer Demonstration Script (How to Present this Live)

| Time | Action on Android Phone | Action on Laptop | Examiner Experience |
| :---: | :--- | :--- | :--- |
| **0:00** | Reviewer holds your Android phone. App is open. | You open Depot Manager Dashboard on laptop. | Reviewer sees their stop (Bellandur) and green bus approaching (ETA: 4 min). |
| **0:30** | Phone shows bus moving smoothly. | You toggle **"Monsoon Flood Scenario"** on Outer Ring Road. | Model predicts +32 min delay. Bus turns red on laptop. |
| **0:45** | Phone vibrates. Screen displays **⚠️ Detour Active**. Map route updates. | You show the $A^*$ graph search result on laptop screen. | Reviewer reads natural SHAP explanation card on their phone explaining waterlogging (+18m) and saved time (+25m). |
| **1:15** | Reviewer taps **Diagnostics** gear. | You explain the zero-leakage ML pipeline & spatial radius culling. | Examiners see true hardware-in-the-loop distributed mobile software engineering. |

---

*This document serves as the official mobile architecture and UX specification for the final capstone project submission.*
