#!/bin/bash

dur=${1:-1}
load=${2:-50}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "$1 could not be found"
        echo "Please install $1"
        exit 1
    fi
}

check_command stress-ng

stress-ng -c 0 --mq 1 --iomix 1 --vm 1 --vm-bytes 50% -l $load --cpu-method fft --metrics-brief --tz -t "$dur"m
