import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import sys 

# Script to compute auROC values and plot ROC curves given the docking results in CSV format. 

input_file=sys.argv[1]

# Read the CSV file
data_random = pd.read_csv(input_file, header=None).dropna()
data = pd.read_csv(input_file[:input_file.rfind('_')]+".csv", header=None).dropna()


data_concat = pd.concat([data,data_random])
# Plot ROC curve for each group
plt.figure(figsize=(8, 6))

fpr, tpr, _ = roc_curve(data_concat.iloc[:, 1], data_concat.iloc[:, 0])
roc_auc = auc(fpr, tpr)
print(input_file, roc_auc)

plt.plot(fpr, tpr, label=f'{labels[i]} (AUC = {roc_auc:.2f})')

plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random Guess')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Reversed Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
#plt.show()

