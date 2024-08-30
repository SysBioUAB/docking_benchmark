#!/bin/bash



# This script takes as an input a protein complex PDB file and ligands in SDF file. A protein-ligand docking centered in the interface region using Schrodinger maestro is carried out. A list of the ligands is outputted including the docking score and physicochemical information.   

# Paths pointing to Schrodinger binaries
export SCHRODINGER=~/Schrodinger2021-2/

grid_templ='glide-grid_template.in'
dock_templ='glide-dock.HTVS_SP.template.in'
ifd_templ='ifd_template.in'
n_cores=$(lscpu | grep "Núcleo(s)" | cut -d' ' -f17)
color="$(tput setab 6)#$(tput sgr 0)"

# Usage function
usage() {
    printf "Usage example: bash $0 -o ../outputs_enamine/gramn/ -l ./ligands_proteins/Ligands/ligands_enamine.sdf -i ../ligands_proteins/PDB/gramn/ -p SP\n\n Options:\n-l <PATH_LIGANDS_SDF>: Path to folder containing ligand .sdf files.\n-o <PATH_OUTPUT>: Path to store all the results.\n-i <PATH_PDB>: Path pointing to folder containing all the protein complex PDB files or pointing to specific PDB file (the filename should be proteinA-proteinB.pdb and only chains A and B are choosen\!)\n-p <HTVS|SP>: Schrodinger docking precision: High throughput virtual screening (HTVS) or Standard Precision (SP)\n-h <HELP>: Prints this information.\n"
    exit 1
}

while getopts :l:i:o:I:t:b:h option; do
	case $option in
		l) lig_file=$OPTARG;;
		i) pdb_dir=$OPTARG;;
		o) out_dir=$OPTARG;;
		I) ifd=$OPTARG;;
		b) benchmark_random=$OPTARG;;
		t) structure_type=$OPTARG;;
		\?) echo "Invalid option: -$OPTARG"; usage;;
        	:) echo "Option -$OPTARG requires an argument." ; usage;;
		h) usage;;	
	esac
done


[ -z "$lig_file" ] || [ -z "$pdb_dir" ] || [ -z "$out_dir" ] || [ -z "$structure_type" ] || [ -z "$benchmark_random" ] && usage 

	
[ -z $grid_templ ] && { echo "Error: Missing $grid_templ"; exit 1; }
[ -z $ifd_templ ] && { echo "Error: Missing $ifd_templ"; exit 1; }
[ -z $dock_templ ] && { echo "Error: Missing $dock_templ"; exit 1; }
[ ! -d $SCHRODINGER ] && { echo "Error: Schrodinger not installed in "$SCHRODINGER; exit 1; }
#lig_name=$(basename $lig_file .sdf) 
#lig_dir=$(dirname $lig_file) ONLY USED IN QIKPROP!!


cat << "EndOfMessage"


 .oooooo..o                      oooooooooo.   o8o              .oooooo.             
d8P\'    `Y8                      `888'   `Y8b  `"'             d8P'  `Y8b            
Y88bo.      oooo    ooo  .oooo.o  888     888 oooo   .ooooo.  888           oooo d8b 
 `"Y8888o.   `88.  .8'  d88(  "8  888oooo888' `888  d88' `88b 888           `888""8P 
     `"Y88b   `88..8'   `"Y88b.   888    `88b  888  888   888 888     ooooo  888     
oo     .d8P    `888'    o.  )88b  888    .88P  888  888   888 `88.    .88'   888     
8""88888P'      .8'     8""888P' o888bood8P'  o888o `Y8bod8P'  `Y8bood8P'   d888b    
            .o..P'                                                                   
            `Y8P'                                                                    
                                                                                     

EndOfMessage

# QIKPROP DISABLED! 
                   
# Compute ligand's physicochemical properties using qikprop 

#if [ ! -f $lig_dir"/qikprop_""ligands"".csv" ] && [ -f $lig_file ]; then

#echo "${color/'#'/Running Qikprop on "ligands"}"                            
  
#${SCHRODINGER}/qikprop -fast -WAIT -LOCAL -nosa -nosim -input $lig_file
  
#cat "ligands"".CSV" | csvcut -c molecule,mol_MW,SASA,donorHB,accptHB,QPlogPo/w,RuleOfFive,RuleOfThree | tr ',' '\t' > $lig_dir"/qikprop_""ligands"".csv"
#rm "ligands"* 

#fi

for complex in $pdb_dir*; do

	complex_filename=$(basename $complex)
	prot="${complex_filename:0:4}"
	FIRST=$(basename $complex .pdb | cut -d'-' -f1)
	SECOND=$(basename $complex .pdb | cut -d'-' -f2)
	
	prots=( $FIRST $SECOND )

	out_dir_complex="$out_dir"$benchmark_random"_"$prot

        
	[[ ! -d $out_dir_complex ]] && mkdir $out_dir_complex
	[[ ! -d $out_dir_complex"/"$FIRST ]] && mkdir $out_dir_complex"/"$FIRST
	[[ ! -d $out_dir_complex"/"$SECOND ]] && mkdir $out_dir_complex"/"$SECOND
	[[ ! -d $out_dir_complex"/out_interfaces/" ]] && mkdir $out_dir_complex"/out_interfaces/"
	
 	# Compute interface residues. Separate chains into individual PDB files. 
	if [[ ! -f $out_dir_complex"/out_interfaces/"$FIRST".pdb" ]]; then 
		
	echo "${color/'#'/Computing protein interfaces $FIRST-$SECOND}"
			
	python3 GetInterfaces.py --f1 $complex --f2 $complex --c1 A --c2 B  --o $out_dir_complex"/out_interfaces/"
	
	for step in {1..2}; do
		
		protein="${prots[$((step-1))]}"
		rename "s/molecule_$step/$protein/g" $out_dir_complex"/out_interfaces/"*
		cp $out_dir_complex"/out_interfaces/"$protein".pdb" $out_dir_complex/$protein/	
		grep 'C' $out_dir_complex"/out_interfaces/$protein.txt" | cut -d' ' -f2 | tr '\n' ',' > $out_dir_complex"/out_interfaces/"$protein"_interface_residues.txt"
	 	
 	done	
	fi

	for protein in "${prots[@]}"; do
	
		output=$out_dir_complex/$protein
		
		# Prepare protein
		if [ ! -f $output/$protein.maegz ]; then

	        echo "${color/'#'/Preparing protein $protein}"

	      	${SCHRODINGER}/utilities/prepwizard -WAIT -SAVE -NOJOBID \
		    	-disulfides -rehtreat -captermini -fillsidechains \
		    	-propka_pH '7.0' -fix -f '3' \
		    	-epik_pH '7.0' \
		 	$output/$protein.pdb $output/$protein.maegz
		fi
		
	 	
	    # GRID GENERATION

		if [ ! -f $output/$protein".grid.zip" ]; then

		echo "${color/'#'/Generating grid $protein}"

		GRID_COORDINATES=$(bash grid_coordinates.sh $out_dir_complex"/out_interfaces/"$protein $protein)

		sed "s/GNAME/$protein/g" $grid_templ | sed "s@GPROTNAME@$output/$protein.maegz@g"  > $output"/glide-grid.in"
		echo $GRID_COORDINATES >> $output"/glide-grid.in"
		${SCHRODINGER}/glide -WAIT -SAVE -NOJOBID -NOLOCAL -OVERWRITE $output"/glide-grid.in"
		mv $protein* $output
		fi
		
	    # DOCKING


		if [ ! -f $output/"ligands_lib.sdfgz" ]; then
		
		echo "${color/'#'/Protein docking SP $protein}"
		sed "s@HOMEDIR@$output/$protein.grid.zip@g" $dock_templ | sed "s/GDOCKPRECIS/SP/g" | sed "s@XDIRECTORY@$lig_file@g"> $output/"ligands".in

		${SCHRODINGER}/glide -WAIT -SAVE -LOCAL -HOST localhost:$n_cores -SUBLOCAL -OVERWRITE -noforce -NJOBS $n_cores $output/"ligands".in
		mv $protein* $output
		mv "ligands"*  $output
	
	    	fi
	        
	   	
		if [ ! -f $output"_"$benchmark_random"_"$structure_type".csv" ]; then
		
		echo "${color/'#'/Preparing output $protein}"

		# Exporting CSV table
		
		${SCHRODINGER}/utilities/proplister -a -c $output/"ligands_lib.sdfgz" > $output/$protein".ligands.csv"

	    	# Merging qikprop and docking score dataframes. WAIT UNTIL QIKPROP CODE ABOVE IS FIXED! ALSO FIX MERGE_RESULTS.PY
	      
	   	cat $output/$protein".ligands.csv" | csvcut -c entry,r_i_glide_gscore > $output"_"$benchmark_random"_"$structure_type".csv"
	    
	   	#python3 merge_results.py $output"_docking_score.csv" $lig_dir"/qikprop_""ligands.csv" $protein random PDB
	   	
	        fi
	        
	   	# Remove intermediate files
		
		[[ -f $output"_docking_score.csv" ]] && rm $output"_docking_score.csv"
	   	find . -name "*$USER*" -delete
	    	
	    	echo "${color/'#'/Finished docking $protein}"
		
		if [[ ! -f $output/ifd_$protein"-out.maegz" ]] && [[ $ifd -eq 1 ]]; then
		
		echo "${color/'#'/Induced Fit Docking $protein}"

		obabel -isdf $output/"ligands_lib.sdfgz" -osdf -l 1 > $output/$protein."ligands_best.sdf"
		
		${SCHRODINGER}/utilities/structcat -imae $output/$protein.maegz -isd $output/"ligands_lib.sdfgz" -omae $output/$protein"_pv".mae
		
		${SCHRODINGER}/utilities/structcat -isd $output/"ligands_lib.sdfgz" -omae $output/$protein."ligands.mae"
		
		sed "s@LIGAND_NAME@$output/$protein."ligands.mae"@g" $ifd_templ | sed "s@RECEPTOR_NAME@$output/$protein"_pv.mae"@g"  > $output"/ifd_$protein.inp"
		
		${SCHRODINGER}/ifd -WAIT -SUBHOST localhost -NGLIDECPU $n_cores -NPRIMECPU $n_cores $output"/ifd_$protein.inp" 
		
		mv ./ifd_$protein"_workdir"/* $output/
		mv ./ifd_$protein"-out.maegz" $output/
		rmdir ./ifd_$protein"_workdir"
		
		
		fi
		${SCHRODINGER}/utilities/proplister -a -c $output/ifd_$protein"-out.maegz"  > $output"_"$benchmark_random"_"$structure_type"_IDF.csv"
  	done
done
