# Detailed Project Objectives Breakdown

This document breaks down the three main objectives of the **Intelligent Public Transport Delay Prediction and Route Optimization System** into actionable, project-specific sub-objectives.

---

## Main Objective 1: Develop a Machine Learning model that accurately predicts public transport delays by analyzing historical transit, traffic, weather, and holiday data for top cities (e.g., Chicago, New York)

To achieve this main objective, the following sequential sub-objectives must be completed:

*   **Sub-Objective 1.1: Multimodal Data Ingestion and Fusion**
    *   **Action:** Ingest and parse static schedules from General Transit Feed Specification (GTFS) feeds, extracting tables for scheduled arrival/departure times, routes, trips, and stops (`stop_times.txt`, `routes.txt`, `trips.txt`, `stops.txt`).
    *   **Action:** Integrate actual vehicle movement data by parsing historical and real-time Automatic Vehicle Location (AVL) GPS telemetry logs.
    *   **Action:** Fuse environmental context by pulling meteorological parameters (precipitation, visibility, wind speed) from weather APIs (e.g., OpenWeatherMap) and traffic congestion indexes for target cities (e.g., NYC OpenData, Chicago Data Portal).
    *   **Action:** Incorporate calendar feeds to map national holidays, weekends, and high-ridership events.

*   **Sub-Objective 1.2: Preprocessing and KNN-Based Telemetry Imputation**
    *   **Action:** Map GPS trace coordinate points onto scheduled transit lines and compute target variables (e.g., $\text{Delay} = \text{Actual Arrival Time} - \text{Scheduled Arrival Time}$).
    *   **Action:** Implement a **K-Nearest Neighbors (KNN) Imputer** and historical segment averages to fill data gaps, ensuring model stability under up to 15% random GPS sensor dropouts.

*   **Sub-Objective 1.3: Sequential Feature Engineering (SA-SDP)**
    *   **Action:** Construct temporal lag features (hour of day, day of week) and peak-hour indicators.
    *   **Action:** Develop the **Schedule-Aware Sequential Delay Propagation (SA-SDP)** framework by linking sequential stop features (e.g., passing the actual delay at Stop $i-1$ as a feature to predict the delay at Stop $i$) to model cascading delay ripples.

*   **Sub-Objective 1.4: Dual-Engine Model Training & Optimization**
    *   **Action:** Train an **XGBoost Classifier** to predict binary delay risk ($\text{is\_delayed} = 1$ if delay $> 5$ mins, else $0$) along with a probability score.
    *   **Action:** Train a **LightGBM Regressor** to predict the precise delay duration in minutes for the high-risk transit runs.
    *   **Action:** Conduct hyperparameter tuning to satisfy performance benchmarks (Classification ROC-AUC $\ge 0.85$, Regression MAE $< 3.0$ minutes).

---

## Main Objective 2: Optimize travel routes by recommending efficient alternative paths based on predicted delays and provide explainable AI

To achieve this main objective, the following sequential sub-objectives must be completed:

*   **Sub-Objective 2.1: Transit Graph Representation**
    *   **Action:** Extract and model the physical street and transit network of target cities as a directed graph using **OpenStreetMap (OSM)** data via the `OSMnx` library.
    *   **Action:** Map transit stops and routes onto the nearest graph vertices and edges.

*   **Sub-Objective 2.2: Dynamic Edge Weight Cost Formulation**
    *   **Action:** Define a multi-criteria cost function for graph edges that updates dynamically:
        $$\text{Cost} = w_1(\text{Base Travel Time}) + w_2(\text{Predicted Delay Duration}) + w_3(\text{Weather Congestion Risk})$$
    *   **Action:** Bind cost recalculation hooks to the outputs of the LightGBM delay regressor, making the road network cost model responsive to live predictive alerts.

*   **Sub-Objective 2.3: Explainable Multi-Criteria Dijkstra Routing (X-MCDR)**
    *   **Action:** Develop and execute an **Explainable Multi-Criteria Dijkstra Routing (X-MCDR)** algorithm to run shortest-path queries.
    *   **Action:** Configure the algorithm to automatically calculate dynamic alternative detour paths when standard transit corridors experience high predicted delays.

*   **Sub-Objective 2.4: SHAP Explainability Integration**
    *   **Action:** Run **SHAP (Shapley Additive exPlanations)** on the predictive models during routing queries to isolate the main feature impact (e.g., weather contribution vs. traffic contribution).
    *   **Action:** Translate SHAP feature impact scores into natural-language explanation cards (e.g., *"Bypassing segment B because Stop B has an 82% delay risk driven by heavy rain (+5 min) and traffic (+8 min)"*).

---

## Main Objective 3: Design an interactive dashboard that visualizes delay predictions, route performance, and delay hotspots, providing actionable insights for transport authorities

To achieve this main objective, the following sequential sub-objectives must be completed:

*   **Sub-Objective 3.1: Commuter Portal Dashboard Development**
    *   **Action:** Build a frontend page in **Streamlit** for passengers to input their starting stop, destination, and departure time.
    *   **Action:** Embed interactive **Folium** maps displaying standard and alternative routes, with stops color-coded by predicted delay risk (Low, Medium, High).
    *   **Action:** Display natural-language SHAP explainability cards alongside recommended detour routes to explain route adjustments to passengers.

*   **Sub-Objective 3.2: Transit Planner Portal & Hotspot Mapping**
    *   **Action:** Build an administrative dashboard view to visualize system-wide transit performance metrics.
    *   **Action:** Apply **DBSCAN Spatial Clustering** to coordinates of delayed transit logs to identify and render recurring smart-city delay hotspots on a heatmap.

*   **Sub-Objective 3.3: Actionable Rule-Based Recommendations**
    *   **Action:** Code rule-based heuristics that evaluate recurrent delays and suggest buffer adjustments (e.g., *"Route 204 has repeated delays at Stop A. Suggestion: Add 5 mins buffer to the timetable"*).
    *   **Action:** Generate dispatcher dashboard notifications recommending auxiliary vehicle injections when a route's average delay exceeds operating limits.
