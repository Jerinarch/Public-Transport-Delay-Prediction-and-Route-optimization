# Sub-Domain Definition: Machine Learning & Predictive Analytics

This document contains refined and tailored definitions of the **Machine Learning & Predictive Analytics** sub-domain for **An Intelligent Public Transport Delay Prediction and Route Optimization System**. 

These versions are designed to replace the generalized definition with project-specific language suitable for your presentation slides and project reports.

---

## 1. Presentation Slide Version (Concise)
*Designed for quick reading and high impact on slides.*

> **Sub-Domain:** Machine Learning & Predictive Analytics
>
> In this project, **Machine Learning and Predictive Analytics** leverage historical and real-time transit telemetry (GTFS & AVL) to uncover hidden delay patterns and forecast transit disruptions. By fusing traffic, weather, and schedule data, the system predicts stop-level delay probabilities and dynamically optimizes commuter routes using delay-weighted algorithms, transforming raw data into actionable, explainable transit intelligence.

---

## 2. Project Report Version (Detailed)
*Designed for the project report, thesis, or academic documentation.*

> **Sub-Domain:** Machine Learning & Predictive Analytics
>
> **Machine Learning (ML) and Predictive Analytics** utilize historical datasets to uncover complex, non-linear patterns and forecast future states. Within this project, these methodologies are applied to design a dual-engine prediction pipeline (integrating **XGBoost Classification** and **LightGBM Regression**) that forecasts public transport delay risks and durations. 
> 
> By ingesting static GTFS schedules, real-time Automatic Vehicle Location (AVL) feeds, meteorological conditions, and traffic indices, the predictive models account for cascading downstream delays (via a **Schedule-Aware Sequential Delay Propagation** framework). These predictions are directly integrated into an **Explainable Multi-Criteria Dijkstra Routing (X-MCDR)** engine to dynamically recalculate optimal travel paths, thereby enhancing the operational efficiency of urban public transport systems and improving commuter decision-making.

---

## 3. Bulleted Breakdown of Sub-Domain Application
*Useful for explaining **how** Machine Learning & Predictive Analytics are applied in your project:*

* **Data Fusion & Predictive Modeling:** Integrates scheduled GTFS baselines, real-time GPS telemetry, weather parameters, and traffic congestion indices to predict stop-by-stop delay metrics.
* **Dual-Engine Predictive Pipeline:**
  * **Classification (XGBoost):** Forecasts binary delay risk (e.g., $82\%$ chance of delay $> 5$ minutes).
  * **Regression (LightGBM):** Estimates the precise duration of the expected delay in minutes.
* **Sequential Delay Propagation:** Captures the network-level ripple effect of delays by passing upstream delay features to downstream predictors.
* **Explainable AI (XAI):** Uses **SHAP (Shapley Additive exPlanations)** to interpret model predictions, identifying the exact contribution of factors like traffic, precipitation, or peak-hour surges.
* **Prescriptive Optimization:** Translates predictive delay insights into live, optimized detour routes for commuters and strategic schedule buffer recommendations for transit operators.
