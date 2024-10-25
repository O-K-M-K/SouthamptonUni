#!/bin/bash

echo "Algorithm   Array size, Time (ms)" 
for i in {10..1000..10}; do
    num=$(shuf -i 0-10 -n 1);
    #echo "Bubble sort" $i,$(($num + $(($i * $i))));
   
    if [[ $(shuf -i 0-5 -n 1) -gt 4 ]]
    then
        echo "Bubble sort" $i,-----$(($num + $(($i * $i))));    
    else
        echo "Bubble sort" $i, $(($num + $(($i * $i))));
	echo "DebugMsg: Bubble sort completed for array size " $i;
    fi

    if [[ $(shuf -i 0-5 -n 1) -gt 4 ]]
    then
 	echo "Quicksort" $i,-----$(echo $i | awk '{printf "%1.4f\n",$i*log($i)}')
    else
	#j=$(echo $i | awk '{printf "%1.4f\n",log($i)}')
	#echo $(($j + 10))
	echo "Quicksort" $i,$(echo $i | awk '{printf "%1.4f\n",$i*log($i)}')
	echo "DebugMsg: Quick sort completed for array size " $i;
    fi
    
    #echo "Quicksort" $i,$(echo $i | awk '{printf "%1.4f\n",log($i)}')
done
