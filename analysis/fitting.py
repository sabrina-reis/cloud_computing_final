"""
Scaling Model Analysis for Database Performance
Derives capacity scaling model
Determines if scaling is linear, sub-linear, or super-linear
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# mongo_db
data = {
    'Instances': [1, 2, 4, 8],
    'Throughput_QPS': [162.51, 101.03, 101.14, 114.73],  
    'P95_Latency': [1.73, 1.06, 1.06, 8.85]
}

# mysql
# data = {
#     'Instances': [1, 2, 4, 8],
#     'Throughput_QPS': [131.19, 133.93, 113, 102.84],
#     'P95_Latency': [1.65, 1.74, 3.48, 3.48],
# }

# change this for graph titles
data_type = "mongo"

df = pd.DataFrame(data)
# print("Data:")
# print(df)
# print()

# Calculate metrics for number of instances
baseline_throughput = df['Throughput_QPS'].iloc[0]  # 1-instance throughput
df['Per_Instance_QPS'] = df['Throughput_QPS'] / df['Instances']
df['Ideal_Linear_Throughput'] = baseline_throughput * df['Instances']


# Fit linear regression model
x = df['Instances'].values
y = df['Throughput_QPS'].values
y_2 = df['P95_Latency'].values

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print("Linear regression: y = mx + b")
print(f"b (baseline constant/y-intercept) = {intercept:.4f} QPS")
print(f"m (slope) = {slope:.4f}")
print()

# Interpolate for other numbers of instances
instances_range = np.linspace(1, 8, 100)
predicted_throughput = (instances_range * slope) + intercept
ideal_linear = baseline_throughput * instances_range

# Plot 1: throughput vs. instances
fig, ax1 = plt.subplots()
ax1.scatter(x, y, s=100, color='blue', label='Measured Data', zorder=5)
ax1.plot(instances_range, predicted_throughput, 'r--', linewidth=2, 
         label=f'Linear regression: y = {slope:.3f}x + {intercept:.2f}')
ax1.plot(instances_range, ideal_linear, 'g:', linewidth=2, 
         label=f'Linear: T = {baseline_throughput:.2f} x N')
ax1.set_xlabel('Number of Instances', fontsize=12)
ax1.set_ylabel('Throughput (QPS)', fontsize=12)
ax1.legend()
# plt.show()
plt.savefig(f'throughput_vs_instances_{data_type}.png', dpi=300, bbox_inches='tight')

# Plot 2: per-instance throughput
fig, ax2 = plt.subplots()
ax2.plot(df['Instances'], df['Per_Instance_QPS'], 'o-', linewidth=2, 
         markersize=10, color='green')
ax2.set_xlabel('Number of Instances', fontsize=12)
ax2.set_ylabel('Throughput per Instance (QPS)', fontsize=12)
ax2.set_title('Per-Instance Throughput', fontsize=12, fontweight='bold')
plt.show()
plt.savefig(f'throughput_per_instances_{data_type}.png', dpi=300, bbox_inches='tight')


# Plot 3: P(95) Latency
fig, ax3 = plt.subplots()
ax3.plot(df['Instances'], df['P95_Latency'], 'o-', linewidth=2, 
         markersize=10, color='red')
ax3.set_xlabel('Number of Instances', fontsize=12)
ax3.set_ylabel('P(95) Latency', fontsize=12)
ax3.set_title('Per-Instance Latency', fontsize=12, fontweight='bold')
plt.show()
plt.savefig(f'latency_{data_type}.png', dpi=300, bbox_inches='tight')

# plt.savefig('scaling_model_analysis.png', dpi=300, bbox_inches='tight')
# print("Saved plot: scaling_model_analysis.png")

