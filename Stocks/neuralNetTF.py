import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn import preprocessing as pp
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, LSTM
from keras.models import Sequential
from datetime import datetime
# from_date = "2022-03-03 06:00:00"
# epoch = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S").timestamp()

folder = os.getcwd()
csvFile = folder + '\\Stocks_daily\\BA.csv'
# Step 1: Load the Data
data_df = pd.read_csv(csvFile)
# sentCSV = folder + '\\MarketSentiment\\csvData\BA\BA.csv'

# data_sent = pd.read_csv(sentCSV)
# data_df = data_df.iloc[:-9]
# print(len(data_sent))
# print(len(data_df))
# data_sent.set_index(data_sent.columns[0], inplace = True)
# data_df = pd.concat([data_df, data_sent], axis=1)
# data_df.dropna(inplace = True)

# data_df['netSent'] = data_sent['Total Sentiment']
# data_df['numArt'] = data_sent['Number of Articles']
# print(data_EMA.tail(5))
# newDataName = 'EMA'
# EMA = []
# for i in data_EMA:
    
#     # print(i)
#     epochTime.append(datetime.strptime(i, '%Y-%m-%d').timestamp())
# data_df[newDataName] = epochTime
# data_df.to_csv(csvFile)
# raise Exception('this is where the csv file should have been rewritten')
# print('\nepoch times: [length, the list]',len(epochTime),epochTime)
# data_df.set_index(data_df.columns[0], inplace=True)
# data_df.to_csv(csvFile)
# print(data_df.tail(5))
# print('\n==============\n')
data_df.index = pd.to_datetime( data_df.index, format='%Y-%m-%d' )
data_df.sort_index( inplace=True )
# data_df.to_csv('THISISATEST___.csv')
# print(data_df.tail(5))
# raise Exception('this is where the csv file should have been rewritten')
# print(data_df)
# Step 2: Split the Data into training and validation sets
X = data_df[['Open', 'High', 'Low', 'Close', 'Volume']]  # Input features (5 columns)
X_close_cur = X['Close']
y_1weekActual = data_df['Close'].shift(-7)
y_1_week = data_df['Close'].shift(-7)  # Closing price 1 week in advance (shifted 7 rows up)
y_2_weeks = data_df['Close'].shift(-14)  # Closing price 2 weeks in advance (shifted 14 rows up)
y_3_weeks = data_df['Close'].shift(-21)  # Closing price 3 weeks in advance (shifted 21 rows up) 21 NaN's starting in the first date so based on the first date of the 
y_2weekActual = y_2_weeks
y_3weekActual = y_3_weeks

# print(y_3_weeks)

startTrain_index = len(data_df)
endTrain_index = len(data_df) + 365*10


# Drop rows with NaN values in the target columns due to shifting
# X = X.dropna()
# print('length before changes\n',len(X),len(y_1_week),len(y_2_weeks),len(y_3_weeks))
X = X.iloc[:-21]
y_1_week = y_1_week.iloc[7:-14]
y_2_weeks = y_2_weeks.iloc[14:-7]
y_3_weeks = y_3_weeks.iloc[21:]
# y_1_week = y_1_week.dropna()
# y_2_weeks = y_2_weeks.dropna()
# y_3_weeks = y_3_weeks.dropna()
# print('lengths of X, y_1_week, y_2_week, y_3_week\n', len(X),len(y_1_week), len(y_2_weeks), len(y_3_weeks))
# print('lengths of X, y_1_week, y_2_week, y_3_week\n', X.index,y_1_week.index, y_2_weeks.index, y_3_weeks.index)
# Combine the target values into a single DataFrame
print(y_1_week.index)
print(y_2_weeks.index)
print(y_3_weeks.index)
print(X.index)
y = pd.DataFrame({'Close_1_Week': y_1_week.values, 'Close_2_Weeks': y_2_weeks.values, 'Close_3_Weeks': y_3_weeks.values}, index=None)
# print(X.tail(5))
# print(y.tail(5))
# raise Exception('this is where the csv file should have been rewritten')
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
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y_scaled, test_size=0.3, random_state=42, shuffle = False)
print('X_train type',type(X_train))
print('\nshape of X_train',X_train.shape)
length_ = len(y_val)

# Step 4: Create and Train the Model
X_train = X_train.reshape(X_train.shape[0],X_train.shape[1],1)
model = Sequential()
model.add(LSTM(128, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(64, activation='relu'))
model.add(Dense(3))  # Output layer for 3 target values (no activation function)

# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(128, activation='relu', input_shape=(5,)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(3)  # Output layer for 3 target values (no activation function)
# ])

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train.reshape(X_train.shape[0], X_train.shape[1], 1), y_train, 
          epochs=100, batch_size=32, validation_data=(X_val.reshape(X_val.shape[0], X_val.shape[1], 1), y_val))

# model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_val, y_val))
#model.fit(X_train, y_train, epochs=1, batch_size=32, validation_data=(X_val, y_val))

# Step 5: Predict using the Trained Model
y_pred_scaled = model.predict(X_val.reshape(X_val.shape[0], X_val.shape[1], 1))
# y_pred_scaled = model.predict(X_val)

# Step 6: Inverse Transform to Original Scale
y_pred = scaler.inverse_transform(y_pred_scaled)
y_val_actual = scaler.inverse_transform(y_val)
# y_pred = scaler.inverse_transform(y_pred_scaled)
# y_val_actual = scaler.inverse_transform(y_val)

# Step 7: Plot the Results
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, roc_curve
one_week_y_pred = y_pred[:, 0]
one_week_y_actual = y_1weekActual
print('ength of stuff\n',len(y_1weekActual), len(X_close_cur))
buy_actual = np.where( y_1weekActual.iloc[-length_:] > X_close_cur[-length_:], 1, 0 )
# print(one_week_y_actual)
# print(X_val[:,3])
buy_pred = np.where( one_week_y_pred > X_close_cur[-length_:], 1, 0)
test_accuracy = accuracy_score( buy_actual, buy_pred )
test_precision = precision_score( buy_actual, buy_pred )
test_recall = recall_score( buy_actual, buy_pred )
print( 'Test Accuracy:', test_accuracy )
print( 'Test Precision:', test_precision )
print( 'Test Recall:', test_recall )
# Plot residual statistics# predict probabilities
ns_probs = [0 for _ in range(len(buy_pred))]
lr_probs = np.where( buy_pred == 0, 0.49, 0.51 ) #regr.predict_proba(X_test)
# keep probabilities for the positive outcome only
#lr_probs = lr_probs[:, 1]
# calculate scores
ns_auc = roc_auc_score(buy_actual, ns_probs)
lr_auc = roc_auc_score(buy_actual, lr_probs)
# summarize scores
print('No Skill: ROC AUC=%.3f' % (ns_auc))
print('Linear: ROC AUC=%.3f' % (lr_auc))
# calculate roc curves
ns_fpr, ns_tpr, _ = roc_curve(buy_actual, ns_probs)
lr_fpr, lr_tpr, _ = roc_curve(buy_actual, lr_probs)
# plot the roc curve for the model
plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
plt.plot(lr_fpr, lr_tpr, marker='.', label='Linear')
# axis labels
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# show the legend
plt.legend()
# show the plot
plt.show()
print(np.average(np.square([y_val_actual-y_pred])))
for i in range(3):
    plt.figure(figsize=(10, 6))
    plt.subplot(2,1,1)
    plt.plot(X_close_cur[-length_:].index, y_val_actual[:, i], label=f'Actual {i+1}-Week')
    plt.plot(X_close_cur[-length_:].index, y_pred[:, i], label=f'Predicted {i+1}-Week')
    plt.xlabel('Time')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.title(f'Closing Price Prediction {i+1}-Weeks Ahead')
    plt.subplot(2,1,2)
    plt.plot( X_close_cur[-length_:].index, y_val_actual[:, i] - y_pred[:, i] )
    plt.show()
