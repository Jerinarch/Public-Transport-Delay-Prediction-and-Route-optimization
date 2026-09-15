# Project Proposal: An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning

---

## 1. Project Metadata
* **Project Title:** An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning
* **Academic Level:** Undergraduate B.Tech Final Year (4th Year) Project
* **Milestone:** Review 0 — Refined Problem Statement and Suggested Solution Proposal
* **Sub-Domain:** Machine Learning & Predictive Analytics
* **Core Domains:** Supervised Machine Learning, Explainable AI (XAI), Spatial Clustering, GIS Routing, Data Fusion

> **Sub-Domain Context:** 
> Historical and real-time transit telemetry is leveraged by Machine Learning and Predictive Analytics to uncover complex delay patterns and forecast transit disruptions. In this project, these methods (including XGBoost Classification, LightGBM Regression, and DBSCAN Clustering) are utilized to predict transport delay risks and durations, while dynamically optimizing travel routes via delay-weighted routing algorithms to enhance the efficiency of public transit systems.

---

## 2. Executive Summary
**The Problem:** Urban public transit networks are critical to modern smart cities, yet increasing vehicular traffic, severe weather shocks, and volatile peak-hour commuter demands cause cascading delays that degrade transit reliability and passenger trust. Modern solutions struggle to mitigate these disruptions because they rely on mathematically opaque, "black-box" machine learning models that fail to explain the root causes of delays to operators. Furthermore, these systems are highly sensitive to telemetry noise and GPS/AVL sensor packet drops, treat transit stops as isolated entities without modeling sequential downstream delay propagation, and operate on static timetables that cannot translate predicted delays into dynamic, actionable detours or dispatch decisions.

**The Motivation:** The motivation for this research is to bridge the gap between complex predictive machine learning and real-world, actionable decision support in urban transit. By replacing static schedules and opaque models with an explainable, resilient routing intelligence layer, this project seeks to empower both commuters and transit planners with transparent, real-time insights. The ultimate goal is to minimize average commuter travel times by 12% to 18% during congested incidents, restore public confidence in transit schedules, and provide transit operators with the empirical tools necessary to identify bottleneck hotspots and make proactive dispatch modifications.

**The Solution:** To achieve this, the project proposes **An Intelligent Public Transport Delay Prediction and Route Optimization System** built on a multi-stage machine learning and geospatial framework. The solution integrates a robust K-Nearest Neighbors (KNN) imputer to handle up to 15% sensor telemetry loss, a dual-engine prediction pipeline using an XGBoost Classifier for delay risk probability and a LightGBM Regressor for precise delay duration, and a Schedule-Aware Sequential Delay Propagation (SA-SDP) model to capture cascading delay ripples. These predictions are interpreted using SHAP explainability and ingested by an Explainable Multi-Criteria Dijkstra Routing (X-MCDR) engine to generate dynamic detour options, all of which are deployed on an interactive, dual-perspective Streamlit dashboard tailored for commuters and transit planners.


---

## 3. Formulated Project Objectives

To address the identified research gaps and successfully deliver the proposed system, the following three core project objectives and their detailed sub-objectives have been formulated:

### Objective 1: Develop a Machine Learning model that accurately predicts public transport delays by analyzing historical transit, traffic, weather, and holiday data for top cities (e.g., Chicago, New York)
*   **Sub-Objective 1.1: Multimodal Data Ingestion and Fusion:** Ingest static schedules from GTFS zip files (parsing `routes.txt`, `trips.txt`, `stops.txt`, `stop_times.txt`, and `calendar.txt`) and integrate them with real-time Automatic Vehicle Location (AVL) GPS feeds, meteorological logs (precipitation, visibility, wind speed), and urban traffic congestion scores.
*   **Sub-Objective 1.2: Preprocessing and KNN-Based Telemetry Imputation:** Align GPS traces with scheduled stop sequences, formulate target variables ($\text{Delay} = \text{Actual Time} - \text{Scheduled Time}$), and deploy a K-Nearest Neighbors (KNN) imputer to handle up to 15% missing sensor packets.
*   **Sub-Objective 1.3: Sequential Feature Engineering (SA-SDP):** Design the Schedule-Aware Sequential Delay Propagation (SA-SDP) framework by constructing sequential lag features (e.g., injecting the delay of Stop $i-1$ to predict the delay at Stop $i$) to model network-wide cascading delay propagation.
*   **Sub-Objective 1.4: Dual-Engine Model Training & Tuning:** Train and optimize an XGBoost Classifier for binary delay risk probability and a LightGBM Regressor for precise delay duration in minutes.

### Objective 2: Optimize travel routes by recommending efficient alternative paths based on predicted delays and provide explainable AI
*   **Sub-Objective 2.1: Graph Modeling of the Transit Network:** Represent the target cities' physical street and transit network as a directed weighted graph using OpenStreetMap (OSM) data via the `OSMnx` library.
*   **Sub-Objective 2.2: Dynamic Edge Weight Cost Formulation:** Design a dynamic edge weight function ($\text{Dynamic Cost} = w_1(\text{Base Time}) + w_2(\text{Predicted Delay}) + w_3(\text{Safety Risk})$) that updates graph edges in real-time based on the output of the LightGBM delay regressor.
*   **Sub-Objective 2.3: Explainable Multi-Criteria Dijkstra Routing (X-MCDR):** Implement and run the X-MCDR dynamic pathfinder to search for optimal routes and suggest real-time detours when bottlenecks are predicted.
*   **Sub-Objective 2.4: SHAP Explainability Integration:** Run SHAP (Shapley Additive exPlanations) on predictions to identify local feature contributions and generate natural-language "Detour Cards" (e.g., *"Bypassing segment A due to a heavy rain delay bottleneck"*).

### Objective 3: Design an interactive dashboard that visualizes delay predictions, route performance, and delay hotspots, providing actionable insights for transport authorities
*   **Sub-Objective 3.1: Commuter Portal Development:** Build a Streamlit page featuring delay prediction inputs, Folium/Plotly transit maps color-coded by delay risk, and the dynamic route planner with natural-language explanation cards.
*   **Sub-Objective 3.2: Transit Planner & Operator Portal:** Design a planner dashboard to monitor system-wide transit performance and apply DBSCAN Spatial Clustering to GPS coordinates of delays to visualize smart-city congestion hotspots on heatmaps.
*   **Sub-Objective 3.3: Actionable Rule-Based Recommendations:** Code rule-based heuristics that evaluate recurrent delays to suggest schedule buffer adjustments (e.g., adding 5 minutes of buffer time) or backup vehicle injections.

---

## 4. The Current Problem Statement

### 3.1. Baseline Statement
> *The increasing complexity of urban transportation networks makes it difficult to accurately predict delays and optimize travel routes using conventional scheduling methods. Existing transit management systems provide limited real-time insights, resulting in inefficient vehicle scheduling, longer travel times for commuters, and insufficient decision support for both transit operators and passengers.*

### 3.2. Detailed Industry Pain Points & Research Gaps
To elevate this project to undergraduate final-year research standards, the baseline problem is deconstructed into five core technical gaps identified in contemporary transit literature:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           CORE RESEARCH & INDUSTRY GAPS                           │
├──────────────────┬────────────────────────────────────────────────────────────────┤
│ Gap A:           │ ML models (DNNs, XGBoost) output high-accuracy predictions but │
│ Black-Box Models │ act as "black-boxes", leaving users and operators without      │
│                  │ explanations for delay causes (e.g., weather vs. traffic).     │
├──────────────────┼────────────────────────────────────────────────────────────────┤
│ Gap B:           │ Route optimization algorithms remain static (scheduling stage)  │
│ Static vs. Live  │ and cannot adapt dynamically to real-time road incidents, road │
│ Disruptions      │ closures, or sudden meteorological shocks.                      │
├──────────────────┼────────────────────────────────────────────────────────────────┤
│ Gap C:           │ Real-world GPS/AVL feeds suffer from dropouts (up to 15-20%)   │
│ Telemetry Noise  │ and sensor noise. Standard ML models degrade significantly if  │
│                  │ missing data is not robustly imputed.                         │
├──────────────────┼────────────────────────────────────────────────────────────────┤
│ Gap D:           │ Predictions are often isolated stop-to-stop calculations,      │
│ Isolated Models  │ failing to model downstream cascading delay propagation.       │
├──────────────────┼────────────────────────────────────────────────────────────────┤
│ Gap E:           │ Systems display raw delay minutes but offer no actionable      │
│ Non-Actionable   │ decisions, such as dispatch adjustments for operators or       │
│ Output           │ explainable detour cards for commuters.                       │
└───────────────────────────────────────────────────────────────────────────────────┘
```

1. **Interpretability Deficit ("Black-Box" ML):** High-accuracy models (e.g., Deep Neural Networks, Gradient Boosting) are mathematically opaque. Without local explanations, a transit operator cannot distinguish if a 15-minute delay is caused by temporary weather anomalies or systemic intersection bottlenecks.
2. **Static Timetables vs. Dynamic Real-Time Incidents:** Traditional routing applications rely on static GTFS timetables or historical averages. They fail to dynamically recalculate path weights when real-time operational disruptions (e.g., accidents, waterlogging, sudden surges in passenger boarding) occur.
3. **High Sensitivity to Telemetry Noise & Sensor Gaps:** Live Automatic Vehicle Location (AVL) and GPS streams are highly susceptible to signal loss, urban canyon interference, and missing telemetry packets. Standard systems lack automated, robust imputation pipelines, leading to model failure during data dropouts.
4. **Omission of Network Delay Propagation:** Delays are rarely isolated events; a delay at Stop $i$ naturally cascades to downstream stops $i+1$, $i+2$, etc. Most prediction architectures treat transit stops as independent tabular rows, completely ignoring the sequential, schedule-aware flow of delays.
5. **Absence of Actionable Decision Support:** Existing platforms act as passive notification channels ("Bus 10B is late") rather than decision support tools. They fail to provide commuters with alternative routing based on live delays, and they fail to recommend schedule buffer adjustments or vehicle injection triggers to transit planners.

---

## 5. The Suggested Solution

The proposed solution is **An Intelligent Public Transport Delay Prediction and Route Optimization System**. By merging GTFS static schedules, live/historical AVL logs, meteorological feeds, traffic indices, and calendar events, the system provides a holistic, explainable, and resilient intelligence layer.

```
                              [ MULTIMODAL INGESTION ]
                       (GTFS + AVL Logs + Weather + Traffic)
                                         │
                                         ▼
                             [ KNN IMPUTATION PIPELINE ]
                        (Resolves 15% Sensor Dropouts)
                                         │
                                         ▼
                     [ FEATURE ENGINEERING & SEQUENTIAL SA-SDP ]
                      (Injects Stop i-1 Delay to Stop i Predictor)
                                   ┌─────┴─────┐
                                   ▼           ▼
                         [ XGBOOST CLASSIFIER ] [ LIGHTGBM REGRESSOR ]
                         (Delay Risk Prob %)    (Delay Duration Mins)
                                   └─────┬─────┘
                                         ▼
                             [ SHAP EXPLAINABILITY ENGINE ]
                             (Extracts Local & Global Factors)
                                   ┌─────┴─────┐
                                   ▼           ▼
                       [ DYNAMIC OSM PATHFINDING ] [ DBSCAN HOTSPOT MAP ]
                        (X-MCDR Delay-Weighted Dijkstra) (Geospatial Clustering)
                                   └─────┬─────┘
                                         ▼
                             [ DUAL-PERSPECTIVE DASHBOARD ]
                         (Streamlit: Commuter vs. Planner Views)
```

The system is structured into five core, interconnected modules that directly address the identified research gaps:

### Module 1: Multimodal Data Ingestion & Robust Imputation Pipeline
* **Target Gaps Addressed:** Gap B (Static vs. Live) & Gap C (Telemetry Noise)
* **Technical Approach:** 
  * The system ingests and fuses:
    * **Static Schedules (GTFS):** `routes.txt`, `trips.txt`, `stops.txt`, `stop_times.txt`, and `calendar.txt` to index planned baselines.
    * **Operational Logs/AVL:** Actual arrival and departure timestamps to calculate the ground-truth target variable: $\text{Delay} = \text{Actual Time} - \text{Scheduled Time}$.
    * **Exogenous Context:** Meteorological data (precipitation, visibility) and temporal features (holidays, peak hours, weekends).
  * To ensure robustness against sensor dropouts, the ingestion layer incorporates a **K-Nearest Neighbors (KNN) Imputer** and historical segment-average fallbacks, ensuring prediction stability even with up to 15% missing telemetry.

### Module 2: Explainable ML Delay Prediction Engine
* **Target Gaps Addressed:** Gap A (Black-Box Models)
* **Technical Approach:**
  * **Classification Sub-Engine:** Trains an **XGBoost Classifier** to output binary delay risk ($\text{is\_delayed} = 1$ if delay $> 5$ minutes, else $0$) along with a calibrated probability score (e.g., $78\%$).
  * **Regression Sub-Engine:** Trains a **LightGBM Regressor** to predict the precise delay duration in minutes (e.g., $14.2$ minutes) for all trips flagged as high-risk.
  * **Explainable AI Integration:** Incorporates **SHAP (Shapley Additive exPlanations)**. For every prediction, SHAP calculates the exact contribution of each feature (e.g., Rain: $+5.2$ mins, Congestion: $+8.0$ mins, Peak Hour: $+1.0$ min), converting black-box models into transparent, audit-ready systems.

### Module 3: Schedule-Aware Sequential Delay Propagation (SA-SDP)
* **Target Gaps Addressed:** Gap D (Isolated Models)
* **Technical Approach:**
  * Instead of building resource-intensive Graph Neural Networks (GNNs), the project introduces a highly feasible **Schedule-Aware Sequential Feature Framework**. 
  * When predicting delay at Stop $i$ for Trip $T$, the system injects the actual or predicted delay of Trip $T$ at the upstream stop ($i-1$) as a dynamic feature. This captures cascading delay propagation along the route transit chain using efficient tabular models.

### Module 4: Explainable Multi-Criteria Dijkstra Routing (X-MCDR)
* **Target Gaps Addressed:** Gap B (Static vs. Live) & Gap E (Non-Actionable Output)
* **Technical Approach:**
  * The system represents the road network as a directed graph using **OpenStreetMap (OSM)** data via `OSMnx`.
  * Street segment weights (edges) are dynamically updated using predicted delay regressors: 
    $$\text{Dynamic Cost} = \text{Baseline Travel Time} + \text{Predicted Delay Duration}$$
  * A modified Dijkstra/A* algorithm searches for paths. If a delay bottleneck is detected on the standard path, the system suggests a detour.
  * Crucially, the dashboard renders **Explainable Detour Cards** using SHAP values: *"Bypassing segment B because Stop B has an 82% delay risk driven by heavy rain (+5 min) and traffic (+8 min)."*

### Module 5: Dual-Perspective Interactive Decision Support Dashboard
* **Target Gaps Addressed:** Gap E (Non-Actionable Output)
* **Technical Approach:**
  * Built using **Streamlit, Plotly, and Folium**, the dashboard provides two distinct portals:
    1. **Commuter Portal:** Features delay prediction inputs, estimated arrival times, risk levels (Low, Medium, High), and the X-MCDR dynamic route planner with natural-language detour explanations.
    2. **Transit Planner Portal:** Applies **DBSCAN Clustering** to coordinate logs of recurrent delays to map physical smart-city bottlenecks (hotspots). It generates automated planner recommendations (e.g., *"Route 204 has repeated delays at Stop A during morning peak hours. Suggestion: Add 5 mins buffer or inject 1 backup vehicle"*).

---

## 6. Expected Performance & System Validation
To validate the system's performance and ensure academic excellence, the project defines the following target validation benchmarks:

* **Machine Learning Performance:**
  * **Classification Accuracy:** $\ge 82\%$ (ROC-AUC $\ge 0.85$, F1-score $\ge 0.80$).
  * **Regression MAE (Mean Absolute Error):** $< 3.0$ minutes.
  * **Clustering Silhouette Coefficient:** Positive score verifying distinct, non-overlapping DBSCAN spatial delay clusters.
* **System-Level Impact:**
  * **Commuter Time Savings:** A target of $12\%$ to $18\%$ average travel time reduction under congested simulation scenarios compared to static timetable paths.
  * **Imputation Resilience:** Maintaining prediction accuracy within $3\%$ of the baseline under simulated $15\%$ random sensor packet drops.
