# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:37:32 2024

@author: Anelli
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_preprocess(csv_file):
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None
    
    if 'Strains' not in data.columns:
        print("CSV file must contain a 'Strains' column.")
        return None
    
    data.set_index('Strains', inplace=True)
    return data

def create_heatmap(data):
    log_data = data.copy()
    log_data.iloc[:, 1:] = np.log10(data.iloc[:, 1:].replace(0, np.nan))
    
    # Custom colormap: Shifted towards red for values > 1 with adjusted scale
    cmap = sns.diverging_palette(220, 5, as_cmap=True)
    
    plt.figure(figsize=(18, 14))
    heatmap = sns.heatmap(
        log_data, cmap=cmap, center=0.5, vmax=1.5, cbar_kws={'label': 'log IC values'}, 
        annot=data, fmt=".2f", annot_kws={"size": 26, "color": "black"},  # Black text for readability
        linewidths=0.5, linecolor='black'  # Thin grid lines for better separation
    )
    
    control_col = 'ASW'
    if control_col in data.columns:
        control_index = data.columns.get_loc(control_col)
        for y in range(data.shape[0]):
            heatmap.add_patch(plt.Rectangle((control_index, y), 1, 1, fill=True, lw=1, facecolor='lightgray'))
    
    colorbar = heatmap.collections[0].colorbar
    colorbar.ax.tick_params(labelsize=20, color = 'black')
    colorbar.set_label('log IC values', size=28, color = 'black')
    plt.ylabel('Strains', fontsize=28, color = 'black')
    plt.xticks(rotation=45, fontsize=26, color = 'black')
    plt.yticks(rotation = 360, fontsize=28, fontstyle='italic', color = 'black')
    plt.tight_layout()
    plt.show()
    
   

def main():
    csv_file = "C:/Users/Anelli/Desktop/Experiments/ISCA_experiments/Fucoidan project/Heatmap_ISCA_Fucoidan_Fucus_purified.csv"
    data = load_and_preprocess(csv_file)
    if data is not None:
        create_heatmap(data)

if __name__ == "__main__":
    main()


#%% Code for black background plot
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:37:32 2024

@author: Anelli
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Function to load and preprocess data
def load_and_preprocess(csv_file):
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

    if 'Strains' not in data.columns:
        print("CSV file must contain a 'Strains' column.")
        return None

    data.set_index('Strains', inplace=True)
    return data

# Function to create the heatmap with a black background
def create_heatmap(data):
    # Compute log-transformed values for the gradient colors
    log_data = data.copy()
    log_data.iloc[:, 1:] = np.log10(data.iloc[:, 1:].replace(0, np.nan))  # Avoid log(0) by replacing 0 with NaN

    # Define the color map with better contrast on a black background
    cmap = sns.color_palette("coolwarm", as_cmap=True)  # Try 'magma' or 'viridis' for better visibility

    # Create the heatmap with a black background
    plt.figure(figsize=(16, 14), facecolor='black')  # Set background to black
    heatmap = sns.heatmap(
        log_data,
        cmap=cmap,
        cbar_kws={'label': 'log IC values'},
        annot=data,
        fmt=".2f",
        annot_kws={"size": 26, "color": "white"},  # Change annotation text color to white
        linewidths=1,
        linecolor="black"
    )

    # Highlight the control column in grey
    control_col = 'ASW'
    if control_col in data.columns:
        control_index = data.columns.get_loc(control_col)
        for y in range(data.shape[0]):
            heatmap.add_patch(plt.Rectangle((control_index, y), 1, 1, fill=True, lw=1, facecolor='grey'))

    # Adjust color bar legend font size and color
    colorbar = heatmap.collections[0].colorbar
    colorbar.ax.tick_params(labelsize=20, colors='white')  # White color for tick labels
    colorbar.set_label('log IC values', size=28, color='white')  # White color for the label

    # Customize the plot appearance for a black background
    plt.gca().set_facecolor('black')  # Ensure the plot area is black
    plt.ylabel('Strains', fontsize=28, color='white')
    plt.xticks(rotation=45, fontsize=26, color='white')
    plt.yticks(fontsize=28, fontstyle='italic', color='white')
    
    # Adjust layout
    plt.tight_layout()
    
    # Show the plot
    plt.show()

# Main function
def main():
    csv_file = 'C:/Users/Anelli/Desktop/Experiments/ISCA_experiments/Fucoidan project/Heatmap_ISCA_Fucoidan_fractions.csv'
    data = load_and_preprocess(csv_file)
    if data is not None:
        create_heatmap(data)

if __name__ == "__main__":
    main()
#%% Final version ?
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:37:32 2024

@author: Anelli
Refined for publication-quality heatmap visualization.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_preprocess(csv_file):
    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None
    
    if 'Strains' not in data.columns:
        print("CSV file must contain a 'Strains' column.")
        return None
    
    data.set_index('Strains', inplace=True)
    return data

def create_heatmap(data):
    log_data = data.copy()
    log_data.iloc[:, :] = np.log10(data.replace(0, np.nan))

    # Choose a publication-quality color palette
    cmap = sns.color_palette("vlag", as_cmap=True)

    plt.figure(figsize=(18, 14))  # Compact but readable

    # Plot base heatmap (no annotations yet)
    ax = sns.heatmap(
        log_data,
        cmap=cmap,
        center=0.5,
        vmax=1.5,
        cbar_kws={'label': 'log IC values'},
        linewidths=0.5,
        linecolor='black',
        mask=log_data.isnull()  # mask NaNs for visual clarity
    )

    # Annotation with dynamic text color
    def get_text_color(value, threshold=0.8):
        return 'black' if value < threshold else 'black'

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            value = data.iloc[y, x]
            log_value = log_data.iloc[y, x]
            if not pd.isna(value):
                text = f"{value:.2f}"
                text_color = get_text_color(log_value)
                ax.text(
                    x + 0.5, y + 0.5, text,
                    ha='center', va='center',
                    fontsize=32, color=text_color
                )

    # Highlight control column (e.g., ASW)
    control_col = 'ASW'
    if control_col in data.columns:
        control_index = data.columns.get_loc(control_col)
        for y in range(data.shape[0]):
            ax.add_patch(plt.Rectangle((control_index, y), 1, 1, fill=True, lw=1.5, facecolor='lightgray', edgecolor='black'))

    # Customize axes and colorbar
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=32, color='black')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=32, color='black', fontstyle='italic')
    plt.title('Purified Fucus vesiculosus', size = '34')
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=32, color='black')
    cbar.set_label('log Chemotactic Index (IC)', size=32, color='black')

    plt.tight_layout()
    plt.savefig("heatmap_fucoidan_Laminaria_purified.svg", dpi=600, bbox_inches='tight')
    plt.show()

def main():
    csv_file = "C:/Users/Anelli/Desktop/Experiments/ISCA_experiments/Fucoidan project/Heatmap_ISCA_Fucoidan_Fucus_purified.csv"
    data = load_and_preprocess(csv_file)
    if data is not None:
        create_heatmap(data)

if __name__ == "__main__":
    main()

