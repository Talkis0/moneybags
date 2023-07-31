"""
import requests
import csv
import os
import yfinance as yf

def fundamentalData(ticker, API_KEY):
    symbol = yf.Ticker(f"{ticker}")
    info = symbol.info
    # url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'
    # r = requests.get(url)
    # data = r.json()
    return info

ticker = 'BA'
API_KEY = 'GOIR6JKN4TW5HNGO'
data = fundamentalData(ticker, API_KEY)
print(data)
"""
import requests
import pandas as pd

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = 'YOUR_API_KEY'
symbol = 'BA'  # Boeing stock symbol

# Define the function to fetch daily fundamental data
def get_fundamental_data(api_key, symbol):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'apikey': api_key,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'Time Series (Daily)' in data:
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df.index = pd.to_datetime(df.index)
        df.sort_index(ascending=True, inplace=True)
        return df
    else:
        print("Data retrieval failed. Check your API key and symbol.")
        return None

# Call the function to fetch the data
fundamental_data = get_fundamental_data(API_KEY, symbol)

# Filter data from November 1st, 2000
start_date = '2000-11-01'
fundamental_data = fundamental_data[fundamental_data.index >= start_date]

print(fundamental_data)


