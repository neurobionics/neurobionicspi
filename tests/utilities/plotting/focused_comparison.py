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
LOAD = "100"
KERNELS = [
    "6.8.0-1005-raspi",
    "6.8.0-2004-raspi-realtime",
]
colors = ["gold", "mediumturquoise", "salmon", "mediumspringgreen"]
KERNEL_BETTER_NAMES = [
    "Ubuntu-Generic",
    "Ubuntu-RealTime",
]
KERNEL_LEGENDS = ["" for _ in KERNELS]
CORE_LEGENDS = [f"Core {i+1}" for i in range(4)]
THRESHOLD = 100  # us

if args.data:
    data_path = args.data
else:
    script_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(script_path.split("/utilities")[0], "data")

figure, axs = plt.subplots(
    1, len(KERNELS), figsize=(10, 6)
)  # Create a 2x2 grid of subplots
axs = axs.ravel()

for j, kernel_name in enumerate(KERNELS):
    total_occurrences = 0
    for i in range(4):  # Loop over the 4 cores
        folders = [
            folder
            for folder in os.listdir(data_path)
            if os.path.isdir(os.path.join(data_path, folder))
            and folder.startswith(kernel_name)
        ]
        folders.sort()
        folder = folders[LOAD_MAP.index(LOAD)]

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

        latencies = pd.read_csv(
            os.path.join(data_path, folder, f"histograms/histogram{i+1}"),
            delimiter="\t",
        )
        latencies.columns = [
            "latency",
            "frequency",
        ]

        latencies = latencies[latencies["latency"] > THRESHOLD]

        latencies_extended = latencies.loc[
            latencies.index.repeat(latencies["frequency"])
        ].reset_index(drop=True)

        sns.histplot(
            latencies_extended["latency"],
            label=CORE_LEGENDS[i] + f" [Max: {max_value} us]",
            color=colors[i],
            fill=True,
            ax=axs[j],
            bins=200,
        )

        total_occurrences += latencies_extended.shape[0]

    axs[j].set_title(f"{KERNEL_BETTER_NAMES[j]}")  # Set the title of the subplot
    axs[j].set_ylabel("Number of Occurrences")  # Set the y-label of the subplot
    axs[j].set_xlabel(f"Latency (us) [Total Occurences: {total_occurrences}]")
    axs[j].legend(loc="upper right")  # Add a legend to the subplot

# Set the labels of the overall figure
figure.suptitle(f"[RT-Benchmark] Latency Histogram (> {THRESHOLD} us) @{LOAD}% Load")
plt.tight_layout()  # Adjust the layout so that the subplots do not overlap
plt.savefig(
    f"{KERNEL_BETTER_NAMES[0]}_vs_{KERNEL_BETTER_NAMES[1]}_{LOAD}L_{THRESHOLD}T.png"
)  # Save the figure to a file
