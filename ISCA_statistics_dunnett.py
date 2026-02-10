# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 10:12:31 2025

@author: Anelli
"""

#%% Statistical test using ONE-WAY ANOVA + POST HOC DUNNETT'S TEST for single strains
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

def run_anova_dunnett(file_path, log_transform=False, alpha=0.05, alternative='two-sided'):
    """
    Run one-way ANOVA followed by Dunnett’s test (ASW as control).
    
    Parameters:
        file_path (str): Path to CSV file (must have 'ID' and 'IC' columns)
        log_transform (bool): If True, uses log(IC) values
        alpha (float): Significance threshold for ANOVA
        alternative (str): 'two-sided', 'less', or 'greater'
    
    Returns:
        tuple: (anova_table, dunnett_results or None)
    """
    # Load data
    df = pd.read_csv(file_path)
    if log_transform:
        df['cellcounts'] = np.log(df['cellcounts'])
    
    # --- 1. One-way ANOVA ---
    model = ols('cellcounts ~ C(ID)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    
    print("\n=== One-way ANOVA ===")
    print(anova_table)
    
    # --- 2. Dunnett’s test if ANOVA significant ---
    p_val_anova = anova_table['PR(>F)'][0]
    dunnett_results = None
    if p_val_anova < alpha:
        print("\nANOVA significant (p < {:.3f}), proceeding with Dunnett’s test...".format(alpha))
        
        control = df[df['ID'] == 'FSW']['cellcounts'].values
        treatments = [df[df['ID'] == cmpd]['cellcounts'].values
                      for cmpd in df['ID'].unique() if cmpd != 'FSW']
        labels = [cmpd for cmpd in df['ID'].unique() if cmpd != 'FSW']
        
        res = stats.dunnett(*treatments, control=control, alternative=alternative)
        
        dunnett_results = pd.DataFrame({
            'Compound': labels,
            'statistic': res.statistic,
            'p-value': res.pvalue
        })
        
        print("\n=== Dunnett’s Test Results ===")
        print(dunnett_results)
    else:
        print("\nANOVA not significant (p >= {:.3f}), skipping Dunnett’s test.".format(alpha))
    
    return anova_table, dunnett_results


# Example usage:
file_path = "C:/Users/Anelli/Desktop/Experiments/ISCA_experiments/Mallorca_ISCA_deployment/041023/041022_Depth_statistics.csv"

# Raw IC values
anova_raw, dunnett_raw = run_anova_dunnett(file_path, log_transform=False)

# Log-transformed IC values
anova_log, dunnett_log = run_anova_dunnett(file_path, log_transform=True)

#%% Statistical test using ONE-WAY ANOVA + POST HOC DUNNETT'S TEST for multiple strains

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from pathlib import Path
from scipy import stats  # needs a version that exposes stats.dunnett

# ---------------- CONFIG ----------------
FILE_PATH = Path("C:/Users/Anelli/Desktop/Experiments/ISCA_experiments/Fucoidan project/Fucoidan_purified_Fucus_gradient/Fucoidan_Fucus_purified_gradient_ISCA_screening_statistics.csv")
ALPHA = 0.05
ALTERNATIVE = "two-sided"  # 'two-sided' | 'greater' | 'less'

# If SciPy lacks stats.dunnett, you can use scikit-posthocs:
# pip install scikit-posthocs
# import scikit_posthocs as sp

# ------------- helpers -------------
def _pick_group_and_response(df: pd.DataFrame):
    group_col = "ID" if "ID" in df.columns else None
    if group_col is None:
        obj = [c for c in df.columns if df[c].dtype == object]
        if not obj:
            raise ValueError("No group column found.")
        group_col = obj[0]
    if "IC" in df.columns:
        resp_col = "IC"
    else:
        num = [c for c in df.columns if c != group_col and pd.api.types.is_numeric_dtype(df[c])]
        if not num:
            raise ValueError("No numeric response column found (expected 'IC').")
        resp_col = num[0]
    return group_col, resp_col

def _split_strain_condition(label: str):
    parts = str(label).rsplit("_", 1)
    return (parts[0], parts[1]) if len(parts) == 2 else (str(label), "")

# ------------- main -------------
def run_per_strain_exact_dunnett_log10(csv_path: Path, alpha=0.05, alternative="two-sided"):
    df = pd.read_csv(csv_path).copy()
    group_col, resp_col = _pick_group_and_response(df)
    df = df[[group_col, resp_col]].dropna().rename(columns={group_col: "ID", resp_col: "IC"})
    parsed = df["ID"].apply(_split_strain_condition)
    df["strain"] = parsed.apply(lambda t: t[0])
    df["condition"] = parsed.apply(lambda t: t[1])

    # log10 transform (zero-safe)
    if (df["IC"] <= 0).any():
        eps = np.nextafter(0, 1)
        df["IC"] = df["IC"].clip(lower=0) + eps
    df["IC"] = np.log10(df["IC"])

    if not hasattr(stats, "dunnett"):
        raise ImportError(
            "Your SciPy does not provide stats.dunnett (exact Dunnett). "
            "Upgrade SciPy, or use scikit-posthocs:\n"
            "  pip install scikit-posthocs\n"
            "and replace the per-strain block with:\n"
            "  sp.posthoc_dunnett(sub, val_col='IC', group_col='condition', control='ASW', alternative=alternative)"
        )

    anova_rows = []
    dunnett_rows = []

    for s, sub in df.groupby("strain"):
        if "ASW" not in set(sub["condition"]):
            continue

        # --- ANOVA within strain ---
        model = ols('IC ~ C(condition)', data=sub).fit()
        anova_tbl = sm.stats.anova_lm(model, typ=2)
        try:
            p_anova = anova_tbl.loc['C(condition)', 'PR(>F)']
            F = anova_tbl.loc['C(condition)', 'F']
            df1 = anova_tbl.loc['C(condition)', 'df']
            df2 = anova_tbl.loc['Residual', 'df']
        except KeyError:
            row = anova_tbl.iloc[0]
            p_anova, F, df1 = row['PR(>F)'], row['F'], row['df']
            df2 = anova_tbl.iloc[1]['df'] if anova_tbl.shape[0] > 1 else np.nan

        anova_rows.append({
            "strain": s, "df_between": df1, "df_within": df2, "F": F, "p_value": p_anova, "n_total": len(sub)
        })

        if p_anova >= alpha:
            continue

        # --- Exact Dunnett: treatments vs ASW ---
        ctrl = sub.loc[sub["condition"] == "ASW", "IC"].values
        labels, arrays = [], []
        for cond, g in sub.groupby("condition"):
            if cond == "ASW":
                continue
            labels.append(cond)
            arrays.append(g["IC"].values)

        # SciPy dunnett expects *treatments, control=ctrl
        res = stats.dunnett(*arrays, control=ctrl, alternative=alternative)
        # res.statistic and res.pvalue are arrays aligned with 'labels'

        for cond, stat, pval in zip(labels, np.atleast_1d(res.statistic), np.atleast_1d(res.pvalue)):
            tr = sub.loc[sub["condition"] == cond, "IC"].values
            dunnett_rows.append({
                "strain": s,
                "comparison": f"{cond} vs ASW",
                "condition": cond,
                "n_group": len(tr),
                "n_ctrl": len(ctrl),
                "mean_group_log10": float(np.mean(tr)),
                "mean_ctrl_log10": float(np.mean(ctrl)),
                "t_stat_dunnett": float(stat),
                "p_value_dunnett": float(pval)
            })

    anova_df = pd.DataFrame(anova_rows)
    dunnett_df = pd.DataFrame(dunnett_rows) if dunnett_rows else None
    return anova_df, dunnett_df

# ---- run & save ----
anova, posthoc = run_per_strain_exact_dunnett_log10(FILE_PATH, alpha=ALPHA, alternative=ALTERNATIVE)

prefix = FILE_PATH.stem
outdir = FILE_PATH.parent
anova.to_csv(outdir / f"{prefix}__anova_log10_per_strain_exact_dunnett.csv", index=False)
if posthoc is not None:
    posthoc.to_csv(outdir / f"{prefix}__posthoc_log10_per_strain_exact_dunnett.csv", index=False)

print("Saved ANOVA and post-hoc CSVs next to the input file.")
