#!/bin/bash

echo "Algorithm   Array size,Time (ms)" 
for i in {10..1000..10}; do
    for j in {1..5}; do
	num=$(shuf -i 0-10 -n 1);
   
	if [[ $(shuf -i 0-5 -n 1) -gt 4 ]]
	then
            echo "Bubble sort" $i,-----$(($num + $(($i * $i))));    
	else
	    echo "Bubble sort" $i,$(($num + $(($i * $i))));
	    echo "DebugMsg: Bubble sort completed for array size " $i;
	fi

	if [[ $(shuf -i 0-5 -n 1) -gt 4 ]]
	then
 	    echo "Quicksort" $i,$(echo "$i $num" | awk '{printf "%1.4f\n",$2+$1*log($1)}')
	else
	    echo "Quicksort" $i,$(echo "$i $num" | awk '{printf "%1.4f\n", $2+$1*log($1)}')
	    echo "DebugMsg: Quicksort completed for array size " $i;
	fi
    
    done
done
