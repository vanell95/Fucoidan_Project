# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:58:31 2023

@author: Anelli
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simps  # For AUC
from scipy.signal import savgol_filter  # For optional smoothing

plt.close('all')

# Load the data and calculate time column (assuming 10 measurements per hour)
DAT = pd.read_excel("C:/Users/Anelli/Desktop/Experiments/Growth assay/PAPER_241206_OligoAlginate_gradient_Fucoidan_ baseline/061224_Fucoidan_fucus_Oligo_Alginate_gradient.xlsx")
DAT['time'] = DAT.index / 10  # in hours

# Define strains and experimental conditions
strainList = ['ZF270', 'Pseudoalt. ASV16', 'Pseudocolwellia AS88', 'YB1']
conditionList = [
    'Fucoid 1mg/ml','Oligo Alginate 1mg/ml','Fucoid 1mg/ml + Alginate 1mg/ml','Fucoid 1mg/ml + Alginate 0.1mg/ml','Fucoid 1mg/ml + Alginate 0.01mg/ml','F/2 medium'
]

# Color coding for strains
strain_colors = {
    'ZF270': 'dodgerblue',
    'Pseudoalt. ASV16': 'forestgreen',
    'Pseudocolwellia AS88': 'firebrick',
    'YB1': 'darkorchid'
}

# Parameters
num_strains = len(strainList)
num_conditions = len(conditionList)
measurements_per_hour = 10
smoothing = True  # Toggle for growth rate smoothing

# Helper: Generate well map (96-well layout)
rows = list("ABCDEFGH")
cols = [str(i) for i in range(1, 13)]
well_map = [r + c for c in cols for r in rows]

# Storage
metrics = []

# Plot settings
plt.figure(figsize=(28, 28))
plt.subplots_adjust(hspace=0.7, wspace=0.3)

# Iterate through combinations
for idx in range(num_strains * num_conditions):
    strain_idx = idx % num_strains
    cond_idx = idx // num_strains

    strain = strainList[strain_idx]
    condition = conditionList[cond_idx]
    label = f"{strain}_{condition}"

    # Get 4 replicate wells (automated from well_map)
    start = idx * 4
    wells = well_map[start:start + 4]

    # Background correction
    background = DAT[wells].mean(axis=1)[0] + 0.001
    opt_dens = DAT[wells].mean(axis=1) - background
    opt_dens_std = DAT[wells].std(axis=1)

    # Log-transformed growth
    DAT[label] = np.log(opt_dens)

    # Growth rate calculation
    growth_rate = opt_dens.diff() * measurements_per_hour
    if smoothing:
        growth_rate = pd.Series(savgol_filter(growth_rate.fillna(0), 11, 3))  # Savitzky-Golay smoothing

    # AUC calculation
    auc = simps(opt_dens, DAT['time'])

    # Metrics
    metrics.append({
        'strain': strain,
        'condition': condition,
        'max_growth_rate': growth_rate.max(),
        'time_to_max_growth': growth_rate.idxmax() / measurements_per_hour,
        'lag_time_OD': np.argmax(opt_dens > 0.001) / measurements_per_hour,
        'lag_time_GR': np.argmax(growth_rate > 0.001) / measurements_per_hour,
        'OD_max': opt_dens.max(),
        'OD_std_max': opt_dens_std.max(),
        'gr_OD_mean': growth_rate[(opt_dens > 0.001) & (opt_dens < 1.5)].mean(),
        'initial_gr': growth_rate[:50].mean(),
        'gr_std': growth_rate.std(),
        'AUC': auc,
        'wells': wells
    })

    # Plotting
    plt.subplot(num_conditions, num_strains, idx + 1)
    plt.plot(DAT['time'], opt_dens, color=strain_colors[strain])
    plt.fill_between(DAT['time'], opt_dens - opt_dens_std, opt_dens + opt_dens_std, color=strain_colors[strain], alpha=0.3)
    plt.yscale('log')
    plt.ylim(0.0001,1)
    plt.xlim(0, 48)
    plt.xlabel("Time (h)", fontsize=12)
    plt.ylabel("OD", fontsize=12)
    plt.title(label, fontsize=14)
    plt.grid(color='grey')

# Show the final plot
plt.show()

# Save metrics to CSV
results_df = pd.DataFrame(metrics)
results_df.to_csv("growth_metrics_output.csv", index=False)

print("✅ Analysis complete. Results saved to 'growth_metrics_output.csv'")


