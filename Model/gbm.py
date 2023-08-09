import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plot
from scipy.integrate import solve_ivp
from datetime import timedelta
from datetime import datetime

def running_mean(x, N):
    cumsum = np.cumsum(x) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def estimate_single_sigma(series, T):
    return np.sqrt( ( np.diff(series)**2 ).sum() / T )

def estimate_single_mu( series, T ):
    return (series[-1] - series[0]) / T

def estimate_sigma(series, T):
    window = 365
    series = series.to_numpy()
    T = T.to_numpy()
    SIGMA = np.sqrt( np.cumsum( np.diff(series, prepend=series[0])**2 ) / T )
    return np.asarray( list( np.cumsum(SIGMA[:window]) / np.arange(1, window+1, 1) ) + list( running_mean( SIGMA, window ) ) )
    #return np.sqrt( ( np.diff(series)**2 ).sum() / T )

def simple_estimate_mu(series, T):
    window = 365
    MU = np.asarray([ ( series[idx] - series[0] ) / t for idx, t in enumerate(T) ])
    return np.asarray( list( np.cumsum(MU[:window]) / np.arange(1, window+1, 1) ) + list( running_mean( MU, window ) ) )
    #return (series[-1] - series[0]) / T

sns.set_style('darkgrid')
# Data Cleaning
data = pd.read_csv('../Stocks_daily/BA.csv', index_col=0)
data.index = pd.to_datetime( data.index, format='%Y-%m-%d' )
data.sort_index( inplace=True, ascending=True )
vix_data = pd.read_csv('../Stocks_daily/VIX.csv', index_col=0)
vix_data.index = pd.to_datetime( vix_data.index, format='%Y-%m-%d' )
vix_data.sort_index( inplace=True, ascending=True )
data['dt'] = data.index.to_series().diff() / timedelta(days=1)
data['vix'] = vix_data['Close']
data['Close'] = data['Adjusted Close'].copy()
data['Close.next'] = data['Close'].shift(-1) 
data['Buy'] = np.where( data['Close.next'] > data['Close'], 1, 0 )
data['Return'] = np.log( data['Close.next'] / data['Close'] )
data = data.dropna()
data['T'] = data['dt'].cumsum()
# GBM
# Python code for the plot
data['Close.log'] = np.log( data['Close'] )
n = data['Close'].shape[0]
T = (data.index[-1] - data.index[0]) / timedelta(days=1)
mu = simple_estimate_mu( data['Close.log'], data['T'] )
x0 = data['Close'].iloc[0]
np.random.seed(1)
sigma = estimate_sigma( data['Close.log'], data['T'] )
W = np.random.normal( [0]*n, np.sqrt(data['dt']) )
drift = ( mu - sigma**2 / 2 ) * data['dt']
noise = sigma * W
log_dS = drift + noise
x = np.exp( log_dS )
x = x0 * x.cumprod(axis=0)

plot.subplot(3,2,1)
plot.plot(x)
plot.xlabel("$t$")
plot.ylabel("$x$")
plot.subplot(3,2,2)
plot.plot(data['Close'])
plot.subplot(3,2,3)
plot.plot( data['Close'] - x )
plot.subplot(3,2,4)
plot.hist( data['Close'] - x )
plot.subplot(3,2,5)
plot.scatter( x, data['Close'], s=0.5 )
plot.xlabel('Fitted')
plot.ylabel('True')
plot.subplot(3,2,6)
plot.plot( data.index, data['vix'] )
plot.show()