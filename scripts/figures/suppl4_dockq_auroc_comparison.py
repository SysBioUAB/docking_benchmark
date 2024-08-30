import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
import numpy as np

df = pd.read_csv("../../data/input_files/figure_datasets/Supplementary_4_tankbind.csv")
# Sample data (replace with your actual data)
pdb_list = df["PDB"]
dockq_values_afnat = df["DockQ_afnat"]
auroc_values_afnat = df["auROC_afnat"]

dockq_values_mdpdb = df["DockQ_MDPDB"]
auroc_values_mdpdb = df["auROC_MDPDB"]

dockq_values_afflow = df["DockQ_Afflow"]
auroc_values_afflow = df["auROC_Afflow"]


# Create subplots for each subset
fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)

# Plot data for subset 1
axs[0].scatter(dockq_values_afnat, auroc_values_afnat, color='blue', alpha=0.8)
axs[0].set_title('AF', fontsize=16)
axs[0].set_xlabel('DockQ', fontsize=16)
axs[0].set_ylabel('auROC', fontsize=16)
axs[0].set_xlim(0, 1)
axs[0].set_ylim(0, 1)

# Plot data for subset 2
axs[1].scatter(dockq_values_mdpdb, auroc_values_mdpdb, color='red', alpha=0.8)
axs[1].set_title('MD_PDB', fontsize=16)
axs[1].set_xlabel('DockQ', fontsize=16)
axs[1].set_ylabel('auROC', fontsize=16)
axs[1].set_xlim(0, 1)
axs[1].set_ylim(0, 1)

# Plot data for subset 3
axs[2].scatter(dockq_values_afflow, auroc_values_afflow, color='green', alpha=0.8)
axs[2].set_title('AlphaFlow', fontsize=16)
axs[2].set_xlabel('DockQ', fontsize=16)
axs[2].set_ylabel('auROC', fontsize=16)
axs[2].set_xlim(0, 1)
axs[2].set_ylim(0, 1)

# Add horizontal line at y=0.5
for ax in axs:
    ax.axhline(y=0.5, color='black', linestyle='--', alpha=0.5)
    
    
# Add trendlines and get slopes for each subset
for i, (dockq_subset, auroc_subset) in enumerate([(dockq_values_afnat, auroc_values_afnat),
                                                  (dockq_values_mdpdb, auroc_values_mdpdb),
                                                  (dockq_values_afflow, auroc_values_afflow)]):
    slope, intercept, r_value, _, _ = linregress(dockq_subset, auroc_subset)
    axs[i].plot(dockq_subset, np.polyval([slope, intercept], dockq_subset), "r--")
    axs[i].text(0.05, 0.95, f'r-value: {r_value:.2f}', fontsize=12, color='black', transform=axs[i].transAxes)
    
# Add text labels for each point
    for j, pdb in enumerate(pdb_list[:len(dockq_subset)]):
        axs[i].text(dockq_subset[j], auroc_subset[j], pdb, fontsize=10, ha='center', va='bottom', color='black')

# Set font size for tick labels
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Set font size for tick labels
for ax in axs:
    ax.tick_params(labelsize=12)
    
# Show plots
plt.tight_layout()
#plt.savefig("Supplementary_4_tankbind.tif")
plt.show()




