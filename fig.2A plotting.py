# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 12:13:58 2025

@author: Anelli
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re

# -----------------------------
# USER INPUT
# -----------------------------
# Put one or two CSVs here. Each CSV should have columns: ID, IC
# Example: one experiment
csv_paths = ["C:/Users/Anelli/Desktop/plottingYB1.csv"]
exp_labels = ["YB1"]  # must match length of csv_paths

# Order concentrations as you want them on the x-axis
conc_order = ["ASW", "0.001mg/ml", "0.01mg/ml", "0.1mg/ml", "1mg/ml"]

# -----------------------------
# LOAD + TIDY
# -----------------------------
def parse_id(id_str):
    # Split like "WT_0.01mg/ml" or "ΔCheA_ASW"
    # Genotype = part before first underscore; Concentration = remainder
    parts = id_str.split("_", 1)
    genotype = parts[0]
    concentration = parts[1] if len(parts) > 1 else ""
    return genotype, concentration

frames = []
for path, label in zip(csv_paths, exp_labels):
    df = pd.read_csv(path)
    if not {"ID","IC"}.issubset(df.columns):
        raise ValueError(f"{path} must contain columns: ID, IC")
    parsed = df["ID"].apply(parse_id)
    df["Genotype"] = parsed.apply(lambda t: t[0])
    df["Concentration"] = parsed.apply(lambda t: t[1])
    df["Experiment"] = label
    frames.append(df)

data = pd.concat(frames, ignore_index=True)

# Ensure concentration order (treat as categorical)
data["Concentration"] = pd.Categorical(data["Concentration"], categories=conc_order, ordered=True)

# -----------------------------
# AGGREGATE (mean ± SD)
# -----------------------------
summary = (
    data
    .groupby(["Experiment", "Genotype", "Concentration"], observed=True, as_index=False)
    .agg(IC_mean=("IC", "mean"), IC_sd=("IC", "std"), n=("IC", "size"))
)

# Drop rows with concentrations not in the chosen order (NaN categories)
summary = summary.dropna(subset=["Concentration"])

fig, ax = plt.subplots(figsize=(10, 8))

x_levels = [c for c in conc_order
            if c in summary["Concentration"].cat.categories
            and c in summary["Concentration"].unique().tolist()]
x_pos = {c: i for i, c in enumerate(x_levels)}

# Jitter across experiments (set to 0.0 if you want exact alignment)
if len(exp_labels) == 1:
    jitter_map = {exp_labels[0]: 0.0}
elif len(exp_labels) == 2:
    jitter_map = {exp_labels[0]: -0.05, exp_labels[1]: 0.05}
else:
    offsets = np.linspace(-0.08, 0.08, num=len(exp_labels))
    jitter_map = {lab: off for lab, off in zip(exp_labels, offsets)}

linestyles = ["-", "--", "-.", ":"]
ls_map = {lab: linestyles[i % len(linestyles)] for i, lab in enumerate(exp_labels)}

for exp in exp_labels:
    for genotype in summary["Genotype"].unique():
        sub = summary[(summary["Experiment"] == exp) & (summary["Genotype"] == genotype)].copy()
        if sub.empty:
            continue
        sub = sub.sort_values("Concentration")
        x = np.array([x_pos[c] + jitter_map.get(exp, 0.0) for c in sub["Concentration"]])
        y = sub["IC_mean"].to_numpy()
        sd = sub["IC_sd"].to_numpy()

        ax.plot(
            x, y,
            linestyle=ls_map[exp],
            marker="o",
            linewidth=4,     # thicker line
            markersize=12,     # bigger points
            label=f"{genotype} ({exp})"
        )
        ax.fill_between(x, y - sd, y + sd, alpha=0.2)

# Axis labels & title
ax.set_xticks([x_pos[c] for c in x_levels])
ax.set_xticklabels(x_levels)
ax.tick_params(axis='both', labelsize=25) 
ax.set_xlabel("Fucoidan concentration (mg/ml)", fontsize=25)
ax.set_ylabel("Chemotactic Index (IC)", fontsize=25)
ax.set_ylim(0,20)


# Ensure no grid at all
ax.grid(False)

# Simple legend (no dedup step that could drop handles)
ax.legend(loc="best", frameon=False, fontsize=24, ncol=2)

# Optional: slightly larger tick labels
# ax.tick_params(axis="both", labelsize=12)

plt.tight_layout()
plt.show()
