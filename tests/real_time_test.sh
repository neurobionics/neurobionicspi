#!/bin/bash

offline=0
enable_plotting=1
dur=1
load=50

# Get the kernel type
kernel_type=$(uname -r)
current_time=$(date +%H:%M:%S)

# Create the folder name
folder_name="${kernel_type}_${current_time}"

# Create the new folder
mkdir -p "$PWD/data/$folder_name"
raw_data_path="$PWD/data/$folder_name/raw"
histograms_path="$PWD/data/$folder_name/histograms"
analysis_path="$PWD/data/$folder_name/analysis"
plots_path="$PWD/data/$folder_name/plots"
logs_path="$PWD/data/$folder_name/logs"

mkdir -p "$raw_data_path" "$histograms_path" "$analysis_path" "$plots_path" "$logs_path"

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --offline)
        offline=1
        shift
        ;;
        --enable_plotting)
        enable_plotting=1
        shift
        ;;        
        --duration)
        dur="$2"
        shift 2
        ;;
        --load)
        load="$2"
        shift 2
        ;;
        *)
        echo "Unknown option: $key"
        exit 1
        ;;
    esac
done


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

    cores=$(nproc)

    # Measuring cpu temperature
    sudo bash "$PWD/utilities/measure_temp.sh" > "$raw_data_path/temperature" 2>&1 &

    # Adding stress to the system
    sudo bash "$PWD/utilities/add_stress.sh" "$dur" "$load" > "$logs_path/stress.log" 2>&1 &

    echo "Running cyclictest for $dur minute"
    cyclictest -D"$dur"m -m -Sp90 -i200 -h400 -q > "$raw_data_path/cyclicresults"
fi

# 3. Grep data lines, remove empty lines and create a common field separator
grep -v -e "^#" -e "^$" "$raw_data_path/cyclicresults" | tr " " "\t" > "$histograms_path/histogram"

# 4. Set the number of cores
read -r -a max <<< $(grep "Max Latencies" "$raw_data_path/cyclicresults" | awk -F: '{print $2}')
read -r -a min <<< $(grep "Min Latencies" "$raw_data_path/cyclicresults" | awk -F: '{print $2}')

# 5. Create two-column data sets with latency classes and frequency values for each core, for example
for i in `seq 1 $cores`
do
    column=`expr $i + 1`
    cut -f1,$column "$histograms_path/histogram" > "$histograms_path/histogram$i"

    echo "Max: ${max[$i-1]}" > "$analysis_path/statistics$i"
    echo "Min: ${min[$i-1]}" >> "$analysis_path/statistics$i"

    awk '{print $1, $2, $1*$2}' "$histograms_path/histogram$i" > "$analysis_path/data$i"
    mean=$(awk '{xf+=$3; n+=$2} END {print xf/n}' "$analysis_path/data$i")
    echo "Mean: $mean" >> "$analysis_path/statistics$i"

    awk -v mean="$mean" '{print $1, $2, $3, $2*($1-mean)^2, $2*($1-mean)^2}' "$analysis_path/data$i" > "$analysis_path/data$i.tmp"
    mv "$analysis_path/data$i.tmp" "$analysis_path/data$i"
    variance=$(awk '{x+=$4; n+=$2} END {print x/(n-1)}' "$analysis_path/data$i")
    echo "Variance: $variance" >> "$analysis_path/statistics$i"

    std_dev=$(awk -v variance="$variance" 'BEGIN {print sqrt(variance)}')
    echo "Standard Deviation: $std_dev" >> "$analysis_path/statistics$i"
done

if [ "$enable_plotting" -eq 1 ]; then
    # 6. Create plot command header
    echo -n -e "set title \"Worst Case Latency Test \"\n\
    set terminal png\n\
    set xlabel \"Latency (us) [Max Latencies:${max[@]} us]\"\n
    set logscale y\n\
    set xrange [0:400]\n\
    set yrange [0.8:*]\n\
    set ylabel \"Number of latency samples\"\n\
    set output \"$plots_path/plot.png\"\n\
    plot " >"$plots_path/plotcmd"

    # 7. Append plot command data references
    for i in `seq 1 $cores`
    do
    if test $i != 1
    then
        echo -n ", " >> "$plots_path/plotcmd"
    fi
    cpuno=`expr $i - 1`
    if test $cpuno -lt 10
    then
        title=" CPU$cpuno"
    else
        title="CPU$cpuno"
    fi
    echo -n "\"$histograms_path/histogram$i\" using 1:2 title \"$title\" with histeps" >> "$plots_path/plotcmd"
    done

    # 8. Execute plot command
    gnuplot -persist < "$plots_path/plotcmd"
    echo "Histogram plot saved in $plots_path/plot.png"
fi
