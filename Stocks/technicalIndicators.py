import requests
import csv
import os

# ticker = "BA"

# this will give us stock sentiment
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

# month = '2009-01'
# function  = 'BOP'
def csvTechnicalSMA(ticker, time_interval, time_period, series_type, API_KEY):
    current_folder = os.getcwd()

    # series_type can equal close, open, high or low
    # time_period can be 
    technical_indicators = {
    'SMA': f'https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'EMA': f'https://www.alphavantage.co/query?function=EMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'WMA': f'https://www.alphavantage.co/query?function=WMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'DEMA': f'https://www.alphavantage.co/query?function=DEMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'TEMA': f'https://www.alphavantage.co/query?function=TEMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'TRIMA': f'https://www.alphavantage.co/query?function=TRIMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'KAMA': f'https://www.alphavantage.co/query?function=KAMA&symbol={ticker}&interval={time_interval}&time_period={time_period}&series_type={series_type}&apikey={API_KEY}',
    'MAMA': f'https://www.alphavantage.co/query?function=MAMA&symbol={ticker}&interval={time_interval}&series_type={series_type}&fastlimit=.01&apikey={API_KEY}',
    'T3': f'https://www.alphavantage.co/query?function=VWAP&symbol={ticker}&interval={time_interval}min&apikey={API_KEY}',
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
        
        r = requests.get(url)
        data = r.json()

    # fieldnames = ['Date','BOP']
        filename = f'{current_folder}\{ticker}\{indicator}_.csv'

        dates = []
        values = []

        data = data[f'Technical Analysis: {indicator}']
        for key,value in data.items():
            dates.append(key)
            for k, v in value.items():
                values.append(v)

        data = list(zip(dates, values))
        # folder_path = f'{current_folder}\{ticker}'
    # Open the file in write mode
        if not os.path.exists(filename):
            # os.makedirs(folder_path)
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

# API_KEY = 'GOIR6JKN4TW5HNGO'
API_KEY = 'FVDFYPUKXD8YETUJ'
ticker = 'BA'
time_interval = 'daily'
# time_period = [10, 50, 200]
time_period = 10
# series_type = ['close','open','high','low']
series_type = 'close'
csvTechnicalSMA(ticker, time_interval, time_period, series_type, API_KEY)




