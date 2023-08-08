import os
import requests
import numpy as np
import pandas as pd
import time
import csv

#%% Collect and concatenate daily data from a given folder
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
        data = pd.read_csv(file_path, index_col=0)

        #1. interval = int_start & int_stop
        #2. if time interval =/= daily:
        #3.     interpolate to the # trading days between int_start & int_stop

        concatenated_data = pd.concat([concatenated_data, data], axis=1)
        i+=1

    # Write the concatenated data to the output file
    concatenated_data = concatenated_data.dropna()
    concatenated_data.to_csv(output)
    print(f"Concatenated data saved to {output}.")

folder = os.getcwd() + '\data\Industrials\Boeing'
files = [file for file in os.listdir(folder) if file.endswith('.csv')]
print(files)
dataframes = [pd.read_csv(folder + '\\' + file) for file in files]
print(dataframes)
merged_data = dataframes
dataframes.to_csv('THIS_IS_A_TEST.csv',index = False)

