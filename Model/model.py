import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plot
from sklearn.metrics import precision_score, recall_score, accuracy_score, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from scipy.stats import probplot, norm
from sklearn.preprocessing import SplineTransformer
sns.set_style('darkgrid')
# Data Cleaning
data = pd.read_csv('../Stocks_daily/BA.csv', index_col=0)
data.index = pd.to_datetime( data.index, format='%Y-%m-%d' )
data.sort_index( inplace=True, ascending=True )
data['Close.next'] = data['Close'].shift(-3) 
data['Buy'] = np.where( data['Close.next'] > data['Close'], 1, 0 )
sentiment_data = pd.read_csv('../MarketSentiment/csvData/BA/BA.csv', index_col=0)
sentiment_data.index = pd.to_datetime( sentiment_data.index, format='%Y-%m-%d' )
data['Sentiment'] = sentiment_data['Total Sentiment']
data['Number of Articles'] = sentiment_data['Number of Articles']
fundamentals_data = pd.read_csv('../Fundamentals/csvData/BA.csv', index_col=0)
fundamentals_data.index = pd.to_datetime( fundamentals_data.index, format='%Y-%m-%d' )
fundamentals_data = fundamentals_data.resample('D').ffill()
data['Earnings'] = fundamentals_data['eps_diluted']
data['Book Value'] = fundamentals_data['bvps_diluted']
data['Earnings.exp'] = np.exp( data['Earnings'] )
data['Volume.inv'] = 1. / data['Volume']
data = data.dropna()
input_vars = ['Close', 'Sentiment', 'Number of Articles', 'Volume', 'Earnings', 'Book Value', 'Earnings.exp', 'Volume.inv']
output_var = 'Close.next'
# Training
X = data[ input_vars ]
y = data[ output_var ]
X = SplineTransformer(degree=3, knots='quantile').fit_transform(X)
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split( X, y, data.index, shuffle=False, train_size=0.3 )
regr = MLPRegressor( hidden_layer_sizes=[32, 32, 32, 1], activation='relu', solver='lbfgs', alpha=0.000005, max_iter=1000000000, max_fun=1000000, learning_rate='invscaling', learning_rate_init=1e-18 )
InputScaler = StandardScaler()
InputScaler.fit( X_train )
X_train = InputScaler.transform( X_train )
X_test = InputScaler.transform( X_test )
X = InputScaler.transform( X )
regr.fit(X_train, y_train)
y_hat = regr.predict( X )
y_hat = np.where( y_hat / data['Close'] > 1.2, data['Close'] * 1.2, y_hat )
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