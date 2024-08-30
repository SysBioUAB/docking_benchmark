#!/bin/bash

for i in $(cat $1_interface_residues.txt | tr ',' '\n')
do
	awk -v var=$i '{if ( $6 == var ) {print $0}}' $1.pdb >> coord_$2.txt
done

python3 grid_coordinates.py coord_$2.txt

rm coord_$2.txt