import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
LOAD = "25"
KERNELS = [
    "6.8.0-1005-raspi",
    "6.6.20+rpt-rpi-2712",
    "6.8.0-2004-raspi-realtime",
]
colors = ["gold", "mediumturquoise", "salmon"]
KERNEL_BETTER_NAMES = [
    "UBU",
    "RAS",
    "URT",
]
KERNEL_LEGENDS = ["" for _ in KERNELS]
DISTRIBUTION = 3

if args.data:
    data_path = args.data
else:
    script_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(script_path.split("/utilities")[0], "data")

figure, axs = plt.subplots(2, 2, figsize=(10, 6))  # Create a 2x2 grid of subplots
axs = axs.ravel()

for i in range(4):  # Loop over the 4 cores
    for j, kernel_name in enumerate(KERNELS):
        folders = [
            folder
            for folder in os.listdir(data_path)
            if os.path.isdir(os.path.join(data_path, folder))
            and folder.startswith(kernel_name)
        ]
        folders.sort()
        folder = folders[LOAD_MAP.index(LOAD)]

        latencies = pd.read_csv(
            os.path.join(data_path, folder, "histograms/histogram"), delimiter="\t"
        )
        latencies.columns = [
            "latency",
            "core_1_count",
            "core_2_count",
            "core_3_count",
            "core_4_count",
        ]

        # Assuming 'text' is the selected text
        with open(os.path.join(data_path, folder, f"analysis/statistics{i+1}")) as f:
            text = f.read()

        # Use regex to find the mean and standard deviation
        mean = float(re.search(r"Mean: (\d+\.\d+)", text).group(1))
        std_dev = float(re.search(r"Standard Deviation: (\d+\.\d+)", text).group(1))
        max_value = float(re.search(r"Max: (\d+)", text).group(1))

        KERNEL_LEGENDS[j] = (
            f"{KERNEL_BETTER_NAMES[j]}: x̄={mean:.2f} us; max={max_value/1000:.2f} ms"
        )

        min_val = mean - DISTRIBUTION * std_dev
        max_val = mean + DISTRIBUTION * std_dev

        temp_df = latencies[
            (latencies["latency"] >= min_val) & (latencies["latency"] <= max_val)
        ]

        axs[i].bar(
            temp_df["latency"],
            temp_df[f"core_{i+1}_count"],
            label=f"Core {i+1}",
            alpha=0.75,
            color=colors[j],
        )

    axs[i].yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: "{:,.0f}".format(x / 100000))
    )
    axs[i].set_title(f"Core {i+1}")  # Set the title of the subplot
    axs[i].set_ylabel("Number of Occurrences (1e-5)")  # Set the y-label of the subplot
    axs[i].set_xlabel("Latency (us)")
    axs[i].legend(KERNEL_LEGENDS, loc="upper right")  # Add a legend to the subplot

# Set the labels of the overall figure
figure.suptitle(f"[RT-Benchmark] Latency Histogram @{LOAD} Load")
plt.tight_layout()  # Adjust the layout so that the subplots do not overlap
plt.savefig(f"histogram_comparison_{LOAD}.png")  # Save the figure to a file
