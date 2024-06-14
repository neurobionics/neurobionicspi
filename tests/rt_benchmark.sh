#!/bin/bash

load=(100 25 75 50)
idle_temp=63
duration=7

while [ ${#load[@]} -gt 0 ]; do
    temp=$(vcgencmd measure_temp)
    temp=${temp:5:4}

    # Compare the temperature as an integer
    if (( $(echo "$temp < $idle_temp" | bc -l) )); then
        sudo bash "$PWD/rt_test.sh" --duration $duration --load ${load[0]}
        
        load=("${load[@]:1}")
    else
        sleep 60
        continue
    fi
done
