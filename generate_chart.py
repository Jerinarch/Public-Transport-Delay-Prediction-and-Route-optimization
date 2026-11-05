import matplotlib.pyplot as plt
import os

output_path = r"D:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning\regression_performance_comparison.png"

models = ['XGBoost Regressor', 'BiLSTM + Attention']
mae_values = [1.30, 0.35]
colors = ['#e74c3c', '#2ecc71'] # Red for worse (higher error), Green for better (lower error)

fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.barh(models, mae_values, color=colors, height=0.5)

# Add values to the end of bars
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f'{width:.2f} min', 
            ha='left', va='center', fontweight='bold', fontsize=12)

ax.set_xlabel('Mean Absolute Error (Minutes) - Lower is Better', fontweight='bold', fontsize=12)
ax.set_title('Figure 6.1: Regression Performance Visual Comparison', fontweight='bold', fontsize=14, pad=20)
ax.set_xlim(0, 1.6)
ax.grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Successfully saved to: {output_path}")
