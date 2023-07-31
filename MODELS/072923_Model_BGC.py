import csv
import os
import numpy as np
import pandas as pd
import csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

def combine_csv_files(directory_path):
    data_frames = {}  # Dictionary to store the dataframes with file names as keys
    # Get a list of all files in the specified directory
    # Filter out only the CSV files from the list
    csv_files = find_csv_files_recursive(directory_path)
    # Loop through each CSV file and read its content
    for csv_file in csv_files:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            # Skip the header if present (uncomment the next line if your CSV files have headers)
            next(reader, None)
            data = list(reader)
            # Check if data list is not empty before creating a DataFrame
            if data:
                # Get the root of the file name without the extension
                file_root = os.path.splitext(os.path.basename(csv_file))[0]
                # Create a DataFrame from the data
                df = pd.DataFrame(data, columns=None)  # If your CSV files have headers, set 'columns' to the header names
                # Convert the date column to datetime
                df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
                # Set the date column as the index
                df.set_index(df.columns[0], inplace=True)
                df.sort_index(inplace=True)
                # Store the DataFrame with the file name root as the key
                data_frames[file_root] = df
    # Sort the data_frames dictionary based on the maximum date across all DataFrames
    data_frames = dict(sorted(data_frames.items(), key=lambda item: item[1].index.max(), reverse=True))
    return data_frames


def cut_dataframes_to_min_date(data_frames):
    # Find the minimum date across all DataFrames
    min_date = max([df.index.min() for df in data_frames.values()])
    # Cut each DataFrame to start from the minimum date
    for df in data_frames.values():
        df.drop(df[df.index < min_date].index, inplace=True)

def find_csv_files_recursive(directory_path):
    csv_files = []
    # Walk through all directories and subdirectories starting from 'directory_path'
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files

def process_subdirectories(main_directory):
    # Step 1: Combine CSV files into DataFrames
    data_frames_dict = combine_csv_files(main_directory)
    # Step 2: Cut DataFrames to start from the minimum date and sort in descending order
    cut_dataframes_to_min_date(data_frames_dict)
    # Step 3: Resample and interpolate DataFrames
    resample_and_interpolate(data_frames_dict)
    # Step 2: Cut DataFrames to start from the minimum date and sort in descending order
    cut_dataframes_to_min_date(data_frames_dict)
    return data_frames_dict

def resample_and_interpolate(data_frames_dict):
    # Find the DataFrame with the most dates
    max_dates_df = max(data_frames_dict.values(), key=lambda df: len(df))
    # Resample all other DataFrames to have the same dates as max_dates_df
    for df_name, df in data_frames_dict.items():
        if df is not max_dates_df:
            # Convert all columns to numeric data types (excluding the index column)
            if df.index.name:
                numeric_columns = df.columns.drop(df.index.name)
            else:
                numeric_columns = df.columns
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
            # Perform interpolation on numeric columns
            df_resampled = df.reindex(max_dates_df.index).interpolate(method='time')
            # Drop rows with missing values
            df_resampled.dropna(inplace=True)
            # Set the date column as the index
            if df.index.name:
                df_resampled.set_index(df_resampled.columns[0], inplace=True)
            data_frames_dict[df_name] = df_resampled

# Example usage
main_directory = "C:/moneyBags-1"  # Replace this with the path to your main directory containing subdirectories with CSV files
data_frames_dict = process_subdirectories(main_directory)
# Write the DataFrame to a CSV file
combined_df.to_csv('C:/moneyBags-1/MODELS/modelData.csv')
                   

#######################################################################################################################################################################################
#
# THIS IS WHERE THE MODEL BEGINS
#
#######################################################################################################################################################################################
""" # Combine the data frames into a single data frame
combined_df = pd.concat(data_frames_dict.values())

# Check if 'Diff_Close' column exists before dropping it

# Extract features (X) and target variable (y)
X = combined_df.drop('Diff_Close', axis=1)  # Assuming 'Diff_Close' is the target variable
print(X)
y = combined_df['Diff_Close']
# Step 1: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Step 2: Model Selection and Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
# Step 3: Model Training and Evaluation (Linear Regression)
model_lr = LinearRegression()
model_lr.fit(X_train_scaled, y_train)
y_pred_lr = model_lr.predict(X_test_scaled)
mse_lr = mean_squared_error(y_test, y_pred_lr)
r_squared_lr = r2_score(y_test, y_pred_lr)
print("Linear Regression - Mean Squared Error:", mse_lr)
print("Linear Regression - R-squared:", r_squared_lr)
# Step 4: Feature Engineering - Polynomial Features
poly_features = PolynomialFeatures(degree=2)  # Try different degrees
X_train_poly = poly_features.fit_transform(X_train_scaled)
X_test_poly = poly_features.transform(X_test_scaled)
# Step 5: Model Training and Evaluation (Polynomial Regression)
model_poly = LinearRegression()
model_poly.fit(X_train_poly, y_train)
y_pred_poly = model_poly.predict(X_test_poly)
mse_poly = mean_squared_error(y_test, y_pred_poly)
r_squared_poly = r2_score(y_test, y_pred_poly)
print("Polynomial Regression - Mean Squared Error:", mse_poly)
print("Polynomial Regression - R-squared:", r_squared_poly)
# Step 6: Regularization (Ridge Regression)
""" """ model_ridge = Ridge(alpha=1.0)  # Try different alpha values
model_ridge.fit(X_train_scaled, y_train)
y_pred_ridge = model_ridge.predict(X_test_scaled)
mse_ridge = mean_squared_error(y_test, y_pred_ridge)
r_squared_ridge = r2_score(y_test, y_pred_ridge)
print("Ridge Regression - Mean Squared Error:", mse_ridge)
print("Ridge Regression - R-squared:", r_squared_ridge) """
# Step 7: Regularization (Lasso Regression)
""" model_lasso = Lasso(alpha=1.0)  # Try different alpha values
model_lasso.fit(X_train_scaled, y_train)
y_pred_lasso = model_lasso.predict(X_test_scaled)
mse_lasso = mean_squared_error(y_test, y_pred_lasso)
r_squared_lasso = r2_score(y_test, y_pred_lasso)
print("Lasso Regression - Mean Squared Error:", mse_lasso)
print("Lasso Regression - R-squared:", r_squared_lasso) """ 