#!/bin/bash

if [ "$#" -ne 1 ]
then
	echo "The first argument have to be the name of the folder containing the alphafold's outputs. Example: bash $0 AF_OUTPUT_PATH"
	exit
fi

AF_FOLDER=$1

for FILE in $AF_FOLDER/*
do
        PPI=$(echo $(basename $FILE ))
	if [[ ! -f $FILE/ranking_debug.json ]]; then
		printf  "$PPI\n"
	else
		PTM=$(cat $FILE/ranking_debug.json | head -n 7 | tail -n +3 | cut -d':' -f2 | tr ',' ' ' | LC_ALL=C sort -nr | head -n 1)
		printf  "$PPI\t$PTM\n"

	fi
done
