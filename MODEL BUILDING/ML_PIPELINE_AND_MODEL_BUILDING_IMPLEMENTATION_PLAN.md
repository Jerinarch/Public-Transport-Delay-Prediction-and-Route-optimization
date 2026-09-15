# ENTERPRISE ML PIPELINE & EXPERIMENTAL BENCHMARKING PLAN
## Intelligent Public Transport Delay Prediction and Route Optimization System (BMTC Case Study)

---

### EXECUTIVE SPECIFICATION & MODEL HIERARCHY
- **Dataset Reference**: `final yr dataset new/final yr dataset/final_integrated_dataset.csv` (729,648 rows, 35 features, Date Range: `2022-01-01` to `2026-08-16`)
- **Primary Focus**: Experimental Model Evaluation, Performance Comparison, Metric Profiling & Explainability (No deployment/FastAPI services in this phase).
- **Target Leakage Protocol**: Strict Zero-Leakage Architecture with Purged Temporal Splits.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       PRIMARY EXPERIMENTAL MODEL HIERARCHY & STORAGE MAP                                         │
├─────────────────────────┬──────────────────────────────────────────┬─────────────────────────────────────────────────────────────┤
│ MODELING DOMAIN         │ MODEL FAMILY & SPECIFICATION             │ DEDICATED OUTPUT STORAGE DIRECTORY                          │
├─────────────────────────┼──────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 🏆 Regression           │ 1st: XGBoost Regressor                   │ D:\An Intelligent Public Transport Delay Prediction and     │
│    (Delay Prediction    │ - Fast CPU tabular baseline              │     Route Optimization System Using Machine Learning\       │
│     in Minutes)         │ - Domain features (traffic, weather, etc)│     MODEL BUILDING\OUTPUTS\Regressor\XGBoost Regressor\     │
│                         ├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│                         │ 2nd: Bidirectional LSTM with Attention   │ D:\An Intelligent Public Transport Delay Prediction and     │
│                         │ - 3 Layers, 32 Units, Bahdanau Attention │     Route Optimization System Using Machine Learning\       │
│                         │ - Dropout: 0.383, Learning Rate: 1.54e-3 │     MODEL BUILDING\OUTPUTS\Regressor\                       │
│                         │ - 31K params, Trajectory sequence memory │     Bidirectional LSTM with Bahdanau Attention\             │
│                         │ - Skip: PatchTST, Autoformer, xLSTM      │                                                             │
├─────────────────────────┼──────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 🎯 Classification       │ 1st: XGBoost Classifier                  │ D:\An Intelligent Public Transport Delay Prediction and     │
│    (Disruption Severity │ - Multi-class (`multi:softprob`)         │     Route Optimization System Using Machine Learning\       │
│     & Occupancy Status) │ - Class-weighted loss for rare incidents │     MODEL BUILDING\OUTPUTS\Classifier\XGBoost Classifier\   │
│                         ├──────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│                         │ 2nd: Random Forest Classifier            │ D:\An Intelligent Public Transport Delay Prediction and     │
│                         │ - Tree ensemble comparison baseline      │     Route Optimization System Using Machine Learning\       │
│                         │ - Built-in Gini feature importance       │     MODEL BUILDING\OUTPUTS\Classifier\                      │
│                         │                                          │     Random Forest Classifier\                               │
├─────────────────────────┼──────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 🗺️ Route Optimization   │ Dynamic ML-Augmented Dijkstra & A*       │ MODEL BUILDING\OUTPUTS\Route_Optimization\                  │
│ 📊 Global Comparison    │ Unified Metrics & Benchmark Dashboard    │ MODEL BUILDING\OUTPUTS\Model_Comparison_Summary\            │
└─────────────────────────┴──────────────────────────────────────────┴─────────────────────────────────────────────────────────────┘
```

---

```
                                  ==================================================
                                    EXPERIMENTAL MACHINE LEARNING WORKFLOW & STAGES
                                  ==================================================

 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 1: INGESTION & ZERO-LEAKAGE AUDIT (`01_data_audit_and_leakage_checks.py`)                                  │
 │ - Verify 729,648 rows, 35 columns, dtypes, nulls (`holiday_name`), and chronologically sort by timestamp         │
 │ - Automated zero-leakage assertions: Confirm strict exclusion of `actual_arrival` and target-derived columns     │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                          │
                                                          ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 2: LEAKAGE-FREE FEATURE ENGINEERING & TEMPORAL SPLITTING (`02_feature_engineering_pipeline.py`)           │
 │ - Purged Temporal Split: Train (2022-2024, 70%), Val (2025, 15%), Test (2026, 15% Out-of-Time)                   │
 │ - Cyclical time features (sin/cos hour & month), Peak hour flags, Stop sequence lags, Weather severity index     │
 │ - Sequence 3D Tensor Generation for BiLSTM (`[batch_size, sequence_length_stops, feature_dim]`)                 │
 │ - Scikit-Learn `ColumnTransformer` (RobustScaler, OneHotEncoder) fit ONLY on Train split                         │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                          │
                                                          ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 3: REGRESSION EXPERIMENTS (`03_train_xgboost_regressor.py` & `04_train_bilstm_attention_regressor.py`)     │
 │ - Model 1: XGBoost Regressor -> Output to `OUTPUTS/Regressor/XGBoost Regressor/`                                 │
 │ - Model 2: Bidirectional LSTM with Bahdanau Attention -> Output to `OUTPUTS/Regressor/BiLSTM Attention/`        │
 │ - Outputs: Model files, JSON metrics (RMSE, MAE, R², Acc ±3min), SHAP beeswarm & Attention Heatmaps             │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                          │
                                                          ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 4: CLASSIFICATION EXPERIMENTS (`05_train_xgboost_classifier.py` & `06_train_random_forest_classifier.py`) │
 │ - Model 1: XGBoost Multi-Class Classifier -> Output to `OUTPUTS/Classifier/XGBoost Classifier/`                  │
 │ - Model 2: Random Forest Classifier -> Output to `OUTPUTS/Classifier/Random Forest Classifier/`                   │
 │ - Targets: (A) Disruption Label (4 classes), (B) Occupancy Status (5 classes)                                    │
 │ - Outputs: Model files, Classification metrics (Macro F1, Balanced Acc), Confusion matrices & Gini charts        │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                          │
                                                          ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 5: DYNAMIC ROUTE OPTIMIZATION SIMULATION (`07_route_optimization_simulation.py`)                          │
 │ - Build OSM Road Network Graph (`dim_road_network`) across Bengaluru transit corridors                           │
 │ - Inject real-time ML delay predictions into dynamic edge cost function: $W(e) = T_0(e) + \hat{\text{Delay}}_{ML}(e) + \text{Cost}_{inc}$ │
 │ - Benchmark Dijkstra vs A* Search -> Output to `OUTPUTS/Route_Optimization/`                                     │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                          │
                                                          ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 6: MASTER BENCHMARK & COMPARISON SUMMARY (`08_generate_master_comparison_summary.py`)                     │
 │ - Ingest all individual model JSON metrics and compile master comparison table (CSV & JSON)                      │
 │ - Output to `OUTPUTS/Model_Comparison_Summary/`                                                                  │
 └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. TARGET DEFINITIONS & ZERO-LEAKAGE FEATURE MATRIX

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FEATURE SPACE & TARGET SEGREGATION MATRIX                                      │
├──────────────────────┬──────────────────────────────────────────────┬────────────────────────────────────────────┤
│ MODELING OBJECTIVE   │ INCLUDED FEATURES ($X$)                      │ STRICTLY EXCLUDED FEATURES (LEAKAGE)       │
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────────────────────┤
│ 1. Bus Delay         │ - Route & Bus: `route_id`, `bus_type`,       │ ❌ `actual_arrival` (Direct target math)   │
│    Prediction        │   `fuel_type`, `bus_capacity`                │ ❌ `disruption_label` (Derived from delay) │
│    (Regression)      │ - Spatial: `stop_id`, `area`, `zone`,        │ ❌ `passenger_count` (Unobserved at sched) │
│                      │   `stop_sequence`                            │ ❌ `occupancy_percentage`                  │
│    Target:           │ - Temporal: `sched_hour`, `sched_min`,       │ ❌ `occupancy_status`                      │
│    `delay_minutes`   │   `day_of_week`, `is_weekend`, `is_holiday`  │ ❌ Future stop records for same trip       │
│                      │ - Weather: `temperature`, `humidity`,        │                                            │
│                      │   `precipitation`, `rain`, `weather_code`    │                                            │
│                      │ - Traffic: `traffic_speed`, `congestion_idx` │                                            │
│                      │ - Incident: `incident_flag`                  │                                            │
│                      │ - Lagged: `lag_delay_prev_stop` (Stop $k-1$) │                                            │
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────────────────────┤
│ 2. Disruption        │ - Environmental: `temperature`, `humidity`,  │ ❌ `actual_arrival` (Direct leakage)       │
│    Detection         │   `precipitation`, `rain`, `weather_code`    │ ❌ `delay_minutes` (Used in formula to     │
│    (Multi-Class      │ - Traffic: `traffic_speed`, `congestion_idx`,│    create `disruption_label`)              │
│    Classification)   │   `congestion_level`                         │ ❌ Future sequence observations            │
│                      │ - Spatial/Temporal: `route_id`, `stop_id`,   │                                            │
│    Target:           │   `sched_hour`, `day_of_week`, `is_holiday`  │                                            │
│    `disruption_label`│ - Incident: `incident_flag`                  │                                            │
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────────────────────┤
│ 3. Passenger         │ - Route & Spatial: `route_id`, `stop_id`,    │ ❌ `passenger_count` (Mathematical formula │
│    Occupancy         │   `stop_sequence`, `area`, `zone`            │    used to construct target)               │
│    Prediction        │ - Temporal: `sched_hour`, `day_of_week`,     │ ❌ `occupancy_percentage` (Direct target   │
│    (Classification)  │   `is_weekend`, `is_holiday`                 │    translation identity)                   │
│                      │ - Fleet: `bus_type`, `bus_capacity`          │ ❌ `actual_arrival`                        │
│    Target:           │ - Environmental & Traffic context            │                                            │
│    `occupancy_status`│                                              │                                            │
└──────────────────────┴──────────────────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 2. STRICT TEMPORAL DATA SPLITTING

```
[2022-01-01 ────────────────────────────── 2024-12-31] │ [2025-01-01 ─────── 2025-12-31] │ [2026-01-01 ─────── 2026-08-16]
                  TRAIN SET (70%)                      │       VALIDATION SET (15%)      │      OUT-OF-TIME TEST (15%)
                 (~510,750 instances)                  │       (~109,450 instances)      │       (~109,448 instances)
```

- **Train Set (2022-01-01 to 2024-12-31)**: Preprocessor fitting & model weight training.
- **Validation Set (2025-01-01 to 2025-12-31)**: Hyperparameter optimization & early stopping.
- **Out-of-Time Test Set (2026-01-01 to 2026-08-16)**: Final holdout evaluation and comparison.

---

## 3. DETAILED DIRECTORY OUTPUT SPECIFICATIONS

```
D:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning\MODEL BUILDING\OUTPUTS\
│
├── Regressor/
│   ├── XGBoost Regressor/
│   │   ├── xgboost_delay_regressor_model.joblib          <-- Serialized trained model
│   │   ├── xgboost_regression_metrics.json               <-- RMSE, MAE, R², MAPE, Acc ±3min
│   │   ├── xgboost_actual_vs_predicted_scatter.png       <-- Actual vs Predicted plot
│   │   ├── xgboost_residual_distribution_plot.png        <-- Error distribution & Q-Q plot
│   │   ├── xgboost_shap_summary_beeswarm.png             <-- TreeSHAP feature attribution plot
│   │   └── xgboost_shap_local_waterfall.png              <-- Single trip delay explanation
│   │
│   └── Bidirectional LSTM with Bahdanau Attention/
│       ├── bilstm_attention_model.pt                     <-- PyTorch model weights
│       ├── bilstm_regression_metrics.json                <-- RMSE, MAE, R², MAPE, Acc ±3min
│       ├── bilstm_training_loss_curves.png               <-- Train/Val convergence curves
│       ├── bilstm_actual_vs_predicted_scatter.png        <-- Actual vs Predicted trajectory plot
│       ├── bilstm_stop_attention_weights_heatmap.png     <-- Attention matrix across stops 1..9
│       └── bilstm_integrated_gradients_attribution.png   <-- Feature importance gradients
│
├── Classifier/
│   ├── XGBoost Classifier/
│   │   ├── xgboost_classifier_model.joblib               <-- Trained classifier model
│   │   ├── xgboost_classification_metrics.json           <-- Macro F1, Balanced Acc, PR-AUC
│   │   ├── xgboost_confusion_matrix.png                  <-- Normalized confusion matrix
│   │   ├── xgboost_precision_recall_curves.png           <-- Multi-class PR curves
│   │   └── xgboost_classifier_shap_importance.png       <-- Disruption driver importances
│   │
│   └── Random Forest Classifier/
│       ├── random_forest_classifier_model.joblib         <-- Trained RF model
│       ├── random_forest_classification_metrics.json     <-- Macro F1, Balanced Acc, Gini
│       ├── random_forest_confusion_matrix.png            <-- Normalized confusion matrix
│       ├── random_forest_gini_feature_importance.png     <-- MDI Gini importance bar chart
│       └── random_forest_decision_tree_sample.png        <-- Visual sub-tree for viva defense
│
├── Route_Optimization/
│   ├── dynamic_routing_benchmark_results.json            <-- Travel time savings, latency
│   ├── dijkstra_vs_astar_speed_comparison.png            <-- Execution latency comparison
│   └── dynamic_rerouting_trajectory_map.png              <-- Detour path around congestion
│
├── Preprocessor/
│   ├── column_transformer_preprocessor.joblib            <-- Fitted Scalers & Encoders
│   └── sequence_tensor_generator.joblib                  <-- 3D tensor sequence config
│
└── Model_Comparison_Summary/
    ├── master_model_comparison_table.json                <-- All models side-by-side
    ├── master_model_comparison_table.csv                 <-- Excel/CSV formatted table
    └── master_benchmark_radar_chart.png                  <-- Visual trade-off comparison chart
```

---

## 4. EXPERIMENTAL SCRIPT ARCHITECTURE

All scripts will be placed inside `MODEL BUILDING/`:
1. `01_data_audit_and_leakage_checks.py`: Ingestion validation, nulls, and automated zero-leakage assertions.
2. `02_feature_engineering_pipeline.py`: Temporal split, `ColumnTransformer`, and 3D sequence tensors (`[batch, seq_len=9, features]`).
3. `03_train_xgboost_regressor.py`: Tabular regression training, TreeSHAP, and output export to `OUTPUTS/Regressor/XGBoost Regressor/`.
4. `04_train_bilstm_attention_regressor.py`: 3-layer BiLSTM with Bahdanau Attention in PyTorch, Attention Heatmap extraction, and export to `OUTPUTS/Regressor/Bidirectional LSTM with Bahdanau Attention/`.
5. `05_train_xgboost_classifier.py`: Multi-class disruption classification with class weighting, PR curves, and export to `OUTPUTS/Classifier/XGBoost Classifier/`.
6. `06_train_random_forest_classifier.py`: Random Forest classifier baseline with Gini feature importances, export to `OUTPUTS/Classifier/Random Forest Classifier/`.
7. `07_route_optimization_simulation.py`: Dynamic Dijkstra vs A* routing with ML edge penalty, export to `OUTPUTS/Route_Optimization/`.
8. `08_generate_master_comparison_summary.py`: Master multi-model benchmark consolidation, export to `OUTPUTS/Model_Comparison_Summary/`.

---

## 5. STEP-BY-STEP EXECUTION SCHEDULE

Execution will proceed in strict order upon your command:
1. **Step 1**: Ingestion & Leakage Check
2. **Step 2**: Feature Engineering & Sequence Generation
3. **Step 3**: XGBoost Regressor Training & Evaluation
4. **Step 4**: Bidirectional LSTM with Attention Training & Evaluation
5. **Step 5**: XGBoost Classifier Training & Evaluation
6. **Step 6**: Random Forest Classifier Training & Evaluation
7. **Step 7**: Dynamic Route Optimization Simulation
8. **Step 8**: Master Benchmark Consolidation
