import requests
from sec_edgar_api import EdgarClient

headers = {
    'User-Agent': 'admin admin@moneybagz.com'
}

CIK = "12927"
CIK = '0'*(10-len(CIK))+CIK

""" url = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json?from=2000&last=2023".format(CIK)
response = requests.get(url, headers=headers)
response = response.json()
 """

statements = {}
url = "https://www.sec.gov/Archives/edgar/data/{}/{}/{}"
edgar = EdgarClient( user_agent='admin admin@moneybagz.com' )
all_filings = edgar.get_submissions(CIK)['filings']['recent']
for idx, accessionNumber in enumerate( all_filings['accessionNumber'] ):
    if all_filings['form'][idx] == '10-Q':
        primaryDocument = all_filings['primaryDocument'][idx]
        if primaryDocument == '':
            primaryDocument = accessionNumber + '.txt'
        statements[ all_filings['reportDate'][idx] ] = url.format( CIK, accessionNumber.replace('-', ''), primaryDocument ) #dictionary mapping dates to document urls

statement = list(statements.values())[0]
response = requests.get( statement, headers=headers )