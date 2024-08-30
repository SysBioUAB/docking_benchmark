import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from matplotlib import rcParams

# figure size in inches
rcParams['figure.figsize'] = 19.20,10.80

# Read your data
df = pd.read_csv("../../data/input_files/figure_datasets/Figure_6A_roc_results.csv",sep=';')
data_array = df.iloc[:,1:].values
proteins = df["PDB_ID_chain"].tolist()
structure_types = ["PDB","AF","MD","AlphaFlow"]*8

# Define custom color map boundaries and colors
bounds = [0, 0.4, 0.7, 1]
colors = ['#fc8d59', '#ffffbf', '#91cf60']

# Extend colors to cover the entire range from 0 to 1
full_colors = ['#fc8d59'] + colors + ['#91cf60']

# Extend boundaries to cover the entire range from 0 to 1
full_bounds = np.linspace(0, 1, len(full_colors))

# Create the custom color map
custom_color_map = LinearSegmentedColormap.from_list('custom_colors', list(zip(full_bounds, full_colors)))

# Create a mask for values equal to 0
mask = np.where(data_array == 0, True, False)

# Create the heatmap
heatmap = sns.heatmap(data_array, vmin=0, vmax=1, annot=False, fmt=".2f", cbar_kws={"ticks": np.arange(0,1.1,0.1)}, annot_kws={'color':'black'}, linewidths=1, linecolor='white', cmap=custom_color_map, yticklabels=proteins, xticklabels=structure_types, mask=mask, cbar=True)  

# Apply linewidths every two columns
for i in range(4, len(structure_types), 4):
    heatmap.axvline(i, color='white', lw=4)
for i in range(2, len(structure_types), 2):   
    heatmap.axhline(i, color='white', lw=4)

heatmap.collections[0].colorbar.ax.tick_params(labelsize=18)
heatmap.collections[0].colorbar.ax.set_ylabel('auROC', fontsize=18)


plt.xticks(rotation=45, ha='right',fontsize=14)
plt.yticks(fontsize=14)

plt.xlabel('Initial structure', fontsize=14)
plt.ylabel('PDB code', fontsize=18)

plt.savefig("Figure_6_heatmap.svg", format='svg')

