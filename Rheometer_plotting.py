# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 10:59:51 2024

@author: Anelli
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Load CSV
# -----------------------------
df = pd.read_csv("C:/Users/Anelli/Desktop/Fig.S2A plotting.csv")

# Convert values to numeric just in case
df = df.apply(pd.to_numeric, errors="coerce").dropna()

# -----------------------------
# Normalize by ASW viscosity
# -----------------------------
df["F1_norm"] = df["F1_Shear_Viscosity"] / df["ASW_Shear_Viscosity"]
df["F10_norm"] = df["F10_Shear_Viscosity"] / df["ASW_Shear_Viscosity"]

# -----------------------------
# Error propagation for ratio
# R = A/B
# -----------------------------
df["F1_norm_std"] = df["F1_norm"] * np.sqrt(
    (df["F1_std"] / df["F1_Shear_Viscosity"])**2 +
    (df["ASW_std"] / df["ASW_Shear_Viscosity"])**2
)

df["F10_norm_std"] = df["F10_norm"] * np.sqrt(
    (df["F10_std"] / df["F10_Shear_Viscosity"])**2 +
    (df["ASW_std"] / df["ASW_Shear_Viscosity"])**2
)

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(figsize=(6,4))

color1 = "#D55E00"   # 1 mg/mL
color2 = "#0072B2"   # 10 mg/mL

# 1 mg/mL
ax.plot(df["Shear_Rate"], df["F1_norm"],
        marker="o", linewidth=2.2, color=color1,
        label="Fucoidan 1 mg/mL")

ax.fill_between(df["Shear_Rate"],
                df["F1_norm"] - df["F1_norm_std"],
                df["F1_norm"] + df["F1_norm_std"],
                color=color1, alpha=0.2)

# 10 mg/mL
ax.plot(df["Shear_Rate"], df["F10_norm"],
        marker="o", linewidth=2.2, color=color2,
        label="Fucoidan 10 mg/mL")

ax.fill_between(df["Shear_Rate"],
                df["F10_norm"] - df["F10_norm_std"],
                df["F10_norm"] + df["F10_norm_std"],
                color=color2, alpha=0.2)

# Reference line for ASW
ax.axhline(1, color="black", linestyle="--", linewidth=1.3, label="ASW control")

# Formatting
ax.set_xscale("log")
ax.set_xlabel("Shear rate (s$^{-1}$)")
ax.set_ylabel("Normalized shear viscosity")
plt.ylim(0.1,10)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(frameon=False)

plt.tight_layout()

# Save publication-quality figure
plt.savefig("Fig_S2A_fucoidan_viscosity.pdf", bbox_inches="tight")
plt.savefig("Fig_S2A_fucoidan_viscosity.svg", bbox_inches="tight")
plt.savefig("Fig_S2A_fucoidan_viscosity.png", dpi=600, bbox_inches="tight")

plt.show()