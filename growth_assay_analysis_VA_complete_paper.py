# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:58:31 2023

@author: Anelli
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.cm as cm
import re

plt.close('all')

# Load the data and adjust the time column
DAT = pd.read_excel("C:/Users/Anelli/Desktop/Experiments/Growth assay/PAPER_241206_OligoAlginate_gradient_Fucoidan_ baseline/241206_OligoAlginate_gradient_Fucoidan_ baseline.xlsx")
DAT['time'] = DAT.index /10  # in hours, given 10 measurements per hour

# Define strain and condition lists
strainList = ['ZF270','ASV16','AS88','YB1']
#conditionList = ["Oligo alginate 1mg/ml", "Fucoid 1mg/ml + Oligo Alginate 1mg/ml","Fucoid 0.1mg/ml + Oligo Alginate 1mg/ml", "Fucoid 0.01mg/ml + Oligo Alginate 1mg/ml","Fucoid 0.001mg/ml + Oligo Alginate 1mg/ml","F/2 medium"]
#conditionList = ["Fucoid 1mg/ml","GlucNAc 0.1mM + Fucoidan 1mg/ml","GlucNAc 1mM + Fucoidan 1mg/ml","GlucNAc 10mM + Fucoidan 1mg/ml","GlucNAc 10mM","F/2 medium"]
#conditionList = ['F/2 medium','Fucoid 0.001mg/ml','Fucoid 0.01mg/ml','Fucoid 0.1mg/ml','Fucoid 1mg/ml']
#conditionList = ['GlucNAc 1mM','GlucNAc 1mM + Fucoid 0.001mg/ml','GlucNAc 1mM + Fucoid 0.01mg/ml','GlucNAc 1mM + Fucoid 0.1mg/ml','GlucNAc 1mM + Fucoid 1mg/ml','F/2 medium']
conditionList = ['Fucoid 1mg/ml','Oligo Alginate 1mg/ml','Fucoid 1mg/ml + Alginate 1mg/ml','Fucoid 1mg/ml + Alginate 0.1mg/ml','Fucoid 1mg/ml + Alginate 0.01mg/ml','F/2 medium']
#conditionList =[0,0.01,0.1,1] #to plot the max O.D or max growth rate you exclude all the control values
# Define colors for each strain
strain_colors = {
    'ZF270': 'dodgerblue',
    'ASV16': 'forestgreen',
    'AS88': 'firebrick',
    'YB1': 'darkorchid'
}

#bck = 0.001
d = []
wells = [None] * 24  # 4 strains * 6 conditions

# Create the figure with more space between subplots
plt.figure(figsize=(34,34))
plt.subplots_adjust(hspace=0.7, wspace=0.3)

for ii in range(24):  # 24 combinations (4 strains * 6 conditions)
    rowIn = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    colIn = ['1','2','3','4','5','6','7','8','9','10','11','12']
    wells[ii] = [rowIn[rr] + colIn[cc] for rr, cc in zip(range(4 * np.mod(int(np.floor(ii / 1)), 2), 4 * np.mod(int(np.floor(ii / 1)), 2) + 4), [1 * int(np.floor(ii / 2)) for x in range(4)])]
    bck = DAT[wells[ii]].mean(axis=1)[0] + 0.001
    strain_condition_key = strainList[np.mod(ii, 4)] + '_' + str(conditionList[int(np.floor(ii / 4))])
    DAT[strain_condition_key] = np.log(DAT[wells[ii]].mean(axis=1) - bck)
    growth_rate = 10*DAT[strain_condition_key].diff().rolling(window=11, center=True).mean() #multiply for the number of measurements x hour (usually 10)
    opt_dens = DAT[wells[ii]].mean(axis=1) - bck
    opt_dens_std = DAT[wells[ii]].std(axis=1)

    d.append({
        'strain': strainList[np.mod(ii, 4)],
        'concentration': conditionList[int(np.floor(ii / 4))],
        'max_growth_rate': np.max(growth_rate),
        'time_to_max_g': np.argmax(growth_rate) / 10,  # Adjusted for 10 measurements per hour
        'lag_time_OD': np.argmax(opt_dens > 0.001) / 10,  # Adjusted for 10 measurements per hour
        'lag_time': np.argmax(growth_rate > 0.001) / 10,  # Adjusted for 10 measurements per hour
        'well_index': str(wells[ii]),
        'OD': np.max(opt_dens),
        'OD_std': opt_dens_std.max(),  # Store the maximum standard deviation of OD
        'gr_OD': np.nanmean(growth_rate[(opt_dens > 0.001) & (opt_dens < 1.5)]),
        'gr_time': np.mean(growth_rate[0:50]),  # Average growth rate during initial time
        'gr_std': growth_rate.std(),  # Store the standard deviation of growth rate
  })

    # Plotting optical density with colors for each strain
    plt.subplot(6, 4, ii + 1 )
    plt.plot(DAT['time'], opt_dens, color=strain_colors[strainList[np.mod(ii, 4)]])
    plt.fill_between(DAT['time'], opt_dens - opt_dens_std, opt_dens + opt_dens_std, color=strain_colors[strainList[np.mod(ii, 4)]], alpha=0.3)
    plt.ylim((0.001, 1))
    plt.title(strain_condition_key, fontsize=15)
    plt.yscale('log')
    plt.xlabel('Time (h)', fontsize=15)
    plt.ylabel('O.D Measurement', fontsize=15)
    plt.yticks(size=15)
    plt.xticks(size=15)
    plt.xlim(0,48)
    plt.grid(False)
    
# Create DataFrame from the collected data
dF = pd.DataFrame(d)

plt.show()

plt.plot()


#%% PLOT SINGLE STRAIN O.D MEASUREMENT 
import matplotlib.pyplot as plt

# Assuming DAT is a DataFrame and wells is a list of column names or indices
plt.figure(figsize=(20,20))

# Plotting the data with thicker lines and standard deviation as shaded regions
ii = 1
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
std_values = DAT[wells[ii]].std(axis=1)
plt.plot(DAT['time'], mean_values, 'olive', linewidth=8, label='Fucoidan 1 mg/mL')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='olive', alpha=0.3)

ii = 5
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
std_values = DAT[wells[ii]].std(axis=1)
plt.plot(DAT['time'], mean_values, 'salmon', linewidth=8, label='Oligo Alginate 1 mg/mL')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='salmon', alpha=0.3)

ii = 9
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
std_values = DAT[wells[ii]].std(axis=1)
plt.plot(DAT['time'], mean_values, 'tomato', linewidth=8, label='Fucoidan 1 mg/ml + Alginate 1 mg/ml')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='tomato', alpha=0.3)

ii = 13
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
std_values = DAT[wells[ii]].std(axis=1)
plt.plot(DAT['time'], mean_values, 'red', linewidth=8, label='Fucoidan 1 mg/ml + Alginate 0.1 mg/ml')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='red', alpha=0.3)

ii = 17
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
std_values = DAT[wells[ii]].std(axis=1)
plt.plot(DAT['time'], mean_values, 'darkred', linewidth=8, label='Fucoidan 1 mg/ml + Alginate 0.01 mg/ml')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='darkred', alpha=0.3)

ii = 21
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
std_values = DAT[wells[ii]].std(axis=1)
plt.plot(DAT['time'], mean_values, 'grey', linewidth=8, label='F/2 medium')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='grey', alpha=0.3)


# Labeling axes
plt.xlabel('Time (h)', fontsize=38)
plt.xlim(0, 48)
plt.ylabel('log(OD)', fontsize=38)
plt.yticks(size=38)
plt.xticks(size=38)
plt.yscale('log')
#plt.title("ASV16", fontsize=34)
plt.ylim(0.001,2)
plt.gca().set_facecolor('white')
plt.grid(False)

# Adding legend

plt.legend(prop={'size': 40},loc='upper left')

# Displaying the plot
plt.show()

#%% PLOT CUMULATIVE MAX OD
import matplotlib.pyplot as plt
import numpy as np

# Manually defined colors based on your image
custom_colors = [
    '#1f77b4',  # Blue — Vibrio cyclitrophicus
    '#2ca02c',  # Orange - Vibrio coralliilyticus 
    '#d62728',  # Green — Pseudoalteromonas ASV16
    '#ff7f0e'   # Red — Pseudocollwellia AS88
]

strains = dF['strain'].unique()
plt.figure(figsize=(16, 16))

for i, strain in enumerate(strains):
    strain_data = dF[dF['strain'] == strain]

    # Group once, then convert to arrays
    grouped = strain_data.groupby('concentration')[['OD', 'OD_std']].mean()
    concentrations = grouped.index.to_numpy(dtype=float)
    mean_values = grouped['OD'].to_numpy()
    std_values = grouped['OD_std'].to_numpy()

    # ---- NEW: remove non-positive concentrations to avoid log(0) ----
    mask = concentrations > 0
    concentrations = concentrations[mask]
    mean_values = mean_values[mask]
    std_values = std_values[mask]

    # If nothing left, skip this strain
    if concentrations.size == 0:
        continue
    # ---------------------------------------------------------------

    color = custom_colors[i % len(custom_colors)]

    # Plot the line
    plt.plot(concentrations, mean_values, label=strain, linewidth=5, color=color)

    # Add scatter points
    plt.scatter(concentrations, mean_values, color=color, s=200)

    # Add the shaded error area
    plt.fill_between(
        concentrations,
        mean_values - std_values,
        mean_values + std_values,
        alpha=0.3,
        color=color,
    )

# Axis and style settings
plt.xscale('log')
plt.xlabel('Oligo alginate)', fontsize=34)
plt.ylabel('Max OD', fontsize=38)
plt.ylim(0.0001, 0.5)
plt.xlim(0.009, 1.1)
plt.xticks(size=38)
plt.yticks(size=38)
plt.grid(False)
plt.legend(prop={'size': 34}, loc='upper left')
plt.tight_layout()
plt.show()
