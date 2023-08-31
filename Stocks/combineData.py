import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
# from sklearn import preprocessing as pp
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, LSTM
from keras.models import Sequential, model_from_json

frames = []

folder = os.getcwd()
print('==========================',folder)

for _,_,files in os.walk(folder + '\\data\\Industrials\\Boeing'):
    for file in files:
        print(file)
        # print(dataPath + '\\' + file)
        data = folder + '\\data\\Industrials\\Boeing' + '\\' + file
        data = pd.read_csv(data)
        if file != 'BA.csv' and 'Fundamental' not in file:
            data = data.set_index('Dates')
        if 'Fundamental' in file:
            data = data.rename(columns = {'Unnamed: 0': 'Dates'})
            data = data.set_index('Dates')
        data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
        data = data.resample('D').ffill()
        data.sort_index(inplace = True)
        data.columns.values[0] = file
        # data.rename(columns={"Values": file}, inplace=True)
        frames.append(data)


# frames = [data_df, sentData, rsi10, sma10]
data_df = pd.concat(frames,axis =1)
data_df = data_df.dropna()
data_df.sort_index(inplace=True)

# Get a list of all variable names in the current scope
all_variable_names = dir()

# Remove all variables except the one you want to keep
# for var_name in all_variable_names:
#     if var_name != 'data_df':
#         del globals()[var_name]

data_df = data_df.replace('.', 0)

column_names = list(data_df.columns.values)

X = data_df[column_names]
X = X.iloc[:-21]
# y_3_days = data_df['Close'].iloc[3:-18]
y_1_week = data_df['Close'].iloc[7:-14]
y_2_weeks = data_df['Close'].iloc[14:-7]
y_3_weeks = data_df['Close'].iloc[21:]

y = pd.DataFrame({'Close_1_Week': y_1_week.values, 'Close_2_Weeks': y_2_weeks.values, 'Close_3_Weeks': y_3_weeks.values}, index=None)

X, X_test, y, y_test = train_test_split(X, y, test_size=0.1, random_state=42, shuffle = False)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42, shuffle = False)

scaler = MinMaxScaler()
X_trainScaled = scaler.fit_transform(X_train)
X_valScaled = scaler.fit_transform(X_val)
y_trainScaled = scaler.fit_transform(y_train)
y_valScaled = scaler.fit_transform(y_val)

X_trainScaled = X_trainScaled.reshape(X_trainScaled.shape[0],X_trainScaled.shape[1],1)
model = Sequential()
model.add(LSTM(128, activation='relu', input_shape=(X_trainScaled.shape[1], X_trainScaled.shape[2])))
model.add(Dense(64, activation='relu'))
model.add(Dense(3))

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_trainScaled, y_trainScaled, 
          epochs=3, batch_size=32, validation_data=(X_valScaled.reshape(X_valScaled.shape[0], X_valScaled.shape[1], 1), y_valScaled))

# Step 1: Get predicted probabilities
predicted_probabilities = model.predict(X_test)

# Step 2: Convert probabilities into class predictions
predicted_classes = np.argmax(predicted_probabilities, axis=1)

# Step 3: Compare with true labels
accuracy = np.mean(predicted_classes == np.argmax(y_test, axis=1))

print('\nhello this will save the model in the next line\n')
model.save(folder + '\\models\\tristan0.keras')
# model_json  =model.to_json()
# with open("model.json","w") as json_file:
#     json_file.write(model_json)

# model.save_weights("model.h5")

y_pred_scaled = model.predict(X_valScaled.reshape(X_valScaled.shape[0], X_valScaled.shape[1], 1))
y_pred = scaler.inverse_transform(y_pred_scaled)
y_val1 = y_val['Close_1_Week'].tolist()
X_close = X_val['Close'].tolist()
buyReal=False
buyReal_dic={'buy':[],'sell':[]}
buyTrain = False
buyTrain_dic = {'buy':[],'sell':[]}
for i in range(0,len(X_close)):
    # print(y_1_week_train_actual[i],X_close_actual[i])
    if y_val1[i] > X_close[i]:
        if buyReal == True:
            pass
        else:
            buyReal = True
            buyReal_dic['buy'].append(X_close[i])
    if y_val1[i] < X_close[i]:
        if buyReal == False:
            pass
        else:
            buyReal = False
            buyReal_dic['sell'].append(X_close[i])


    if y_pred[i,0] > X_close[i]:
        if buyTrain == True:
            pass
        else:
            buyTrain = True
            buyTrain_dic['buy'].append(X_close[i])
    if y_pred[i,0] < X_close[i]:
        if buyTrain == False:
            pass
        else:
            buyTrain = False
            buyTrain_dic['sell'].append(X_close[i])

print(len(buyTrain_dic['sell']),len(buyTrain_dic['buy']))
trainGain = 100
realGainPotential = 100
for i in range(0,len(buyTrain_dic['sell'])):
    trainGain = (1+(buyTrain_dic['buy'][i]-buyTrain_dic['sell'][i])/buyTrain_dic['buy'][i])*trainGain
    realGainPotential = (1+(buyReal_dic['buy'][i]-buyReal_dic['sell'][i])/buyReal_dic['buy'][i])*realGainPotential

print(trainGain)
print(realGainPotential)

