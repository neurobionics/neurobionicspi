#!/bin/bash

dur=${1:-1}
frequency=${2:-500}

timestart=$(date +%s)

while [ $(($(date +%s) - timestart)) -lt $dur*60 ]
do
    temp=$(vcgencmd measure_temp)
    temp=${temp:5:2}
    echo $temp >> $PWD/data/raw/temp
    sleep 1/$frequency
done

