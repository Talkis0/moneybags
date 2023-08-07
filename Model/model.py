import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plot
from sklearn.metrics import precision_score, recall_score, accuracy_score, roc_auc_score, roc_curve
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
sns.set_style('darkgrid')
# Data Cleaning
data = pd.read_csv('../Stocks_daily/BA.csv', index_col=0)
data.index = pd.to_datetime( data.index, format='%Y-%m-%d' )
data.sort_index( inplace=True, ascending=True )
data['Close.lag1'] = data['Close'].shift(1)
data['Close.lag2'] = data['Close'].shift(2)
data['Close.lag4'] = data['Close'].shift(4)
data['Close.lag6'] = data['Close'].shift(6)
data['Close.lag8'] = data['Close'].shift(8)
data['Close.next'] = data['Close'].shift(-1) 
data['Buy'] = np.where( data['Close.next'] > data['Close'], 1, 0 )
sentiment_data = pd.read_csv('../MarketSentiment/csvData/BA/BA.csv', index_col=0)
sentiment_data.index = pd.to_datetime( sentiment_data.index, format='%Y-%m-%d' )
data['Sentiment'] = sentiment_data['Total Sentiment']
data['Number of Articles'] = sentiment_data['Number of Articles']
data = data.dropna()
input_vars = ['Close', 'Close.lag1', 'Close.lag2', 'Close.lag4', 'Close.lag8', 'Sentiment', 'Number of Articles']
output_var = 'Buy'
# Training
X = data[ input_vars ]
y = data[ output_var ]
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split( X, y, data.index, shuffle=False, train_size=0.7 )
regr = LogisticRegressionCV(cv=5, tol=1e-5, max_iter=100000, class_weight='balanced').fit(X_train, y_train)
# Testing
y_hat = regr.predict( X )
data['Buy.estimate'] = y_hat
# Report Metrics
print('UNIQUE PREDICTED:', data['Buy.estimate'].loc[idx_test].unique())
print('UNIQUE ACTUAL:', y.unique())
test_accuracy = accuracy_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
test_precision = precision_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
test_recall = recall_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
print( 'Test Accuracy:', test_accuracy )
print( 'Test Precision:', test_precision )
print( 'Test Recall:', test_recall )
# Plot residual statistics# predict probabilities
lr_probs = regr.predict_proba(X_test)
# keep probabilities for the positive outcome only
lr_probs = lr_probs[:, 1]
# calculate scores
lr_auc = roc_auc_score(data['Buy'].loc[idx_test], lr_probs)
# summarize scores
print('Linear: ROC AUC=%.3f' % (lr_auc))
# calculate roc curves
lr_fpr, lr_tpr, _ = roc_curve(data['Buy'].loc[idx_test], lr_probs)
# plot the roc curve for the model
plot.plot(lr_fpr, lr_tpr, marker='.', label='Linear')
# axis labels
plot.xlabel('False Positive Rate')
plot.ylabel('True Positive Rate')
# show the legend
plot.legend()
# show the plot
plot.show()