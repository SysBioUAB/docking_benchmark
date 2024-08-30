import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

SMALL_SIZE = 14
MEDIUM_SIZE = 16
BIGGER_SIZE = 20

plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

afnat = pd.read_csv("../../data/input_files/figure_datasets/Supplementary_1_AFnat.csv")
affull = pd.read_csv("../../data/input_files/figure_datasets/Supplementary_1_AFfull.csv")
md_pdb = pd.read_csv("../../data/input_files/figure_datasets/Supplementary_1_MDPDB.csv")
md_af = pd.read_csv("../../data/input_files/figure_datasets/Supplementary_1_MDAF.csv")

fig = plt.figure(constrained_layout=True)
axs = fig.subplot_mosaic(
	"""
	AB
	CD
	"""
)

proteins = [x.upper() for x in afnat["PDB"].tolist()]
proteins_affull = [x.upper() for x in affull["PDB"].tolist()]

axs["A"].scatter(range(len(proteins)), afnat["ipTM+pTM"].tolist(), color='coral', label='ipTM+pTM')
axs["A"].scatter(range(len(proteins)), afnat["TM-score"].tolist(), color='orchid', label='TM-score')
axs["A"].scatter(range(len(proteins)), afnat["DockQ"].tolist(), color='wheat', label='DockQ')

axs["B"].scatter(range(len(proteins_affull)), affull['ipTM+pTM'].tolist(), color='coral', label='ipTM+pTM')
axs["B"].scatter(range(len(proteins_affull)), affull['pDockQ2'].tolist(), color='navy', label='pDockQ2')

axs["C"].scatter(range(len(proteins)), md_pdb['DockQ'], color='wheat', label='DockQ')
axs["C"].scatter(range(len(proteins)), md_pdb['TM-score'].tolist(), color='orchid', label='TM-score')

axs["D"].scatter(range(len(proteins)), md_af['DockQ'], color='wheat', label='DockQ')
axs["D"].scatter(range(len(proteins)), md_af['TM-score'].tolist(), color='orchid', label='TM-score')

axs["A"].set_xticks(range(len(proteins)), proteins, rotation=45)
axs["B"].set_xticks(range(len(proteins_affull)), proteins_affull, rotation=45)
axs["C"].set_xticks(range(len(proteins)), proteins, rotation=45)
axs["D"].set_xticks(range(len(proteins)), proteins, rotation=45)

axs["A"].set_yticks([0,0.2,0.4,0.6,0.8,1])
axs["B"].set_yticks([0,0.2,0.4,0.6,0.8,1])
axs["C"].set_yticks([0,0.2,0.4,0.6,0.8,1])
axs["D"].set_yticks([0,0.2,0.4,0.6,0.8,1])

axs["A"].set_title("AFnat")
axs["B"].set_title("AFfull")
axs["C"].set_title("MD_PDB")
axs["D"].set_title("MD_AF")


fig.supxlabel("PDB ID")
fig.supylabel("Scores")

#fig.savefig("supplementary_3.png",dpi=300)

plt.show()
