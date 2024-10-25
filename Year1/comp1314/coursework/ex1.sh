#!/bin/bash

#Ensuring correct No. of command line arguments are given
if [[ $# != 1 ]]; then
	echo "Error: one command Line argument must be provided"
	exit 1
fi


if [[ "$1" != "faculty.xml" && "$1" != "students.xml" ]]; then
	echo "Error: command line arguemt must be either faculty.xml or students.xml"
	exit 1
fi

#Processing data and outputting to CSV
if [[ "$1" == "faculty.xml" ]]; then
	echo "Writing to faculty.csv..."
	grep -v xml "$1" | sed -E 's/<\/?[a-z]*>//g' | awk '{$1=$1; print}' | tr -d '\r' | sed '/./ N; s/\n/,/g' | sed '/./ N; s/\n/,/g' | awk 'NF {printf"%s\n",$0}' > faculty.csv
fi

if [[ "$1" == "students.xml" ]]; then
	echo "Writing to students.csv..."
	grep -v xml "$1" | tr -d '\r\n' | sed 's/,//g' | sed -E 's/<\/?[a-z]*[0-2]*_?[a-z]*>/\n/g' | awk '{$1=$1; print}' | sed -E 's/>/&\n/g' | sed -E 's/<[a-z]*[0-9]*>//g' | tr -s '\n' | sed 's/$/,/g' | sed -E 's/<.*[^3]\/>/NULL/g' | awk '{$1=$1; print}' | sed -E 's/<.*\/>,/NULL\n/g' | sed -E 's/<.*>,/\n/g' | awk 'NF {printf "%s", $0} !NF {print ""}' | sed '1s/^.\(.*\)/\1/' > students.csv
fi

echo "Done"
