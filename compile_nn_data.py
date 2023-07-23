import os
import pandas as pd
import csv

def compile_data(folder, output):
    files = [file for file in os.listdir(folder) if file.endswith('.csv')]
    # Check if there are any CSV files in the folder
    if not files:
        print("No CSV files found in the folder.")
        return 

    # Initialize an empty DataFrame to store the concatenated data
    concatenated_data = pd.DataFrame()

    # Loop through the CSV files and concatenate them horizontally
    i=1
    for file in files:
        file_path = os.path.join(folder, file)
        if i>1:
            data = pd.read_csv(file_path, usecols=lambda column: column != 'Dates')
        else:
            data = pd.read_csv(file_path)
        concatenated_data = pd.concat([concatenated_data, data], axis=1)
        i+=1

    # Write the concatenated data to the output file
    print(concatenated_data)
    concatenated_data.to_csv(output)
    print(f"Concatenated data saved to {output}.")

# Example usage:
compile_data('C:\Projects\moneybags\data\Industrials\Boeing', 'output.csv')
