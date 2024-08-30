#!/bin/bash

if [ "$#" -ne 1 ]
then
	echo "The first argument must be the path to the protein structure in PDB format. Put the PDB file inside the data/output_files/MD/forcefields_and_parameters folder as it contains the parameter and forcefield files. Example: bash $0 PDB_FILE"
	exit
fi

# Run a MD simulation of a protein in water. Forcefield and parameter files are in forcefields_and_parameters folder.
structure=$1

source /usr/local/gromacs/bin/GMXRC
grep -v HOH "$structure".pdb > "$structure"_clean.pdb


echo -e '1\n' | gmx pdb2gmx -f "$structure"_clean.pdb -o "$structure"_processed.gro -water spce -ignh 
gmx editconf -f "$structure"_processed.gro -o "$structure"_newbox.gro -c -d 1.0 
gmx solvate -cp "$structure"_newbox.gro -cs spc216.gro -o "$structure"_solv.gro -p topol.top
echo -e '13\n' | gmx grompp -f ions.mdp -c "$structure"_solv.gro -p topol.top -o ions.tpr
echo -e '13\n' | gmx genion -s ions.tpr -o "$structure"_solv_ions.gro -p topol.top -pname NA -nname CL -neutral
gmx grompp -f em.mdp -c "$structure"_solv_ions.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -v -deffnm nvt
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -v -deffnm npt
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_2.tpr
gmx mdrun -v -deffnm md_0_2 -nb gpu
echo -e '1\n1\n' | gmx trjconv -s md_0_2.tpr -f md_0_2.xtc -o md_0_2_noPBC.xtc -pbc nojump -center
echo -e '1\n1\n' | gmx rms -s md_0_2.tpr -f md_0_2_noPBC.xtc -o rmsd.xvg -tu ns
echo -e '1\n1\n' | gmx rms -s em.tpr -f md_0_2_noPBC.xtc -o rmsd_xtal.xvg -tu ns



