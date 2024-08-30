#!/bin/bash

# Parse command-line arguments
while getopts ":p:m:o:c:v:l:" opt; do
  case ${opt} in
    p ) PROT_PATH=$OPTARG
      ;;
    m ) METHOD=$OPTARG
      ;;
    o ) OUT_PATH=$OPTARG
      ;;
    c ) COORD_FILE=$OPTARG
      ;;
    v ) VINA_PATH=$OPTARG
      ;;
    l ) LIGAND_PATH=$OPTARG
      ;;
    \? ) echo "Usage: bash $0 [-p] protein_path [-m] method [-o] output_path [-c] coord_file [-v] vina_path [-l] ligands_path"
         exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# Ensure that only the allowed methods are used
if [[ "$METHOD" != "PDB" && "$METHOD" != "AF" && "$METHOD" != "MD" && "$METHOD" != "AFlow" ]]; then
  echo "Error: Invalid method. Choose one of the following: PDB, AF, MD, AFlow."
  exit 1
fi

for complex in $PROT_PATH
do
	complex_no_extension=$(basename "$complex" .pdbqt)
	prot=$(echo "$complex_no_extension" | cut -c1-4 | tr '[[:lower:]]' '[[:upper:]]')
	chain=$(echo "${complex_no_extension: -1}")
	num=$(echo "${complex_no_extension: -3: -2}")

	

        
	# Extract coordinates and size based on the method
	if [[ "$METHOD" == "MD" || "$METHOD" == "AFlow" ]]; then
	
	  mkdir -p $OUT_PATH/$METHOD/$prot"_"$METHOD"$num"/$chain
	  mkdir -p $OUT_PATH/$METHOD/$prot"_"$METHOD"$num"/$chain"_random"
	  
	  x=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num" | cut -d' ' -f2)
	  y=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num" | cut -d' ' -f3)
	  z=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num" | cut -d' ' -f4)
	  size_x=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num" | cut -d' ' -f5)
	  size_y=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num" | cut -d' ' -f6)
	  size_z=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num" | cut -d' ' -f7)
	  
	  prot_method=$prot"_"$METHOD"$num"
	else
	
	  mkdir -p $OUT_PATH/$METHOD/$prot/$chain
	  mkdir -p $OUT_PATH/$METHOD/$prot/$chain"_random"
	  
	  x=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f2)
	  y=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f3)
	  z=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f4)
	  size_x=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f5)
	  size_y=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f6)
	  size_z=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f7)
	fi
	
	
	./$VINA_PATH --receptor $complex --batch $LIGAND_PATH/ligands_benchmark_$prot/* --exhaustiveness 8 --dir $OUT_PATH/$METHOD/$prot_method/$chain --center_x $x --center_y $y --center_z $z --size_x $size_x --size_y $size_y --size_z $size_z
	
	./$VINA_PATH --receptor $complex --batch $LIGAND_PATH/ligands_random_$prot/* --exhaustiveness 8 --dir $OUT_PATH/$METHOD/$prot_method/$chain"_random" --center_x $x --center_y $y --center_z $z --size_x $size_x --size_y $size_y --size_z $size_z

done

