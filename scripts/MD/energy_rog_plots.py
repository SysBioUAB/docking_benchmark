import numpy as np
import matplotlib.pyplot as plt
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Plot energy and radius of gyration (RoG) from MD simulation data.")

parser.add_argument('-md', '--md-path', type=str, required=True, help='Path to the MD simulation data.')
parser.add_argument('-n', '--prot-name', type=str, required=True, help='Name of the protein.')
parser.add_argument('-emin', '--energy-min', type=float, required=True, help='Minimum value for the energy plot (y-axis).')
parser.add_argument('-emax', '--energy-max', type=float, required=True, help='Maximum value for the energy plot (y-axis).')
parser.add_argument('-t', '--traj-time', type=float, required=True, help='Total trajectory time for the x-axis in nanoseconds.')
parser.add_argument('-rmin', '--rog-min', type=float, required=True, help='Minimum value for the RoG plot (y-axis).')
parser.add_argument('-rmax', '--rog-max', type=float, required=True, help='Maximum value for the RoG plot (y-axis).')

# Parse arguments
args = parser.parse_args()

# Assign arguments to variables
MD_PATH = args.md_path
PROT_NAME = args.prot_name
ENERGY_MIN = args.energy_min
ENERGY_MAX = args.energy_max
TRAJ_TIME = args.traj_time
ROG_MIN = args.rog_min
ROG_MAX = args.rog_max

# Load potential energy data from energy.xvg
gyrate = np.loadtxt(MD_PATH + '/gyrate.xvg', comments=['#', '@'])
energy = np.loadtxt(MD_PATH + '/potential_energy.xvg', comments=['#', '@'])

# Extract time and potential energy
time = energy[:, 0] / 1000
potential_energy = energy[:, 1]
rog = gyrate[:, 1]

# Apply moving average
window_size = 500  # Adjust the window size as needed
smoothed_energy = np.convolve(potential_energy, np.ones(window_size) / window_size, mode='valid')
smoothed_gyrate = np.convolve(rog, np.ones(window_size) / window_size, mode='valid')

fig, ax1 = plt.subplots()

color = 'tab:green'
ax1.set_xlabel('Time (ns)', fontsize=14)
ax1.set_ylabel('Potential Energy (kJ/mol)', fontsize=14)
line1, = ax1.plot(time[(window_size // 2):-(window_size // 2)], smoothed_energy[:len(smoothed_energy) - 1], color=color, label='Potential Energy')  # Add label
ax1.tick_params(axis='y')

ax1.set_ylim(ENERGY_MIN, ENERGY_MAX)
ax1.set_xlim(0, TRAJ_TIME)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('RoG (nm)', fontsize=14)  # we already handled the x-label with ax1
line2, = ax2.plot(time[(window_size // 2):-(window_size // 2)], smoothed_gyrate[:len(smoothed_gyrate) - 1], color=color, label='RoG')  # Add label
ax2.tick_params(axis='y')
ax2.set_ylim(ROG_MIN, ROG_MAX)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Adding legend
lines = [line1, line2]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='best', fontsize=10, frameon=False)

fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.savefig("energy_rog_" + PROT_NAME + ".png", dpi=300)

