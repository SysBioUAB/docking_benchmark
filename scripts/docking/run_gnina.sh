#!/bin/bash

# Download the gnina's pre-built binary from https://github.com/gnina/gnina


# Parse command-line arguments
while getopts ":p:m:o:c:l:g:" opt; do
  case ${opt} in
    p ) PROT_PATH=$OPTARG
      ;;
    m ) METHOD=$OPTARG
      ;;
    o ) OUT_PATH=$OPTARG
      ;;
    c ) COORD_FILE=$OPTARG
      ;;
    l ) LIGAND_PATH=$OPTARG
      ;;
    g ) GNINA_PATH=$OPTARG
      ;;
    \? ) echo "Usage: bash $0 [-p] protein_path [-m] method [-o] output_path [-c] coord_file [-l] ligands_path [-g] gnina_path"
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
	complex_no_extension=$(basename "$complex" .pdb)
	prot=$(echo "$complex_no_extension" | cut -c1-4 | tr '[[:lower:]]' '[[:upper:]]')
	chain=$(echo "${complex_no_extension: -1}")
	num=$(echo "${complex_no_extension: -3: -2}")
	
	mkdir -p $OUT_PATH/$METHOD/
	mkdir -p $OUT_PATH/$METHOD/
	
	# Extract coordinates and size based on the method
	if [[ "$METHOD" == "MD" || "$METHOD" == "AFlow" ]]; then

	  x=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num".pdb | cut -d' ' -f2)
	  y=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num".pdb | cut -d' ' -f3)
	  z=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num".pdb | cut -d' ' -f4)
	  size_x=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num".pdb | cut -d' ' -f5)
	  size_y=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num".pdb | cut -d' ' -f6)
	  size_z=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | grep $METHOD"$num".pdb | cut -d' ' -f7)
          METHOD_num="$METHOD"_$num
          
	else

	  x=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f2)
	  y=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f3)
	  z=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f4)
	  size_x=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f5)
	  size_y=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f6)
	  size_z=$(grep "$METHOD" "$COORD_FILE" | grep -i "$prot" | cut -d' ' -f7)
	  
	  METHOD_num="$METHOD"
	fi

       
	[[ ! -f $OUT_PATH/"$prot"_$METHOD"$num"_$chain.sdf ]] && ./$GNINA_PATH -r "$complex" -l $LIGAND_PATH/ligands_benchmark_$prot.sdf -o "$OUT_PATH"/$METHOD/"$prot"_"$METHOD_num"_$chain.sdf  --cpu 16 --center_x $x --center_y $y --center_z $z --size_x $size_x --size_y $size_y --size_z $size_z 
	
	[[ ! -f $OUT_PATH/"$prot"_$METHOD"$num"_"$chain"_random.sdf ]] && ./$GNINA_PATH -r "$complex" -l $LIGAND_PATH/ligands_random_$prot.sdf -o "$OUT_PATH"/$METHOD/"$prot"_"$METHOD_num"_"$chain"_random.sdf  --cpu 16 --center_x $x --center_y $y --center_z $z --size_x $size_x --size_y $size_y --size_z $size_z

done

