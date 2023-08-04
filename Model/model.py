from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plot
import seaborn as sns
import numpy as np
from sklearn.metrics import precision_score, recall_score, accuracy_score, roc_auc_score, roc_curve
from scipy.stats import probplot, norm
from scipy.stats import kstest
from sklearn.utils import shuffle
sns.set_style('darkgrid')
data = pd.read_csv('../Stocks_daily/BA.csv')
data.index = pd.to_datetime( data.index )
data.sort_index( inplace=True )
data['Next_Close'] = data['Close'].shift(-1) 
data['Buy'] = np.where( data['Next_Close'] > data['Close'], 1, 0 )
data = data.dropna()
data = data.sort_index( ascending=True )
input_vars = ['Open', 'High', 'Low', 'Close']
output_var = 'Buy'
X = data[ input_vars ]
y = data[ output_var ]
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split( X, y, data.index, shuffle=False, train_size=0.4 )
X_train, y_train = shuffle( X_train, y_train )
regr = LogisticRegression().fit( X_train, y_train )
y_hat = regr.predict( X )
data['Buy.estimate'] = y_hat
test_accuracy = accuracy_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
test_precision = precision_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
test_recall = recall_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
print( 'Test Accuracy:', test_accuracy )
print( 'Test Precision:', test_precision )
print( 'Test Recall:', test_recall )
# Plot residual statistics# predict probabilities
ns_probs = [0 for _ in range(len(y_test))]
lr_probs = regr.predict_proba(X_test)
# keep probabilities for the positive outcome only
lr_probs = lr_probs[:, 1]
# calculate scores
ns_auc = roc_auc_score(y_test, ns_probs)
lr_auc = roc_auc_score(y_test, lr_probs)
# summarize scores
print('No Skill: ROC AUC=%.3f' % (ns_auc))
print('Logistic: ROC AUC=%.3f' % (lr_auc))
# calculate roc curves
ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
# plot the roc curve for the model
plot.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
plot.plot(lr_fpr, lr_tpr, marker='.', label='Logistic')
# axis labels
plot.xlabel('False Positive Rate')
plot.ylabel('True Positive Rate')
# show the legend
plot.legend()
# show the plot
plot.show()