#!/bin/bash
# Download the gnina's pre-built binary from https://github.com/gnina/gnina

# Download our docking outputs from 

METHOD=$1

process_pdb_file() {
    local sdf_file="$1"
    local prot=$(echo $sdf_file | cut -d'/' -f4 | cut -d'_' -f3 | cut -c1-4 | tr '[:upper:]' '[:lower:]')
    local chain=$(echo $sdf_file | cut -d'/' -f4 | cut -d'_' -f3 | cut -c5)
    local method=$(echo $sdf_file | cut -d'/' -f3 | cut -d'_' -f3 )
    local receptor="docking_data/Protein_structures/Gnina_tankbind_diffdock/"$method/$prot$chain".pdb"
    local score=$(./gnina -r "$receptor" -l "$sdf_file" --minimize  | awk '/Affinity/ {print $2}')
    local output_file="outputs/roc/diffdock/"$(echo $sdf_file | cut -d'/' -f4)_$method.csv
    

    
    if (( $(echo "$score > 0" | bc -l) )); then
    score=0
fi
    
    if [[ $sdf_file =~ benchmark ]]; then
        echo "$score,1" >> "$output_file"
    else
        echo "$score,0" >> "$output_file"
    fi
}

process_pdb_file_MD() {
    local sdf_file="$1"
    local prot=$(echo $sdf_file | cut -d'/' -f5 | cut -d'_' -f3 | cut -c1-4 | tr '[:upper:]' '[:lower:]')
    local chain=$(echo $sdf_file | cut -d'/' -f5 | cut -d'_' -f3 | cut -c5)
    local method=$(echo $sdf_file | cut -d'/' -f3 | cut -d'_' -f3 )
    local method_num=$(echo $sdf_file | cut -d'/' -f4 | cut -d'_' -f3 )
    local receptor="docking_data/Protein_structures/Gnina_tankbind_diffdock/$method/"$prot"A-"$prot"B_"$method_num"_"$chain".pdb"
    local score=$(./gnina -r "$receptor" -l "$sdf_file" --minimize  | awk '/Affinity/ {print $2}')
    local output_file="outputs/roc/diffdock/"$(echo $sdf_file | cut -d'/' -f5)_$method_num.csv
  
    
    if (( $(echo "$score > 0" | bc -l) )); then
    score=0
fi
    
    
    if [[ $sdf_file =~ benchmark ]]; then
        echo "$score,1" >> "$output_file"
    else
        echo "$score,0" >> "$output_file"
    fi
}

if [[ "$METHOD" == "MD" || "$METHOD" == "AFlow" ]]; then

	for sdf_file in outputs/Outputs_diffdock/$METHOD/$METHOD*/*/rank1_*; do process_pdb_file_MD "$sdf_file"; done
else
	for sdf_file in outputs/Outputs_diffdock/$METHOD/*/rank1_*; do process_pdb_file "$sdf_file"; done
fi


