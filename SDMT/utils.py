import os
import argparse
import pickle
import gzip
import re
import pandas as pd
import matplotlib.pyplot as plt

def unpack_pickle(pickle_path):
# Open the pickle file
    with open(pickle_path, 'rb') as file:
        data = pickle.load(file)
    # Print the loaded data
    print(data)


def delut_manifest(path_to_manifest, outdir, one_line_out_of=10):
    counter = one_line_out_of
    with open(path_to_manifest, "r") as in_mani, open(os.path.join(outdir, "deluted_" + os.path.basename(path_to_manifest)), "w") as out_mani:
        for i, line in enumerate(in_mani):
            if counter and i: 
                counter -= 1
                continue
            counter = one_line_out_of - 1
            out_mani.write(line)
            print(f"-I- Wrote line: {i}")
    return

def split_manifest_by_svs(path_to_manifest, outdir, how_many_svs=300):
    count_svs = 1
    count_mani = 1
    with open(path_to_manifest, "r") as in_mani:
        out_mani = open(os.path.join(outdir, f"deluted_no{count_mani}_" + os.path.basename(path_to_manifest)), "w")
        for i, line in enumerate(in_mani):
            if not i:
                header = line
            out_mani.write(line)
            if re.search("svs", line):
                count_svs += 1
            if not count_svs%how_many_svs:
                out_mani.close()
                out_mani = open(os.path.join(outdir, f"deluted_no{count_mani}_" + os.path.basename(path_to_manifest)), "w")
                out_mani.write(header)
                count_mani += 1
                count_svs = 1
            

def get_first_row_from_csv(csv_file_path):
    # try:
        # Read the first row of the Excel file
    df = pd.read_csv(csv_file_path)
    
    # Convert the first row to a list
    first_row = df.columns.tolist()
    print(first_row)
    return first_row
    
    # except Exception as e:
    #     return f"An error occurred: {e}"


def check_and_save_csv_columns(csv_file_path, required_columns):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Get the columns present in the CSV file
        actual_columns = set(df.columns)
        
        # Convert required_columns list to a set for easy comparison
        required_columns_set = set(required_columns)
        
        # Determine missing columns
        missing_columns = required_columns_set - actual_columns
        
        # Determine redundant columns
        redundant_columns = actual_columns - required_columns_set
        
        # Print missing columns
        if missing_columns:
            print("Missing columns:", ', '.join(missing_columns))
        else:
            print("No columns are missing.")
        
        # Print redundant columns
        if redundant_columns:
            print("Redundant columns:", ', '.join(redundant_columns))
        else:
            print("No redundant columns.")
        
        # Create a DataFrame with only the specified columns that exist in the original DataFrame
        valid_columns = [col for col in required_columns if col in actual_columns]
        df_filtered = df[valid_columns]
        
        # Write the filtered DataFrame to a new CSV file
        df_filtered.to_csv('deluted_summary_iman.csv', index=False)
        print("Filtered CSV saved as 'deluted_summary_iman.csv'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def print_unique_second_column(df):
    # Get all values from both columns
    first_column_values = set(df.iloc[:, 0])
    second_column_values = set(df.iloc[:, 1])
    print(len(first_column_values))
    print(len(second_column_values))
    found = 0
    for sec_val in list(second_column_values):
        # print(f"checking if {sec_val} is in first col")
        for first_val in list(first_column_values):
            if str(sec_val).lower().strip() == str(first_val).lower().strip():
                found = 1
                break
        if not found:
            print(sec_val)
        found = 0

        # if val not in list(first_column_values):
        #     print(val, "IS NOT IN FIRST COL")
    
    # Find values in the second column that are not in the first column
    # unique_to_second = second_column_values - first_column_values
    
    # Print the results
    # print("Values in the second column that are not in the first column:")
    # for value in unique_to_second:
    #     print(value)

# Define a function to plot mean, standard deviation, and range for each feature
def plot_summary_statistics(stats, feature):
    mean = stats.loc['mean', feature]
    std = stats.loc['std', feature]
    min_val = stats.loc['min', feature]
    max_val = stats.loc['max', feature]

    plt.figure(figsize=(8, 6))
    plt.bar(['Mean', 'Standard Deviation'], [mean, std], color=['blue', 'orange'])
    plt.errorbar(['Mean'], [mean], yerr=[[mean - min_val], [max_val - mean]], fmt='o', color='black', label='Range (Min-Max)')
    plt.title(f'Summary Statistics for {feature}')
    plt.ylabel('Value')
    plt.grid(True, axis='y', linestyle='--', linewidth=0.7, alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    args = parser.parse_args()
    summary_data = pd.read_csv(r'/home/ilants/Documents/multi_image_single_set_params_run/Summary_Table.csv')

    # Selected parameters for analysis
    selected_columns = [
        'Nucleus_Area', 'Nucleus_Perimeter', 'Nucleus_Circularity', 
        'Nucleus_Eccentricity', 'Nucleus_HematoxylinODmean', 
        'Clustermean_Delaunay_Numneighbors', 'Clustermean_Delaunay_Meandistance', 
        'Clustermean_Delaunay_Mediandistance', 'Clustersize'
    ]

    # Calculate summary statistics
    summary_statistics = summary_data[selected_columns].describe()
    # Plot statistics for each selected feature
    for feature in selected_columns:
        plot_summary_statistics(summary_statistics, feature)
    # delut_manifest(args.manifest, args.outdir)
    # unpack_pickle(args.pickle)
    # split_manifest_by_svs(args.manifest, args.outdir)

    # check_and_save_csv_columns("/home/ilants/Documents/example_image_dir/outdir/Summary_Table.csv", get_first_row_from_csv("/home/ilants/Documents/summary_table_GUI.csv"))
    print_unique_second_column(pd.read_csv("/home/ilants/Documents/compare_summary.csv"))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-outdir", type=str, default="", help="Path to ouput directory")
    parser.add_argument("-manifest", type=str, default="", help="Path to manifest file")
    parser.add_argument("-pickle", type=str, default="", help="pickle path")

    main()