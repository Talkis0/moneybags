import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

model = tf.keras.Sequential([tf.keras.layers.dense(1, input_shape = (128,))])

model.compile(optimizer='adam', loss = 'mse', metrics=['accuracy'])

model.fit(X, y, epochs=100, batch_size=32)



# Step 1: Load the Data
data_df = pd.read_csv("stock_data.csv")

# Step 2: Split the Data into training and validation sets
X = data_df[['Open', 'High', 'Low', 'Close', 'Volume']]  # Input features (5 columns)
y_1_week = data_df['Close'].shift(-7)  # Closing price 1 week in advance (shifted 7 rows up)
y_2_weeks = data_df['Close'].shift(-14)  # Closing price 2 weeks in advance (shifted 14 rows up)
y_3_weeks = data_df['Close'].shift(-21)  # Closing price 3 weeks in advance (shifted 21 rows up)

# Drop rows with NaN values in the target columns due to shifting
X = X.dropna()
y_1_week = y_1_week.dropna()
y_2_weeks = y_2_weeks.dropna()
y_3_weeks = y_3_weeks.dropna()

# Combine the target values into a single DataFrame
y = pd.DataFrame({'Close_1_Week': y_1_week, 'Close_2_Weeks': y_2_weeks, 'Close_3_Weeks': y_3_weeks})

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.4, random_state=42)

# Step 3: Convert Data to NumPy Arrays
X_train = X_train.values
y_train = y_train.values
X_val = X_val.values
y_val = y_val.values

# Step 4: Create and Train the Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(5,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(3)  # Output layer for 3 target values (no activation function)
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_val, y_val))


