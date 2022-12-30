import pandas as pd
import numpy as np
import custom_functions
from matplotlib.ticker import Formatter
import matplotlib.pyplot as plt
import yfinance as yf
import datetime

ticker = 'F'
interval = '2m'
capital = 1000
shares_bought = 0


start_date = (datetime.datetime.today() -
              datetime.timedelta(2)).strftime('%Y-%m-%d')
end_date = (datetime.datetime.today() -
            datetime.timedelta(1)).strftime('%Y-%m-%d')


df = yf.download(ticker, interval=interval, start=start_date, end=end_date)
df = pd.DataFrame(df)
cum_tpv = 0
cum_volume = 0
vwap = []
count = 0
df['buy'] = np.nan
df['sell'] = np.nan
df['capital'] = np.nan


for point in range(0, len(df)):
    total_price_volume = (df['High'][point]+df['Close'][point] +
                          df['Low'][point])/3*df['Volume'][point]
    cum_tpv += total_price_volume
    cum_volume += df['Volume'][point]
    vwap.append(cum_tpv/cum_volume)

    if point != 0:
        if df['Close'][point] > vwap[point] and df['Close'][point-1] < vwap[point-1] and capital > 2:
            df['buy'][point] = df['Close'][point]
            shares_bought = capital/df['Close'][point]
            capital = 0

        if df['Close'][point] < vwap[point] and df['Close'][point-1] > vwap[point-1] and shares_bought > 0:
            df['sell'][point] = df['Close'][point]
            capital = shares_bought * df['Close'][point]
            shares_bought = 0

    df['capital'][point] = capital + shares_bought*df['Close'][point]


df['vwap'] = vwap
print('test start date: ' + start_date)
print('test end date: ' + end_date)
print('total capital is:')
print(capital)
print('total shares held: ')
print(shares_bought)
print('total share value is:')
print(shares_bought*df['Close'].iloc[-1])


custom_functions.easy_plot(df)
