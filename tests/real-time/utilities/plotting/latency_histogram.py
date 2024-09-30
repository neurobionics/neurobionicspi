import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import argparse
import numpy as np
import re

parser = argparse.ArgumentParser(description="Process data path.")
parser.add_argument("--data", type=str, help="The path to the data directory")
parser.add_argument("--kernel", type=str, help="The kernel name")
args = parser.parse_args()

plt.style.use("dark_background")

MVA_WINDOW = 16
DT = 1 / 500
LOAD_MAP = ["100", "25", "75", "50"]
DISTRIBUTION = 25

if args.data:
    data_path = args.data
else:
    script_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(script_path.split("/utilities")[0], "data")

if args.kernel:
    kernel_name = args.kernel
else:
    kernel_name = "6.8.0-2004-raspi-realtime"

# find all folders that start with the kernel name within the data folder
folders = [
    folder
    for folder in os.listdir(data_path)
    if os.path.isdir(os.path.join(data_path, folder)) and folder.startswith(kernel_name)
]
folders.sort()

latencies = pd.DataFrame()

# Collect data from all folders
for i, folder in enumerate(folders):
    temp_df = pd.read_csv(
        os.path.join(data_path, folder, "histograms/histogram"), delimiter="\t"
    )
    temp_df.columns = [
        "latency",
        "core_1_count",
        "core_2_count",
        "core_3_count",
        "core_4_count",
    ]
    latencies = temp_df
    # latencies["latency"] = latencies["latency"] / 1000  # convert to ms

    figure, ax = plt.subplots(figsize=(10, 6))
    ax.title.set_text(
        f"[RT-Benchmark] Latency Histogram @{LOAD_MAP[i]} Load: {kernel_name}"
    )
    ax.set_ylabel("Number of Occurrences")

    for j in range(1, 5):

        # Assuming 'text' is the selected text
        with open(os.path.join(data_path, folder, f"analysis/statistics{j}")) as f:
            text = f.read()

        # Use regex to find the mean and standard deviation
        mean = float(re.search(r"Mean: (\d+\.\d+)", text).group(1))
        std_dev = float(re.search(r"Standard Deviation: (\d+\.\d+)", text).group(1))
        max_value = int(re.search(r"Max: (\d+)", text).group(1))

        min_val = mean - DISTRIBUTION * std_dev
        max_val = mean + DISTRIBUTION * std_dev

        ax.set_xlabel(
            f"Latency [us] [Mean: {mean} us, Standard Deviation: {std_dev} us, Max: {max_value} us]"
        )

        temp_df = latencies[
            (latencies["latency"] >= min_val) & (latencies["latency"] <= max_val)
        ]

        plt.bar(
            temp_df["latency"],
            temp_df[f"core_{j}_count"],
            label=f"Core {j}",
        )
        plt.legend()

    plt.savefig(f"latency_histogram_{kernel_name}_{LOAD_MAP[i]}.png")
