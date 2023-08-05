import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn import preprocessing as pp
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

folder = os.getcwd()
csvFile = folder + '\\Stocks_daily\\BA.csv'
# Step 1: Load the Data
data_df = pd.read_csv(csvFile)
# print(data_df)
# Step 2: Split the Data into training and validation sets
X = data_df[['Open', 'High', 'Low', 'Close', 'Volume']]  # Input features (5 columns)
y_1_week = data_df['Close'].shift(-7)  # Closing price 1 week in advance (shifted 7 rows up)
y_2_weeks = data_df['Close'].shift(-14)  # Closing price 2 weeks in advance (shifted 14 rows up)
y_3_weeks = data_df['Close'].shift(-21)  # Closing price 3 weeks in advance (shifted 21 rows up) 21 NaN's starting in the first date so based on the first date of the 
# print(y_3_weeks)

startTrain_index = len(data_df)
endTrain_index = len(data_df) + 365*10


# Drop rows with NaN values in the target columns due to shifting
# X = X.dropna()
print('length before changes\n',len(X),len(y_1_week),len(y_2_weeks),len(y_3_weeks))
X = X.iloc[21:]
y_1_week = y_1_week.iloc[14:-7]
y_2_weeks = y_2_weeks.iloc[7:-14]
y_3_weeks = y_3_weeks.iloc[:-21]
# y_1_week = y_1_week.dropna()
# y_2_weeks = y_2_weeks.dropna()
# y_3_weeks = y_3_weeks.dropna()
print('lengths of X, y_1_week, y_2_week, y_3_week\n', len(X),len(y_1_week), len(y_2_weeks), len(y_3_weeks))
print('lengths of X, y_1_week, y_2_week, y_3_week\n', X.index,y_1_week.index, y_2_weeks.index, y_3_weeks.index)
# Combine the target values into a single DataFrame
y = pd.DataFrame({'Close_1_Week': y_1_week.values, 'Close_2_Weeks': y_2_weeks.values, 'Close_3_Weeks': y_3_weeks.values}, index=None)

# Step 3: Normalize Data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
y_scaled = scaler.fit_transform(y)
print('length of X_scaled and y_scaled\n', len(X_scaled), len(y_scaled))
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(y_2_weeks)
#     print(len(y_scaled),len(X_scaled))
    # print(y_scaled)
# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y_scaled, test_size=0.4, random_state=42, shuffle = False)

# Step 4: Create and Train the Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(5,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(3)  # Output layer for 3 target values (no activation function)
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_val, y_val))

# Step 5: Predict using the Trained Model
y_pred_scaled = model.predict(X_val)

# Step 6: Inverse Transform to Original Scale
y_pred = scaler.inverse_transform(y_pred_scaled)
y_val_actual = scaler.inverse_transform(y_val)

# Step 7: Plot the Results
print(np.average(np.square([y_val_actual-y_pred])))
for i in range(3):
    plt.figure(figsize=(10, 6))
    plt.plot(y_val_actual[:, i], label=f'Actual {i+1}-Week')
    plt.plot(y_pred[:, i], label=f'Predicted {i+1}-Week')
    plt.xlabel('Time')
    plt.ylabel('Closing Price')
    plt.title(f'Closing Price Prediction {i+1}-Weeks Ahead')
    plt.legend()
    plt.show()
