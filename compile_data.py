import os
import requests
import numpy as np
import pandas as pd
import time
import csv

#%% Collect and concatenate daily data from a given folder
def compile_data(folder, output):
    files = [file for file in os.listdir(folder) if file.endswith('.csv')]
    # Check if there are any CSV files in the folder
    if not files:
        print("No CSV files found in the folder.")
        return 

    # Initialize an empty DataFrame to store the concatenated data
    concatenated_data = pd.DataFrame()

    # Loop through the CSV files and concatenate them horizontally
    i=1
    for file in files:
        file_path = os.path.join(folder, file)
        data = pd.read_csv(file_path, index_col=0)

        #1. interval = int_start & int_stop
        #2. if time interval =/= daily:
        #3.     interpolate to the # trading days between int_start & int_stop

        concatenated_data = pd.concat([concatenated_data, data], axis=1)
        i+=1

    # Write the concatenated data to the output file
    concatenated_data = concatenated_data.dropna()
    concatenated_data.to_csv(output)
    print(f"Concatenated data saved to {output}.")

#%% Query ETF price data
def etf_query(folder, *symbols):
    query_limit = 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 100 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'
    dirname = os.path.dirname(__file__)
    if len(symbols) == 0:
        symbols = ['BIL', 'ACWV', 'BNDW', 'FREL', 'GLDM', 'GLOF', 'PDBC', 'RSP', 'SCHP', 'VT']

    KEY = pd.read_csv('keys.csv', header=None).to_numpy().ravel()
    print(KEY.shape[0])
    idx = 0
    n_keys = KEY.shape[0]
    API_KEY = KEY[idx]
    
    for symbol in symbols:
        print(API_KEY)
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        # Extract the time series data
        if 'Note' in data:
            print(data['Note'])
            if data['Note'] == query_limit:
                # incomplete
                idx = (idx+1)%n_keys
                API_KEY = KEY[idx]
                print(API_KEY)
                url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'
                response = requests.get(url)
                data = response.json()
                if 'Note' not in data:
                    print('Good thing Alphavantage is my bitch')

        time_series = data['Time Series (Daily)']

        # Prepare CSV file for writing
        filename = folder + f'\{symbol}.csv'
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([symbol])

            # Write each data point to CSV
            for timestamp, values in time_series.items():
                row = [timestamp, values['4. close']]
                writer.writerow(row)
    

#%% Query Stock data
def stock_price_data(symbol, destination):
    query_limit = 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 100 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'
    dirname = os.path.dirname(__file__)
    filename = destination + f'\{symbol}.csv'
    API_KEY = 'GOIR6JKN4TW5HNGO'

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data['Note'] == query_limit:
            # incomplete
            API_KEY = API_KEY
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'
            response = requests.get(url)
            data = response.json()

    # Extract the time series data
    time_series = data['Time Series (Daily)']

    # Prepare CSV file for writing
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Open', 'High', 'Low', 'Close', 'Volume'])

        # Write each data point to CSV
        for timestamp, values in time_series.items():
            row = [timestamp, values['1. open'], values['2. high'], values['3. low'], values['4. close'], values['5. volume']]
            writer.writerow(row)

#%% Query all indicators for a given stock
def stock_indicators(ticker, folder):
    query_limit = 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 100 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'
    time_interval = 'daily'
    series_type = 'close'
    API_KEY = 'GOIR6JKN4TW5HNGO'
    # gotta figure out iterating between time_periods
    time_period = 10

    KEY = pd.read_csv('keys.csv', header=None).to_numpy().ravel()
    print(KEY.shape[0])
    idx = 0
    n_keys = KEY.shape[0]
    API_KEY = KEY[idx]

    technical_indicators = {
    'SMA': f'https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'EMA': f'https://www.alphavantage.co/query?function=EMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'WMA': f'https://www.alphavantage.co/query?function=WMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'DEMA': f'https://www.alphavantage.co/query?function=DEMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'TEMA': f'https://www.alphavantage.co/query?function=TEMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'TRIMA': f'https://www.alphavantage.co/query?function=TRIMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'KAMA': f'https://www.alphavantage.co/query?function=KAMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'MAMA': f'https://www.alphavantage.co/query?function=MAMA&symbol={ticker}&interval={time_interval}&series_type={series_type}&fastlimit=.01&apikey={API_KEY}',
    'T3': f'https://www.alphavantage.co/query?function=T3&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'MACDEXT': f'https://www.alphavantage.co/query?function=MACDEXT&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={API_KEY}',
    'RSI': f'https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'MOM': f'https://www.alphavantage.co/query?function=MOM&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'STOCH': f'https://www.alphavantage.co/query?function=STOCH&symbol={ticker}&interval={time_interval}&apikey={API_KEY}',
    'STOCHF': f'https://www.alphavantage.co/query?function=STOCHF&symbol={ticker}&interval={time_interval}&apikey={API_KEY}',
    'STOCHRSI': f'https://www.alphavantage.co/query?function=STOCHRSI&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&fastkperiod=5&fastdmatype=0&apikey={API_KEY}',
    'WILLR': f'https://www.alphavantage.co/query?function=WILLR&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'ADX': f'https://www.alphavantage.co/query?function=ADX&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'ADXR': f'https://www.alphavantage.co/query?function=ADXR&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'APO': f'https://www.alphavantage.co/query?function=APO&symbol={ticker}&interval={time_interval}&series_type={series_type}&fastperiod=12&matype=1&apikey={API_KEY}',
    'PPO': f'https://www.alphavantage.co/query?function=PPO&symbol={ticker}&interval={time_interval}&series_type={series_type}&fastperiod=12&matype=1&apikey={API_KEY}',
    'CCI': f'https://www.alphavantage.co/query?function=CCI&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'ROCR': f'https://www.alphavantage.co/query?function=ROCR&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'AROON': f'https://www.alphavantage.co/query?function=AROON&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'AROONOSC': f'https://www.alphavantage.co/query?function=AROONOSC&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'DX': f'https://www.alphavantage.co/query?function=DX&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'MINUS_DI': f'https://www.alphavantage.co/query?function=MINUS_DI&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'PLUS_DI': f'https://www.alphavantage.co/query?function=PLUS_DI&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'MINUS_DM': f'https://www.alphavantage.co/query?function=MINUS_DM&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'PLUS_DM': f'https://www.alphavantage.co/query?function=PLUS_DM&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'BBANDS': f'https://www.alphavantage.co/query?function=BBANDS&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&nbdevup=2&nbdevdn=2&apikey={API_KEY}',
    'MIDPRICE': f'https://www.alphavantage.co/query?function=MIDPRICE&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'SAR': f'https://www.alphavantage.co/query?function=SAR&symbol={ticker}&interval={time_interval}&acceleration=.01&maximum=.2&apikey={API_KEY}',
    'AD': f'https://www.alphavantage.co/query?function=AD&symbol={ticker}&interval={time_interval}&apikey={API_KEY}',
    'OBV': f'https://www.alphavantage.co/query?function=OBV&symbol={ticker}&interval={time_interval}&apikey={API_KEY}',
    'ATR': f'https://www.alphavantage.co/query?function=ATR&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'NATR': f'https://www.alphavantage.co/query?function=NATR&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'TRANGE': f'https://www.alphavantage.co/query?function=TRANGE&symbol={ticker}&interval={time_interval}&apikey={API_KEY}',
    'ROC': f'https://www.alphavantage.co/query?function=ROC&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'MFI': f'https://www.alphavantage.co/query?function=MFI&symbol={ticker}&interval={time_interval}&time_period={time_period}&apikey={API_KEY}',
    'TRIX': f'https://www.alphavantage.co/query?function=TRIX&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'ULTOSC': f'https://www.alphavantage.co/query?function=ULTOSC&symbol={ticker}&interval={time_interval}&timeperiod1=8&apikey={API_KEY}',
    'CMO': f'https://www.alphavantage.co/query?function=CMO&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'ADOSC': f'https://www.alphavantage.co/query?function=ADOSC&symbol={ticker}&interval={time_interval}&fastperiod=3&apikey={API_KEY}',
    'BOP': f'https://www.alphavantage.co/query?function=BOP&symbol={ticker}&interval={time_interval}&apikey={API_KEY}',
    'MIDPOINT': f'https://www.alphavantage.co/query?function=MIDPOINT&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'HT_TRENDLINE': f'https://www.alphavantage.co/query?function=HT_TRENDLINE&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={API_KEY}',
    'HT_SINE': f'https://www.alphavantage.co/query?function=HT_SINE&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={API_KEY}',
    'HT_TRENDMODE': f'https://www.alphavantage.co/query?function=HT_TRENDMODE&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={API_KEY}',
    'HT_DCPERIOD': f'https://www.alphavantage.co/query?function=HT_DCPERIOD&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={API_KEY}',
    'HT_DCPHASE': f'https://www.alphavantage.co/query?function=HT_DCPHASE&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={API_KEY}',
    'HT_PHASOR': f'https://www.alphavantage.co/query?function=HT_PHASOR&symbol={ticker}&interval={time_interval}&series_type={series_type}&apikey={API_KEY}'
    }

    for indicator, url in technical_indicators.items():
        print('indicator: ',indicator,'\n')
        if 'time_period' in url:
            filename = f'{folder}\{indicator}_{time_period}.csv'
        else:
            filename = f'{folder}\{indicator}.csv'
        if not os.path.exists(filename):
            print('indicator in if statement: ',indicator,'\n')
            r = requests.get(url)
            data = r.json()

            if 'Note' in data:
                print(data['Note'])
                if data['Note'] == query_limit:
                    # incomplete
                    idx = (idx+1)%n_keys
                    API_KEY = KEY[idx]
                    print(API_KEY)
                    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={API_KEY}'
                    response = requests.get(url)
                    data = response.json()
                    if 'Note' not in data:
                        print('Good thing Alphavantage is my bitch')

            valuesList = list(data.values())
            data = valuesList[1]

            dates = []
            values = []

            for key,value in data.items():
                dates.append(key)
                for k, v in value.items():
                    values.append(v)

            data = list(zip(dates, values))

            with open(filename, 'w', newline='') as csvfile:
                # Create a CSV writer object
                writer = csv.writer(csvfile)
                # Write the header
                writer.writerow(['Dates', f'{indicator} Values'])
                # Write the data to the CSV file
                writer.writerows(data)
        else:
            # The file already exists, so do nothing
            pass

#%% This will gather all data such that it is perfectly up to date and consistent in formatting
if __name__ == "__main__":
    # Example code for Boeing
    ticker = 'BA'
    dirname = os.path.dirname(__file__)
    folder = dirname + '\data\Industrials\Boeing'
    file = folder + '/all_data.csv'

    print(folder)
    print(file)

    # indicator query still needs to be updated
    # stock_indicators(ticker, folder)

    # stock_price_data(ticker, folder)
    etf_query(folder)

    # compile_data(folder, file)
