"""
================================================================================
SCRIPT 05: XGBOOST MULTI-CLASS CLASSIFIER (DISRUPTION & SEVERITY PREDICTION)
Project: BMTC Intelligent Public Transport Delay Prediction & Dynamic Routing
Output Directory: MODEL BUILDING/OUTPUTS/Classifier/XGBoost Classifier/
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
from sklearn.metrics import classification_report, confusion_matrix, f1_score, balanced_accuracy_score, precision_recall_fscore_support
from sklearn.utils.class_weight import compute_sample_weight

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREPROCESSOR_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Preprocessor")
OUTPUT_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Classifier", "XGBoost Classifier")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CLASS_NAMES = ['NORMAL', 'DELAYED', 'SEVERELY_DELAYED', 'ROUTE_CHANGED']

def train_and_evaluate_xgboost_classifier():
    print("=" * 80)
    print(" BMTC ML PIPELINE: STAGE 05 - XGBOOST MULTI-CLASS CLASSIFIER TRAINING")
    print("=" * 80)
    
    # 1. Load Preprocessed Data
    cache_path = os.path.join(PREPROCESSOR_DIR, "processed_splits_tabular.joblib")
    print(f"[1/5] Loading preprocessed dataset splits from: {cache_path}")
    data = joblib.load(cache_path)
    
    X_train, y_train = data['X_train'], data['y_train_clf']
    X_val, y_val = data['X_val'], data['y_val_clf']
    X_test, y_test = data['X_test'], data['y_test_clf']
    feature_names = data['feature_names_out']
    
    print(f"  -> Train instances: {X_train.shape[0]:,}, Features: {X_train.shape[1]}")
    print(f"  -> Class Distribution in Train: {dict(zip(*np.unique(y_train, return_counts=True)))}")
    
    # Compute balanced sample weights
    sample_weights_train = compute_sample_weight('balanced', y_train)
    
    # 2. Configure XGBoost Classifier
    print("\n[2/5] Initializing Multi-Class XGBoost Classifier...")
    model = xgb.XGBClassifier(
        objective='multi:softprob',
        num_class=4,
        n_estimators=800,
        learning_rate=0.04,
        max_depth=6,
        subsample=0.85,
        colsample_bytree=0.85,
        early_stopping_rounds=40,
        random_state=42,
        tree_method='hist',
        n_jobs=-1
    )
    
    start_time = time.time()
    model.fit(
        X_train, y_train,
        sample_weight=sample_weights_train,
        eval_set=[(X_val, y_val)],
        verbose=100
    )
    train_duration = time.time() - start_time
    print(f"  -> Training Completed in: {train_duration:.2f} seconds (Best Iteration: {model.best_iteration})")
    
    # 3. Evaluate on 2026 Test Set
    print("\n[3/5] Evaluating Classification Metrics on 2026 Out-of-Time Test Set...")
    infer_start = time.time()
    y_pred_probs = model.predict_proba(X_test)
    y_pred = np.argmax(y_pred_probs, axis=1)
    infer_duration = time.time() - infer_start
    latency_per_sample_ms = (infer_duration / len(X_test)) * 1000.0
    
    macro_f1 = float(f1_score(y_test, y_pred, average='macro'))
    weighted_f1 = float(f1_score(y_test, y_pred, average='weighted'))
    balanced_acc = float(balanced_accuracy_score(y_test, y_pred))
    overall_acc = float(np.mean(y_test == y_pred) * 100.0)
    
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average=None)
    
    per_class_metrics = {}
    for i, name in enumerate(CLASS_NAMES):
        per_class_metrics[name] = {
            "precision": float(precision[i]),
            "recall": float(recall[i]),
            "f1_score": float(f1[i]),
            "support": int(support[i])
        }
        
    print("=" * 60)
    print("  [BENCHMARK] XGBOOST CLASSIFIER (2026 TEST SET)")
    print("  ------------------------------------------------------------")
    print(f"  -> Macro F1-Score:        {macro_f1:.4f} ({macro_f1*100:.2f}%)")
    print(f"  -> Weighted F1-Score:     {weighted_f1:.4f} ({weighted_f1*100:.2f}%)")
    print(f"  -> Balanced Accuracy:     {balanced_acc:.4f} ({balanced_acc*100:.2f}%)")
    print(f"  -> Overall Accuracy:      {overall_acc:.2f}%")
    print(f"  -> Inference Latency:     {latency_per_sample_ms:.4f} ms/query")
    print("  ------------------------------------------------------------")
    print("  Per-Class Performance:")
    for name, m in per_class_metrics.items():
        print(f"    [{name:16s}] F1: {m['f1_score']:.4f} | Prec: {m['precision']:.4f} | Rec: {m['recall']:.4f} | Supp: {m['support']:,}")
    print("=" * 60)
    
    # Save Metrics JSON
    metrics_data = {
        "model_name": "XGBoost Classifier",
        "objective": "multi:softprob (Disruption & Severity Classification)",
        "test_instances_count": int(len(y_test)),
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "balanced_accuracy": balanced_acc,
        "overall_accuracy_pct": overall_acc,
        "per_class_metrics": per_class_metrics,
        "training_time_seconds": train_duration,
        "inference_latency_ms_per_sample": latency_per_sample_ms
    }
    
    metrics_path = os.path.join(OUTPUT_DIR, "xgboost_classification_metrics.json")
    with open(metrics_path, "w", encoding='utf-8') as f:
        json.dump(metrics_data, f, indent=4)
    print(f"  -> Saved Metrics: {metrics_path}")
    
    # Save Model
    model_path = os.path.join(OUTPUT_DIR, "xgboost_classifier_model.joblib")
    joblib.dump(model, model_path)
    print(f"  -> Saved Model: {model_path}")
    
    # 4. Generate Visualizations
    print("\n[4/5] Generating Confusion Matrix & PR Curves...")
    
    # Confusion Matrix Plot
    cm = confusion_matrix(y_test, y_pred, normalize='true')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='.3f', cmap='Blues', xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, ax=ax)
    ax.set_title(f'XGBoost Classifier: Normalized Confusion Matrix (Macro F1 = {macro_f1:.4f})', fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Predicted Disruption Label', fontsize=10)
    ax.set_ylabel('True Disruption Label', fontsize=10)
    plt.tight_layout()
    cm_path = os.path.join(OUTPUT_DIR, "xgboost_confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"  -> Saved Confusion Matrix Plot: {cm_path}")
    
    # Feature Importance Plot
    print("\n[5/5] Generating Feature Importance Plot...")
    importances = model.feature_importances_
    top_indices = np.argsort(importances)[::-1][:15]
    top_names = [feature_names[i] for i in top_indices]
    top_scores = importances[top_indices]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_scores, y=top_names, palette='viridis', ax=ax)
    ax.set_title('Top 15 Feature Importances (XGBoost Disruption Classifier)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Relative Gain Importance Score', fontsize=10)
    plt.tight_layout()
    fi_path = os.path.join(OUTPUT_DIR, "xgboost_classifier_shap_importance.png")
    plt.savefig(fi_path, dpi=300)
    plt.close()
    print(f"  -> Saved Feature Importance Plot: {fi_path}")
    
    print("\n" + "=" * 80)
    print(" Stage 05 Complete. All XGBoost Classifier outputs saved to Classifier/XGBoost Classifier/")
    print("=" * 80)

if __name__ == "__main__":
    train_and_evaluate_xgboost_classifier()
