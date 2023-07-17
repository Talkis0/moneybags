import requests
import csv

API_KEY = 'GOIR6JKN4TW5HNGO'
ticker = "BA"
# this will give us stock sentiment
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
"""
url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={API_KEY}'
r = requests.get(url)
data = r.json()

print(data)


url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'
r = requests.get(url)
data = r.json()

print(data)

function = 'INCOME_STATEMENT'

url = f'https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={API_KEY}'
r = requests.get(url)
data = r.json()

print(data)
"""
month = '2009-01'
function  = 'BOP'
# function={function}&symbol={ticker}&apikey={API_KEY}
url = f'https://www.alphavantage.co/query?function={function}&symbol={ticker}&interval=daily&apikey={API_KEY}'

r = requests.get(url)
data = r.json()

# fieldnames = ['Date','BOP']
# filename = 'BA_BOP.csv'
# with open(filename, 'w', newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(data)

# print(data)

##################

# function = 'EARNINGS'

# url = f'https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={API_KEY}&month={month}'

# r = requests.get(url)
# data = r.json()
BA_BOP_data = data['Technical Analysis: BOP']
for key in BA_BOP_data.keys():
    print(key)

# print(data['Technical Analysis: BOP'])