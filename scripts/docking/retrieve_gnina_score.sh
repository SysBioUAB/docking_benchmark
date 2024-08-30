#!/bin/bash
# This script extract gnina scores from SDF files containing all the poses and outputs a CSV file to plot the ROC curves:

input_dir=$1
output_dir=$2

# Check if output directory exists, if not, create it
mkdir -p "$output_file"

for i in $input_dir; do num=0; if [[ $i =~ "random" ]]; then num=1; fi; cat $i | grep -EA1 "minimizedAffinity|\\$" | grep [0-9]  | tail -n +2 | paste - - | LC_ALL=C sort -nk2 | awk -v var=$num '!seen[$1]++ {print $2","var}' >> $output_dir/$(basename $i .sdf).csv;  done
