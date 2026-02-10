# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:41:15 2023

@author: Anelli
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV file
df = pd.read_csv("C:/Users/Anelli/Desktop/Experiments/Connected_chambers_chip_experiments/NaturalFucoidan_1mg_ASW_Pseudoalteromonas_ASV16_nogradient_starvation/Images_for_analysis/Pos_8_middle/STrack/global_df/Unfiltered_cell_counts.csv")

# Extract the timepoints and cell counts
timepoints = df['Timepoints']
cell_counts = df['CellCounts']
plt.style.use('dark_background')


# Create a line plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.plot(timepoints, cell_counts, marker='o', linestyle='-')
plt.title('Fucoidan')
plt.xlabel('Timepoints', size = 28)
plt.ylabel('Cell Counts', size = 28)
plt.xticks(size= 20)
plt.yticks(size= 20)
plt.grid(False)

# Show the plot
plt.show()
#Make sure to replace 'your_data.csv' with the actual file path to your CSV file. This code will read the data from the CSV file, create a line plot with timepoints on the x-axis and cell counts on the y-axis, and display the plot. You can customize the figure size, title, labels, and other plot properties according to your preferences.
plt.savefig("C:/Users/Anelli/Desktop/Fucoidan.png")
