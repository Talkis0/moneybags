from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plot
import seaborn as sns
sns.set_style('darkgrid')
data = pd.read_csv('../Stocks_daily/BA.csv')
data.index = pd.to_datetime( data.index )
data['Next_Close'] = data['Close'].shift(-1) 
data = data.dropna()
input_vars = ['Open', 'High', 'Low', 'Close']
output_var = 'Next_Close'
X = data[ input_vars ]
y = data[ output_var ]
X_train, X_test, y_train, y_test = train_test_split( X, y, train_size=0.8 )
regr = LinearRegression().fit( X_train, y_train )
y_hat = regr.predict( X )
plot.figure()
plot.plot( data.index, y, 'b-', label='True' )
plot.plot( data.index, y_hat, 'r-', label='Estimate' )
plot.ylabel( 'Closing Price (USD)' )
plot.xlabel( 'Time' )
plot.legend()
plot.tight_layout()
plot.show()