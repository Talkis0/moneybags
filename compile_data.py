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
    for file in files:
        file_path = os.path.join(folder, file)
        data = pd.read_csv(file_path, index_col=0)
        concatenated_data = pd.concat([concatenated_data, data], axis=1)

    # Write the concatenated data to the output file
    concatenated_data = concatenated_data.dropna(axis = 0)
    print(concatenated_data)
    with open(output, 'w') as file:
        concatenated_data.to_csv(file, index = True)
        print(f"Concatenated data writen over and saved to {output}.")

#%% Interpolation function
def resample_and_interpolate(folder):
    files = [file for file in os.listdir(folder) if file.endswith('.csv')]
    if not files:
        print("No CSV files found in the folder.")
        return 
    df_dict = {}
    for file in files:
        file_path = os.path.join(folder, file)
        df_dict[file] = pd.read_csv(file_path, index_col=0)
        df_dict[file].index = pd.to_datetime(df_dict[file].index)
        mask = df_dict[file].apply(lambda row: all(value == '.' for value in row.values), axis=1)
        df_dict[file] = df_dict[file][~mask]

    # Find the DataFrame with the most dates
    max_dates_df = max(df_dict.values(), key=lambda df: len(df))
    # Resample all other DataFrames to have the same dates as max_dates_df
    for df_name, df in df_dict.items():
        if df is not max_dates_df:
            # Convert all columns to numeric data types (excluding the index column)
            for k in df.columns:
                if not (df.index.name == k):
                    df[k] = df[k].astype(float)
            
            # Perform interpolation on numeric columns
            df_resampled = df.reindex(max_dates_df.index).interpolate(method='time')
            # Drop rows with missing values
            # df_resampled.dropna(inplace=True, axis = 0)
            df_dict[df_name] = df_resampled

    for df_name, df in df_dict.items():
        output_file_path = f"{folder}/{df_name}"
        df.to_csv(output_file_path)    

#%% This will gather all data such that it is perfectly up to date and consistent in formatting
if __name__ == "__main__":
    # Example code for Boeing
    ticker = 'BA'
    dirname = os.path.dirname(__file__)
    folder = dirname + '\data\Industrials\Boeing'

    print(dirname)
    print(folder)

    # resample_and_interpolate('MacroEcon')
    # compile_data('MacroEcon', 'C:\Projects\moneybags\data\Industrials\Boeing\MacroEcon_all.csv')
    compile_data(folder, 'C:\Projects\moneybags\data\Industrials\Boeing\BA_all.csv')
