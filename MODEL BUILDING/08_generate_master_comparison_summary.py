"""
================================================================================
SCRIPT 08: MASTER COMPARISON & BENCHMARK SUMMARY GENERATOR
Project: BMTC Intelligent Public Transport Delay Prediction & Dynamic Routing
Output Directory: MODEL BUILDING/OUTPUTS/Model_Comparison_Summary/
================================================================================
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_BASE = os.path.join(BASE_DIR, "OUTPUTS")
SUMMARY_DIR = os.path.join(OUTPUTS_BASE, "Model_Comparison_Summary")
os.makedirs(SUMMARY_DIR, exist_ok=True)

def generate_master_summary():
    print("=" * 80)
    print(" BMTC ML PIPELINE: STAGE 08 - MASTER MULTI-MODEL BENCHMARK CONSOLIDATION")
    print("=" * 80)
    
    # 1. Load Regression Metrics
    xgb_reg_path = os.path.join(OUTPUTS_BASE, "Regressor", "XGBoost Regressor", "xgboost_regression_metrics.json")
    bilstm_reg_path = os.path.join(OUTPUTS_BASE, "Regressor", "Bidirectional LSTM with Bahdanau Attention", "bilstm_regression_metrics.json")
    
    reg_rows = []
    if os.path.exists(xgb_reg_path):
        with open(xgb_reg_path, "r", encoding='utf-8') as f:
            xgb_m = json.load(f)
            reg_rows.append({
                "Model Domain": "Regression (Delay Prediction)",
                "Algorithm": "XGBoost Regressor (Tabular Champion)",
                "RMSE (min)": xgb_m["rmse_minutes"],
                "MAE (min)": xgb_m["mae_minutes"],
                "R2 Score": xgb_m["r2_score"],
                "Acc (+/-3 min)": f"{xgb_m['accuracy_within_3min_pct']:.1f}%",
                "Training Time (s)": f"{xgb_m['training_time_seconds']:.1f}",
                "Latency (ms/sample)": f"{xgb_m['inference_latency_ms_per_sample']:.4f}"
            })
            
    if os.path.exists(bilstm_reg_path):
        with open(bilstm_reg_path, "r", encoding='utf-8') as f:
            bilstm_m = json.load(f)
            reg_rows.append({
                "Model Domain": "Regression (Delay Prediction)",
                "Algorithm": "BiLSTM + Bahdanau Attention (Sequential Champion)",
                "RMSE (min)": bilstm_m["rmse_minutes"],
                "MAE (min)": bilstm_m["mae_minutes"],
                "R2 Score": bilstm_m["r2_score"],
                "Acc (+/-3 min)": f"{bilstm_m['accuracy_within_3min_pct']:.1f}%",
                "Training Time (s)": f"{bilstm_m['training_time_seconds']:.1f}",
                "Latency (ms/sample)": f"{bilstm_m['inference_latency_ms_per_sample']:.4f}"
            })
            
    # 2. Load Classification Metrics
    xgb_clf_path = os.path.join(OUTPUTS_BASE, "Classifier", "XGBoost Classifier", "xgboost_classification_metrics.json")
    rf_clf_path = os.path.join(OUTPUTS_BASE, "Classifier", "Random Forest Classifier", "random_forest_classification_metrics.json")
    
    clf_rows = []
    if os.path.exists(xgb_clf_path):
        with open(xgb_clf_path, "r", encoding='utf-8') as f:
            xgb_c = json.load(f)
            clf_rows.append({
                "Model Domain": "Classification (Disruption Severity)",
                "Algorithm": "XGBoost Classifier (Primary Model)",
                "Macro F1": xgb_c["macro_f1"],
                "Weighted F1": xgb_c["weighted_f1"],
                "Balanced Accuracy": xgb_c["balanced_accuracy"],
                "Overall Accuracy": f"{xgb_c['overall_accuracy_pct']:.1f}%",
                "Training Time (s)": f"{xgb_c['training_time_seconds']:.1f}",
                "Latency (ms/sample)": f"{xgb_c['inference_latency_ms_per_sample']:.4f}"
            })
            
    if os.path.exists(rf_clf_path):
        with open(rf_clf_path, "r", encoding='utf-8') as f:
            rf_c = json.load(f)
            clf_rows.append({
                "Model Domain": "Classification (Disruption Severity)",
                "Algorithm": "Random Forest Classifier (Baseline Comparison)",
                "Macro F1": rf_c["macro_f1"],
                "Weighted F1": rf_c["weighted_f1"],
                "Balanced Accuracy": rf_c["balanced_accuracy"],
                "Overall Accuracy": f"{rf_c['overall_accuracy_pct']:.1f}%",
                "Training Time (s)": f"{rf_c['training_time_seconds']:.1f}",
                "Latency (ms/sample)": f"{rf_c['inference_latency_ms_per_sample']:.4f}"
            })
            
    # 3. Load Route Optimization Results
    routing_path = os.path.join(OUTPUTS_BASE, "Route_Optimization", "dynamic_routing_benchmark_results.json")
    routing_data = {}
    if os.path.exists(routing_path):
        with open(routing_path, "r", encoding='utf-8') as f:
            routing_data = json.load(f)
            
    # Build Master DataFrames
    df_reg = pd.DataFrame(reg_rows)
    df_clf = pd.DataFrame(clf_rows)
    
    print("\n[1/3] REGRESSION DELAY PREDICTION BENCHMARK TABLE:")
    print("-" * 80)
    print(df_reg.to_string(index=False))
    
    print("\n[2/3] CLASSIFICATION DISRUPTION SEVERITY BENCHMARK TABLE:")
    print("-" * 80)
    print(df_clf.to_string(index=False))
    
    # Export JSON and CSV
    master_summary = {
        "project_name": "BMTC Intelligent Public Transport Delay Prediction and Route Optimization",
        "dataset": "final_integrated_dataset.csv (729,648 rows, 35 features)",
        "evaluation_partition": "2026 Out-of-Time Test Set",
        "regression_benchmark": reg_rows,
        "classification_benchmark": clf_rows,
        "route_optimization_benchmark": routing_data
    }
    
    json_path = os.path.join(SUMMARY_DIR, "master_model_comparison_table.json")
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(master_summary, f, indent=4)
    print(f"\n  -> Saved Master JSON Summary: {json_path}")
    
    csv_path = os.path.join(SUMMARY_DIR, "master_model_comparison_table.csv")
    combined_df = pd.concat([df_reg, df_clf], ignore_index=True)
    combined_df.to_csv(csv_path, index=False)
    print(f"  -> Saved Master CSV Table: {csv_path}")
    
    # 4. Generate Master Comparison Visualization
    print("\n[3/3] Generating Master Comparison Charts...")
    
    if len(reg_rows) == 2:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
        
        models = [r["Algorithm"].split('(')[0].strip() for r in reg_rows]
        r2_scores = [r["R2 Score"] for r in reg_rows]
        rmse_scores = [r["RMSE (min)"] for r in reg_rows]
        
        sns.barplot(x=models, y=r2_scores, palette=['#1f77b4', '#e377c2'], ax=ax1)
        ax1.set_title('Regression Accuracy: R2 Score (Higher is Better)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('R2 Score', fontsize=10)
        ax1.set_ylim(0, 1.0)
        for i, v in enumerate(r2_scores):
            ax1.text(i, v + 0.02, f"{v:.4f}\n({v*100:.1f}%)", ha='center', fontweight='bold')
            
        sns.barplot(x=models, y=rmse_scores, palette=['#1f77b4', '#e377c2'], ax=ax2)
        ax2.set_title('Regression Error: RMSE in Minutes (Lower is Better)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('RMSE (Minutes)', fontsize=10)
        ax2.set_ylim(0, max(rmse_scores) * 1.3)
        for i, v in enumerate(rmse_scores):
            ax2.text(i, v + 0.1, f"{v:.2f} min", ha='center', fontweight='bold')
            
        plt.tight_layout()
        reg_chart_path = os.path.join(SUMMARY_DIR, "master_regression_comparison_bar.png")
        plt.savefig(reg_chart_path, dpi=300)
        plt.close()
        print(f"  -> Saved Regression Benchmark Chart: {reg_chart_path}")
        
    print("\n" + "=" * 80)
    print(" Master Multi-Model Comparison Complete. All summary files saved to Model_Comparison_Summary/")
    print("=" * 80)

if __name__ == "__main__":
    generate_master_summary()
