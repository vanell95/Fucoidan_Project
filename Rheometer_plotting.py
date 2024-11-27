# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 10:59:51 2024

@author: Anelli
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file into a DataFrame
df = pd.read_csv("C:/Users/Anelli/Desktop/Experiments/Rheometer experiment (Sam)/Analysis_rheometer_experiments_Fucoidan.csv")

# Get the name of the first column (assuming it contains shear rate values)
shear_rate_column = df.columns[0]

# Set the Shear Rate column as the index
df.set_index(shear_rate_column, inplace=True)

# Use Seaborn style for better aesthetics
sns.set_style("whitegrid")

# Plotting
plt.figure(figsize=(10, 6))

# Plot each treatment against Shear Rate with different line styles and colors
colors = sns.color_palette("husl", n_colors=len(df.columns))
linestyles = ['solid', 'solid', 'solid'] * (len(df.columns) // 4 + 1)
for i, treatment in enumerate(df.columns):
    plt.plot(df.index, df[treatment], label=treatment, linestyle=linestyles[i % len(linestyles)], color=colors[i], linewidth=4) # Increased linewidth

# Set logarithmic scale for both axes
plt.yscale('log')
plt.xscale('log')

# Add labels and title
plt.xlabel(shear_rate_column)
plt.ylabel('Shear Viscosity (Pa s)')
plt.title('Fucoidan Shear Viscosity vs. ' + shear_rate_column)

# Add legend with adjusted location and fontsize
plt.legend(loc='best', fontsize='large')

# Show plot
plt.tight_layout()
plt.show()




#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file into a DataFrame
df = pd.read_csv("C:/Users/Anelli/Desktop/Experiments/Rheometer experiment (Sam)/Analysis_rheometer_experiments_Fucoidan_1.csv")

# Get the name of the first column (assuming it contains shear rate values)
shear_rate_column = df.columns[0]

# Set the Shear Rate column as the index
df.set_index(shear_rate_column, inplace=True)

# Extract unique concentration names without replicates (assuming a naming convention like "Concentration_1", "Concentration_2", etc.)
unique_concentrations = list(set(col.rsplit('_', 1)[0] for col in df.columns))

# Use Seaborn style for better aesthetics
sns.set_style("whitegrid")

# Plotting
plt.figure(figsize=(10, 6))

# Plot each treatment against Shear Rate with different line styles and colors
colors = sns.color_palette("husl", n_colors=len(unique_concentrations))
for i, concentration in enumerate(unique_concentrations):
    # Get all replicates for the current concentration
    replicate_columns = [col for col in df.columns if col.startswith(concentration)]
    
    # Calculate mean and standard deviation across replicates
    mean_values = df[replicate_columns].mean(axis=1)
    std_values = df[replicate_columns].std(axis=1)
    
    # Plot the mean line
    plt.plot(df.index, mean_values, label=concentration, color=colors[i], linewidth=4)
    
    # Plot the shaded area representing the standard deviation
    plt.fill_between(df.index, mean_values - std_values, mean_values + std_values, color=colors[i], alpha=0.2)

# Set logarithmic scale for both axes
plt.yscale('log')
plt.xscale('log')

# Add labels and title
plt.xlabel(shear_rate_column, fontsize = 18)
plt.xticks(size = 16)
plt.ylabel('Shear Viscosity (Pa s)', fontsize = 18)
plt.yticks(size = 16)
plt.title('Fucoidan Shear Viscosity', fontsize = 18)

# Add legend with adjusted location and fontsize
plt.legend(loc='best', fontsize='large')

# Show plot
plt.tight_layout()
plt.show()
