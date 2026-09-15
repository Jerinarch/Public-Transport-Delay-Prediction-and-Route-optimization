"""
================================================================================
SCRIPT 04: BIDIRECTIONAL LSTM WITH BAHDANAU ATTENTION (SEQUENTIAL CHAMPION)
Project: BMTC Intelligent Public Transport Delay Prediction & Dynamic Routing
Output Directory: MODEL BUILDING/OUTPUTS/Regressor/Bidirectional LSTM with Bahdanau Attention/
================================================================================
"""

import os
import sys
import json
import time
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Visual style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREPROCESSOR_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Preprocessor")
OUTPUT_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Regressor", "Bidirectional LSTM with Bahdanau Attention")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# 1. Neural Network Architecture: 3-Layer BiLSTM + Bahdanau Attention
# ----------------------------------------------------------------------
class BahdanauAttention(nn.Module):
    def __init__(self, hidden_dim):
        super(BahdanauAttention, self).__init__()
        self.Wa = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.va = nn.Linear(hidden_dim, 1, bias=False)
        
    def forward(self, lstm_outputs):
        # lstm_outputs: [batch_size, seq_len, hidden_dim]
        energy = torch.tanh(self.Wa(lstm_outputs)) # [batch_size, seq_len, hidden_dim]
        scores = self.va(energy).squeeze(-1)       # [batch_size, seq_len]
        attention_weights = torch.softmax(scores, dim=1) # [batch_size, seq_len]
        context_vector = torch.bmm(attention_weights.unsqueeze(1), lstm_outputs).squeeze(1) # [batch_size, hidden_dim]
        return context_vector, attention_weights

class BiLSTMAttentionRegressor(nn.Module):
    def __init__(self, input_dim, hidden_dim=32, num_layers=3, dropout=0.383):
        super(BiLSTMAttentionRegressor, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        self.attention = BahdanauAttention(hidden_dim * 2)
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(hidden_dim * 2, 32)
        self.relu = nn.ReLU()
        self.out = nn.Linear(32, 1)
        
    def forward(self, x):
        # x: [batch_size, seq_len, input_dim]
        lstm_out, _ = self.lstm(x) # [batch_size, seq_len, hidden_dim * 2]
        context, attention_weights = self.attention(lstm_out)
        h = self.dropout(context)
        h = self.relu(self.fc1(h))
        pred = self.out(h)
        return pred.squeeze(-1), attention_weights

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

# ----------------------------------------------------------------------
# 2. Training and Evaluation Pipeline
# ----------------------------------------------------------------------
def train_and_evaluate_bilstm():
    print("=" * 80)
    print(" BMTC ML PIPELINE: STAGE 04 - BiLSTM WITH BAHDANAU ATTENTION TRAINING")
    print("=" * 80)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"[1/5] Initializing device: {device}")
    
    # Load 3D Sequence Tensors
    seq_cache_path = os.path.join(PREPROCESSOR_DIR, "processed_splits_sequences.joblib")
    print(f"  -> Loading 3D sequence tensors from: {seq_cache_path}")
    data = joblib.load(seq_cache_path)
    
    X_train_seq = torch.tensor(data['X_train_seq'], dtype=torch.float32)
    y_train_seq = torch.tensor(data['y_train_seq'][:, -1], dtype=torch.float32) # Predict terminal/corridor delay
    
    X_val_seq = torch.tensor(data['X_val_seq'], dtype=torch.float32)
    y_val_seq = torch.tensor(data['y_val_seq'][:, -1], dtype=torch.float32)
    
    X_test_seq = torch.tensor(data['X_test_seq'], dtype=torch.float32)
    y_test_seq = torch.tensor(data['y_test_seq'][:, -1], dtype=torch.float32)
    
    print(f"  -> Train sequences: {X_train_seq.shape}")
    print(f"  -> Val sequences:   {X_val_seq.shape}")
    print(f"  -> Test sequences:  {X_test_seq.shape}")
    
    batch_size = 256
    train_loader = DataLoader(TensorDataset(X_train_seq, y_train_seq), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val_seq, y_val_seq), batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(TensorDataset(X_test_seq, y_test_seq), batch_size=batch_size, shuffle=False)
    
    # Initialize Model
    input_dim = X_train_seq.shape[2]
    model = BiLSTMAttentionRegressor(
        input_dim=input_dim,
        hidden_dim=32,
        num_layers=3,
        dropout=0.383
    ).to(device)
    
    total_params = count_parameters(model)
    print(f"\n[2/5] Model Initialized: 3-Layer BiLSTM + Bahdanau Attention")
    print(f"  -> Total Trainable Parameters: {total_params:,} (Lightweight ~31K target)")
    
    criterion = nn.SmoothL1Loss()
    optimizer = optim.Adam(model.parameters(), lr=1.54e-3, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)
    
    # Training Loop
    epochs = 20
    best_val_loss = float('inf')
    train_losses = []
    val_losses = []
    
    print("\n[3/5] Starting Model Training...")
    start_time = time.time()
    
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            preds, _ = model(batch_x)
            loss = criterion(preds, batch_y)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            running_loss += loss.item() * len(batch_y)
            
        epoch_train_loss = running_loss / len(X_train_seq)
        train_losses.append(epoch_train_loss)
        
        # Validation
        model.eval()
        val_running_loss = 0.0
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                preds, _ = model(batch_x)
                val_loss = criterion(preds, batch_y)
                val_running_loss += val_loss.item() * len(batch_y)
                
        epoch_val_loss = val_running_loss / len(X_val_seq)
        val_losses.append(epoch_val_loss)
        scheduler.step(epoch_val_loss)
        
        if epoch % 5 == 0 or epoch == 1:
            print(f"  -> Epoch [{epoch:02d}/{epochs:02d}] - Train Loss: {epoch_train_loss:.4f} | Val Loss: {epoch_val_loss:.4f}")
            
        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            torch.save(model.state_dict(), os.path.join(OUTPUT_DIR, "bilstm_attention_model.pt"))
            
    train_duration = time.time() - start_time
    print(f"  -> Training Completed in: {train_duration:.2f} seconds")
    
    # Load Best Model for Evaluation
    model.load_state_dict(torch.load(os.path.join(OUTPUT_DIR, "bilstm_attention_model.pt")))
    model.eval()
    
    # 4. Evaluation on Test Set
    print("\n[4/5] Evaluating on 2026 Test Set and extracting Attention Weights...")
    all_preds = []
    all_targets = []
    all_attentions = []
    
    infer_start = time.time()
    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x = batch_x.to(device)
            preds, att_weights = model(batch_x)
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(batch_y.numpy())
            all_attentions.extend(att_weights.cpu().numpy())
            
    infer_duration = time.time() - infer_start
    latency_per_sample_ms = (infer_duration / len(X_test_seq)) * 1000.0
    
    y_test = np.array(all_targets)
    y_pred = np.array(all_preds)
    attention_matrix = np.array(all_attentions) # [num_test_trips, 9]
    
    rmse = float(np.sqrt(np.mean((y_test - y_pred) ** 2)))
    mae = float(np.mean(np.abs(y_test - y_pred)))
    r2 = float(1.0 - (np.sum((y_test - y_pred) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2)))
    mape = float(np.mean(np.abs((y_test - y_pred) / (np.abs(y_test) + 1.0))) * 100.0)
    acc_3min = float(np.mean(np.abs(y_test - y_pred) <= 3.0) * 100.0)
    acc_5min = float(np.mean(np.abs(y_test - y_pred) <= 5.0) * 100.0)
    
    print("=" * 60)
    print("  [BENCHMARK] BiLSTM + BAHDANAU ATTENTION (2026 TEST)")
    print("  ------------------------------------------------------------")
    print(f"  -> Root Mean Squared Error (RMSE): {rmse:.4f} minutes")
    print(f"  -> Mean Absolute Error (MAE):       {mae:.4f} minutes")
    print(f"  -> Coefficient of Determination (R2): {r2:.4f} ({r2*100:.2f}%)")
    print(f"  -> Mean Absolute Percentage Error:   {mape:.2f}%")
    print(f"  -> Accuracy within +/- 3 Minutes:    {acc_3min:.2f}%")
    print(f"  -> Accuracy within +/- 5 Minutes:    {acc_5min:.2f}%")
    print(f"  -> Inference Latency per Sample:     {latency_per_sample_ms:.4f} ms/query")
    print("=" * 60)
    
    # Save Metrics JSON
    metrics_data = {
        "model_name": "Bidirectional LSTM with Bahdanau Attention",
        "architecture_details": {
            "num_layers": 3,
            "hidden_units_per_direction": 32,
            "total_hidden_dim": 64,
            "attention_mechanism": "Bahdanau Additive Attention",
            "dropout_rate": 0.383,
            "learning_rate": 0.00154,
            "trainable_parameters": total_params
        },
        "evaluation_dataset": "2026 Out-of-Time Test Partition",
        "test_instances_count": int(len(y_test)),
        "rmse_minutes": rmse,
        "mae_minutes": mae,
        "r2_score": r2,
        "mape_percentage": mape,
        "accuracy_within_3min_pct": acc_3min,
        "accuracy_within_5min_pct": acc_5min,
        "training_time_seconds": train_duration,
        "inference_latency_ms_per_sample": latency_per_sample_ms
    }
    
    metrics_path = os.path.join(OUTPUT_DIR, "bilstm_regression_metrics.json")
    with open(metrics_path, "w", encoding='utf-8') as f:
        json.dump(metrics_data, f, indent=4)
    print(f"  -> Saved Metrics JSON: {metrics_path}")
    
    # 5. Visualizations & Attention Heatmap
    print("\n[5/5] Generating Loss curves, Actual vs Predicted, and Attention Heatmaps...")
    
    # Plot 1: Training & Validation Loss
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(1, epochs + 1), train_losses, label='Training Loss (SmoothL1)', color='#1f77b4', linewidth=2)
    ax.plot(range(1, epochs + 1), val_losses, label='Validation Loss', color='#ff7f0e', linewidth=2, linestyle='--')
    ax.set_title('BiLSTM with Bahdanau Attention: Training Convergence Curves', fontsize=12, fontweight='bold')
    ax.set_xlabel('Epoch', fontsize=10)
    ax.set_ylabel('Loss', fontsize=10)
    ax.legend()
    plt.tight_layout()
    loss_plot_path = os.path.join(OUTPUT_DIR, "bilstm_training_loss_curves.png")
    plt.savefig(loss_plot_path, dpi=300)
    plt.close()
    print(f"  -> Saved Convergence Curve: {loss_plot_path}")
    
    # Plot 2: Actual vs Predicted Scatter
    fig, ax = plt.subplots(figsize=(8, 7))
    sample_indices = np.random.choice(len(y_test), size=min(10000, len(y_test)), replace=False)
    ax.scatter(y_test[sample_indices], y_pred[sample_indices], alpha=0.3, color='#e377c2', edgecolors='none', s=18, label='Trip Instances')
    max_val = max(np.percentile(y_test, 99.5), np.percentile(y_pred, 99.5))
    ax.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Perfect 1:1 Reference')
    ax.set_title(f'BiLSTM-Attention: Actual vs Predicted Delay (R2 = {r2:.4f}, RMSE = {rmse:.2f} min)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Actual Observed Terminal Delay (Minutes)', fontsize=10)
    ax.set_ylabel('Predicted Delay (Minutes)', fontsize=10)
    ax.legend(loc='upper left')
    plt.tight_layout()
    scatter_path = os.path.join(OUTPUT_DIR, "bilstm_actual_vs_predicted_scatter.png")
    plt.savefig(scatter_path, dpi=300)
    plt.close()
    print(f"  -> Saved Scatter Plot: {scatter_path}")
    
    # Plot 3: Attention Weights Heatmap across Stop Sequence
    fig, ax = plt.subplots(figsize=(10, 6))
    sample_attentions = attention_matrix[:20]         # First 20 sample trips
    
    sns.heatmap(
        sample_attentions,
        cmap='YlOrRd',
        annot=True,
        fmt='.2f',
        xticklabels=[f'Stop {i}' for i in range(1, 10)],
        yticklabels=[f'Trip {j+1}' for j in range(20)],
        cbar_kws={'label': 'Bahdanau Attention Weight (alpha)'},
        ax=ax
    )
    ax.set_title('Spatiotemporal Explainability: Attention Weight Matrix Across Stop Sequences', fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Stop Sequence Along Transit Corridor (k=1 .. 9)', fontsize=10)
    ax.set_ylabel('Sample Bus Trip Instances', fontsize=10)
    plt.tight_layout()
    heatmap_path = os.path.join(OUTPUT_DIR, "bilstm_stop_attention_weights_heatmap.png")
    plt.savefig(heatmap_path, dpi=300)
    plt.close()
    print(f"  -> Saved Attention Weights Heatmap: {heatmap_path}")
    
    print("\n" + "=" * 80)
    print(" Stage 04 Complete. All BiLSTM outputs saved to Regressor/Bidirectional LSTM with Bahdanau Attention/")
    print("=" * 80)

if __name__ == "__main__":
    train_and_evaluate_bilstm()
