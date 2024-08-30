#!/bin/bash

PROT_PATH=$1

cd $PROT_PATH

# Obtaining protein's potential energy. Extract only protein information from the simulation (no solvent)
echo -e '1\n' | gmx trjconv -f md_0_2.xtc -s md_0_2.tpr -o protein_only.xtc
echo -e '1\n' | gmx convert-tpr -s md_0_2.tpr -o protein_only.tpr 
gmx mdrun -s protein_only.tpr  -rerun protein_only.xtc -deffnm protein_only
echo -e '11\n\n' | gmx energy -f potential_energy.edr  -s protein_only.tpr  -o potential_energy.xvg

# Computing RoG of the protein backbone
echo -e '4\n' | gmx gyrate -s md_0_2.tpr -f md_0_2.xtc   -o gyrate.xvg 

# Free energy landscape
echo -e '4\n4\n' | gmx covar -s md_0_2.gro -f md_0_2.xtc -o eigenvalues.xvg -v eigenvectors.trr -xpma covapic.xpm
echo -e '4\n4\n' | gmx anaeig -f md_0_2.xtc -s md_0_2.gro -v eigenvectors.trr -last 1 -proj pc1.xvg
echo -e '4\n4\n' | gmx anaeig -f md_0_2.xtc -s md_0_2.gro -v eigenvectors.trr -first 2 -last 2 -proj pc2.xvg
paste pc1.xvg pc2.xvg  | awk '{print $1, $2, $4}' > PC1PC2.xvg
echo -e '4\n4\n' | gmx sham -f PC1PC2.xvg -ls FES.xpm


