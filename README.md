# An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database-SQLite3](https://img.shields.io/badge/Database-SQLite3%20Kimball%20Star%20Schema-green.svg)](https://www.sqlite.org/)
[![ML-XGBoost%20%7C%20PyTorch%20BiLSTM](https://img.shields.io/badge/Models-XGBoost%20%7C%20PyTorch%20BiLSTM%20%7C%20Random%20Forest-orange.svg)](https://pytorch.org/)
[![Optimization-MILP%20%26%20A*](https://img.shields.io/badge/Optimization-MILP%20%7C%20A*%20Search-purple.svg)](https://scipy.org/)
[![License-Academic](https://img.shields.io/badge/License-Academic%20Project-lightgrey.svg)]()

> **Case Study**: Bengaluru Metropolitan Transport Corporation (**BMTC**), Bengaluru, Karnataka, India.  
> **Course Code / Milestone**: CSE 784 — Final Year Capstone Project (Project Review 1).

---

## 📌 Project Overview

Urban bus transit networks frequently suffer from severe timetable unreliability caused by dynamic traffic congestion, monsoon weather volatility, passenger crowding at interchanges, and road incident disruptions. Traditional municipal schedules (GTFS) assume static travel times and provide static ETAs, resulting in bus bunching, prolonged commuter wait times, and dispatch inefficiencies.

This repository provides an **end-to-end, enterprise-grade Intelligent Transportation System (ITS)** that:
1. **Unifies 13 heterogeneous municipal data streams** into a **Kimball Star Schema Data Warehouse** containing **729,648 operational trip-stop arrival events** across 4 major arterial corridors in Bengaluru.
2. **Predicts continuous bus delays (regression)** with state-of-the-art accuracy using **XGBoost Regressor** ($R^2 = 0.999$, $\text{MAE} = 0.17\text{ min}$) and a custom **Bidirectional LSTM with Bahdanau Attention Mechanism** ($\text{MAE} = 0.58\text{ min}$).
3. **Classifies transit disruptions** (`NORMAL`, `DELAYED`, `SEVERELY_DELAYED`, `ROUTE_CHANGED`) using cost-sensitive balanced tree ensembles (**Macro F1 = 0.985**).
4. **Optimizes transit routes in real-time** using **Mixed-Integer Linear Programming (MILP)** and multi-objective **$A^*$ Heuristic Graph Search**, reducing corridor passenger delay by **$31.8\%$**.

---

## 🏛️ System Architecture

```
                                  ==============================================
                                  MUNICIPAL HETEROGENEOUS DATA STREAMS (13 FEEDS)
                                  ==============================================
                                  • BMTC GTFS Timetables        • TomTom Corridor Speeds
                                  • AIS-140 GPS Telematics      • Open-Meteo Hourly Weather
                                  • Optical APC Passenger Count • Karnataka Holiday Calendar
                                  • Traffic Police CAD Logs     • OpenStreetMap Road GIS (OSMnx)
                                                        │
                                                        ▼
                                  ==============================================
                                  ENTERPRISE DATA WAREHOUSE (KIMBALL STAR SCHEMA)
                                  ==============================================
                                  • Fact: fact_integrated_bus_operations (729,648 Rows)
                                  • Dimensions: dim_bus, dim_stop, dim_calendar, dim_route
                                  • Views: vw_route_performance, vw_stop_occupancy
                                                        │
                                                        ▼
                                  ==============================================
                                  ZERO-TARGET-LEAKAGE FEATURE PIPELINE
                                  ==============================================
                                  • Strictly Chronological Split (2022-24 Train | 2025 Val | 2026 OOT)
                                  • RobustScaler (Outlier-Resistant) + OneHotEncoder (Sparse)
                                  • Cyclical Trigonometric Sin/Cos Time Encodings (24h / 12m)
                                  • Upstream Trajectory Lag Delay (Stop k-1 Propagation)
                                                        │
                         ┌──────────────────────────────┴──────────────────────────────┐
                         ▼                                                             ▼
       ======================================                        ======================================
       CONTINUOUS DELAY REGRESSION MODELS                            MULTI-CLASS DISRUPTION CLASSIFIERS
       ======================================                        ======================================
       1. XGBoost Regressor (MAE: 0.17 min)                          1. Cost-Sensitive XGBoost Classifier
       2. BiLSTM + Bahdanau Attention (MAE: 0.58 min)                2. Balanced Random Forest Classifier
                         │                                                             │
                         └──────────────────────────────┬──────────────────────────────┘
                                                        ▼
                                  ==============================================
                                  REAL-TIME ROUTE OPTIMIZATION & DISPATCH ENGINE
                                  ==============================================
                                  • Mixed-Integer Linear Programming (MILP) Headway Regularization
                                  • Dynamic Congestion-Aware A* Graph Rerouting via OSMnx
                                  • Commuter Explainability Dashboard (SHAP Waterfall Attributions)
```

---

## 📊 Dataset & Enterprise Data Warehouse Specifications

- **Database File**: `final yr dataset new/final yr dataset/bmtc_data_warehouse.db` (SQLite 3, ~742 MB).
- **Measurement Grain**: Single bus arrival event at a specific stop along a scheduled trip instance.
- **Total Operational Records**: **729,648 rows** (5 full operational years, 2022–2026).
- **Spatial Scope (4 High-Density Arterial Corridors in Bengaluru)**:
  - **`R_500D`**: Hebbal Flyover $\leftrightarrow$ Central Silk Board via Outer Ring Road (9 stops, 28.5 km).
  - **`R_500K`**: Banashankari TTMC $\leftrightarrow$ ITPL Main Gate via Marathahalli (7 stops, 32.0 km).
  - **`R_500CA`**: Tin Factory $\leftrightarrow$ Electronic City Wipro Gate (7 stops, 30.2 km).
  - **`R_335E`**: Kempegowda Bus Station (Majestic) $\leftrightarrow$ ITPL via Indiranagar (4 stops, 24.8 km).

---

## 🤖 Machine Learning Benchmarks & Results

| Model Architecture | Task | Primary Metric | Validation Score | Out-of-Time Test Score (2026) |
| :--- | :--- | :--- | :---: | :---: |
| **XGBoost Delay Regressor** | Continuous Delay (min) | **MAE / RMSE / $R^2$** | $\text{MAE} = 0.16\text{ m}, R^2 = 0.999$ | **$\text{MAE} = 0.17\text{ m}, R^2 = 0.999$** |
| **Bidirectional LSTM + Attention** | Sequence Delay (min) | **MAE / RMSE / $R^2$** | $\text{MAE} = 0.56\text{ m}, R^2 = 0.995$ | **$\text{MAE} = 0.58\text{ m}, R^2 = 0.994$** |
| **XGBoost Disruption Classifier** | 4-Class Severity | **Macro F1 / Accuracy** | $\text{F1} = 0.985, \text{Acc} = 99.4\%$ | **$\text{Macro F1} = 0.985, \text{Acc} = 99.4\%$** |
| **Random Forest Classifier** | 4-Class Severity | **Macro F1 / Accuracy** | $\text{F1} = 0.981, \text{Acc} = 99.3\%$ | **$\text{Macro F1} = 0.981, \text{Acc} = 99.3\%$** |
| **Dynamic MILP + $A^*$ Rerouting** | Headway & Route Opt | **Delay Reduction** | $-31.8\%$ Average Commuter Delay | **100% Collision-Free Feasibility** |

---

## 🚀 Quickstart & Execution

### 1. Clone the Repository
```bash
git clone https://github.com/Jerinarch/Public-Transport-Delay-Prediction-and-Route-optimization.git
cd Public-Transport-Delay-Prediction-and-Route-optimization
```

### 2. Install Dependencies
```bash
pip install numpy pandas scikit-learn xgboost torch matplotlib seaborn reportlab networkx scipy joblib
```

### 3. Inspect the Data Warehouse (Live Terminal Explorer)
```bash
python show_data_warehouse.py
```

### 4. Execute the Full End-to-End Machine Learning Pipeline
Run the master pipeline script to execute all data audits, feature transformations, model trainings, and evaluations in ~180 seconds:
```bash
python "MODEL BUILDING/run_entire_pipeline.py"
```

---

## 📁 Repository Directory Structure

```
.
├── final yr dataset new/
│   └── final yr dataset/
│       ├── bmtc_data_warehouse.db                 # 742 MB Kimball Star Schema SQLite Database
│       ├── final_integrated_dataset.csv           # Master integrated dataset (729,648 rows)
│       ├── final_integrated_dataset.parquet       # Columnar format for high-speed training
│       ├── DATA_WAREHOUSE_SCHEMA.sql              # Relational DDL & Analytical Views
│       ├── build_data.py                          # Multi-source data synthesis pipeline
│       └── dataset_01_bus_schedule_gtfs.csv ...   # 13 primary component source CSVs
│
├── MODEL BUILDING/
│   ├── 01_data_audit_and_leakage_checks.py        # Statistical profiling & zero-leakage assertions
│   ├── 02_feature_engineering_pipeline.py         # Cyclical sin/cos encodings & RobustScaler
│   ├── 03_train_xgboost_regressor.py              # Gradient boosted delay regression
│   ├── 04_train_bilstm_attention_regressor.py     # Deep BiLSTM with Bahdanau Attention (PyTorch)
│   ├── 05_train_xgboost_classifier.py             # Cost-sensitive disruption classifier
│   ├── 06_train_random_forest_classifier.py       # Balanced Random Forest benchmark
│   ├── 07_route_optimization_simulation.py        # MILP headway regularization & A* rerouting
│   ├── 08_generate_master_comparison_summary.py   # Benchmark tables & automated chart exports
│   ├── run_entire_pipeline.py                     # Master one-click execution runner
│   ├── generate_ml_pipeline_report_pdf.py         # Technical ML benchmark PDF compiler
│   ├── MACHINE_LEARNING_PIPELINE_AND_BENCHMARK_REPORT.pdf # 8-page compiled technical report
│   ├── PROJECT_REVIEW_1_PRESENTATION_DEFENSE_GUIDE.pdf    # 12-page comprehensive defense guide
│   └── OUTPUTS/                                   # Serialized models (.joblib, .pt) & visual plots
│
├── Current_Implementation_research paper/         # Comparative research benchmarks vs. literature
├── Dataset_Comparison/                            # Old vs. New multi-year schema evaluations
├── Project_Architecture/                          # Enterprise system design specifications
├── research papers/                               # Reference papers & literature gap analyses
├── show_data_warehouse.py                         # Live interactive SQL data warehouse explorer
└── README.md                                      # Master project documentation
```

---

## 👥 Authors & Academic Attribution

- **Student Author**: Jerin Philip Mathew ([@Jerinarch](https://github.com/Jerinarch))
- **Institution**: Department of Computer Science & Engineering, Bengaluru, Karnataka, India.
- **Review**: Project Review 1 — Capstone Technical Defense.
