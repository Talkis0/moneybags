import requests
import csv

def etf_price_data(symbol):
    API_KEY = 'GOIR6JKN4TW5HNGO'

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    # Extract the time series data
    time_series = data['Time Series (Daily)']

    if 'Error Message' in data:
        print('An error occurred:', data['Error Message'])

    # Prepare CSV file for writing
    filename = f'C:\Projects\moneybags\ETF_daily\{symbol}.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Open', 'High', 'Low', 'Close','Adjusted Close', 'Volume', 'Dividend Amount', 'Split Coefficient'])

        # Write each data point to CSV
        for timestamp, values in time_series.items():
            row = [timestamp, values['1. open'], values['2. high'], values['3. low'], values['4. close'], values['5. adjusted close'], values['6. volume'], values['7. dividend amount'], values['8. split coefficient']]
            writer.writerow(row)

    print(f'Intraday data exported to {filename}')

etf_price_data('BIL')
