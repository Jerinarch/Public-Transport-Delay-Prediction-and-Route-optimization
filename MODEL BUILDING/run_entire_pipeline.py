"""
================================================================================
MASTER PIPELINE RUNNER: END-TO-END EXECUTION SUITE
Project: BMTC Intelligent Public Transport Delay Prediction & Dynamic Routing
================================================================================
"""

import os
import sys
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = [
    ("01_data_audit_and_leakage_checks.py", "Data Ingestion Profiling & Zero-Leakage Asserter"),
    ("02_feature_engineering_pipeline.py", "Spatial-Temporal Feature Engineering & Purged Splits"),
    ("03_train_xgboost_regressor.py", "Train XGBoost Regressor (Edge Inference Model)"),
    ("04_train_bilstm_attention_regressor.py", "Train BiLSTM with Bahdanau Attention (Deep Trajectory Model)"),
    ("05_train_xgboost_classifier.py", "Train Multi-Class XGBoost Disruption Classifier"),
    ("06_train_random_forest_classifier.py", "Train Random Forest Disruption Classifier Baseline"),
    ("07_route_optimization_simulation.py", "Run Dynamic A* & Dijkstra Route Optimization on OSM Graph"),
    ("08_generate_master_comparison_summary.py", "Compile Master Model Comparison Table & Charts"),
]

def run_master_pipeline():
    print("=" * 80)
    print("  🚀 STARTING COMPLETE END-TO-END MACHINE LEARNING & ROUTING PIPELINE")
    print("  Project: Intelligent Public Transport Delay Prediction & Dynamic Routing")
    print("=" * 80)
    
    total_start = time.time()
    
    for idx, (script, desc) in enumerate(SCRIPTS, start=1):
        script_path = os.path.join(BASE_DIR, script)
        print(f"\n[{idx}/{len(SCRIPTS)}] EXECUTING: {script}")
        print(f"  -> Purpose: {desc}")
        print("-" * 80)
        
        t0 = time.time()
        result = subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
        t_elapsed = time.time() - t0
        
        if result.returncode != 0:
            print(f"\n❌ ERROR: Execution failed for {script} (Exit code: {result.returncode})")
            sys.exit(result.returncode)
        
        print(f"  -> Finished {script} successfully in {t_elapsed:.2f} seconds.")
    
    total_elapsed = time.time() - total_start
    print("\n" + "=" * 80)
    print(f"  🎉 ALL 8 PIPELINE STAGES COMPLETED SUCCESSFULLY IN {total_elapsed:.2f} SECONDS!")
    print(f"  All models, evaluation metrics, SHAP plots, and reports saved to:")
    print(f"  d:\\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning\\MODEL BUILDING\\OUTPUTS\\")
    print("=" * 80)

if __name__ == '__main__':
    run_master_pipeline()
