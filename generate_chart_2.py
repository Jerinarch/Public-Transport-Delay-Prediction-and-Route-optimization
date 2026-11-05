import matplotlib.pyplot as plt
import os

output_path = r"D:\An Intelligent Public Transport Delay Prediction and Route Optimization System Using Machine Learning\route_optimization_time_savings.png"

labels = ['Scheduled Path\n(Congested)', 'ML Detour Path\n(Optimized)']
times = [109, 27]
colors = ['#e74c3c', '#2ecc71'] # Red for slow, Green for fast

fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.barh(labels, times, color=colors, height=0.5)

# Add values to the end of bars
for i, bar in enumerate(bars):
    width = bar.get_width()
    if i == 1:
        text = f'{width:.0f} mins (75.5% time savings)'
    else:
        text = f'{width:.0f} mins'
        
    ax.text(width + 2, bar.get_y() + bar.get_height()/2, text, 
            ha='left', va='center', fontweight='bold', fontsize=12)

ax.set_xlabel('Travel Time (Minutes) - Lower is Better', fontweight='bold', fontsize=12)
ax.set_title('Figure 6.2: Route Optimization Time Savings Comparison', fontweight='bold', fontsize=14, pad=20)
ax.set_xlim(0, 150)
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Invert y-axis to have Scheduled Path on top
ax.invert_yaxis()

plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Successfully saved to: {output_path}")
