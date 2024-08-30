import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu
import numpy as np


df = pd.read_csv("../../data/input_files/figure_datasets/Figure_6B_roc_results.csv",sep=';')
# Extracting column indexes
# Assuming the first column is not to be used, and the rest are grouped every four columns
groups = [list(range(i, i + 4)) for i in range(1, len(df.columns), 4)]

# Setting up colors for each group
colors = sns.color_palette("husl", len(groups))

# Setting up the violin plot
plt.figure(figsize=(14, 6))

positions = []
significant_pairs = []
# Loop through each group
for i, group in enumerate(groups):
    # Extracting data for the current group
    data = [df.iloc[:, idx] for idx in group]
    
    # Plotting violins for the current group
    vp = plt.violinplot(data, positions=[i * 4 + j + 1 for j in range(len(group))], showmeans=True, showextrema=False, widths=0.7)
    
    positions.extend([i * 4 + j + 1 for j in range(len(group))])
    
    # Coloring the violins
    for patch in vp['bodies']:
        patch.set_facecolor(colors[i])
        patch.set_edgecolor('black')  # Set edge color to black
 
    vp['cmeans'].set_color(['black']*4)
    # Performing statistical tests
    for j in range(len(data)):
        for k in range(j + 1, len(data)):
            p_value = mannwhitneyu(data[j], data[k]).pvalue
            if p_value < 0.05:
                significant_pairs.append((i, j, k, p_value))

# Print significant pairs
for group_idx, col1_idx, col2_idx, p_value in significant_pairs:
    print(f"Groups {group_idx+1}: {df.columns[col1_idx+1]} and {df.columns[col2_idx+1]} are significantly different (p-value: {p_value:.3f})")

plt.axhline(y=0.5, color='black', linestyle='--', lw=1)
# Adding x-axis labels

plt.xlabel('Structure Type')
plt.ylabel('auROC values')
plt.tick_params(bottom=False,labelbottom=False)
plt.ylim(0,1.2)
plt.yticks(np.arange(0,1.1,0.1))
plt.savefig('violin.png',dpi=300)
plt.tight_layout()
plt.show()
