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