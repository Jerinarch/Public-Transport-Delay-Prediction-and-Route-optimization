"""
================================================================================
SCRIPT 06: RANDOM FOREST CLASSIFIER (BASELINE & DEFENSE COMPARISON)
Project: BMTC Intelligent Public Transport Delay Prediction & Dynamic Routing
Output Directory: MODEL BUILDING/OUTPUTS/Classifier/Random Forest Classifier/
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
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, f1_score, balanced_accuracy_score, precision_recall_fscore_support

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREPROCESSOR_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Preprocessor")
OUTPUT_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Classifier", "Random Forest Classifier")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CLASS_NAMES = ['NORMAL', 'DELAYED', 'SEVERELY_DELAYED', 'ROUTE_CHANGED']

def train_and_evaluate_random_forest():
    print("=" * 80)
    print(" BMTC ML PIPELINE: STAGE 06 - RANDOM FOREST CLASSIFIER TRAINING")
    print("=" * 80)
    
    # 1. Load Preprocessed Splits
    cache_path = os.path.join(PREPROCESSOR_DIR, "processed_splits_tabular.joblib")
    print(f"[1/4] Loading preprocessed dataset splits from: {cache_path}")
    data = joblib.load(cache_path)
    
    X_train, y_train = data['X_train'], data['y_train_clf']
    X_test, y_test = data['X_test'], data['y_test_clf']
    feature_names = data['feature_names_out']
    
    # 2. Train Random Forest Classifier
    print("\n[2/4] Training Random Forest Classifier (n_estimators=300, max_depth=16)...")
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=16,
        class_weight='balanced_subsample',
        random_state=42,
        n_jobs=-1
    )
    
    start_time = time.time()
    model.fit(X_train, y_train)
    train_duration = time.time() - start_time
    print(f"  -> Training Completed in: {train_duration:.2f} seconds")
    
    # 3. Evaluate Metrics on 2026 Test Set
    print("\n[3/4] Evaluating Metrics on 2026 Test Set...")
    infer_start = time.time()
    y_pred = model.predict(X_test)
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
    print("  [BENCHMARK] RANDOM FOREST CLASSIFIER (2026 TEST SET)")
    print("  ------------------------------------------------------------")
    print(f"  -> Macro F1-Score:        {macro_f1:.4f} ({macro_f1*100:.2f}%)")
    print(f"  -> Weighted F1-Score:     {weighted_f1:.4f} ({weighted_f1*100:.2f}%)")
    print(f"  -> Balanced Accuracy:     {balanced_acc:.4f} ({balanced_acc*100:.2f}%)")
    print(f"  -> Overall Accuracy:      {overall_acc:.2f}%")
    print(f"  -> Inference Latency:     {latency_per_sample_ms:.4f} ms/query")
    print("  ------------------------------------------------------------")
    for name, m in per_class_metrics.items():
        print(f"    [{name:16s}] F1: {m['f1_score']:.4f} | Prec: {m['precision']:.4f} | Rec: {m['recall']:.4f}")
    print("=" * 60)
    
    # Save Metrics JSON
    metrics_data = {
        "model_name": "Random Forest Classifier",
        "parameters": {"n_estimators": 300, "max_depth": 16, "class_weight": "balanced_subsample"},
        "test_instances_count": int(len(y_test)),
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "balanced_accuracy": balanced_acc,
        "overall_accuracy_pct": overall_acc,
        "per_class_metrics": per_class_metrics,
        "training_time_seconds": train_duration,
        "inference_latency_ms_per_sample": latency_per_sample_ms
    }
    
    metrics_path = os.path.join(OUTPUT_DIR, "random_forest_classification_metrics.json")
    with open(metrics_path, "w", encoding='utf-8') as f:
        json.dump(metrics_data, f, indent=4)
    print(f"  -> Saved Metrics JSON: {metrics_path}")
    
    # Save Model
    model_path = os.path.join(OUTPUT_DIR, "random_forest_classifier_model.joblib")
    joblib.dump(model, model_path)
    print(f"  -> Saved Model Artifact: {model_path}")
    
    # 4. Generate Visualizations
    print("\n[4/4] Generating Confusion Matrix & Gini Importance Charts...")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred, normalize='true')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='.3f', cmap='Greens', xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, ax=ax)
    ax.set_title(f'Random Forest: Normalized Confusion Matrix (Macro F1 = {macro_f1:.4f})', fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Predicted Disruption Label', fontsize=10)
    ax.set_ylabel('True Disruption Label', fontsize=10)
    plt.tight_layout()
    cm_path = os.path.join(OUTPUT_DIR, "random_forest_confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"  -> Saved Confusion Matrix: {cm_path}")
    
    # Gini Feature Importance
    importances = model.feature_importances_
    top_indices = np.argsort(importances)[::-1][:15]
    top_names = [feature_names[i] for i in top_indices]
    top_scores = importances[top_indices]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_scores, y=top_names, palette='magma', ax=ax)
    ax.set_title('Top 15 MDI Gini Feature Importances (Random Forest Classifier)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Mean Decrease in Impurity (Gini Importance)', fontsize=10)
    plt.tight_layout()
    fi_path = os.path.join(OUTPUT_DIR, "random_forest_gini_feature_importance.png")
    plt.savefig(fi_path, dpi=300)
    plt.close()
    print(f"  -> Saved Gini Importance Plot: {fi_path}")
    
    print("\n" + "=" * 80)
    print(" Stage 06 Complete. All Random Forest outputs saved to Classifier/Random Forest Classifier/")
    print("=" * 80)

if __name__ == "__main__":
    train_and_evaluate_random_forest()
