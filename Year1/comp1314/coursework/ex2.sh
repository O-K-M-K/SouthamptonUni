#!/bin/bash

if [[ "$#" -gt 2 || "$#" -lt 1 ]]; then
        echo "Error: Either one or two command line arguments must be provided"
        exit 1
fi



if [[ "$1" != "students.csv" ]]; then
        echo "Error: First command line argument must be students.csv"
        exit 1
fi

if [[ "$#" == 2 && "$2" != *.txt ]]; then
	echo "Error: The second argument must be a text file"
	exit 1
fi

file_name="${2:-students.txt}" #if second cmd line argument does not exist use students.txt instead

echo "Writing to $file_name..."

cut -d, -f1 $1 | sort | uniq > $file_name

echo "Done"
