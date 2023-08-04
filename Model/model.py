from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plot
import seaborn as sns
import numpy as np
from sklearn.metrics import precision_score, recall_score, accuracy_score
from scipy.stats import probplot, norm
from scipy.stats import kstest
from sklearn.utils import shuffle
sns.set_style('darkgrid')
data = pd.read_csv('../Stocks_daily/BA.csv')
data.index = pd.to_datetime( data.index )
data['Next_Close'] = data['Close'].shift(1) 
data['Buy'] = np.where( data['Next_Close'] > data['Close'], 1, 0 )
data = data.dropna()
data = data.sort_index( ascending=True )
input_vars = ['Open', 'High', 'Low', 'Close']
output_var = 'Next_Close'
X = data[ input_vars ]
y = data[ output_var ]
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split( X, y, data.index, shuffle=False, train_size=0.2 )
X_train, y_train = shuffle( X_train, y_train )
regr = LinearRegression().fit( X_train, y_train )
y_hat = regr.predict( X )
data['Next_Close.estimate'] = y_hat
data['Buy.estimate'] = np.where( data['Next_Close.estimate'] > data['Close'], 1, 0 )
test_accuracy = accuracy_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
test_precision = precision_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
test_recall = recall_score( data['Buy'].loc[idx_test], data['Buy.estimate'].loc[idx_test] )
print( 'Test Accuracy:', test_accuracy )
print( 'Test Precision:', test_precision )
print( 'Test Recall:', test_recall )
print( 'R2:', regr.score( X, y ) )
residual = y - y_hat
residual_mean = np.mean(residual)
residual_std = np.std(residual)
print( 'KSTest:', kstest( ( residual - residual_mean ) / residual_std, norm.cdf, N=10000, method='exact' ) )
# Plot residual statistics
plot.figure( figsize=(10,8) )
plot.subplot(3, 2, 1)
plot.hist(residual, color='blue', density=True)
t = np.linspace( residual_mean - 5.*residual_std, residual_mean + 5.*residual_std )
plot.plot( t, norm.pdf(t, residual_mean, residual_std), 'r-', label='Normal PDF' )
plot.ylabel('$P(\epsilon)$')
plot.xlabel('$\epsilon = \hat{{y}} - y$')
plot.title( 'Residual Distribution' )
plot.legend()
plot.subplot(3, 2, 2)
plot.plot( y_hat, np.zeros( (y_hat.shape[0],) ), 'r-', label='$\epsilon = 0$' )
plot.scatter( y_hat, residual, c='b' )
plot.xlabel('$\hat{{y}}$')
plot.ylabel('$\epsilon = \hat{{y}} - y$')
plot.title( 'Residual vs. Predicted' )
plot.legend()
plot.subplot(3, 2, 3)
probplot( ( residual - residual_mean ) / residual_std, dist='norm', plot=plot)
plot.title('Q-Q Plot (against Normal Distribution)')
plot.subplot(3, 2, 4)
plot.scatter( y_hat, y, c='b' )
plot.plot(sorted( y ), sorted( y ), 'r-', label='$y = \hat{{y}}$')
plot.xlabel('$\hat{{y}}$')
plot.ylabel('$y$')
plot.title( 'True vs. Predicted' )
plot.legend()
plot.subplot(3, 2, 5)
plot.plot( data.index, y, 'r-', label='True' )
plot.plot( data.index, y_hat, 'b-', label='Estimate' )
plot.suptitle('E$[\epsilon] = ${:.5f}; Var$[\epsilon] = ${:.5f};'.format( residual_mean, residual_std**2. ))
plot.tight_layout()
plot.show()