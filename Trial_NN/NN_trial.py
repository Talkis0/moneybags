import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Load your data into pandas DataFrames (assuming you have them in CSV format)
# data = pd.read_csv('your_data.csv')

# Perform necessary data preprocessing (e.g., fill missing values, normalize the data)
# ...

# Normalize the data using MinMaxScaler
scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(data)

# Assuming you have already prepared your data into X (features) and y (target label)
# Split the data into training and testing sets
train_size = int(0.8 * len(data))
X_train, y_train = normalized_data[:train_size, :-1], normalized_data[:train_size, -1]
X_test, y_test = normalized_data[train_size:, :-1], normalized_data[train_size:, -1]

# Reshape the data to comply with TensorFlow's input requirements
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=1)

loss = model.evaluate(X_test, y_test, verbose=0)
print(f"Mean Squared Error on Test Data: {loss}")

# Assuming you have new data for prediction in X_new
# Reshape the data to comply with TensorFlow's input requirements
X_new = X_new.reshape((X_new.shape[0], X_new.shape[1], 1))

# Make predictions
predictions = model.predict(X_new)

# Inverse transform the predictions to get the actual stock price values
predictions = scaler.inverse_transform(predictions)
