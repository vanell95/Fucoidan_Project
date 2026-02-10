# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# USER INPUT
# -----------------------------
csv_paths = ["C:/Users/Anelli/Desktop/Experiments/ISCA_experiments/Fucoidan project/Fucoidan_purified_Fucus_gradient/plottingYB1_FIG2A.csv"]
exp_labels = ["YB1"]  # can still keep this even if single experiment

# Order on x-axis (as in panel A)
conc_order = ["ASW", "0.001mg/ml", "0.01mg/ml", "0.1mg/ml", "1mg/ml"]
baseline_conc = "ASW"

# Colors as in panel A (matplotlib default blue + orange)
genotype_colors = {
    "WT": "#1f77b4",
    "ΔCheA": "#ff7f0e"
}

# For raw-point jitter (within each x category)
rng = np.random.default_rng(0)
raw_jitter = 0.06

# -----------------------------
# LOAD + TIDY
# -----------------------------
def parse_id(id_str: str):
    parts = str(id_str).split("_", 1)
    genotype = parts[0]
    concentration = parts[1] if len(parts) > 1 else ""
    return genotype, concentration

frames = []
for path, label in zip(csv_paths, exp_labels):
    df = pd.read_csv(path)
    if not {"ID", "IC"}.issubset(df.columns):
        raise ValueError(f"{path} must contain columns: ID, IC")
    parsed = df["ID"].apply(parse_id)
    df["Genotype"] = parsed.apply(lambda t: t[0])
    df["Concentration"] = parsed.apply(lambda t: t[1])
    df["Experiment"] = label
    frames.append(df)

data = pd.concat(frames, ignore_index=True)

# categorical concentration order
data["Concentration"] = pd.Categorical(
    data["Concentration"], categories=conc_order, ordered=True
)

# -----------------------------
# AGGREGATE (mean ± SD)
# -----------------------------
summary = (
    data
    .groupby(["Genotype", "Concentration"], observed=True, as_index=False)
    .agg(IC_mean=("IC", "mean"), IC_sd=("IC", "std"), n=("IC", "size"))
)
summary = summary.dropna(subset=["Concentration"])

# -----------------------------
# PLOT (panel A style)
# -----------------------------
fig, ax = plt.subplots(figsize=(6.0, 5.0))  # close to panel A aspect

# X mapping
x_levels = [c for c in conc_order if c in summary["Concentration"].cat.categories]
x_pos = {c: i for i, c in enumerate(x_levels)}

# Baseline dashed line at IC = 1 (grey, dashed)
ax.axhline(1, linestyle=(0, (4, 4)), linewidth=1.5, color="0.7", zorder=0)

# Raw replicate dots (black), jittered slightly; ASW in grey
for conc in x_levels:
    sub = data[data["Concentration"] == conc].copy()
    if sub.empty:
        continue

    x0 = x_pos[conc]
    xj = x0 + rng.uniform(-raw_jitter, raw_jitter, size=len(sub))

    if conc == baseline_conc:
        ax.scatter(xj, sub["IC"], s=30, color="0.5", alpha=0.9, zorder=2)
    else:
        ax.scatter(xj, sub["IC"], s=30, color="k", alpha=0.9, zorder=2)

# Mean ± SD for ASW (control), shown as colored point + error bar (no line)
asw_summary = summary[summary["Concentration"] == baseline_conc]
for genotype in asw_summary["Genotype"].unique():
    sub = asw_summary[asw_summary["Genotype"] == genotype]
    if sub.empty:
        continue

    x = x_pos[baseline_conc]
    y = float(sub["IC_mean"].iloc[0])
    sd = float(sub["IC_sd"].iloc[0]) if not np.isnan(sub["IC_sd"].iloc[0]) else 0.0
    ax.errorbar(
    x, y, yerr=sd,
    fmt="o",
    color="0.35",          # dark grey for control
    markersize=6.5,
    capsize=3.5,
    linewidth=1.8,
    zorder=3
    )

# Genotype means ± SD as colored lines/markers, excluding ASW from the line
for genotype in summary["Genotype"].unique():
    col = genotype_colors.get(genotype, None)

    sub = summary[summary["Genotype"] == genotype].copy()
    sub = sub[sub["Concentration"] != baseline_conc].sort_values("Concentration")
    if sub.empty:
        continue

    x = np.array([x_pos[c] for c in sub["Concentration"]])
    y = sub["IC_mean"].to_numpy()
    sd = np.nan_to_num(sub["IC_sd"].to_numpy(), nan=0.0)

    ax.errorbar(
        x, y, yerr=sd,
        fmt="o-",
        color=col,
        linewidth=2.2,
        markersize=6.5,
        capsize=3.5,
        zorder=3,
        label=f"Vibrio coralliilyticus YB1 {genotype}"
    )

# Axis formatting (panel A: log y)
ax.set_yscale("log")
ax.set_ylim(0.6, 20)

ax.set_xticks([x_pos[c] for c in x_levels])
ax.set_xticklabels(["ASW", "0.001", "0.01", "0.1", "1"], fontsize=11)

ax.set_xlabel("Fucoidan (mg/mL)", fontsize=13)
ax.set_ylabel(r"Chemotactic Index ($I_c$)", fontsize=13)

ax.tick_params(axis="y", labelsize=11)
ax.grid(False)

# Legend in upper-left, with box
leg = ax.legend(loc="upper left", frameon=True, fontsize=10, borderpad=0.4)
leg.get_frame().set_linewidth(0.8)
leg.get_frame().set_edgecolor("0.8")

plt.tight_layout()

# Export if needed:
# plt.savefig("Fig2A_panelA.pdf", dpi=300, bbox_inches="tight")
plt.show()
