import requests
from sec_edgar_api import EdgarClient
import datetime
import pandas as pd

headers = {
    'User-Agent': 'admin admin@moneybagz.com'
}

CIK = "12927"
CIK = '0'*(10-len(CIK))+CIK

url = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json?from=2000&last=2023".format(CIK)
response = requests.get(url, headers=headers)
response = response.json()
# Dates Assets Liabilities EarningsPerShareDiluted WeightedAverageNumberOfDilutedSharesOutstanding
assets_raw = response['facts']['us-gaap']['Assets']['units']['USD']
liabilities_raw = response['facts']['us-gaap']['Liabilities']['units']['USD']
eps_diluted_raw = response['facts']['us-gaap']['EarningsPerShareDiluted']['units']['USD/shares']
n_shares_diluted_raw = response['facts']['us-gaap']['WeightedAverageNumberOfDilutedSharesOutstanding']['units']['shares']

# sort by date and filter for 10-Q/10-K
assets_raw = sorted( filter( lambda a: ( a['form'] == '10-Q' ) or ( a['form'] == '10K' ), assets_raw ), key=lambda k: datetime.datetime.strptime( k['filed'], '%Y-%m-%d' ) )
liabilities_raw = sorted( filter( lambda a: ( a['form'] == '10-Q' ) or ( a['form'] == '10K' ), liabilities_raw ), key=lambda k: datetime.datetime.strptime( k['filed'], '%Y-%m-%d' ) )
eps_diluted_raw = sorted( filter( lambda a: ( a['form'] == '10-Q' ) or ( a['form'] == '10K' ), eps_diluted_raw ), key=lambda k: datetime.datetime.strptime( k['filed'], '%Y-%m-%d' ) )
n_shares_diluted_raw = sorted( filter( lambda a: ( a['form'] == '10-Q' ) or ( a['form'] == '10K' ), n_shares_diluted_raw ), key=lambda k: datetime.datetime.strptime( k['filed'], '%Y-%m-%d' ) )

# Convert to pandas series
assets_df = pd.Series( [ a['val'] for a in assets_raw ], index=pd.to_datetime( [ a['filed'] for a in assets_raw ] ) )
liabilities_df = pd.Series( [ a['val'] for a in liabilities_raw ], index=pd.to_datetime( [ a['filed'] for a in liabilities_raw ] ) )
eps_diluted_df = pd.Series( [ a['val'] for a in eps_diluted_raw ], index=pd.to_datetime( [ a['filed'] for a in eps_diluted_raw ] ) )
n_shares_diluted_df = pd.Series( [ a['val'] for a in n_shares_diluted_raw ], index=pd.to_datetime( [ a['filed'] for a in n_shares_diluted_raw ] ) )