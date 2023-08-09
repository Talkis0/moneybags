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