import pandas as pd
import numpy as np
from matplotlib.ticker import Formatter
import matplotlib.pyplot as plt
import yfinance as yf
import datetime


def get_historical_data(ticker_list, interval):
    # ticker list can be a one ticker must be within list fromat
    # intervals are 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    # time frame will always be today - 59 days (since 2 min data is only available for 2 days)

    startDate = (datetime.datetime.today() -
                 datetime.timedelta(1)).strftime('%Y-%m-%d')
    print(startDate)

    for ticker in ticker_list:
        print(ticker)
        df = yf.download(ticker, interval=interval, start=startDate)
        df = pd.DataFrame(df)
        df.index = pd.to_datetime(df.index.strftime('%Y-%m-%d %H:%M'))
        df.to_csv('{}.csv'.format(ticker))

    print('Complete')


def polyfit(degree, database, parameter):
    dbpoly = database
    # this will make present time 0
    dbpoly = dbpoly.reindex(index=dbpoly.index[::-1])
    # this will make past times (+) integers, future can be (-1)
    dbpoly.insert(1, 'hours', range(0, len(dbpoly)))
    idx = np.isfinite(dbpoly[parameter])
    db_esd = dbpoly[idx]
    polyfit = np.polyfit(db_esd['hours'], db_esd[parameter], deg=degree)
    polyfit_diff = [None]*(degree+1)
    polyfit_diff_2 = [None]*(degree+1)
    deg1 = degree
    for item in range(0, len(polyfit)):
        # print(item)
        polyfit_diff[item] = polyfit[item]*deg1
        deg1 = deg1-1

    deg1 = degree-1
    for item in range(0, len(polyfit)):
        # print(item)
        polyfit_diff_2[item] = polyfit_diff[item]*deg1
        if deg1 is not 0:
            deg1 = deg1-1

    database = database.reindex(index=database.index[::-1])
    database.insert(0, 'hours', range(0, len(database)))

    deg2 = degree
    deg3 = degree
    for item in range(0, len(polyfit)):
        database['degree1_{}'.format(
            str(deg3))] = polyfit[item]*database['hours']**float(deg2)
        if deg2 is not 0:
            deg2 = deg2-1
        deg3 = deg3-1

    summing1 = database.iloc[:, (-1*(degree+1)):]
    database['parameter_curve_fit'] = summing1.sum(axis=1)

    deg2 = degree-1
    deg3 = degree-1
    for item in range(0, len(polyfit_diff)):
        database['degree2_{}'.format(
            str(deg3))] = polyfit_diff[item]*database['hours']**float(deg2)
        if deg2 is not 0:
            deg2 = deg2-1
        deg3 = deg3-1

    summing2 = database.iloc[:, (-1*(degree+1)):]
    database['parameter_1st_diff'] = summing2.sum(axis=1)

    deg2 = degree-2
    deg3 = degree-2
    for item in range(0, len(polyfit_diff_2)):
        database['degree_{}'.format(
            str(deg3))] = polyfit_diff_2[item]*database['hours']**float(deg2)
        if deg2 is not 0:
            deg2 = deg2-1
        deg3 = deg3-1

    summing = database.iloc[:, (-1*(degree+1)):]
    database['parameter_2nd_diff'] = summing.sum(axis=1)
    database.set_index('Datetime', drop=True, inplace=True)
    database.index = pd.to_datetime(database.index)
    database = database.reindex(index=database.index[::-1])

    return database


def SMA(df, period):
    df['SMA_{}'.format(period)] = np.NaN
    for row in range(period, df.shape[0], 1):
        df['SMA_{}'.format(period)][row] = (
            df.iloc[row-period:row, 3].sum())/period


def EMA(df, period):
    df['EMA_{}'.format(period)] = np.NaN
    df['EMA_{}'.format(period)][period] = df['Close'][period] * \
        (2/(1+period))+df['Close'][period-1]
    for row in range(period+1, df.shape[0], 1):
        df['EMA_{}'.format(period)][row] = df['Close'][row]*(2/(1+period)) + \
            df['EMA_{}'.format(period)][row-1]*(1-(2/(1+period)))


def RSI(df, rsi_period, ticker):

    df.reset_index(drop=False, inplace=True)

    df['RSI'] = np.NaN

    for item in df.index[rsi_period::]:
        AvgUp = 0
        AvgUpCount = 0
        AvgDn = 0
        AvgDnCount = 0
        for period in range(item-rsi_period+1, item):
            deltaC = df.loc[period, 'Close'] - df['Close'][period-1]
            if deltaC > 0:
                AvgUp = AvgUp + deltaC
                AvgUpCount = AvgUpCount + 1
            else:
                AvgDn = AvgDn + -1*deltaC
                AvgDnCount = AvgDnCount + 1
        if AvgUpCount == 0:
            AvgUpCount = 1
        if AvgDnCount == 0:
            AvgDnCount = 1

        AvgUp = AvgUp/AvgUpCount
        AvgDn = AvgDn/AvgDnCount
        RS = AvgUp/AvgDn
        df.loc[item, 'RSI'] = 100-100/(1+RS)

    return df


def easy_plot(database):

    class MyFormatter(Formatter):
        def __init__(self, dates, fmt='%m/%d %H:%M'):
            self.dates = dates
            self.fmt = fmt

        def __call__(self, x, pos=0):
            'Return the label for time x at position pos'
            ind = int(np.round(x))
            if ind >= len(self.dates) or ind < 0:
                return ''

            return self.dates[ind].strftime(self.fmt)

    database = database.reindex(index=database.index[::-1])
    fig, ax1 = plt.subplots()
    formatter = MyFormatter(database.index)
    ax1.xaxis.set_major_formatter(formatter)
    ax1.invert_xaxis()
    plt.locator_params(axis='x', nbins=20)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    ax1.plot(np.arange(len(database.index)),
             database['Close'], label='Close')
    ax1.plot(np.arange(len(database.index)),
             database['buy'], 'bo', label='buy')
    ax1.plot(np.arange(len(database.index)),
             database['sell'], 'ro', label='sell')

    ax1.legend()
    ax2 = ax1.twinx()
    ax2.plot(np.arange(len(database.index)),
             database['capital'], 'g', label='capital')
    ax2.legend()
    plt.show()
