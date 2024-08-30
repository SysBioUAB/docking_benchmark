#!/bin/bash

# Define the method argument (can be PDB, AFnat, AFfull, MD, or AFlow)
method="$1"
out_path=$2
prot_path=$3
ligand_path=$4
# Validate method argument
if [[ "$method" != "PDB" && "$method" != "AFnat" && "$method" != "AFfull" && "$method" != "MD" && "$method" != "AFlow" ]]; then
  echo "Invalid method specified. Use PDB, AFnat, AFfull, MD, or AFlow."
  exit 1
fi

for complex in $prot_path
do
	complex_no_extension=$(basename "$complex" .pdb)
	prot=$(echo "$complex_no_extension" | cut -c1-4 | tr '[[:lower:]]' '[[:upper:]]')
	chain=$(echo "${complex_no_extension: -1}")
	num=$(echo "${complex_no_extension: -3: -2}")
	
	echo $complex $complex_no_extension $prot $chain $num
	
	mkdir -p $out_path/$method/
	exit
	
	if [[ "$method" == "MD" || "$method" == "AFlow" ]]; then
	mkdir -p $out_path/"$method"
	
	python multiligand_inference.py -o $out_path/$method/"$j"_"$method"$k/A \
		                      -r $prot_path/"$j"A-"$j"B_$method"$k"_A.pdb \
		                      -l $ligand_path/ligands_benchmark_"$complex".sdf

	python multiligand_inference.py -o $out_path/$method/"$j"_"$method"$k/A_random \
		                      -r $prot_path/"$j"A-"$j"B_$method"$k"_A.pdb \
		                      -l $ligand_path/ligands_random_"$complex".sdf

	python multiligand_inference.py -o $out_path/$method/"$j"_"$method"$k/B \
		                      -r $prot_path/"$j"A-"$j"B_$method"$k"_B.pdb \
		                      -l $ligand_path/ligands_benchmark_"$complex".sdf

	python multiligand_inference.py -o $out_path/"$method"/"$j"_"$method"$k/B_random \
		                      -r $prot_path/"$j"A-"$j"B_$method"$k"_B.pdb \
		                      -l $ligand_path/ligands_random_"$complex".sdf
	
	else
	mkdir -p $out_path/"$method"

	python multiligand_inference.py -o $out_path/"$method"/"$j"/A \
		                    -r $prot_path/"$j"A-"$j"B_"$method"_A.pdb \
		                    -l $ligand_path/ligands_benchmark_"$complex".sdf

	python multiligand_inference.py -o $out_path/"$method"/"$j"/A_random \
		                    -r $prot_path/"$j"A-"$j"B_"$method"_A.pdb \
		                    -l $ligand_path/ligands_random_"$complex".sdf

	python multiligand_inference.py -o $out_path/"$method"/"$j"/B \
		                    -r $prot_path/"$j"A-"$j"B_"$method"_B.pdb \
		                    -l $ligand_path/ligands_benchmark_"$complex".sdf

	python multiligand_inference.py -o $out_path/"$method"/"$j"/B_random \
		                    -r $prot_path/"$j"A-"$j"B_"$method"_B.pdb \
		                    -l $ligand_path/ligands_random_"$complex".sdf
	fi
done


