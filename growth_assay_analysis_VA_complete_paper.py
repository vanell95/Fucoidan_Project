# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:58:31 2023

@author: Anelli
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.close('all')

# Load the data and adjust the time column
DAT = pd.read_excel("C:/Users/Anelli/Desktop/Experiments/Growth assay/PAPER_240701_Growthassay_Fucoidan_GlucNAG/Growth_assay_Fucoidan_GlucNAG_plotting_48h.xlsx")
DAT['time'] = DAT.index /10  # in hours, given 10 measurements per hour

# Define strain and condition lists
strainList = ['Vibrio cyclitrophicus', 'Pseudoalteromonas ASV16','Pseudocolwellia AS88','Vibrio coralliilytiicus']
#conditionList = ["Fucoidan 1mg/ml","Oligo Alginate 0.01mg/ml + Fucoidan 1mg/ml","Oligo alginate 0.1mg/ml + Fucoidan 1mg/ml","Oligo alginate 1mg/ml + Fucoidan 1mg/ml","Oligo alginate 10mg/ml + Fucoidan 1mg/ml","F/2 medium"]
#conditionList = ["Oligo alginate 1mg/ml", "Fucoid 1mg/ml + Oligo Alginate 1mg/ml","Fucoid 0.1mg/ml + Oligo Alginate 1mg/ml", "Fucoid 0.01mg/ml + Oligo Alginate 1mg/ml","Fucoid 0.001mg/ml + Oligo Alginate 1mg/ml","F/2 medium"]
conditionList = ["Fucoidan 1mg/ml", "Fucoid 1mg/ml + GlucNAc 0.1mM", "Fucoid 1mg/ml + GlucNAc 1mM", "Fucoid 1mg/ml + GlucNAc 10mM","F/2 medium"]
conditionList =[0,0.1,1,10] #to plot the max O.D or max growth rate you exclude all the control values
# Define colors for each strain
strain_colors = {
    'Vibrio cyclitrophicus': 'dodgerblue',
    'Pseudoalteromonas ASV16': 'forestgreen',
    'Pseudocolwellia AS88': 'firebrick',
    'Vibrio coralliilytiicus': 'darkorchid'
}

#bck = 0.001
d = []
wells = [None] * 16  # 4 strains * 6 conditions

# Create the figure with more space between subplots
plt.figure(figsize=(34,34))
plt.subplots_adjust(hspace=0.7, wspace=0.3)

for ii in range(16):  # 24 combinations (4 strains * 6 conditions)
    rowIn = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    colIn = ['1','2','3','4','5','6', '7', '8']
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
    plt.subplot(5, 4, ii + 1 )
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
plt.figure(figsize=(18,18))

# Plotting the data with thicker lines and standard deviation as shaded regions
ii = 0
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
std_values = DAT[wells[ii]].std(axis=1)
plt.plot(DAT['time'], mean_values, 'k-', linewidth=5, label='Fucoidan 1mg/ml')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='k', alpha=0.3)

ii = 4
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001

plt.plot(DAT['time'], mean_values, 'lightsalmon', linewidth=5, label='GlucNAc 0.1mM + Fucoidan 1mg/ml')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='lightsalmon', alpha=0.3)

ii = 8
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
std_values = DAT[wells[ii]].std(axis=1)
plt.plot(DAT['time'], mean_values, 'red', linewidth=5, label='GlucNAc 1mM + Fucoidan 1mg/ml')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='red', alpha=0.3)

ii = 12
mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
std_values = DAT[wells[ii]].std(axis=1)
plt.plot(DAT['time'], mean_values, 'darkred', linewidth=5, label='GlucNAc 10mM + Fucoidan 1mg/ml')
plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='darkred', alpha=0.3)

#ii = 18
#mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
#std_values = DAT[wells[ii]].std(axis=1)
#plt.plot(DAT['time'], mean_values, 'deepskyblue', linewidth=5, label='F/2 medium')
#plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='deepskyblue', alpha=0.3)

#ii = 21
#mean_values = DAT[wells[ii]].mean(axis=1)-DAT[wells[ii]].mean(axis=1)[0]+0.001
#std_values = DAT[wells[ii]].std(axis=1)
#plt.plot(DAT['time'], mean_values, 'grey', linewidth=5, label='F/2 medium')
#plt.fill_between(DAT['time'], mean_values - std_values, mean_values + std_values, color='grey', alpha=0.3)


# Labeling axes
plt.xlabel('Time (h)', fontsize=32)
plt.xlim(0, 48)
plt.ylabel('Log (O.D)', fontsize=32)
plt.yticks(size=32)
plt.xticks(size=32)
plt.yscale('log')
plt.title("ZF270", fontsize=34)
plt.ylim(0.001,1)


# Adding legend

plt.legend(prop={'size': 20},loc='lower right')

# Displaying the plot
plt.show()

#%% 3 PLOT CUMULATIVE MAX GROWTH RATE

# Create the figure
plt.figure(figsize=(20,20))

# Define color palettes
concentration_palette = sns.color_palette("deep", len(dF['concentration'].unique()))  # For concentrations
custom_colors = ["dodgerblue", "forestgreen", "firebrick", "darkorchid"]
strain_palette = sns.color_palette(custom_colors[:len(dF['strain'].unique())])  # For strains

# Create the boxplot to differentiate concentrations
sns.boxplot(
    x='concentration',
    y='max_growth_rate',
    data=dF,
    palette=concentration_palette,
    showmeans=True,
    meanline=True
)

# Overlay the swarmplot to show individual replicates, colored by strain
sns.swarmplot(
    x='concentration',
    y='max_growth_rate',
    data=dF,
    hue='strain',  # Differentiate points by strain
    palette=strain_palette,
    size=12,
    dodge=True  # Slightly offset points
)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, size=24)
plt.yticks(size=28)

# Set labels and title
plt.xlabel('Concentration', fontsize=28)
plt.ylabel('Max Growth Rate', fontsize=28)
plt.title('Average Max Growth Rate', size=28)

# Add legends for strain colors
plt.legend(fontsize=26, loc='upper right')

# Display the plot
plt.tight_layout()
plt.show()


#%% PLOT CUMULATIVE MAX OD

plt.figure(figsize=(18, 18))

for strain in dF['strain'].unique():
    strain_data = dF[dF['strain'] == strain]
    mean_values = strain_data.groupby('concentration')['OD'].mean()
    std_values = strain_data.groupby('concentration')['OD_std'].mean()  # Use stored standard deviation
    concentrations = mean_values.index

    plt.plot(concentrations, mean_values, label=strain, linewidth=5)
    plt.fill_between(concentrations, mean_values - std_values, mean_values + std_values,
                     alpha=0.3,)

plt.xscale('log')
plt.xlabel('GlucNAc concentration (mM)', fontsize=28)
plt.ylabel('Max OD', fontsize=28)
plt.title('Max OD vs. Concentration', fontsize=28)
plt.xticks(size=28)
plt.yticks(size=28)
plt.legend(prop={'size': 24}, loc='upper left')
plt.tight_layout()
plt.show()

#%% PLOT COMULATIVE MAX FROWTH RATE
plt.figure(figsize=(18,18))
for strain in dF['strain'].unique():
    strain_data = dF[dF['strain'] == strain]
    mean_values = strain_data.groupby('concentration')['gr_time'].mean()
    std_values = strain_data.groupby('concentration')['gr_std'].mean()  # Use stored standard deviation
    concentrations = mean_values.index

    plt.plot(concentrations, mean_values, label=strain, linewidth=5)
    plt.fill_between(concentrations, mean_values - std_values, mean_values + std_values,
                     alpha=0.3,)

plt.xscale('log')
plt.xlabel('GlucNAc concentration (mM)', fontsize=28)
plt.ylabel('Max Growth Rate', fontsize=28)
plt.title('Max Growth Rate vs. Concentration', fontsize=28)
plt.xticks(size=28)
plt.yticks(size=28)
plt.legend(prop={'size': 24}, loc='upper right')
