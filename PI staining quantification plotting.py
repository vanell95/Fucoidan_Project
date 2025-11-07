# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:19:04 2024

@author: Anelli
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load the data from the Excel file
file_path = 'C:/Users/Anelli/Desktop/Experiments/Connected_chambers_chip_experiments/Fucoidan_+30KDa_ASW_PI_staining_ASV16/Plotting_PI_staining.xlsx'
df = pd.read_excel(file_path)

# Inspect the first few rows of the data
print(df.head())

# Clean column names by stripping any leading/trailing whitespace
df.columns = df.columns.str.strip()

# Add a column for the percentage of PI-positive cells
df['percentage PI-positive'] = (df['number of PI-positive cells'] / df['total number of cells']) * 100

# Create a 'Condition' column to differentiate Fucoidan and Control samples
df['Condition'] = df['Sample'].apply(lambda x: 'Fucoidan' if 'Fucoidan' in x else 'ASW')

# Group the data by 'Condition' and calculate mean and standard deviation for total cells and PI-positive percentage
grouped_data = df.groupby('Condition').agg(
    total_mean=('total number of cells', 'mean'),
    total_std=('total number of cells', 'std'),
    pi_positive_mean=('percentage PI-positive', 'mean'),
    pi_positive_std=('percentage PI-positive', 'std')
)

# Create a figure with 2 subplots for total number of cells and percentage of PI-positive cells
# Initialize the figure
fig, ax = plt.subplots(2, 1, figsize=(8, 10))

# Barplot and stripplot for total number of cells
sns.barplot(x='Condition', y='total number of cells', data=df, ci='sd', ax=ax[0], 
            palette=['firebrick', 'lightgrey'], capsize=0.1)
sns.stripplot(x='Condition', y='total number of cells', data=df, ax=ax[0], 
              color='black', dodge=True, jitter=True, size=8, marker='o')

# Set titles and labels for the total cells plot
ax[0].set_title('Total Number of Bacteria in Different Conditions', size = 24)
ax[0].set_ylabel('Number of Bacteria', size = 20)
ax[0].set_xlabel('Condition', size = 20)
ax[0].set_xticklabels(ax[0].get_xticklabels(), fontsize=20)
ax[0].set_yticklabels(ax[0].get_yticks(), fontsize=20)


# Barplot and stripplot for percentage of PI-positive cells
sns.barplot(x='Condition', y='percentage PI-positive', data=df, ci='sd', ax=ax[1], 
            palette=['firebrick', 'lightgrey'], capsize=0.1)
sns.stripplot(x='Condition', y='percentage PI-positive', data=df, ax=ax[1], 
              color='black', dodge=True, jitter=True, size=8, marker='o')

# Set titles and labels for the PI-positive percentage plot
ax[1].set_title('Percentage of PI-positive Cells in Different Conditions', size = 24)
ax[1].set_ylabel('PI-positive Cells (%)', size = 20)
ax[1].set_xlabel('Condition', size = 20)
ax[1].set_xticklabels(ax[1].get_xticklabels(), fontsize=20)
ax[1].set_yticklabels(ax[1].get_yticks(), fontsize=20)

# Adjust layout for better spacing
plt.tight_layout()

# Display the plot
plt.show()

#%% Plot for black background
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the Excel file
file_path = 'C:/Users/Anelli/Desktop/Experiments/Connected_chamber_chip/Fucoidan_+30KDa_ASW_PI_staining_ASV16/Plotting_PI_staining.xlsx'
df = pd.read_excel(file_path)

# Clean column names by stripping any leading/trailing whitespace
df.columns = df.columns.str.strip()

# Add a column for the percentage of PI-positive cells
df['percentage PI-positive'] = (df['number of PI-positive cells'] / df['total number of cells']) * 100

# Create a 'Condition' column to differentiate Fucoidan and Control samples
df['Condition'] = df['Sample'].apply(lambda x: 'Fucoidan' if 'Fucoidan' in x else 'ASW')

# Set Seaborn dark theme for a black background
sns.set_theme(style='dark', rc={'axes.facecolor': 'black', 'figure.facecolor': 'black'})

# Create a figure with 2 subplots
fig, ax = plt.subplots(2, 1, figsize=(8, 10), facecolor='black')

# Define colors for better contrast
bar_colors = ['red', 'grey']
text_color = 'white'

def format_axes(axis):
    axis.title.set_color(text_color)
    axis.xaxis.label.set_color(text_color)
    axis.yaxis.label.set_color(text_color)
    axis.tick_params(colors=text_color)
    axis.spines['bottom'].set_color(text_color)
    axis.spines['left'].set_color(text_color)

# Barplot and stripplot for total number of cells
sns.barplot(x='Condition', y='total number of cells', data=df, ci='sd', ax=ax[0], 
            palette=bar_colors, capsize=0.1)
sns.stripplot(x='Condition', y='total number of cells', data=df, ax=ax[0], 
              color='white', dodge=True, jitter=True, size=8, marker='o')
ax[0].set_title('Total Number of Bacteria in Different Conditions', size=24)
ax[0].set_ylabel('Number of Bacteria', size=20)
ax[0].set_xlabel('Condition', size=20)
format_axes(ax[0])

# Barplot and stripplot for percentage of PI-positive cells
sns.barplot(x='Condition', y='percentage PI-positive', data=df, ci='sd', ax=ax[1], 
            palette=bar_colors, capsize=0.1)
sns.stripplot(x='Condition', y='percentage PI-positive', data=df, ax=ax[1], 
              color='white', dodge=True, jitter=True, size=8, marker='o')
ax[1].set_title('Percentage of PI-positive Cells in Different Conditions', size=24)
ax[1].set_ylabel('PI-positive Cells (%)', size=20)
ax[1].set_xlabel('Condition', size=20)
format_axes(ax[1])

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the Excel file
file_path = 'C:/Users/Anelli/Desktop/Experiments/Connected_chamber_chip/Fucoidan_+30KDa_ASW_PI_staining_ASV16/Plotting_PI_staining.xlsx'
df = pd.read_excel(file_path)

# Clean column names by stripping any leading/trailing whitespace
df.columns = df.columns.str.strip()

# Add a column for the percentage of PI-positive cells
df['percentage PI-positive'] = (df['number of PI-positive cells'] / df['total number of cells']) * 100

# Create a 'Condition' column to differentiate Fucoidan and Control samples
df['Condition'] = df['Sample'].apply(lambda x: 'Fucoidan' if 'Fucoidan' in x else 'ASW')

# Set Seaborn white theme for white background
sns.set_theme(style='white', rc={'axes.facecolor': 'white', 'figure.facecolor': 'white'})

# Create a figure with 2 subplots, white facecolor
fig, ax = plt.subplots(2, 1, figsize=(16, 16), facecolor='white')

# Define colors for bars and text
bar_colors = ['firebrick', 'grey']
text_color = 'black'
point_color = 'black'

def format_axes(axis):
    axis.title.set_color(text_color)
    axis.xaxis.label.set_color(text_color)
    axis.yaxis.label.set_color(text_color)
    axis.tick_params(colors=text_color)
    axis.spines['bottom'].set_color(text_color)
    axis.spines['left'].set_color(text_color)

# Barplot and stripplot for total number of cells
sns.barplot(x='Condition', y='total number of cells', data=df, ci='sd', ax=ax[0], 
            palette=bar_colors, capsize=0.1)
sns.stripplot(x='Condition', y='total number of cells', data=df, ax=ax[0], 
              color=point_color, dodge=True, jitter=True, size=8, marker='o')
ax[0].set_title('Total Number of Bacteria in Different Conditions', size=30)
ax[0].set_ylabel('Number of Bacteria', size=30)
ax[0].set_xlabel('', size=30)
format_axes(ax[0])

# Barplot and stripplot for percentage of PI-positive cells
sns.barplot(x='Condition', y='percentage PI-positive', data=df, ci='sd', ax=ax[1], 
            palette=bar_colors, capsize=0.1)
sns.stripplot(x='Condition', y='percentage PI-positive', data=df, ax=ax[1], 
              color=point_color, dodge=True, jitter=True, size=8, marker='o')
ax[1].set_ylabel('PI-positive Cells (%)', size=30)
ax[1].set_xlabel('', size=30)
format_axes(ax[1])

ax[0].tick_params(axis='both', labelsize=30)  # or larger if you prefer
ax[1].tick_params(axis='both', labelsize=30)

# Adjust layout and show the plot
plt.tight_layout()
plt.show()

#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the Excel file
file_path = 'C:/Users/Anelli/Desktop/Experiments/Connected_chamber_chip/Fucoidan_+30KDa_ASW_PI_staining_ASV16/Plotting_PI_staining.xlsx'
df = pd.read_excel(file_path)

# Clean column names by stripping any leading/trailing whitespace
df.columns = df.columns.str.strip()

# Add a column for the percentage of PI-positive cells
df['percentage PI-positive'] = (df['number of PI-positive cells'] / df['total number of cells']) * 100

# Create a 'Condition' column to differentiate Fucoidan and Control samples
df['Condition'] = df['Sample'].apply(lambda x: 'Fucoidan' if 'Fucoidan' in x else 'ASW')

# Set Seaborn white theme for white background
sns.set_theme(style='white', rc={'axes.facecolor': 'white', 'figure.facecolor': 'white'})

# Define colors for bars and text
bar_colors = ['firebrick', 'grey']
text_color = 'black'
point_color = 'black'

def format_axes(axis):
    axis.title.set_color(text_color)
    axis.xaxis.label.set_color(text_color)
    axis.yaxis.label.set_color(text_color)
    axis.tick_params(colors=text_color)
    axis.spines['bottom'].set_color(text_color)
    axis.spines['left'].set_color(text_color)

# 🔹 First figure: Total number of bacteria
fig1, ax1 = plt.subplots(figsize=(8, 8), facecolor='white')
sns.barplot(x='Condition', y='total number of cells', data=df, ci='sd', ax=ax1, 
            palette=bar_colors, capsize=0.1)
sns.stripplot(x='Condition', y='total number of cells', data=df, ax=ax1, 
              color=point_color, dodge=True, jitter=True, size=8, marker='o')
ax1.set_title('Total Number of Bacteria in Different Conditions', size=20)
ax1.set_ylabel('Number of Bacteria', size=20)
ax1.set_xlabel('', size=20)
ax1.tick_params(axis='both', labelsize=20)
format_axes(ax1)
plt.tight_layout()
plt.show()

# 🔹 Second figure: Percentage PI-positive
fig2, ax2 = plt.subplots(figsize=(16, 16), facecolor='white')
sns.barplot(x='Condition', y='percentage PI-positive', data=df, ci='sd', ax=ax2, 
            palette=bar_colors, capsize=0.1)
sns.stripplot(x='Condition', y='percentage PI-positive', data=df, ax=ax2, 
              color=point_color, dodge=True, jitter=True, size=8, marker='o')
ax2.set_ylabel('PI-positive Cells (%)', size=28)
ax2.set_xlabel('', size=28)
ax2.tick_params(axis='both', labelsize=28)
format_axes(ax2)
plt.tight_layout()
plt.show()
