import pandas as pd
import numpy as np
from matplotlib.ticker import Formatter
import matplotlib.pyplot as plt
import yfinance as yf
import datetime

ticker = 'F'
interval = '2m'
training_start = startDate = (
    datetime.datetime.today() - datetime.timedelta(2)).strftime('%Y-%m-%d')


df = yf.download(ticker, interval=interval, start=startDate, end=(
    datetime.datetime.today() - datetime.timedelta(1)).strftime('%Y-%m-%d'))
df = pd.DataFrame(df)

print(df.empty)

#df.index = pd.to_datetime(df.index.strftime('%Y-%m-%d %H:%M'))

# print(df)
