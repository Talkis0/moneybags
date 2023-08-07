import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plot
from sklearn.metrics import precision_score, recall_score, accuracy_score, roc_auc_score, roc_curve
from sklearn.linear_model import LogisticRegressionCV, LinearRegression
from sklearn.model_selection import train_test_split
from scipy.stats import probplot, norm
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
input_vars = ['Close', 'Sentiment', 'Number of Articles', 'Volume']
output_var = 'Close.next'
# Training
X = data[ input_vars ]
y = data[ output_var ]
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split( X, y, data.index, shuffle=False, train_size=0.7 )
regr = LinearRegression()
regr.fit(X_train, y_train)
y_hat = regr.predict( X )
data['Buy.estimate'] = np.where( y_hat > data['Close'], 1, 0 )
print( accuracy_score( data['Buy'], data['Buy.estimate'] ) )
print( precision_score( data['Buy'], data['Buy.estimate'] ) )
print( recall_score( data['Buy'], data['Buy.estimate'] ) )
residual = data['Close'] - y_hat
plot.figure()
plot.suptitle('$E[\epsilon] = {:.3f}; Var[\epsilon] = {:.3f}$'.format( np.mean(residual), np.var(residual) ))
plot.subplot(3,2,1)
plot.plot( data.index, data['Close'] )
plot.plot( data.index, y_hat )
plot.ylabel('Closing Price')
plot.subplot(3,2,2)
plot.plot( data.index, data['Close'] - y_hat )
plot.ylabel('Residual')
plot.subplot(3,2,3)
t = np.linspace( residual.min(), residual.max(), 1000 )
plot.hist( residual, density=True )
plot.plot( t, norm.pdf( t, loc=residual.mean(), scale=residual.std() ), 'r-' )
plot.ylabel('$P(\epsilon)$')
plot.subplot(3,2,4)
plot.scatter( y_hat, residual, s=0.5 )
plot.ylabel('Residual')
plot.xlabel('Fitted')
plot.subplot(3,2,5)
probplot( (residual - np.mean(residual)) / np.std(residual), plot=plot )
plot.subplot(3,2,6)
plot.scatter( y, y_hat, s=0.5 )
plot.ylabel( 'Fitted' )
plot.xlabel( 'True' )
plot.tight_layout()
plot.show()
for var in input_vars:
    plot.figure()
    plot.scatter( data[var], residual )
    plot.ylabel('Residual')
    plot.xlabel(var)
    plot.savefig(var+'.png')