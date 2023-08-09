import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plot
from scipy.integrate import solve_ivp
sns.set_style('darkgrid')
# Data Cleaning
data = pd.read_csv('../Stocks_daily/BA.csv', index_col=0)
data.index = pd.to_datetime( data.index, format='%Y-%m-%d' )
data.sort_index( inplace=True, ascending=True )
data['Close.next'] = data['Close'].shift(-1) 
data['Buy'] = np.where( data['Close.next'] > data['Close'], 1, 0 )
data['Return'] = np.log( data['Close.next'] / data['Close'] )
data = data.dropna()
# GBM
# Python code for the plot

mu = data['Return'].mean()
n = data['Close'].shape[0]
dt = 1
x0 = data['Close'].iloc[0]
np.random.seed(1)

sigma = data['Return'].std()

x = np.exp(
    (mu - sigma ** 2 / 2) * dt
    + sigma * np.random.normal(0, np.sqrt(dt), size=(1, n)).T
)
x = np.vstack([np.ones(1), x])
x = x0 * x.cumprod(axis=0)

plot.subplot(2,1,1)
plot.plot(x)
plot.xlabel("$t$")
plot.ylabel("$x$")
plot.subplot(2,1,2)
plot.plot(data['Adjusted Close'])
plot.show()