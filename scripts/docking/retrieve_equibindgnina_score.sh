#!/bin/bash

# $1 should be the PDB code, which is the name of the the folder containing the outputs

for ligand in benchmark_MD/*/*/*/*.sdf
do
	chain=$(echo $ligand | cut -d'/' -f3- | cut -d'/' -f1)
	prot=$(echo $ligand | cut -d'/' -f2- | cut -d'/' -f1)
	
	if [[ $chain =~ "random" ]]; then
	
		cat $ligand | grep -A1 'minimizedAffinity' | head -n2 | tail -n1 | LC_ALL=C awk '{if ($1 > 0) print 0",0"; else print $0",0"}' >> roc_data_equibindgnina/"$prot"_"$chain"_equibindgnina_$(echo $prot | cut -d'_' -f2).csv

	else
	
		cat $ligand | grep -A1 'minimizedAffinity' | head -n2 | tail -n1 | LC_ALL=C awk '{if ($1 > 0) print 0",1"; else print $0",1"}' >> roc_data_equibindgnina/"$prot"_"$chain"_equibindgnina_$(echo $prot | cut -d'_' -f2).csv
	fi
done
