import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import argparse
import numpy as np
import re
from scipy.stats import mannwhitneyu

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
            os.path.join(data_path, folder, f"histograms/histogram{i+1}"),
            delimiter="\t",
            names=[
                "latency",
                "frequency",
            ],
        )

        latencies_expanded = latencies.loc[
            latencies.index.repeat(latencies["frequency"])
        ].reset_index(drop=True)

        sns.kdeplot(
            latencies_expanded["latency"],
            color=colors[j],
            label=KERNEL_BETTER_NAMES[j],
            fill=True,
            ax=axs[i],
        )

        axs[i].set_xlim(0, 50)
        axs[i].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))
        axs[i].legend(loc="lower right")
        axs[i].set_xlabel("Latency (us)")
        axs[i].set_ylabel("Density")
        axs[i].set_title(f"Core {i+1}")

figure.suptitle(f"[RT-Benchmark] Latency Density @{LOAD}% Load")
plt.tight_layout()  # Adjust the layout so that the subplots do not overlap
plt.savefig(f"density_comparison_{LOAD}.png")  # Save the figure to a file
# plt.show()
