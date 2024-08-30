import numpy as np
import matplotlib.pyplot as plt
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Plot free energy landscape plot.")

parser.add_argument('-md', '--md-path', type=str, required=True, help='Path to the MD simulation data.')
parser.add_argument('-n', '--prot-name', type=str, required=True, help='Name of the protein.')

# Parse arguments
args = parser.parse_args()

# Assign arguments to variables
MD_PATH = args.md_path
PROT_NAME = args.prot_name

# Load data
data = np.loadtxt(MD_PATH+'free-energy-landscape.dat')

from matplotlib.colors import LinearSegmentedColormap

# Define custom colormap
colors = ['#4260f5', '#ffffbf', '#fc8d59', '#ffffff']

cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)

# Extract columns
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]

# Calculate range
A_min_x = np.min(x)
A_max_x = np.max(x)
B_min_y = np.min(y)
B_max_y = np.max(y)

# Reshape data to 2D
num_rows = len(np.unique(y))
num_cols = len(np.unique(x))
x_2d = x.reshape(num_rows, num_cols)
y_2d = y.reshape(num_rows, num_cols)
z_2d = z.reshape(num_rows, num_cols)

# Create contour plot

levels = np.linspace(np.min(z), np.max(z), 100)  # Adjust number of levels as needed
plt.contourf(x_2d, y_2d, z_2d, levels=levels, cmap=cmap)

# Set labels and title
plt.xlabel('PC1', fontsize=14)
plt.ylabel('PC2', fontsize=14)

# Set ranges
plt.xlim(A_min_x, A_max_x)
plt.ylim(B_min_y, B_max_y)

# Add color bar
colorbar = plt.colorbar()
colorbar.set_label('Gibbs Free Energy (kJ/mol)', fontsize=14)  # Set fontsize as needed

plt.savefig(PROT_NAME+"_FEL.png",dpi=300)
    
# Show plot
#plt.show()

