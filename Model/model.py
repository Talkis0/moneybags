import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plot
from sklearn.utils import shuffle
from sklearn.metrics import precision_score, recall_score, accuracy_score, roc_auc_score, roc_curve
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
sns.set_style('darkgrid')
# Data Cleaning
data = pd.read_csv('../Stocks_daily/BA.csv')
data.index = pd.to_datetime( data.index )
data.sort_index( inplace=True )
data['Next_Close'] = data['Close'].shift(-1) 
data['Buy'] = np.where( data['Next_Close'] > data['Close'], 1, 0 )
data = data.dropna()
input_vars = ['Open', 'High', 'Low', 'Close']
output_var = 'Next_Close'
# Training
X = data[ input_vars ]
y = data[ output_var ]
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split( X, y, data.index, train_size=0.7 )
X_train, y_train = shuffle(  X_train, y_train )
regr = LinearRegression().fit( X_train, y_train )
# Testing
y_hat = regr.predict( X )
data['Next_Close.estimate'] = y_hat
data['Buy.estimate'] = np.where( data['Next_Close.estimate'] > data['Close'], 1, 0 )
# Report Metrics
test_accuracy = accuracy_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
test_precision = precision_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
test_recall = recall_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
print( 'Test Accuracy:', test_accuracy )
print( 'Test Precision:', test_precision )
print( 'Test Recall:', test_recall )
# Plot residual statistics# predict probabilities
ns_probs = [0 for _ in range(len(y_test))]
lr_probs = np.where( data['Buy.estimate'].loc[idx_test] == 0, 0.49, 0.51 ) #regr.predict_proba(X_test)
# keep probabilities for the positive outcome only
#lr_probs = lr_probs[:, 1]
# calculate scores
ns_auc = roc_auc_score(data['Buy'].loc[idx_test], ns_probs)
lr_auc = roc_auc_score(data['Buy'].loc[idx_test], lr_probs)
# summarize scores
print('No Skill: ROC AUC=%.3f' % (ns_auc))
print('Linear: ROC AUC=%.3f' % (lr_auc))
# calculate roc curves
ns_fpr, ns_tpr, _ = roc_curve(data['Buy'].loc[idx_test], ns_probs)
lr_fpr, lr_tpr, _ = roc_curve(data['Buy'].loc[idx_test], lr_probs)
# plot the roc curve for the model
plot.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
plot.plot(lr_fpr, lr_tpr, marker='.', label='Linear')
# axis labels
plot.xlabel('False Positive Rate')
plot.ylabel('True Positive Rate')
# show the legend
plot.legend()
# show the plot
plot.show()