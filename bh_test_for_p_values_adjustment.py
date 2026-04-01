# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:59:22 2026

@author: Anelli
"""

import pandas as pd
from pathlib import Path
from statsmodels.stats.multitest import multipletests

# =========================
# CONFIG
# =========================
INPUT_FILE = Path("C:/Users/Anelli/Desktop/Fig.1A_holmtest.csv")
OUTPUT_FILE = Path("C:/Users/Anelli/Desktop/Fig.S1_BH_adjusted.csv")

# Column names expected in your table
COL_CONDITION = "condition"
COL_PVAL = "p_value_dunnett"

# =========================
# HELPERS
# =========================
def p_to_stars(p):
    if pd.isna(p):
        return ""
    elif p < 1e-4:
        return "****"
    elif p < 1e-3:
        return "***"
    elif p < 1e-2:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return ""

# Optional: enforce logical concentration order
condition_order = ["0.001mg/ml", "0.01mg/ml", "0.1mg/ml", "1mg/ml"]

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(INPUT_FILE)

# Clean column names just in case
df.columns = df.columns.str.strip()

# Check required columns
required_cols = [COL_CONDITION, COL_PVAL]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Make sure p-values are numeric
df[COL_PVAL] = pd.to_numeric(df[COL_PVAL], errors="coerce")

# Prepare output columns
df["p_value_bh_across_strains"] = pd.NA
df["significant_bh_0.05"] = pd.NA
df["stars_bh"] = ""

# =========================
# APPLY BH CORRECTION
# separately for each concentration
# =========================
for cond in df[COL_CONDITION].dropna().unique():
    mask = df[COL_CONDITION] == cond
    sub = df.loc[mask].copy()

    # Drop rows with missing p-values for the correction
    valid = sub[COL_PVAL].notna()
    pvals = sub.loc[valid, COL_PVAL].values

    if len(pvals) == 0:
        continue

    reject, pvals_bh, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")

    # Write results back only to valid rows
    valid_index = sub.loc[valid].index
    df.loc[valid_index, "p_value_bh_across_strains"] = pvals_bh
    df.loc[valid_index, "significant_bh_0.05"] = reject
    df.loc[valid_index, "stars_bh"] = [p_to_stars(p) for p in pvals_bh]

# Optional sorting
if set(condition_order).issubset(set(df[COL_CONDITION].dropna().unique())):
    df[COL_CONDITION] = pd.Categorical(df[COL_CONDITION], categories=condition_order, ordered=True)
    sort_cols = [c for c in ["strain", COL_CONDITION] if c in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols)

# =========================
# SAVE OUTPUT
# =========================
df.to_csv(OUTPUT_FILE, index=False)

print(f"Done. Adjusted table saved to: {OUTPUT_FILE}")
print(df.head(20))