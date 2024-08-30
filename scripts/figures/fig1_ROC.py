import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('../../data/input_files/figure_datasets/Figure_1_ROC.csv')
# Drop rows with NaN values
data.dropna(inplace=True)
# Assuming your CSV has columns 'Score1', 'Condition1', 'Score2', 'Condition2'
scores = [-data['PDB'], -data['AF'], -data['MD'], -data['AlphaFlow']]
conditions = [data['Nat_ran_PDB'], data['Nat_ran_AF'], data['Nat_ran_MD'], data['Nat_ran_AlphaFlow']]
labels = ['PDB','AF','MD','AlphaFlow']

# Plot ROC curve for each group
plt.figure(figsize=(8, 6))
for i in range(len(scores)):
    fpr, tpr, _ = roc_curve(conditions[i], scores[i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'{labels[i]} (AUC = {roc_auc:.3f})')

plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random Guess')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate',fontsize=14)
plt.ylabel('True Positive Rate',fontsize=14)
plt.title('Glide performance 5FMK_A',fontsize=14)
plt.legend(loc="lower right")
#plt.savefig("Figure_1_ROC.png",dpi=300)
plt.show()
