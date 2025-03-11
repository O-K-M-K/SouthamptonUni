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
	echo "faculty,building,room,capacity" > faculty.csv
	grep -v xml "$1" | sed -E 's/<\/?[a-z]*>//g' | awk '{$1=$1; print}' | tr -d '\r' | sed '/./ N; s/\n/,/g' | sed '/./ N; s/\n/,/g' | awk 'NF {printf"%s\n",$0}' >> faculty.csv
fi

if [[ "$1" == "students.xml" ]]; then
	echo "Writing to students.csv..."
	echo "student_name,student_id,student_email,programme,year,address,contact,module_id,module_name,module_leader,lecturer1,lecturer2,faculty,building,room,exam_mark,coursework1,coursework2,coursework3" > students.csv
	grep -v xml "$1" | sed 's|<[^>]*\/>|<1>NULL<\/1>|g' | awk '{$1=$1;print}'| sed -e 's|\(^[^< ]\)| \1|g' | tr -d '\r\n' | sed -e 's|\([^>]*,[^<]*\)|"\1"|g' | sed 's|<\/student>|\n|g' | sed 's|<[^\/]*>||g' | sed 's|<\/[^>]*>|,|g' | sed 's|,$||g' >> students.csv
	
fi

echo "Done"
