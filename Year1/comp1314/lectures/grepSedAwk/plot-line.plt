set terminal png       
set output  "plot-sort-data.png" 
set title "Computational cost of sorting algorithm"
set xlabel "Number of elements to sort"
set ylabel "Time (ms)"
set style line 1 linecolor rgb '#0060ad' linetype 1 linewidth 2 pointtype 7 pointsize 1.5
set datafile separator ','
plot "data.dat" using 1:2 with linespoints ls 1