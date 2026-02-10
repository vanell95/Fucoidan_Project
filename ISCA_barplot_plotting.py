"""
Created on Tues 28 14:13:53 2025

@author: Anelli
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

file_path = "C:/Users/Anelli/Desktop/Experiments/ISCA_experiments/Fucoidan project/Fucoidan_ultrapurified_Milliq_no_ions/plotting.csv"  # Replace with the actual path to your file
data = pd.read_csv(file_path)
def plot_ic_barplot(data, filled_compounds=[]):
    """
    Plots a barplot of IC values with compounds on the x-axis and log-scaled IC values on the y-axis.

    Parameters:
        data (pd.DataFrame): DataFrame containing 'Compound' and 'IC' columns.
        filled_compounds (list): List of compounds to have filled bars.
    """
    # Ensure the IC column is numeric
    data['IC'] = pd.to_numeric(data['IC'], errors='coerce')

    # Group by compound to calculate means and standard deviations
    grouped = data.groupby('ID')['IC']
    means = grouped.mean()
    stds = grouped.std()

    # Sort compounds with "ASW" first if it exists
    sorted_compounds = sorted(means.index, key=lambda x: (x != "MilliQ", x))

    #Set up the plot
    #plt.style.use('dark_background')  # Set matplotlib style to dark background
    #plt.figure(figsize=(20, 20))
    #sns.set_style("darkgrid", rc={
    #"axes.facecolor": "black",       # Black background for the plot
    #"axes.edgecolor": "white",       # White border around the plot
    #"text.color": "white",           # White text
    #"axes.labelcolor": "white",      # White axis labels
    #"xtick.color": "white",          # White x-axis tick labels
    #"ytick.color": "white",          # White y-axis tick labels
    #"grid.color": "gray"             # Optional: Adjust grid color for contrast
    
    plt.style.use('default')
    plt.figure (figsize=(20,20))# Set matplotlib style to white background
    sns.set_style("whitegrid", rc={
        "axes.facecolor": "white",       # White background for the plot
        "axes.edgecolor": "black",       # Black border around the plot
        "text.color": "black",           # Black text
        "axes.labelcolor": "black",      # Black axis labels
        "xtick.color": "black",          # Black x-axis tick labels
        "ytick.color": "black",          # Black y-axis tick labels
        "grid.color": "gray"             # Light gray grid color
})

    # Plot each compound
    colors = sns.color_palette("colorblind", len(sorted_compounds))
    for i, compound in enumerate(sorted_compounds):
        compound_data = data[data['ID'] == compound]
        x_positions = np.full(compound_data.shape[0], i)  # X positions for scatter points

        # Barplot
        bar_color = colors[i] if compound in filled_compounds else 'none'
        edge_color = colors[i] if compound != "MilliQ" else 'gray'
        plt.bar(i, means[compound], yerr=stds[compound], color=bar_color, edgecolor=edge_color, 
                linewidth=8, capsize=5, width=0.6)

        # Scatter points for individual replicates
        plt.scatter(x_positions, compound_data['IC'], color= 'k', zorder=5, s= 300)

    # Log scale for y-axis
    plt.yscale('log')
    plt.ylabel('Chemotactic Index (IC)',fontsize= 50)
    #plt.title('Surface', fontsize = 40)
    #plt.xlabel('', fontsize = 40)
    plt.axhline(y=1, color='grey', linestyle='--', linewidth=1.5)
    plt.yticks(fontsize=50)
    plt.ylim(0,100)
    plt.xlim(-0.5, len(sorted_compounds) - 0.5)
    plt.grid(visible=None)
    tick_labels = [
        r'$\bf{' + compound + '}$' if compound in filled_compounds else compound
        for compound in sorted_compounds
    ]
    plt.xticks(range(len(sorted_compounds)), tick_labels, rotation=45, ha='right', fontsize=50)


    # Add a legend for filled compounds
    if filled_compounds:
        filled_patch = [plt.Line2D([0], [0], color=colors[sorted_compounds.index(compound)], lw=4) 
                        for compound in filled_compounds if compound in sorted_compounds]
        #plt.legend(filled_patch, filled_compounds, loc='upper left',fontsize='50')


    plt.tight_layout()
    plt.show()

# Example usage with the provided dataset
filled_compounds_example = []  # Replace with desired compounds to fill
plot_ic_barplot(data, filled_compounds=filled_compounds_example)