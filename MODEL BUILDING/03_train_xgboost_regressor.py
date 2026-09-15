"""
================================================================================
SCRIPT 03: XGBOOST REGRESSOR (PRIMARY TABULAR CHAMPION)
Project: BMTC Intelligent Public Transport Delay Prediction & Dynamic Routing
Output Directory: MODEL BUILDING/OUTPUTS/Regressor/XGBoost Regressor/
================================================================================
"""

import os
import sys
import json
import joblib
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
import shap

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Set visual style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREPROCESSOR_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Preprocessor")
OUTPUT_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Regressor", "XGBoost Regressor")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def train_and_evaluate_xgboost():
    print("=" * 80)
    print(" BMTC ML PIPELINE: STAGE 03 - XGBOOST REGRESSOR TRAINING & EVALUATION")
    print("=" * 80)
    
    # 1. Load Preprocessed Tabular Splits
    cache_path = os.path.join(PREPROCESSOR_DIR, "processed_splits_tabular.joblib")
    print(f"[1/5] Loading preprocessed dataset splits from: {cache_path}")
    data = joblib.load(cache_path)
    
    X_train, y_train = data['X_train'], data['y_train_reg']
    X_val, y_val = data['X_val'], data['y_val_reg']
    X_test, y_test = data['X_test'], data['y_test_reg']
    feature_names = data['feature_names_out']
    
    print(f"  -> Train instances: {X_train.shape[0]:,}, Features: {X_train.shape[1]}")
    print(f"  -> Val instances:   {X_val.shape[0]:,}")
    print(f"  -> Test instances:  {X_test.shape[0]:,} (2026 Out-of-Time Holdout)")
    
    # 2. Configure and Fit XGBoost Regressor
    print("\n[2/5] Initializing XGBoost Regressor with early stopping...")
    model = xgb.XGBRegressor(
        n_estimators=1000,
        learning_rate=0.03,
        max_depth=7,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.1,
        reg_lambda=1.0,
        early_stopping_rounds=50,
        random_state=42,
        tree_method='hist',
        n_jobs=-1
    )
    
    start_time = time.time()
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=100
    )
    train_duration = time.time() - start_time
    print(f"  -> Training Completed in: {train_duration:.2f} seconds (Best Iteration: {model.best_iteration})")
    
    # 3. Evaluate Performance Metrics on 2026 Out-of-Time Test Set
    print("\n[3/5] Evaluating performance metrics on 2026 Test Set...")
    inference_start = time.time()
    y_pred = model.predict(X_test)
    inference_duration = time.time() - inference_start
    latency_per_sample_ms = (inference_duration / len(X_test)) * 1000.0
    
    rmse = float(np.sqrt(np.mean((y_test - y_pred) ** 2)))
    mae = float(np.mean(np.abs(y_test - y_pred)))
    r2 = float(1.0 - (np.sum((y_test - y_pred) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2)))
    mape = float(np.mean(np.abs((y_test - y_pred) / (np.abs(y_test) + 1.0))) * 100.0)
    acc_3min = float(np.mean(np.abs(y_test - y_pred) <= 3.0) * 100.0)
    acc_5min = float(np.mean(np.abs(y_test - y_pred) <= 5.0) * 100.0)
    
    print("=" * 60)
    print("  [BENCHMARK] XGBOOST REGRESSOR (2026 TEST SET)")
    print("  ------------------------------------------------------------")
    print(f"  -> Root Mean Squared Error (RMSE): {rmse:.4f} minutes")
    print(f"  -> Mean Absolute Error (MAE):       {mae:.4f} minutes")
    print(f"  -> Coefficient of Determination (R2): {r2:.4f} ({r2*100:.2f}%)")
    print(f"  -> Mean Absolute Percentage Error:   {mape:.2f}%")
    print(f"  -> Accuracy within +/- 3 Minutes:    {acc_3min:.2f}%")
    print(f"  -> Accuracy within +/- 5 Minutes:    {acc_5min:.2f}%")
    print(f"  -> Average Inference Latency:        {latency_per_sample_ms:.4f} ms/query")
    print("=" * 60)
    
    # Save Metrics JSON
    metrics_data = {
        "model_name": "XGBoost Regressor",
        "evaluation_dataset": "2026 Out-of-Time Test Partition",
        "test_instances_count": int(len(y_test)),
        "rmse_minutes": rmse,
        "mae_minutes": mae,
        "r2_score": r2,
        "mape_percentage": mape,
        "accuracy_within_3min_pct": acc_3min,
        "accuracy_within_5min_pct": acc_5min,
        "training_time_seconds": train_duration,
        "best_iteration": int(model.best_iteration),
        "inference_latency_ms_per_sample": latency_per_sample_ms
    }
    
    metrics_path = os.path.join(OUTPUT_DIR, "xgboost_regression_metrics.json")
    with open(metrics_path, "w", encoding='utf-8') as f:
        json.dump(metrics_data, f, indent=4)
    print(f"  -> Saved Metrics: {metrics_path}")
    
    # Save Model Artifact
    model_path = os.path.join(OUTPUT_DIR, "xgboost_delay_regressor_model.joblib")
    joblib.dump(model, model_path)
    print(f"  -> Saved Model Artifact: {model_path}")
    
    # 4. Generate Publication-Quality Visualizations
    print("\n[4/5] Generating evaluation charts and residual diagnostic plots...")
    
    # Plot 1: Actual vs Predicted Scatter
    fig, ax = plt.subplots(figsize=(9, 7))
    sample_indices = np.random.choice(len(y_test), size=min(15000, len(y_test)), replace=False)
    ax.scatter(y_test[sample_indices], y_pred[sample_indices], alpha=0.25, color='#1f77b4', edgecolors='none', s=15, label='Trip Instances')
    max_val = max(np.percentile(y_test, 99.5), np.percentile(y_pred, 99.5))
    ax.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Perfect Prediction (1:1 Line)')
    ax.set_title(f'XGBoost Regressor: Actual vs. Predicted Delay (R2 = {r2:.4f}, RMSE = {rmse:.2f} min)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Actual Observed Delay (Minutes)', fontsize=11)
    ax.set_ylabel('Model Predicted Delay (Minutes)', fontsize=11)
    ax.set_xlim(-2, max_val + 5)
    ax.set_ylim(-2, max_val + 5)
    ax.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    scatter_path = os.path.join(OUTPUT_DIR, "xgboost_actual_vs_predicted_scatter.png")
    plt.savefig(scatter_path, dpi=300)
    plt.close()
    print(f"  -> Saved Actual vs Predicted Plot: {scatter_path}")
    
    # Plot 2: Residual Distribution Plot
    residuals = y_test - y_pred
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    sns.histplot(residuals, bins=60, kde=True, color='#2ca02c', ax=ax1)
    ax1.axvline(0, color='red', linestyle='--', linewidth=1.5)
    ax1.set_title('Residual Error Distribution (Actual - Predicted)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Prediction Error (Minutes)', fontsize=10)
    ax1.set_xlim(-15, 15)
    
    ax2.scatter(y_pred[sample_indices], residuals[sample_indices], alpha=0.25, color='#9467bd', s=15)
    ax2.axhline(0, color='red', linestyle='--', linewidth=1.5)
    ax2.set_title('Residuals vs. Predicted Delay', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Predicted Delay (Minutes)', fontsize=10)
    ax2.set_ylabel('Residual (Minutes)', fontsize=10)
    ax2.set_ylim(-20, 20)
    plt.tight_layout()
    residual_path = os.path.join(OUTPUT_DIR, "xgboost_residual_distribution_plot.png")
    plt.savefig(residual_path, dpi=300)
    plt.close()
    print(f"  -> Saved Residual Diagnostic Plot: {residual_path}")
    
    # 5. TreeSHAP Feature Attributions via Native XGBoost contribs
    print("\n[5/5] Computing TreeSHAP global and local feature attributions...")
    shap_sample_idx = np.random.choice(len(X_test), size=min(1000, len(X_test)), replace=False)
    X_shap_sample = X_test[shap_sample_idx]
    
    dmat = xgb.DMatrix(X_shap_sample)
    contribs = model.get_booster().predict(dmat, pred_contribs=True)
    shap_values = contribs[:, :-1]
    expected_value = contribs[0, -1]
    
    # Beeswarm Plot
    fig = plt.figure(figsize=(10, 7))
    shap.summary_plot(shap_values, X_shap_sample, feature_names=feature_names, max_display=15, show=False)
    plt.title('TreeSHAP Global Feature Importance (XGBoost Regressor)', fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    beeswarm_path = os.path.join(OUTPUT_DIR, "xgboost_shap_summary_beeswarm.png")
    plt.savefig(beeswarm_path, dpi=300)
    plt.close()
    print(f"  -> Saved SHAP Beeswarm Plot: {beeswarm_path}")
    
    # Local Waterfall / Bar Plot for Single Severe Delay Trip
    single_idx = np.argmax(y_test[shap_sample_idx] > 15.0)
    fig, ax = plt.subplots(figsize=(9, 6))
    single_shap = shap_values[single_idx]
    top_fi_idx = np.argsort(np.abs(single_shap))[::-1][:10]
    top_fi_names = [feature_names[i] for i in top_fi_idx]
    top_fi_vals = single_shap[top_fi_idx]
    
    colors = ['#d62728' if v > 0 else '#1f77b4' for v in top_fi_vals]
    ax.barh(range(len(top_fi_vals)), top_fi_vals, color=colors)
    ax.set_yticks(range(len(top_fi_vals)))
    ax.set_yticklabels(top_fi_names)
    ax.invert_yaxis()
    ax.set_title(f'Local Trip Explanation (Actual: {y_test[shap_sample_idx][single_idx]:.1f}m, Pred: {y_pred[shap_sample_idx][single_idx]:.1f}m)', fontsize=12, fontweight='bold')
    ax.set_xlabel('SHAP Value (Contribution to Delay in Minutes)', fontsize=10)
    plt.tight_layout()
    waterfall_path = os.path.join(OUTPUT_DIR, "xgboost_shap_local_waterfall.png")
    plt.savefig(waterfall_path, dpi=300)
    plt.close()
    print(f"  -> Saved Local SHAP Plot: {waterfall_path}")
    
    print("\n" + "=" * 80)
    print(" Stage 03 Complete. All XGBoost outputs saved to Regressor/XGBoost Regressor/")
    print("=" * 80)

if __name__ == "__main__":
    train_and_evaluate_xgboost()
