#!/bin/bash

# TODO: Spin up a process to add stress on the CPU with stress-ng ("command > file 2>&1 &") and user defined % of CPU usage
# TODO: Record CPU temperature and power consumption

offline=1
enable_plotting=0
dur=${1:-1}

if [ "$offline" -eq 1 ]; then
    echo "Running offline analysis"
    cores=4
else
    echo "Running tests online"
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

    echo "Running cyclictest for $dur minute"
    cyclictest --nsecs -D"$dur"m -m -Sp90 -i200 -h350000 -q > $PWD/data/raw/output
    cores=$(nproc)
fi

# 2. Get maximum latency
# max=`grep "Max Latencies" data/raw/output | tr " " "\n" | sort -n | tail -1 | sed s/^0*//`
# min=`grep "Min Latencies" data/raw/output | tr " " "\n" | sort -n | head -1 | sed s/^0*//`

# 3. Grep data lines, remove empty lines and create a common field separator
grep -v -e "^#" -e "^$" $PWD/data/raw/output | tr " " "\t" > $PWD/data/histograms/histogram 

# 4. Set the number of cores
read -r -a max <<< $(grep "Max Latencies" $PWD/data/raw/output | awk -F: '{print $2}')
read -r -a min <<< $(grep "Min Latencies" $PWD/data/raw/output | awk -F: '{print $2}')

# 5. Create two-column data sets with latency classes and frequency values for each core, for example
for i in `seq 1 $cores`
do
    column=`expr $i + 1`
    cut -f1,$column $PWD/data/histograms/histogram > $PWD/data/histograms/histogram$i

    echo "Max: ${max[$i-1]}" > $PWD/data/analysis/statistics$i
    echo "Min: ${min[$i-1]}" >> $PWD/data/analysis/statistics$i

    # create a new file called statistics that has a third row in addition to the histogram1 file that
    # is just the multiplication of the first and second row of the histogram1 file
    awk '{print $1, $2, $1*$2}' $PWD/data/histograms/histogram$i > $PWD/data/analysis/data$i
    mean=$(awk '{xf+=$3; n+=$2} END {print xf/n}' $PWD/data/analysis/data$i)
    echo "Mean: $mean" >> $PWD/data/analysis/statistics$i

    awk -v mean="$mean" '{print $1, $2, $3, $2*($1-mean)^2, $2*($1-mean)^2}' $PWD/data/analysis/data$i > $PWD/data/analysis/data$i.tmp
    mv $PWD/data/analysis/data$i.tmp $PWD/data/analysis/data$i
    variance=$(awk '{x+=$4; n+=$2} END {print x/(n-1)}' $PWD/data/analysis/data$i)
    echo "Variance: $variance" >> $PWD/data/analysis/statistics$i

    std_dev=$(awk -v variance="$variance" 'BEGIN {print sqrt(variance)}')
    echo "Standard Deviation: $std_dev" >> $PWD/data/analysis/statistics$i
done

if [ "$enable_plotting" -eq 1 ]; then
    # 6. Create plot command header
    echo -n -e "set title \"Worst Case Latency Test \"\n\
    set terminal png\n\
    set xlabel \"Latency (ns) [Max Latencies:${max[@]} ns]\"\n
    set logscale y\n\
    set xrange [0:350000]\n\
    set yrange [0.8:*]\n\
    set ylabel \"Number of latency samples\"\n\
    set output \"$PWD/data/plots/plot.png\"\n\
    plot " >$PWD/data/plots/plotcmd

    # 7. Append plot command data references
    for i in `seq 1 $cores`
    do
    if test $i != 1
    then
        echo -n ", " >> $PWD/data/plots/plotcmd
    fi
    cpuno=`expr $i - 1`
    if test $cpuno -lt 10
    then
        title=" CPU$cpuno"
    else
        title="CPU$cpuno"
    fi
    echo -n "\"$PWD/data/histograms/histogram$i\" using 1:2 title \"$title\" with histeps" >> $PWD/data/plots/plotcmd
    done

    # 8. Execute plot command
    gnuplot -persist < $PWD/data/plots/plotcmd
    echo "Histogram plot saved in $PWD/data/plots/plot.png"
fi
