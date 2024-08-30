import numpy as np
import matplotlib.pyplot as plt
import argparse

# First, obtain the RMSD values of each protein chain using gmx rms and name them rmsd_A and rmsd_B for chains A and B. This code will plot the RMSD values of each chain along the trajectory.

# Set up argument parser
parser = argparse.ArgumentParser(description="Plot RMSD values of each protein chain along the trajectory.")

parser.add_argument('-md', '--md-path', type=str, required=True, help='Path to the MD simulation data.')
parser.add_argument('-n', '--prot-name', type=str, required=True, help='Name of the protein.')
parser.add_argument('-r', '--rmsd-lim', type=float, required=True, help='Upper limit for the RMSD plot (y-axis).')

# Parse arguments
args = parser.parse_args()

# Assign arguments to variables
MD_PATH = args.md_path
PROT_NAME = args.prot_name
RMSD_LIM = args.rmsd_lim

def plot_rmsd(dataframes, colors):
    plt.figure(figsize=(10, 6))

    for df, color in zip(dataframes, colors):
        plt.plot(df[:, 0], df[:, 1], color=color)

    plt.xlabel('Simulation time (ns)', fontsize=14)
    plt.ylabel('RMSD (nm)', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylim(0, RMSD_LIM)
    plt.savefig("./" + PROT_NAME + "_RMSD.png", dpi=300)
    # plt.show()

# Load RMSD data for each chain
A_chain = np.loadtxt(MD_PATH + '/rmsd_A.xvg', comments=['#', '@'])
B_chain = np.loadtxt(MD_PATH + '/rmsd_B.xvg', comments=['#', '@'])

# Define colors for each dataframe
colors = ['wheat', 'paleturquoise']

# Plot the dataframes
plot_rmsd([A_chain, B_chain], colors)

