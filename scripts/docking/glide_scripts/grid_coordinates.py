import numpy as np
import sys

coord = sys.argv[1]

a = np.genfromtxt(coord, usecols=[6, 7, 8])

mean = a.mean(axis=0)

print("GRID_CENTER   " + str("{:.1f}".format(mean[0])) + ", " + str("{:.1f}".format(mean[1])) + ", " + str("{:.1f}".format(mean[2])))
