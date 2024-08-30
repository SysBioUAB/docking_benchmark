#!/bin/bash

# Script to filter docked ligands from zincpharmer_docking.sh or glide_pipeline.sh

while getopts :i:o:h option; do
	case $option in
		i) pdb_dir=$OPTARG;;
		o) out_dir=$OPTARG;;
		h) printf "Usage example: bash $0 -o ../outputs_summary/gramn/ -i ../ligands_proteins/PDB/gramn/\n\nRequired options:\n-o <PATH_OUTPUT>: Path to store all the results.\n-i <PATH_PDB>: Path pointing to folder containing all the protein complex PDB files or pointing to specific PDB file (the filename should be proteinA-proteinB.pdb\n-h: Prints this information."; exit 1;;	
	esac
done

shift "$(( OPTIND - 1 ))"

[ -z "$pdb_dir" ] || [ -z "$out_dir" ] && printf "Error: -i and -o arguments are mandatory! See $0 -h for more information.\n" && exit 1
[ ! -d $out_dir ] && echo "Error: output directory not found." && exit 1
[ ! -f $pdb_dir ] && [ ! -d $pdb_dir ] && echo "Error: input file or directory not found." && exit 1

for complex in $pdb_dir*; do

	FIRST=$(basename $complex .pdb | cut -d'-' -f1)
	SECOND=$(basename $complex .pdb | cut -d'-' -f2)
	prots=( $FIRST $SECOND )
	
	if [[ ! -f $out_dir$FIRST-$SECOND"_"$protein"_summary.csv" ]]; then 
	for protein in $prots; do
	
	# $6 is logPo/w and $NF is the last column corresponding to glide score.
	find ../outputs*/gramn/ -type f -name "$FIRST-$SECOND"_"$protein"* -exec cat {} \; | LC_ALL=C awk -F',' '{if ($6 < 2 && $NF < -6 && $(NF-1) < -0.24) print $0}' >> $out_dir$FIRST-$SECOND"_"$protein"_summary.csv"
	find $out_dir* -size 0 -delete
	
	done
	
	fi
	
done
