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
MAX_DURATION = 2.5  # seconds

if args.data:
    data_path = args.data
else:
    script_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(script_path.split("/utilities")[0], "data")

figure, axs = plt.subplots(2, 2, figsize=(10, 6))  # Create a 2x2 grid of subplots
axs = axs.ravel()

for i, load in enumerate(LOAD_MAP):
    for j, kernel_name in enumerate(KERNELS):
        folders = [
            folder
            for folder in os.listdir(data_path)
            if os.path.isdir(os.path.join(data_path, folder))
            and folder.startswith(kernel_name)
        ]
        folders.sort()
        folder = folders[LOAD_MAP.index(load)]
        cpu_temp = pd.DataFrame()

        temp_df = pd.read_csv(os.path.join(data_path, folder, "raw/temperature"))
        cpu_temp["temperature"] = temp_df.rolling(window=MVA_WINDOW).mean()
        cpu_temp["time"] = np.arange(cpu_temp.shape[0]) * DT

        cpu_temp = cpu_temp[cpu_temp["time"] <= MAX_DURATION]

        axs[i].plot(
            cpu_temp["time"],
            cpu_temp["temperature"],
            label=KERNEL_BETTER_NAMES[j],
            color=colors[j],
        )

    axs[i].set_title(f"Load: {LOAD_MAP[i]}%")  # Set the title of the subplot
    axs[i].set_ylabel("Temperature (°C)")  # Set the y-label of the subplot
    axs[i].set_xlabel("Time (s)")
    axs[i].legend(KERNEL_BETTER_NAMES, loc="lower right")  # Add a legend to the subplot

# Set the labels of the overall figure
figure.suptitle(f"[RT-Benchmark] CPU Temperature")
plt.tight_layout()  # Adjust the layout so that the subplots do not overlap
plt.savefig(f"cpu_temperature_comparison.png")  # Save the figure to a file
