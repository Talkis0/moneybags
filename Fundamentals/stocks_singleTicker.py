import requests
from sec_edgar_api import EdgarClient
import datetime
import pandas as pd
import numpy as np

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
se_raw = response['facts']['us-gaap']['StockholdersEquity']['units']['USD']
eps_diluted_raw = response['facts']['us-gaap']['EarningsPerShareDiluted']['units']['USD/shares']
n_shares_diluted_raw = response['facts']['us-gaap']['WeightedAverageNumberOfDilutedSharesOutstanding']['units']['shares']

# sort by date and filter for 10-Q/10-K
assets_raw = sorted( assets_raw, key=lambda k: datetime.datetime.strptime( k['filed'], '%Y-%m-%d' ) )
se_raw = sorted( se_raw, key=lambda k: datetime.datetime.strptime( k['filed'], '%Y-%m-%d' ) )
eps_diluted_raw = sorted( eps_diluted_raw, key=lambda k: datetime.datetime.strptime( k['filed'], '%Y-%m-%d' ) )
n_shares_diluted_raw = sorted( n_shares_diluted_raw, key=lambda k: datetime.datetime.strptime( k['filed'], '%Y-%m-%d' ) )

# Convert to pandas series and remove duplicate rows
def aggregate_duplicate_times( rows ):
    best_form = '10-Q'
    best_val = np.inf
    for r in rows:
        if ( r[0] == '10-K' ) and ( best_val > r[1] ):
            best_form = '10-K'
            best_val = r[1]
        elif ( r[0] == '10-Q' ) and ( best_form == '10-Q' ) and ( best_val > r[1] ):
            best_val = r[1]
    return best_val

assets_df = pd.Series( [ ( a['form'], a['val'] ) for a in assets_raw ], index=pd.to_datetime( [ a['filed'] for a in assets_raw ] ) )
assets_df = assets_df.groupby( assets_df.index ).agg( aggregate_duplicate_times )
se_df = pd.Series( [ ( a['form'], a['val'] ) for a in se_raw ], index=pd.to_datetime( [ a['filed'] for a in se_raw ] ) )
se_df = se_df.groupby( se_df.index ).agg( aggregate_duplicate_times )
eps_diluted_df = pd.Series( [ ( a['form'], a['val'] ) for a in eps_diluted_raw ], index=pd.to_datetime( [ a['filed'] for a in eps_diluted_raw ] ) )
eps_diluted_df = eps_diluted_df.groupby( eps_diluted_df.index ).agg( aggregate_duplicate_times )
n_shares_diluted_df = pd.Series( [ ( a['form'], a['val'] ) for a in n_shares_diluted_raw ], index=pd.to_datetime( [ a['filed'] for a in n_shares_diluted_raw ] ) )
n_shares_diluted_df = n_shares_diluted_df.groupby( n_shares_diluted_df.index ).agg( aggregate_duplicate_times )

fundamentals_df = pd.DataFrame({})
fundamentals_df['assets'] = assets_df
fundamentals_df['stockholders_equity'] = se_df
fundamentals_df['eps_diluted'] = eps_diluted_df
fundamentals_df['n_shares_diluted'] = n_shares_diluted_df