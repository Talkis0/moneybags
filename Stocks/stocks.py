# Author: Tristan Alkis
# Date: 5/29/2023
# Time: 15:24
# This python script is designed to tell me whether specific stocks are 
# worth investing in or not. I am using Benjamin Graham's Book "The Intelligent Investor"
# as a go-by to help me determine.
"""
# # Value Investing: Need to determine the value of the stock
# # https://www.investopedia.com/articles/fundamental-analysis/09/five-must-have-metrics-value-investors.asp#:~:text=Typically%20a%20stock%20with%20a,the%20company's%20expected%20earnings%20growth.


# Price-to-book ratio (P/B): We want this to be less than a 1
# if the P/B is greater than a 2 then the stock might be overvalued

# Debt-to-Equity Ratio (D/E): This should not be greater than a 2

# Free cash flow (FCF): Investors tend to look at EPS, we still want
# to look into this but may need more time (for future)

# PEG Ratio (Price/earnings-to-growth): Modified version of the 
# P/E ratio. We want the PEG ratio to be less than 1

# Return on equity (ROE): A high ROE is good, 
# ROE = NetIncome/AvgShareholdersEquity
# this needs to be at the average or above for the company's sector
# the S&P is around 13%, so above that is good

# Price-to-earnings (P/E) ratio: this may depend on the sector
# typically under 20 is considered good

# Earnings per share (EPS): a high eps tends to indicate a more 
# profitable company (80) or higher

# Overall these numbers could depend on the sector so we will need to
# break things down per sector and based on recent trends and
# the history of the sectors

# Sectors include: Energy, Materials, Industrials, Utilities, 
# Healthcare, Financials, Consumer Discretionary, 
# Consumer Staples, Information Technology,
# Communication Services, Real Estate

# Start with the averages for each number at each sector
# Get the leaders or companies that meet our requirements
# Must be outperforming the rest of the sector
"""
import yfinance as yf
import pandas as pd
import numpy as np


msft = yf.Ticker("GM")
pe_ratio = msft.info["trailingPE"]
pb_ratio = msft.info["priceToBook"]
debt_equity_ratio = msft.info["debtToEquity"]
free_cash_flow = msft.info["freeCashflow"]
peg_ratio = msft.info["pegRatio"]
roe = msft.info["returnOnEquity"]
eps = msft.info["trailingEps"]
print("Price-to-Earnings Ratio:", pe_ratio)
print("Price-to-Book Ratio:", pb_ratio)
print("Debt-to-Equity Ratio:", debt_equity_ratio)
print("Free Cash Flow:", free_cash_flow)
print("Price/Earnings to Growth Ratio:", peg_ratio)
print("Return on Equity:", roe)
print("Earnings Per Share:", eps)

sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
sp500 = sp500[0]['Symbol']
PtoB_list = []
PB_dic = {}
PEG_dic = {}
for i in sp500:
    ticker = yf.Ticker(i)
    # print(ticker)
    try:
        PB = ticker.info["priceToBook"]
        # PtoB_list.append(PB)
        if 0<PB<2:
            PB_dic[i] = PB
    except KeyError:
        pass

    try:
        PEG = ticker.info["pegRatio"]
        if 0<PEG<2:
            PEG_dic[i] = PEG
    except KeyError:
        pass

        # print('pricetobook',PB)
    # if PB:
        # PtoB_list.append(i)

PBlist = sorted(PB_dic, key=PB_dic.get, reverse = False)
PEGlist = sorted(PEG_dic, key=PEG_dic.get, reverse = False)
for i in PBlist[0:15]:
    if i in PEGlist[0:15]:
        print(i)

# print(PBlist)
# print(PEGlist)
# sorted_PB_dic = sorted(PB_dic, key=PB_dic.get, reverse=False)
# sorted_PEG_dic = sorted(PEG_dic, key=PEG_dic.get, reverse=False)
# top_PB = sorted_PB_dic[0:15]
# top_PEG = sorted_PEG_dic[0:15]
# print(top_PB)
# print("")
# print(top_PEG)



