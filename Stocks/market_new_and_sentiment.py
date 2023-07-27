import requests
import pandas as pd

 # Define your Alpha Vantage API key
api_key = 'GOIR6JKN4TW5HNGO'

# Define the stock symbol and function to retrieve data
symbol = 'BA'  # Boeing stock symbol
function = 'NEWS_SENTIMENT'  # Adjust the function based on your desired data
ticker = 'BA'

# Make a request to the Alpha Vantage API
url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
r = requests.get(url)
data = r.json()
interval = 'daily'
time_period = [200,100,50,10]

# Convert the retrieved JSON data into a pandas DataFrame
time_series = data['Time Series (Daily)']
df = pd.DataFrame(time_series).T
df = df.astype(float)

# Print the DataFrame
print(df)   
    

