import requests
import csv


# ticker = "BA"

# this will give us stock sentiment
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

# month = '2009-01'
# function  = 'BOP'
def csvTechnicalIndicators(function, ticker, name):
    API_KEY = 'GOIR6JKN4TW5HNGO'
    # function={function}&symbol={ticker}&apikey={API_KEY}
    url = f'https://www.alphavantage.co/query?function={function}&symbol={ticker}&interval=daily&apikey={API_KEY}'

    r = requests.get(url)
    data = r.json()

    # fieldnames = ['Date','BOP']
    filename = f'C:\Users\trist\Documents\moneybags\moneybags\Stocks\csvData\BA_{name}.csv'

    dates = []
    values = []

    data = data['Technical Analysis: BOP']
    for key,value in data.items():
        # print(key)
        dates.append(key)
        # print
        for k, v in value.items():
            values.append(v)

    data = list(zip(dates, values))

    # Open the file in write mode
    with open(filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the header
        writer.writerow(['Dates', 'BOP Values'])

        # Write the data to the CSV file
        writer.writerows(data)
csvTechnicalIndicators(function, 'BA', 'BOP')
