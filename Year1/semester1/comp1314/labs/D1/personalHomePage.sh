#!/bin/bash

if [[ $# -gt 2 || $# -lt 1 ]]; then
        echo "Error: one or 2 command Line argument(s) must be provided"
        exit 1
fi

cleanFile=$(sed 's/,//g' $1)
fileLines=$(echo "$cleanFile" | wc -l)
declare -a results
year=$2
shortYear=${year: -2}
count=0

while read -r p; do
        curl --silent --output /dev/null --fail  http://personal.soton.ac.uk/~"$p"/index.html
        status=$?
	((count++))
        if [[ $status == 0 ]]; then
		charCount=$(curl -s  http://personal.soton.ac.uk/~"$p"/index.html | wc -c)
		#$(echo $p,$(curl -s  http://personal.soton.ac.uk/~"$p"/index.html | wc -c))
                #echo $p,$(curl -s  http://personal.soton.ac.uk/~"$p"/index.html | wc -c) >> username_char_count.csv
		if [[ $# == 2 ]]; then
			#echo $shortYear $p
			if [[ $shortYear == ${p: -2} ]]; then
				#echo "Debug"
				results+=("$p $charCount")
			fi
			#echo "Matched substring: '${BASH_REMATCH[0]}'"
		else
			results+=("$p $charCount")
		fi
        fi

	#if [[ $((count % 1)) -eq 0 ]]; then
	echo -ne "$count/$fileLines lines processed...\r"
	#fi
done < <(echo "$cleanFile")
echo -ne "\r\033[K"
echo  "Done"
sortedResults=$(printf "%s\n" "${results[@]}" | sort -k2 -n -r)

echo "$sortedResults"
