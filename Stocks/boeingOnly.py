import requests
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
url = f'https://www.alphavantage.co/query?function={function}&symbol={ticker}&interval=daily&&apikey={API_KEY}&month={month}&datatype=csv'

r = requests.get(url)
data = r.json()

print(data)