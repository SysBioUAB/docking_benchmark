PDB=(2W2M 3TDZ 4FTG 5C3F)
for i in ${PDB[@]}; do
j=$(echo "$i" | tr '[:upper:]' '[:lower:]')

	bash glide_pipeline.sh -l ../ligands/ligands_random_"$i".sdf -o ../outputs_benchmark_PDB/ -i ../proteins/benchmark/"$j"A-"$j"B.pdb  -I 1 -b random -t PDB
	
	bash glide_pipeline.sh -l ../ligands/ligands_benchmark_"$i".sdf -o ../outputs_benchmark_PDB/ -i ../proteins/benchmark/"$j"A-"$j"B.pdb  -I 1 -b benchmark -t PDB
	
done

