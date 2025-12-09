import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# -------------------------------
# Load CSV
# -------------------------------
df = pd.read_csv("mongodb_results.csv")

# Remove commas in Total Iterations and convert to int
df['Total Iterations'] = df['Total Iterations'].str.replace(',', '').astype(int)

# -------------------------------
# Example: Fit scaling model for throughput vs instances at a fixed VU load
# -------------------------------
# Choose VU load to analyze
vu_load = 230
df_vu = df[df['VUs'] == vu_load]

x = df_vu['Instances'].values
y = df_vu['Throughput (iter/s)'].values

# -------------------------------
# Define scaling models
# -------------------------------
def linear(x, a, b):
    """Linear scaling model"""
    return a * x + b

def sublinear(x, a, b, c):
    """Sublinear/saturation model"""
    return a * x / (b + x) + c

# -------------------------------
# Fit models
# -------------------------------
popt_linear, _ = curve_fit(linear, x, y)
popt_sublinear, _ = curve_fit(sublinear, x, y, maxfev=10000)

# -------------------------------
# Plot results
# -------------------------------
plt.scatter(x, y, label="Data")
plt.plot(x, linear(x, *popt_linear), 'r--', label="Linear Fit")
plt.plot(x, sublinear(x, *popt_sublinear), 'g-', label="Sublinear Fit")
plt.xlabel("Instances")
plt.ylabel("Throughput (iter/s)")
plt.title(f"MongoDB Scaling @ {vu_load} VUs")
plt.legend()
plt.show()

# -------------------------------
# Print fitted parameters
# -------------------------------
print("Linear fit: y = a*x + b")
print(f"a = {popt_linear[0]:.2f}, b = {popt_linear[1]:.2f}")

print("Sublinear fit: y = a*x/(b+x) + c")
print(f"a = {popt_sublinear[0]:.2f}, b = {popt_sublinear[1]:.2f}, c = {popt_sublinear[2]:.2f}")

# -------------------------------
# Optional: Fit models for cost per 1000 iterations vs instances
# -------------------------------
# First calculate cost per 1000 iterations
df['Cost_per_1000_iter'] = df['Total Iterations'] / df['Total Iterations']  # placeholder, replace with real cost calculation

y_cost = df_vu['Cost_per_1000_iter'].values
# Fit a simple model if desired, e.g., linear
popt_cost, _ = curve_fit(linear, x, y_cost)
print(f"Cost model: y = a*x + b -> a={popt_cost[0]:.5f}, b={popt_cost[1]:.5f}")

