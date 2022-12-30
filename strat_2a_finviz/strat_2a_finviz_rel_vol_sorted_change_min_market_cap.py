from finvizfinance.screener.overview import Overview
import yfinance as yf
from datetime import datetime
from datetime import date
import pandas as pd
import time

overview = Overview()
overview.set_filter(
    filters_dict={'Relative Volume': 'Over 1.5', 'Market Cap.': '+Mid (over $2bln)'})


market_open = datetime.strptime('08:00', '%H:%M').time()
market_close = datetime.strptime('13:45', '%H:%M').time()
timing_check = 1

capital = 10000
alloted_capital = capital/3

ticker_bought = ["", "", ""]
shares_bought = [0, 0, 0]
buy_price = [0, 0, 0]
sell_price = [0, 0, 0]


while timing_check:

    if datetime.now().time() > market_open and datetime.now().time() < market_close and capital == 10000:
        df = overview.screener_view()
        filtered_df = df[df['Change'] > 0].sort_values(
            by=['Change'], ascending=False, ignore_index=True)

        print(filtered_df)

        i = 0
        j = 0

        while j < 3 and i < filtered_df.shape[0]:
            try:
                buy_price[j] = yf.Ticker(
                    filtered_df['Ticker'][i]).info['currentPrice']
                print(buy_price)

                ticker_bought[j] = filtered_df['Ticker'][i]
                shares_bought[j] = alloted_capital/buy_price[j]

                i = i+1
                j = j+1

            except:
                print('ticker is not on the canadian exchange')
                i = i+1

        capital = 0

    else:
        print(datetime.now().time())
        print('market is closed or shares have already been bought')
        print('Shares Bought:')
        print(shares_bought)
        print('ticker bought:')
        print(ticker_bought)

    if shares_bought[0] > 0 and datetime.now().time() > market_close:
        for k in range(0, j):
            sell_price[k] = yf.Ticker(ticker_bought[k]).info['currentPrice']
            capital = capital + sell_price[k]*shares_bought[k]
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
    try:
        # handle the zero division error
        gain = (sell_price[i]-buy_price[i])/buy_price[i]*100
    except:
        gain = 0
    print(gain)

print('total gain/loss %:')
print((capital-10000)/10000*100)
print('ending capital')
print(capital)

gain_loss = (capital-10000)/10000*100

daily_gain_data = pd.read_csv('A://Projects/Ultimate Trader/daily_gain_loss.csv')
daily_gain_data.set_index('strategy', inplace=True)
daily_gain_data.loc["strat_2a_finviz_rel_vol_sorted_change_min_market_cap",date.today().strftime("%d/%m/%Y")] = gain_loss
daily_gain_data.to_csv('A://Projects/Ultimate Trader/daily_gain_loss.csv')

cum_capital = pd.read_csv('A://Projects/Ultimate Trader/cumulative_capital.csv')
cum_capital.set_index('strategy', inplace=True)

if date.today().strftime("%d/%m/%Y") in cum_capital:
    cum_capital.loc["strat_2a_finviz_rel_vol_sorted_change_min_market_cap",date.today().strftime("%d/%m/%Y")] = cum_capital.iloc[4,-2]*(1+gain_loss/100)
else:
    cum_capital.loc["strat_2a_finviz_rel_vol_sorted_change_min_market_cap",date.today().strftime("%d/%m/%Y")] = cum_capital.iloc[4,-1]*(1+gain_loss/100)

cum_capital.to_csv('A://Projects/Ultimate Trader/cumulative_capital.csv')

print("executed strat_2a_finviz_rel_vol_sorted_change_min_market_cap")