#!/bin/bash

# Script to retrieve confidence scores from diffdock outputs.

METHOD=$1

mkdir -p "outputs/roc/diffdock_confidence_score/"

if [[ "$METHOD" == "MD" || "$METHOD" == "AFlow" ]]; then

	for sdf_file in outputs/Outputs_diffdock/$METHOD/$METHOD*/*/rank1_*; do 
	name=$(echo $sdf_file | cut -d'/' -f5);
	score=$(basename $sdf_file .sdf | cut -d'_' -f2 | grep -Eo '[-]?[0-9]+([.][0-9]+)?')
	method_num=$(echo $sdf_file | cut -d'/' -f4 | cut -d'_' -f3 )
	
	output_file="outputs/roc/diffdock_confidence_score/""$name"_$method_num.csv
	if [[ $name == *"benchmark"* ]]; then 
	echo $score",1" >> $output_file
	else echo $score",0" >> $output_file
	fi 
	done
else
	for i in outputs/Outputs_diffdock/$METHOD/*/rank1_*; do 
	name=$(echo $i | cut -d'/' -f4);
	score=$(basename $i .sdf | cut -d'_' -f2 | grep -Eo '[-]?[0-9]+([.][0-9]+)?')

	output_file="outputs/roc/diffdock_confidence_score/""$name"_$METHOD.csv
	
	if [[ $name == *"benchmark"* ]]; then 
	echo $score",1" >> $output_file
	else echo $score",0" >> $output_file
	fi 
	done
fi



