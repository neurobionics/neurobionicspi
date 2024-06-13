#!/bin/bash

dur=${1:-1}
frequency=${2:-500}

timestart=$(date +%s)
dur_in_seconds=$((dur * 60))

while [ $(($(date +%s) - timestart)) -lt $dur_in_seconds ]
do
    temp=$(vcgencmd measure_temp)
    temp=${temp:5:2}
    echo $temp
    sleep $(bc <<< "scale=2; 1/$frequency")
done

