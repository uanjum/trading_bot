from matplotlib import ticker
import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import date
import sentiment_flair
import time

market_open = datetime.strptime('08:00', '%H:%M').time()
market_close = datetime.strptime('13:50', '%H:%M').time()
timing_check = 1

capital = 10000
alloted_capital = capital/3

ticker_bought = ["", "", ""]
shares_bought = [0, 0, 0]
buy_price = [0, 0, 0]
sell_price = [0, 0, 0]

while timing_check:

    if datetime.now().time() > market_open and datetime.now().time() < market_close and capital == 10000:
        sentiment_flair.check_tsx_sentiment(pd.read_csv('A://Projects/Ultimate Trader/strat_1b_twitter_sentiment_flair/tsx_index.csv'), datetime.now().strftime('%Y-%m-%d')) #datetime.now().strftime('%Y-%m-%d')
        # above function outputs a csv file with ticker sentiment called 'ticker_w_sentiment.csv'
        ticker_w_sentiment = pd.read_csv('A://Projects/Ultimate Trader/strat_1b_twitter_sentiment_flair/ticker_w_sentiment.csv').sort_values(
            by=['pos_rev'], ascending=False, ignore_index=True)

        for i in range(0, 3):
            ticker_bought[i] = ticker_w_sentiment['ticker'][i]
            print(ticker_bought[i])
            buy_price[i] = yf.Ticker(
                ticker_w_sentiment['ticker'][i]).info['currentPrice']
            shares_bought[i] = alloted_capital/buy_price[i]
        print(ticker_bought)
        print(shares_bought)
        capital = 0

    else:
        print(datetime.now().time())
        print('market is closed or shares have already been bought')
        print('Shares Bought:')
        print(shares_bought)
        print('ticker bought:')
        print(ticker_bought)

    if datetime.now().time() > market_close and shares_bought[0] > 0:
        for i in range(0, 3):
            sell_price[i] = yf.Ticker(
                ticker_w_sentiment['ticker'][i]).info['currentPrice']
            capital = capital + sell_price[i]*shares_bought[i]
        timing_check = 0

    time.sleep(300)

for i in range(0, 3):
    print('ticker bought:')
    print(ticker_bought[i])
    print('bought at:')
    print(buy_price[i])
    print('sold at:')
    print(sell_price[i])
    print('gain/loss')
    print(sell_price[i]-buy_price[i])
    print('gain/loss %')
    print((sell_price[i]-buy_price[i])/buy_price[i]*100)

print('total gain/loss')
print((capital-10000)/10000*100)
print('ending capital')
print(capital)

gain_loss = (capital-10000)/10000*100

daily_gain_data = pd.read_csv('A://Projects/Ultimate Trader/daily_gain_loss.csv')
daily_gain_data.set_index('strategy', inplace=True)
daily_gain_data.loc["strat_1b_twitter_sentiment_flair",date.today().strftime("%d/%m/%Y")] = gain_loss
daily_gain_data.to_csv('A://Projects/Ultimate Trader/daily_gain_loss.csv')

cum_capital = pd.read_csv('A://Projects/Ultimate Trader/cumulative_capital.csv')
cum_capital.set_index('strategy', inplace=True)

if date.today().strftime("%d/%m/%Y") in cum_capital:
    cum_capital.loc["strat_1b_twitter_sentiment_flair",date.today().strftime("%d/%m/%Y")] = cum_capital.iloc[1,-2]*(1+gain_loss/100)
else:
    cum_capital.loc["strat_1b_twitter_sentiment_flair",date.today().strftime("%d/%m/%Y")] = cum_capital.iloc[1,-1]*(1+gain_loss/100)

cum_capital.to_csv('A://Projects/Ultimate Trader/cumulative_capital.csv')

print("executed strat_1b_twitter_sentiment_flair")
time.sleep(43200)