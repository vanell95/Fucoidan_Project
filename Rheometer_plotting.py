# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 10:59:51 2024

@author: Anelli
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file into a DataFrame
df = pd.read_csv("C:/Users/Anelli/Desktop/Experiments/Rheometer experiment (Sam)/Analysis_rheometer_experiments_Fucoidan_1.csv")

# Get the name of the first column (assuming it contains shear rate values)
shear_rate_column = df.columns[0]

# Set the Shear Rate column as the index
df.set_index(shear_rate_column, inplace=True)

# Extract unique concentration names without replicates
unique_concentrations = list(dict.fromkeys(col.rsplit('_', 1)[0] for col in df.columns))  
# dict.fromkeys(...) keeps the order from the CSV

# --- CUSTOM COLORS ---
# Order will follow unique_concentrations
colors = ["darkred", "red", "grey"]

# Use Seaborn style
sns.set_style("whitegrid")

# Plotting
plt.figure(figsize=(10, 8))

for i, concentration in enumerate(unique_concentrations):
    replicate_columns = [col for col in df.columns if col.startswith(concentration)]
    
    mean_values = df[replicate_columns].mean(axis=1)
    std_values = df[replicate_columns].std(axis=1)
    
    # Assign custom color
    color = colors[i % len(colors)]
    
    plt.plot(df.index, mean_values, label=concentration, color=color, linewidth=4)
    plt.fill_between(df.index, mean_values - std_values, mean_values + std_values, color=color, alpha=0.2)

# Log scales
plt.yscale('log')
plt.xscale('log')

# Labels & title
plt.xlabel(shear_rate_column, fontsize=18)
plt.xticks(size=16)
plt.ylabel('Shear Viscosity (Pa s)', fontsize=18)
plt.yticks(size=16)
plt.title('Fucus vesiculosus', fontsize=20)

# Legend
plt.legend(loc='best', fontsize=20)

plt.tight_layout()
plt.show()
