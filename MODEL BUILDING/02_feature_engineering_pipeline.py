"""
================================================================================
SCRIPT 02: FEATURE ENGINEERING & TEMPORAL SPLITTING PIPELINE
Project: BMTC Intelligent Public Transport Delay Prediction & Dynamic Routing
Dataset: final_integrated_dataset.csv (729,648 rows, 35 features)
================================================================================
"""

import os
import gc
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATASET_PATH = os.path.join(PROJECT_ROOT, "final yr dataset new", "final yr dataset", "final_integrated_dataset.csv")
OUTPUT_PREPROCESSOR_DIR = os.path.join(BASE_DIR, "OUTPUTS", "Preprocessor")
os.makedirs(OUTPUT_PREPROCESSOR_DIR, exist_ok=True)

def engineer_features(df):
    """Compute temporal, sequence lag, and spatial domain features."""
    print("  -> Parsing timestamps and temporal coordinates...")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['service_date'] = pd.to_datetime(df['service_date'])
    
    # Extract scheduled hour and minute
    sched_time = pd.to_datetime(df['scheduled_arrival'], format='%H:%M:%S', errors='coerce').dt
    df['sched_hour'] = sched_time.hour.fillna(df['timestamp'].dt.hour).astype(int)
    df['sched_minute'] = sched_time.minute.fillna(df['timestamp'].dt.minute).astype(int)
    df['month'] = df['service_date'].dt.month
    
    # Cyclical trigonometric temporal encoding
    df['sin_hour'] = np.sin(2 * np.pi * df['sched_hour'] / 24.0)
    df['cos_hour'] = np.cos(2 * np.pi * df['sched_hour'] / 24.0)
    df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12.0)
    df['cos_month'] = np.cos(2 * np.pi * df['month'] / 12.0)
    
    # Rush / Peak hour flag (Weekdays morning 8-11, evening 17-20)
    df['is_peak_hour'] = (
        (df['sched_hour'].isin([8, 9, 10, 11, 17, 18, 19, 20])) & 
        (~df['is_weekend'])
    ).astype(int)
    
    # Weather severity compound index
    df['weather_severity'] = (
        (df['precipitation'] * 2.0 + df['rain'] * 3.0) / 10.0 + 
        (df['weather_code'] >= 60).astype(float) * 0.5
    )
    
    # Clean holiday name
    df['holiday_name'] = df['holiday_name'].fillna('NONE').astype(str)
    
    # Convert booleans to int
    df['incident_flag'] = df['incident_flag'].astype(int)
    df['is_weekend'] = df['is_weekend'].astype(int)
    df['is_holiday'] = df['is_holiday'].astype(int)
    
    # Generate sequential trajectory lag features (delay at stop k-1 for same trip instance)
    print("  -> Generating trajectory sequence lag features (Stop k-1 delay)...")
    df = df.sort_values(by=['trip_id', 'stop_sequence']).reset_index(drop=True)
    df['lag_delay_prev_stop'] = df.groupby('trip_id')['delay_minutes'].shift(1).fillna(0.0)
    
    # Target encodings / mappings
    disruption_map = {'NORMAL': 0, 'DELAYED': 1, 'SEVERELY_DELAYED': 2, 'ROUTE_CHANGED': 3}
    df['target_disruption'] = df['disruption_label'].map(disruption_map).fillna(0).astype(int)
    
    occupancy_map = {'LOW': 0, 'MODERATE': 1, 'HIGH': 2, 'NEARLY_FULL': 3, 'FULL': 4}
    df['target_occupancy'] = df['occupancy_status'].map(occupancy_map).fillna(0).astype(int)
    
    return df

def temporal_split(df):
    """Strictly chronologically ordered 3-way temporal split."""
    print("\n[2/4] Executing strictly ordered Temporal Partitioning...")
    
    train_mask = df['service_date'] < '2025-01-01'
    val_mask = (df['service_date'] >= '2025-01-01') & (df['service_date'] < '2026-01-01')
    test_mask = df['service_date'] >= '2026-01-01'
    
    train_df = df[train_mask].copy().reset_index(drop=True)
    val_df = df[val_mask].copy().reset_index(drop=True)
    test_df = df[test_mask].copy().reset_index(drop=True)
    
    print(f"  -> Train Set (2022-2024): {len(train_df):,} rows ({train_df['service_date'].min().date()} to {train_df['service_date'].max().date()})")
    print(f"  -> Val Set   (2025):      {len(val_df):,} rows ({val_df['service_date'].min().date()} to {val_df['service_date'].max().date()})")
    print(f"  -> Test Set  (2026 OOT):  {len(test_df):,} rows ({test_df['service_date'].min().date()} to {test_df['service_date'].max().date()})")
    
    # Verify temporal isolation
    assert train_df['service_date'].max() < val_df['service_date'].min(), "Temporal Leakage detected between Train and Val!"
    assert val_df['service_date'].max() < test_df['service_date'].min(), "Temporal Leakage detected between Val and Test!"
    print("  -> Temporal Isolation Integrity: 100% VERIFIED (Zero Temporal Leakage)")
    
    return train_df, val_df, test_df

def build_and_fit_preprocessors(train_df, val_df, test_df):
    """Construct Scikit-Learn ColumnTransformer fit ONLY on Train split."""
    print("\n[3/4] Building Scikit-Learn ColumnTransformer (Fit strictly on Train Split)...")
    
    numeric_features = [
        'stop_sequence', 'temperature', 'humidity', 'precipitation', 'rain',
        'traffic_speed', 'congestion_index', 'sin_hour', 'cos_hour',
        'sin_month', 'cos_month', 'is_peak_hour', 'weather_severity', 'lag_delay_prev_stop'
    ]
    
    categorical_features = [
        'route_id', 'bus_type', 'fuel_type', 'stop_id', 'area', 'zone', 'day_of_week', 'holiday_name'
    ]
    
    binary_features = [
        'incident_flag', 'is_weekend', 'is_holiday'
    ]
    
    feature_cols = numeric_features + categorical_features + binary_features
    print(f"  -> Total Feature Dimension: {len(feature_cols)} base features")
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', RobustScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
            ('bin', 'passthrough', binary_features)
        ]
    )
    
    # Fit ONLY on Train
    preprocessor.fit(train_df[feature_cols])
    
    # Transform splits
    print("  -> Transforming Train, Validation, and Test feature matrices...")
    X_train = preprocessor.transform(train_df[feature_cols])
    X_val = preprocessor.transform(val_df[feature_cols])
    X_test = preprocessor.transform(test_df[feature_cols])
    
    print(f"  -> Transformed Feature Dimension: {X_train.shape[1]} columns (after OneHot expansion)")
    
    # Targets
    y_train_reg = train_df['delay_minutes'].values
    y_val_reg = val_df['delay_minutes'].values
    y_test_reg = test_df['delay_minutes'].values
    
    y_train_clf = train_df['target_disruption'].values
    y_val_clf = val_df['target_disruption'].values
    y_test_clf = test_df['target_disruption'].values
    
    # Save preprocessor artifact
    preprocessor_path = os.path.join(OUTPUT_PREPROCESSOR_DIR, "column_transformer_preprocessor.joblib")
    joblib.dump(preprocessor, preprocessor_path)
    print(f"  -> Saved Preprocessor: {preprocessor_path}")
    
    # Save processed matrices cache for fast model training
    print("\n[4/4] Serializing processed dataset splits for high-speed training...")
    splits_dict = {
        "X_train": X_train, "y_train_reg": y_train_reg, "y_train_clf": y_train_clf,
        "X_val": X_val, "y_val_reg": y_val_reg, "y_val_clf": y_val_clf,
        "X_test": X_test, "y_test_reg": y_test_reg, "y_test_clf": y_test_clf,
        "feature_cols": feature_cols,
        "feature_names_out": list(preprocessor.get_feature_names_out())
    }
    
    cache_path = os.path.join(OUTPUT_PREPROCESSOR_DIR, "processed_splits_tabular.joblib")
    joblib.dump(splits_dict, cache_path, compress=3)
    print(f"  -> Saved Processed Tabular Cache: {cache_path}")
    
    # Build 3D sequence tensors for BiLSTM: [num_trips, seq_len=9, num_features]
    print("  -> Building 3D Sequence Tensors for Bidirectional LSTM with Attention...")
    def build_sequences(df_split, X_split):
        df_split['row_idx'] = np.arange(len(df_split))
        trip_groups = df_split.groupby('trip_id')
        
        seq_list = []
        target_list = []
        
        for trip_id, group in trip_groups:
            indices = group['row_idx'].values
            seq_feats = X_split[indices]
            seq_targets = group['delay_minutes'].values
            
            # Pad or truncate to max 9 stops
            if len(seq_feats) < 9:
                pad_len = 9 - len(seq_feats)
                pad_feats = np.zeros((pad_len, X_split.shape[1]))
                pad_targets = np.zeros(pad_len)
                seq_feats = np.vstack([seq_feats, pad_feats])
                seq_targets = np.concatenate([seq_targets, pad_targets])
            else:
                seq_feats = seq_feats[:9]
                seq_targets = seq_targets[:9]
                
            seq_list.append(seq_feats)
            target_list.append(seq_targets)
            
        return np.array(seq_list, dtype=np.float32), np.array(target_list, dtype=np.float32)
    
    X_train_seq, y_train_seq = build_sequences(train_df, X_train)
    X_val_seq, y_val_seq = build_sequences(val_df, X_val)
    X_test_seq, y_test_seq = build_sequences(test_df, X_test)
    
    print(f"  -> 3D Sequence Tensors Created:")
    print(f"     Train Sequences: {X_train_seq.shape}, Targets: {y_train_seq.shape}")
    print(f"     Val Sequences:   {X_val_seq.shape}, Targets: {y_val_seq.shape}")
    print(f"     Test Sequences:  {X_test_seq.shape}, Targets: {y_test_seq.shape}")
    
    seq_cache_path = os.path.join(OUTPUT_PREPROCESSOR_DIR, "processed_splits_sequences.joblib")
    joblib.dump({
        "X_train_seq": X_train_seq, "y_train_seq": y_train_seq,
        "X_val_seq": X_val_seq, "y_val_seq": y_val_seq,
        "X_test_seq": X_test_seq, "y_test_seq": y_test_seq,
    }, seq_cache_path, compress=3)
    print(f"  -> Saved Processed Sequence Cache: {seq_cache_path}")

def main():
    print("=" * 80)
    print(" BMTC ML PIPELINE: STAGE 02 - FEATURE ENGINEERING & TEMPORAL SPLITTING")
    print("=" * 80)
    print("[1/4] Loading master dataset and engineering domain features...")
    df = pd.read_csv(DATASET_PATH, low_memory=False)
    df = engineer_features(df)
    train_df, val_df, test_df = temporal_split(df)
    build_and_fit_preprocessors(train_df, val_df, test_df)
    print("\n" + "=" * 80)
    print(" Stage 02 Complete. All tabular & sequence matrices cached for model training.")
    print("=" * 80)

if __name__ == "__main__":
    main()
