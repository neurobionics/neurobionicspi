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
    kernel_name = "6.8.0-2004-raspi-realtime"

# find all folders that start with the kernel name within the data folder
folders = [
    folder
    for folder in os.listdir(data_path)
    if os.path.isdir(os.path.join(data_path, folder)) and folder.startswith(kernel_name)
]
folders.sort()

cpu_temp = pd.DataFrame()

figure, ax = plt.subplots(figsize=(10, 6))
ax.title.set_text(f"[RT-Benchmark] CPU Temperature: {kernel_name}")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Temperature [°C]")

# Collect data from all folders
for i, folder in enumerate(folders):
    temp_df = pd.read_csv(os.path.join(data_path, folder, "raw/temperature"))
    cpu_temp[LOAD_MAP[i]] = temp_df.rolling(window=MVA_WINDOW).mean()

cpu_temp["time"] = np.arange(cpu_temp.shape[0]) * DT

# plot data
for load in LOAD_MAP:
    ax.plot(cpu_temp["time"], cpu_temp[load], label=load)

ax.legend(LOAD_MAP, loc="lower right")
plt.savefig(f"cpu_temperature_{kernel_name}.png")
