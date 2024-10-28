import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd

FULL_PARAMS_NAME = {"brm": ["Background Radius", "μ"], "rpsm": ["Requested Pixel Size", "μ"], "threshold": ["threshold", "intensity"], "count": ["Nuclei count", "# of Nucluos"]}


# Function to gather data from CSV files
def gather_data(folder):
    data = []
    for file in glob.glob(f"{folder}/*.csv"):
        file_name_parts = os.path.splitext(os.path.basename(file))[0].split("_")
        entry = {
            "rpsm": float(file_name_parts[3]),
            "threshold": float(file_name_parts[5]),
            "brm": float(file_name_parts[7]),
            "count": int(pd.read_csv(file).iloc[0]["Clustersize"])
        }
        data.append(entry)
    return data

# Function to plot data
def plot_data(data, x_key, y_key, title, filename):
    x_values = [i[x_key] for i in data]
    y_values = [i[y_key] for i in data]

    plt.figure()
    plt.plot(x_values, y_values, "o")
    plt.xlabel(f"{FULL_PARAMS_NAME[x_key][0]} [{FULL_PARAMS_NAME[x_key][1]}]")
    plt.ylabel(f"{FULL_PARAMS_NAME[y_key][0]} [{FULL_PARAMS_NAME[y_key][1]}]")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()

# Main execution
folder = "./short_exp_get_max_summary"
data = gather_data(folder)

# Define combinations to plot
combinations = [
    {"rpsm": 1.5, "brm": 4, "x": "threshold", "y": "count"},
    {"threshold": 0.1, "brm": 4, "x": "rpsm", "y": "count"},
    {"rpsm": 1.5, "threshold": 0.1, "x": "brm", "y": "count"},

    # Add more combinations as needed
]

# Iterate over combinations to plot
for combo in combinations:
    fixed_params = ["brm", "rpsm", "threshold"]
    fixed_params.remove(combo["x"])
    filtered_data = [entry for entry in data if entry[fixed_params[0]] == combo[fixed_params[0]] and entry[fixed_params[1]] == combo[fixed_params[1]]]
    if filtered_data:
        plot_data(filtered_data, combo["x"], combo["y"], f"Nuclei Count vs {FULL_PARAMS_NAME[combo["x"]][0]}", f"{combo['x']}_{fixed_params[0]}_{fixed_params[1]}.png")
