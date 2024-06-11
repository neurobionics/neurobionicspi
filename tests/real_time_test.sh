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
cyclictest -D"$dur"m -m -Sp90 -i200 -h400 -q >output

# 2. Get maximum latency
max=`grep "Max Latencies" output | tr " " "\n" | sort -n | tail -1 | sed s/^0*//`

# 3. Grep data lines, remove empty lines and create a common field separator
grep -v -e "^#" -e "^$" output | tr " " "\t" >histogram 

# 4. Set the number of cores
cores=$(nproc)

# 5. Create two-column data sets with latency classes and frequency values for each core, for example
for i in `seq 1 $cores`
do
  column=`expr $i + 1`
  cut -f1,$column histogram >histogram$i
done

# 6. Create plot command header
echo -n -e "set title \"Latency plot\"\n\
set terminal png\n\
set xlabel \"Latency (us), max $max us\"\n\
set logscale y\n\
set xrange [0:400]\n\
set yrange [0.8:*]\n\
set ylabel \"Number of latency samples\"\n\
set output \"plot.png\"\n\
plot " >plotcmd

# 7. Append plot command data references
for i in `seq 1 $cores`
do
  if test $i != 1
  then
    echo -n ", " >>plotcmd
  fi
  cpuno=`expr $i - 1`
  if test $cpuno -lt 10
  then
    title=" CPU$cpuno"
   else
    title="CPU$cpuno"
  fi
  echo -n "\"histogram$i\" using 1:2 title \"$title\" with histeps" >>plotcmd
done

# 8. Execute plot command
gnuplot -persist <plotcmd
echo "Histogram plot saved in $PWD/plot.png"