# -*- coding: utf-8 -*-
"""
Created on Thu May 15 15:27:27 2025

@author: Anelli
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the CSV
file_path = "C:/Users/Anelli/Desktop/Experiments/Live_dead_Assay_Fucoidan_fucus_ASV16/plotting_percentage_dead_cells.csv"
df = pd.read_csv(file_path)

# Melt to long format
df_melted = df.melt(id_vars="Percentage dead cells", 
                    var_name="Condition", 
                    value_name="Dead Cells (%)")
df_melted = df_melted.rename(columns={"Percentage dead cells": "Time"})

# Extract numeric value for sorting
df_melted["Time_numeric"] = df_melted["Time"].str.extract(r'(\d+)').astype(int)

# Compute mean and std
summary = df_melted.groupby(["Time", "Time_numeric", "Condition"]).agg(
    mean_pct=("Dead Cells (%)", "mean"),
    std_pct=("Dead Cells (%)", "std")
).reset_index()

# Sort timepoints numerically
summary = summary.sort_values("Time_numeric")

# Plotting
sns.set(style="whitegrid", font_scale=1.2)
plt.figure(figsize=(16, 12))

# Plot each condition
for condition in summary["Condition"].unique():
    data = summary[summary["Condition"] == condition]
    plt.plot(data["Time"], data["mean_pct"], 
             marker='o', 
             linewidth=5, 
             markersize=10, 
             label=condition)
    plt.fill_between(data["Time"], 
                     data["mean_pct"] - data["std_pct"], 
                     data["mean_pct"] + data["std_pct"], 
                     alpha=0.2)

# Final plot tweaks
plt.title("Percentage of Dead Cells Over Time (Mean ± SD)", fontsize=28)
plt.xlabel("Time", fontsize=28)
plt.ylabel("Dead Cells (%)", fontsize=28)
plt.xticks(rotation=45, fontsize = 28)
plt.yticks(fontsize=28)
plt.legend(fontsize = 20)
plt.grid(True)
plt.tight_layout()
plt.show()