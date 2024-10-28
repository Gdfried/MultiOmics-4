import pandas as pd
import numpy as np
import os
import glob
import shutil

def avrege_phenotype_file(file_name, output_path):
    # Read the CSV file
    df = pd.read_csv(file_name)

    # Identify numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    # Make sure 'line' is not in numeric columns
    if 'line' in numeric_columns:
        numeric_columns.remove('line')

    # Group by 'line' and calculate the mean for numeric columns
    result = df.groupby('line')[numeric_columns].mean().reset_index()

    # Save the result to a new CSV file
    header_lines = []
    header_lines.append("# \n")
    header_lines.append(f"# nrow {len(result)}\n")
    header_lines.append(f"# ncol {len(result.columns)}\n")
    with open(output_path, 'w') as f:
        f.writelines(header_lines)
        result.to_csv(f, mode='a', index=False)

    

    print("Averaging complete. Results saved to 'averaged_data.csv'")
    return list(result["line"])


def exract_relevant_data(folder_path, output_folder, columns_to_keep):


    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Function to process a single file
    def process_file(file_path):
        file_name = os.path.basename(file_path)
        
        if file_name.startswith('chr') and file_name.endswith('_geno.csv'):
            # This is a chromosome genotype file that needs special processing
            try:
                with open(file_path, 'r') as f:
                    header_lines = [next(f) for _ in range(3)]
                col = header_lines[2].split()
                col[-1] = str(len(columns_to_keep)+1)
                header_lines[2] = " ".join(col) + "\n"
                # Read the CSV data starting from the 4th line
                df = pd.read_csv(file_path, header=0, skiprows=3, index_col=0)
                
                # Keep only specified columns and the index
                df = df[columns_to_keep]
                
                # Save the processed file
                output_path = os.path.join(output_folder, file_name)
                
                # Write the header lines and then the processed data
                with open(output_path, 'w') as f:
                    f.writelines(header_lines)
                    df.to_csv(f, mode='a')
                
                print(f"Processed and saved: {output_path}")
            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")
        else:
            # For other files, just copy them as is
            output_path = os.path.join(output_folder, file_name)
            shutil.copy2(file_path, output_path)
            print(f"Copied: {output_path}")

    # Process all files in the folder
    for file_path in glob.glob(os.path.join(folder_path, '*')):
        process_file(file_path)

    print("All files have been processed.")

lines = avrege_phenotype_file("mouse_run/Summary_Table.csv", "R_files/qtl_runs/mouse_from_image/pheno.csv")
exract_relevant_data("/Users/gdfri/Documents/Learning/Final_Project/R_files/new_files/", "R_files/qtl_runs/mouse_from_image/", lines)