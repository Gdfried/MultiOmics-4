import pandas as pd
import random
import subprocess
from glob import glob
import numpy as np


def run_r_script(script_path):
    command = f"Rscript {script_path}"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout


def gen_cross_per():
    mouses = ["IL-100","IL-1011","IL-1032","IL-1052","IL-1061","IL-1072","IL-1076","IL-1086","IL-1116","IL-111","IL-1126","IL-1141","IL-1146","IL-1156","IL-1157","IL-1161","IL-1176","IL-1187","IL-1246","IL-1259","IL-1286","IL-1287","IL-1296","IL-1297","IL-1300","IL-1348","IL-1350","IL-1379","IL-1388","IL-1391","IL-1396","IL-1438","IL-1439","IL-1452","IL-1457","IL-145","IL-1462","IL-1467","IL-1468","IL-1469","IL-1478","IL-1480","IL-1488","IL-1509","IL-1513","IL-1573","IL-1575","IL-1650","IL-1654","IL-1664","IL-1668","IL-1675","IL-1689","IL-1693","IL-1694","IL-1703","IL-1715","IL-1750","IL-1754","IL-1799","IL-1814","IL-182","IL-188","IL-1912","IL-1913","IL-1914","IL-196","IL-2011","IL-2032","IL-2052","IL-2072","IL-2076","IL-2116","IL-2126","IL-2131","IL-2141","IL-2146","IL-2156","IL-2157","IL-2161","IL-2176","IL-2187","IL-219","IL-2246","IL-2259","IL-2286","IL-2287","IL-2288","IL-2296","IL-2297","IL-2300","IL-2348","IL-2350","IL-2379","IL-2391","IL-2396","IL-2438","IL-2439","IL-2452","IL-2462","IL-2467","IL-2468","IL-2469","IL-2478","IL-2480","IL-2488","IL-2509","IL-2573","IL-2575","IL-2650","IL-2664","IL-2680","IL-2689","IL-2693","IL-2694","IL-2703","IL-2715","IL-2735","IL-2750","IL-2799","IL-27","IL-2814","IL-285","IL-2912","IL-2913","IL-2914","IL-3032","IL-3052","IL-3072","IL-3086","IL-30","IL-3116","IL-312","IL-313","IL-3156","IL-3246","IL-3288","IL-3296","IL-3300","IL-3348","IL-3391","IL-3396","IL-3438","IL-3439","IL-3457","IL-3480","IL-3509","IL-3575","IL-3654","IL-3668","IL-3689","IL-3693","IL-3703","IL-3750","IL-3754","IL-3814","IL-3912","IL-3914","IL-4032","IL-4052","IL-40","IL-4116","IL-4146","IL-4156","IL-4161","IL-4296","IL-4348","IL-4391","IL-4438","IL-4452","IL-4457","IL-4462","IL-4668","IL-4693","IL-4715","IL-4799","IL-519","IL-51","IL-534","IL-540","IL-551","IL-557","IL-563","IL-568","IL-57","IL-586","IL-600","IL-611","IL-634","IL-643","IL-645","IL-670","IL-682","IL-688","IL-699","IL-711","IL-72","IL-785","IL-86","IL-30D","IL-34","IL-68","IL-170","IL-188D","IL-211","IL-1348D","IL-2513","IL-21","IL-3348D","IL-557D","IL-645D","IL-670D","IL-4750","IL-785D","IL-1052-MDA","IL-1061-MDA","IL-111-MDA","IL-1156-MDA","IL-1157-MDA","IL-1246-MDA","IL-1287-MDA","IL-130","IL-1300-MDA","IL-133","IL-1350-MDA","IL-1379-MDA","IL-1452-MDA","IL-1468-MDA","IL-1488-MDA","IL-150","IL-1513-MDA","IL-16188","IL-16211","IL-16513","IL-16521","IL-16557","IL-1675-MDA","IL-16750","IL-16912","IL-17","IL-170-MDA","IL-1703-MDA","IL-1754-MDA","IL-179","IL-180","IL-1814-MDA","IL-185","IL-187","IL-188-MDA","IL-2011-MDA","IL-203","IL-211-MDA","IL-212","IL-2126-MDA","IL-213","IL-2131-MDA","IL-2141-MDA","IL-2146-MDA","IL-215","IL-2156-MDA","IL-2176-MDA","IL-219-MDA","IL-2288-MDA","IL-2350-MDA","IL-2379-MDA","IL-2391-MDA","IL-2438-MDA","IL-2439-MDA","IL-2452-MDA","IL-2457","IL-2462-MDA","IL-2469-MDA","IL-2573-MDA","IL-2650-MDA","IL-2668","IL-2689-MDA","IL-2693-MDA","IL-291","IL-292","IL-301","IL-302","IL-310","IL-311","IL-3156-MDA","IL-316","IL-3296-MDA","IL-33","IL-3300-MDA","IL-3348-MDA","IL-3438-MDA","IL-3457-MDA","IL-3480-MDA","IL-3509-MDA","IL-3575-MDA","IL-37","IL-3703-MDA","IL-4032-MDA","IL-4052-MDA","IL-4141","IL-4156-MDA","IL-4348-MDA","IL-4438-MDA","IL-4457-MDA","IL-4668-MDA","IL-4799-MDA","IL-48","IL-49","IL-515","IL-519-MDA","IL-527","IL-54","IL-60","IL-611-MDA","IL-630","IL-633","IL-645-MDA","IL-670-MDA","IL-677","IL-688-MDA","IL-711-MDA","IL-72-MDA","IL-76","IL-785-MDA","IL-811","IL-83","IL-85","IL-99","IL-7","IL-507","IL-11","IL-511","IL-15","IL-517","IL-18","IL-518","IL-19","IL-21-MEGA","IL-521","IL-26","IL-526","IL-27-MEGA","IL-30-MEGA","IL-530","IL-31","IL-531","IL-533","IL-34-MEGA","IL-534-MEGA","IL-537","IL-39","IL-40-MEGA","IL-540-MEGA","IL-47","IL-547","IL-548","IL-549","IL-50","IL-550","IL-551-MEGA","IL-55","IL-555","IL-57-MEGA","IL-557-MEGA","IL-63","IL-563-MEGA","IL-68-MEGA","IL-568-MEGA","IL-572","IL-576","IL-77","IL-577","IL-86-MEGA","IL-95","IL-595","IL-599","IL-100-MEGA","IL-600-MEGA","IL-104","IL-604","IL-108","IL-608","IL-114","IL-614","IL-119","IL-619","IL-121","IL-621","IL-125","IL-625","IL-127","IL-627","IL-134","IL-634-MEGA","IL-135","IL-635","IL-136","IL-636","IL-140","IL-640","IL-143","IL-643-MEGA","IL-145-MEGA","IL-152","IL-652","IL-159","IL-166","IL-666","IL-169","IL-177","IL-182-MEGA","IL-682-MEGA","IL-196-MEGA","IL-696","IL-199","IL-699-MEGA","IL-703","IL-217","IL-717","IL-719","IL-285-MEGA","IL-287","IL-787","IL-290","IL-790","IL-792","IL-294","IL-299","IL-799","IL-810","IL-312-MEGA","IL-812","IL-313-MEGA","IL-813","IL-317","IL-817","AU18042","AU8002","AU8004","AU8005","AU8008","AU8010","AU8016","AU8018","AU8021","AU8024","AU8026","AU8027","AU8031","AU8033","AU8036","AU8043","AU8045","AU8046","AU8048","AU8049","AU8052","AU8054","AU8056","IL-16012","IL-16034","IL-16072","IL-16188-MEGA.UNC","IL-16211-MEGA.UNC","IL-16296","IL-16441","IL-16513-MEGA.UNC","IL-16521-MEGA.UNC","IL-16557-MEGA.UNC","IL-16680","IL-16750-MEGA.UNC","IL-16768","IL-16785","IL-16912-MEGA.UNC","OR13067","OR13140","OR13421","OR1515","OR15155","OR15156","OR1566","OR3015","OR3032","OR3154","OR3252","OR3393","OR3415","OR3460","OR3564","OR3609","OR4410","OR477","OR5035","OR5080","OR5119","OR5306","OR5346","OR5358","OR5391","OR5489","OR5612","OR773","OR867"]
    def random_permutation():
        # Create a list of numbers from 1 to 8
        numbers = list(range(1, 9))
        
        # Shuffle the list randomly
        random.shuffle(numbers)
        
        # Return the shuffled list as a permutation
        return numbers

    r_array = []
    with open("/Users/gdfri/Documents/Learning/Final_Project/R_files/qtl_runs/mouse_from_image/cc_crossg.csv", "w") as f:
        f.write(f"# \n")
        f.write(f"# nrow {len(mouses)-1}\n")
        f.write(f"# ncol 9\n")
        for line in mouses:
            s = line
            r = [str(i) for i in random_permutation()]
            while r in r_array:
                r = [str(i) for i in random_permutation()]
            r_array.append(r)
            s += "," + ",".join(r)+"\n"
            f.write(s)


# gen_cross_per()
def run_full_permoutarion_test(n):
    for i in range(n):
        gen_cross_per()
        print("a")
        output = run_r_script("~/Documents/Learning/Final_Project/R_files/qtl_runs/qtl2_run_try/qtl_guide_script.R")
        print(output)
        print(str(i))


dfs = []
for file in glob("./R_files/permutation_test/*.csv"):
    df = pd.read_csv(file)
    dfs.append(df)

first_two_columns = dfs[0].iloc[:, :3]

def calculate_stats(func):
    # Stack all dataframes, keeping only the columns after the first two
    stacked = pd.concat([df.iloc[:, 3:] for df in dfs])
    # Group by the original index and apply the function
    result = stacked.groupby(stacked.index).agg(func)
    return result

# Calculate statistics
average_df = calculate_stats(np.mean)
std_df = calculate_stats(np.std)
min_df = calculate_stats(np.min)
max_df = calculate_stats(np.max)

# Combine the first two columns with the calculated stats
average_df = pd.concat([first_two_columns, average_df], axis=1)
std_df = pd.concat([first_two_columns, std_df], axis=1)
min_df = pd.concat([first_two_columns, min_df], axis=1)
max_df = pd.concat([first_two_columns, max_df], axis=1)

# Create a Pandas Excel writer using openpyxl as the engine
with pd.ExcelWriter('output_tables.xlsx', engine='openpyxl') as writer:
    # Write each DataFrame to a different worksheet
    average_df.to_excel(writer, sheet_name='Average', index=False)
    std_df.to_excel(writer, sheet_name='Standard Deviation', index=False)
    min_df.to_excel(writer, sheet_name='Minimum', index=False)
    max_df.to_excel(writer, sheet_name='Maximum', index=False)

print("Tables have been created and saved in 'output_tables.xlsx'")