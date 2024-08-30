#!/bin/bash

method=$1
output_folder=$2


for ligand in benchmark_$method*/*/*/*.pdbqt
do
	chain=$(echo $ligand | cut -d'/' -f3- | cut -d'/' -f1)
	prot=$(echo $ligand | cut -d'/' -f2- | cut -d'/' -f1)
	if [[ $method == "MD" ]]; then
		prot=$(echo $ligand | cut -d'/' -f2- | cut -d'/' -f1 | cut -d'_' -f1)
		MD=$(echo $ligand | cut -d'/' -f2- | cut -d'/' -f1 | cut -d'_' -f2)
	fi
	

	
	if [[ $chain =~ "random" ]]; then
		
		cat $ligand | grep 'REMARK VINA RESULT' | head -n1 |  LC_ALL=C awk '{if ($4 >= 0) print "0,0"; else print $4",0"}' >> "$output_folder"/"$prot""$chain"_random_"$method".csv.tmp

	else
	
		cat $ligand | grep 'REMARK VINA RESULT' | head -n1  | awk '{if ($4 >= 0) print 0",1"; else print $4",1"}' >> "$output_folder"/"$prot""$chain"_benchmark_"$method".csv.tmp
	fi
done


for output in "$output_folder"/*.tmp
do
	cat $output | uniq > "$output_folder"/$(basename $output .tmp)
	sed -i '1i score,actual' "$output_folder"/$(basename $output .tmp)
	rm $output
done


