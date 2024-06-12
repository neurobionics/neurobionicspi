#!/bin/bash

# Check if cyclictest, stress-ng, and gnuplot are installed
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "$1 could not be found"
        echo "Please install $1"
        exit 1
    fi
}

check_command cyclictest
check_command stress-ng
check_command gnuplot

dur=$1
if [ -z "$dur" ]; then
    dur=1
fi
echo "Running cyclictest for $dur minute"
cyclictest -D"$dur"m -m -Sp90 -i200 -h400 -q > data/raw/output

# 2. Get maximum latency
max=`grep "Max Latencies" data/raw/output | tr " " "\n" | sort -n | tail -1 | sed s/^0*//`
min=`grep "Min Latencies" data/raw/output | tr " " "\n" | sort -n | head -1 | sed s/^0*//`

# 3. Grep data lines, remove empty lines and create a common field separator
grep -v -e "^#" -e "^$" data/raw/output | tr " " "\t" >data/histograms/histogram 

# 4. Set the number of cores
cores=$(nproc)

# 5. Create two-column data sets with latency classes and frequency values for each core, for example
for i in `seq 1 $cores`
do
    column=`expr $i + 1`
    cut -f1,$column data/histograms/histogram >data/histograms/histogram$i

    # create a new file called statistics that has a third row in addition to the histogram1 file that
    # is just the multiplication of the first and second row of the histogram1 file
    awk '{print $1, $2, $1*$2}' data/histograms/histogram$i > data/analysis/data$i
    mean=$(awk '{xf+=$3; n+=$2} END {print xf/n}' data/analysis/data$i)
    echo "Mean: $mean" > data/analysis/statistics$i

    awk -v mean="$mean" '{print $1, $2, $3, $2*($1-mean)^2, $2*($1-mean)^2}' data/analysis/data$i > data/analysis/data$i.tmp
    mv data/analysis/data$i.tmp data/analysis/data$i
    variance=$(awk '{x+=$4; n+=$2} END {print x/(n-1)}' data/analysis/data$i)
    echo "Variance: $variance" >> data/analysis/statistics$i

    std_dev=$(awk -v variance="$variance" 'BEGIN {print sqrt(variance)}')
    echo "Standard Deviation: $std_dev" >> data/analysis/statistics$i

done

# # 6. Create plot command header
# echo -n -e "set title \"Latency plot\"\n\
# set terminal png\n\
# set xlabel \"Latency (us), max $max us\"\n\
# set logscale y\n\
# set xrange [0:400]\n\
# set yrange [0.8:*]\n\
# set ylabel \"Number of latency samples\"\n\
# set output \"plot.png\"\n\
# plot " >plotcmd

# # 7. Append plot command data references
# for i in `seq 1 $cores`
# do
#   if test $i != 1
#   then
#     echo -n ", " >>plotcmd
#   fi
#   cpuno=`expr $i - 1`
#   if test $cpuno -lt 10
#   then
#     title=" CPU$cpuno"
#    else
#     title="CPU$cpuno"
#   fi
#   echo -n "\"histogram$i\" using 1:2 title \"$title\" with histeps" >>plotcmd
# done

# # 8. Execute plot command
# gnuplot -persist <plotcmd
# echo "Histogram plot saved in $PWD/plot.png"