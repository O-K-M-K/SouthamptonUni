#!/bin/bash

if [[ "$#" -ne 2 ]]; then
        echo "Error: Two command line arguments must be provided"
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

file_name="$2"

echo "Writing to $file_name..."

cut -d, -f1,2 $1 | tail -n +2 | sort -t, -k1,1 | uniq -f1 | cut -d, -f1 > $file_name

echo "Done"
