from distutils.archive_util import make_zipfile
from doctest import master
from tracemalloc import start
from numpy.lib.polynomial import polyfit
import pandas as pd
import numpy as np
import custom_functions
from matplotlib.ticker import Formatter
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.signal import argrelextrema
import yfinance as yf
import datetime
import math


# How to run the strat:
# 1. comment out the test set and only run the training set code in between the commented section
# 2. copy the over_bought_signal and over_sold_signal values into their respective variables in the test code
# 3. comment out the trainig code and only run the test code


ticker = 'F'
interval = '2m'
training_set = 21
startDate = (datetime.datetime.today() -
             datetime.timedelta(1)).strftime('%Y-%m-%d')


############################################################################################################################################################
# TRAINING CODE START
############################################################################################################################################################

# for i in range(training_set, 9, -1):
#     start_date = (datetime.datetime.today() -
#                   datetime.timedelta(i)).strftime('%Y-%m-%d')

#     if i == training_set:
#         save_start_date = start_date

#     end_date = (datetime.datetime.today() -
#                 datetime.timedelta(i-1)).strftime('%Y-%m-%d')
#     print(i)
#     print(training_set)
#     print(start_date)
#     print(end_date)
#     df = yf.download(ticker, interval=interval, start=start_date, end=end_date)
#     df = pd.DataFrame(df)

#     if df.empty == False:
#         df.index = pd.to_datetime(df.index.strftime('%Y-%m-%d %H:%M'))
#         master_data = custom_functions.RSI(df, 14, ticker)
#         master_data.set_index('Datetime', inplace=True)

#         master_data['Smooth'] = gaussian_filter1d(master_data['Close'], 3)
#         local_max = argrelextrema(master_data['Smooth'].values, np.greater)
#         local_min = argrelextrema(master_data['Smooth'].values, np.less)

#         max_df = pd.DataFrame(local_max[0], columns=['values'])
#         max_df['date'] = np.nan
#         max_df['extreme'] = np.nan
#         max_df['over_bought'] = np.nan

#         count = 0
#         for item in max_df['values']:
#             max_df.loc[count, 'date'] = master_data.index.array[int(item)]
#             max_df.loc[count, 'extreme'] = master_data['Close'][int(item)]
#             max_df.loc[count, 'over_bought'] = master_data['RSI'][int(item)]
#             count += 1

#         max_df.set_index('date', drop=True, inplace=True)
#         max_df.drop(['values'], axis=1, inplace=True)

#         min_df = pd.DataFrame(local_min[0], columns=['values'])
#         min_df['date'] = np.nan
#         min_df['extreme'] = np.nan
#         min_df['over_sold'] = np.nan

#         count = 0
#         for item in min_df['values']:
#             min_df.loc[count, 'date'] = master_data.index.array[int(item)]
#             min_df.loc[count, 'extreme'] = master_data['Close'][int(item)]
#             min_df.loc[count, 'over_sold'] = master_data['RSI'][int(item)]

#             count += 1

#         min_df.set_index('date', drop=True, inplace=True)
#         min_df.drop(['values'], axis=1, inplace=True)

#         if i == training_set:
#             max_min_data = pd.concat([max_df, min_df])

#         else:
#             print(max_min_data.empty)
#             max_min_data = pd.concat([max_min_data, max_df])
#             max_min_data = pd.concat([max_min_data, min_df])
#     else:
#         print('No data for the day')
#         if i == training_set:
#             training_set = i-1


# plt.subplot(1, 2, 1)
# n1, bins1, patches = plt.hist(x=max_min_data['over_bought'], bins=30)
# plt.title('over bought')

# plt.subplot(1, 2, 2)
# n2, bins2, patches = plt.hist(x=max_min_data['over_sold'], bins=30)
# plt.title('over sold')

# over_bought_signal = bins1[np.where(n1 == n1.max())]
# over_sold_signal = bins2[np.where(n2 == n2.max())]

# print(save_start_date)
# print(end_date)
# print(over_bought_signal)
# print(over_sold_signal)

############################################################################################################################################################
# TRAINING CODE END
############################################################################################################################################################


############################################################################################################################################################
# TEST CODE START
############################################################################################################################################################


overbought_signal = [52.88774817]
oversold_signal = [42.5618024]

test_set = 7

capital = 1000
shares = 0
commission = 5
share_buy_price = 0

for i in range(test_set, 1, -1):
    start_date = (datetime.datetime.today() -
                  datetime.timedelta(i)).strftime('%Y-%m-%d')

    if i == test_set:
        save_start_date = start_date

    end_date = (datetime.datetime.today() -
                datetime.timedelta(i-1)).strftime('%Y-%m-%d')

    print(start_date)
    print(end_date)

    df = yf.download(ticker, interval=interval, start=start_date, end=end_date)
    df = pd.DataFrame(df)

    if df.empty == False:
        df.index = pd.to_datetime(df.index.strftime('%Y-%m-%d %H:%M'))
        test_data = custom_functions.RSI(df, 14, ticker)
        test_data.set_index('Datetime', inplace=True)
        test_data['buy'] = np.nan
        test_data['sell'] = np.nan
        test_data['capital'] = np.nan

        for index, row in test_data.iterrows():

            if row['RSI'] != np.nan:
                for item in oversold_signal:
                    if row['RSI'] < item:
                        if shares == 0:
                            share_buy_price = row['Close']
                            shares = (capital-commission)/row['Close']
                            capital = 0
                            test_data.loc[index, 'buy'] = row['Close']
                            print('bought')

                for item in overbought_signal:
                    if row['RSI'] > item:
                        if shares != 0:
                            capital = shares*row['Close']-commission
                            shares = 0
                            test_data.loc[index, 'sell'] = row['Close']
                            print('sold')
            test_data.loc[index, 'capital'] = capital+shares*row['Close']

        if i < test_set:
            master_data = master_data.append(test_data)

        else:
            master_data = test_data


master_data = master_data[~master_data.index.duplicated(keep=False)]

print('test start date: ' + save_start_date)
print('test end date: ' + end_date)
print('total capital is:')
print(capital)
print('total shares held: ')
print(shares)
print('total share value is:')
print(shares*test_data['Close'].iloc[-1])

custom_functions.easy_plot(master_data)


############################################################################################################################################################
# TEST CODE END
############################################################################################################################################################
