import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd

folder = "./short_exp_get_max_summary"

data = []
for file in glob.glob(f"{folder}/*.csv"):
    entery = {}
    file_s = os.path.split(os.path.splitext(file)[0])[-1].split("_")
    entery["rpsm"] = float(file_s[3])
    entery["threshold"] = float(file_s[5])
    entery["brm"] = float(file_s[7])
    df = pd.read_csv(file)
    entery["count"] = int(df["Clustersize"])
    data.append(entery)
    
thr_starts_x = [i["threshold"] for i in data if i["rpsm"] == 1.5 and i["brm"] == 4]
thr_starts_y = [i["count"] for i in data if i["rpsm"] == 1.5 and i["brm"] == 4]

plt.plot(thr_starts_x, thr_starts_y, "o")
plt.xlabel("Threshold")
plt.ylabel("Nucluos count")
plt.title("Nucluos count VS Threshold")
plt.savefig("Threshold.png")
plt.clf()

rpsm_starts = [i for i in data if "0.1" in i and "4.0" in i]
rpsm_data = []
for i in rpsm_starts:
    rpsm_data.append([float(i[3]), i[-1]])
rpsm_data = np.array(rpsm_data)
plt.plot(rpsm_data[:,0], rpsm_data[:,1], "o")
plt.xlabel("Requested Pixel Size Microns")
plt.ylabel("Nucluos count")
plt.title("Nucluos count VS Requested Pixel Size Microns")
plt.savefig("epsm.png")
plt.clf()

brm_starts = [i for i in data if "1.5" in i and "0.1" in i]
brm_data = []
for i in brm_starts:
    brm_data.append([float(i[-2]), i[-1]])
brm_data = np.array(brm_data)
plt.plot(brm_data[:,0], brm_data[:,1], "o")
plt.xlabel("Background Radius Microns")
plt.ylabel("Nucluos count")
plt.title("Nucluos count VS Background Radius Microns")
plt.savefig("brm.png")
