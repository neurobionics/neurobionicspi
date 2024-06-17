import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import argparse
import numpy as np

parser = argparse.ArgumentParser(description="Process data path.")
parser.add_argument("--data", type=str, help="The path to the data directory")
parser.add_argument("--kernel", type=str, help="The kernel name")
args = parser.parse_args()

plt.style.use("dark_background")

MVA_WINDOW = 16
DT = 1 / 500
LOAD_MAP = ["100", "25", "75", "50"]

if args.data:
    data_path = args.data
else:
    script_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(script_path.split("/utilities")[0], "data")

if args.kernel:
    kernel_name = args.kernel
else:
    kernel_name = "6.8.0-1005-raspi"

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
    ax.title.set_text(f"[RT-Benchmark] Latency Histogram: {kernel_name}")
    ax.set_xlabel("Latency [ms]")
    ax.set_ylabel("Number of Occurrences")
    plt.bar(
        latencies["latency"],
        latencies["core_1_count"],
        color="r",
        alpha=0.5,
        label="Core 1",
    )

    plt.show()
