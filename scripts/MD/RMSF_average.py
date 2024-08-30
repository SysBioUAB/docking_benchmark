import numpy as np
import biotite.structure as struc
import biotite.structure.io.pdb as pdb
from scipy.spatial.distance import cdist
import biotite.structure.io as strucio
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import sys
import os

# Read PDB file containing multiple models
file_path = sys.argv[1]

# Set up argument parser
parser = argparse.ArgumentParser(description="Compute C-alpha RMSF plot by residue index.")

parser.add_argument('-i', '--input', type=str, required=True, help='Path to the folder containing all the PDB files.')
parser.add_argument('-o', '--output', type=str, required=True, help='Path to save the output plot.')
parser.add_argument('-n', '--prot-name', type=str, required=True, help='Name of the protein.')


# Parse arguments
args = parser.parse_args()

# Assign arguments to variables
INPUT_PATH = args.input
OUTPUT_PATH = args.output
PROT_NAME = args.prot_name


def calculate_rmsd(matrix):
    """
    Calculate RMSD from pairwise distance matrix
    """
    return np.sqrt(np.mean(matrix ** 2, axis=1))

def average_structure(models, rmsd_matrix):
    """
    Identify the average structure based on the pairwise RMSD matrix
    """
    min_rmsd_sum = np.inf
    average_model = None
    for i, model in enumerate(models):
        rmsd_sum = np.sum(rmsd_matrix[i])
        if rmsd_sum < min_rmsd_sum:
            min_rmsd_sum = rmsd_sum
            average_model = model
    return average_model


def load_structures_from_folder(folder_path):
    structures = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdb'):
            file_path = os.path.join(folder_path, file_name)
            structure = strucio.load_structure(file_path)
            structure = structure[structure.atom_name == "CA"]
            structures.append(structure)
    return structures
    

stack = load_structures_from_folder(INPUT_PATH)


# Calculate pairwise RMSD matrix
num_models = len(stack)
rmsd_matrix = np.zeros((num_models, num_models))
for i in range(num_models):
    for j in range(num_models):
        rmsd_matrix[i, j] = struc.rmsd(stack[i], stack[j])


# Identify the average structure
avg_structure = average_structure(stack, rmsd_matrix)

# Align each model against the average conformation
for i in range(len(stack)):
    stack[i], _ = struc.superimpose(avg_structure, stack[i])

# Extract coordinates from average structure
avg_coords = avg_structure.coord
# Extract coordinates from all models in stack
stack_coords = [model.coord for model in stack]

# Calculate the RMSF relative to the average of all models
rmsf = struc.rmsf(avg_coords, stack_coords)

x = [i for i in range(len(rmsf))]

# Define custom colors
colors = [
    (0, 'blue'),
    (1/5, 'cyan'),
    (2/5, 'lime'),
    (3/5, 'yellow'),
    (4/5, 'orange'),
    (1, 'red')
]

# Create colormap
cmap = LinearSegmentedColormap.from_list('custom_colors', colors)

plt.figure(figsize=(10, 6))

# Plotting stuff
plt.scatter(x, rmsf,c=x+rmsf, cmap=cmap, alpha=0.8)
plt.ylim(0,25)

plt.xlabel('Residue index',fontsize=14)
plt.ylabel('RMSF (Å)',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.savefig(OUTPUT_PATH+'/'+PROT_NAME,dpi=300, format='svg')
#plt.show()
