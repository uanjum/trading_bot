# Trading bot
<p align="center">
  <img src="https://github.com/user-attachments/assets/b5d1cc3b-46d6-4a09-bed9-f2bb107eb769" alt="trading background" />
</p>

This project is more related to data science and machine learning with one goal. Let’s automate the stock picking, let the bot trade it for us and get rich (easy right?). After numerous failed quantitative strategies, e.g. SMA, EMA crossovers, RSI, support resistance mapping, I pivoted to sentiment analysis on social media. Keep in mind this is a very naïve strategy.

 I decided to use Twitter data as my social media platform, and two different sets of the NLP libraries in python.
 
 1.	NLTK Vader sentiment
 2.	Flair NLP library

Using twint to fetch tweets from the Twitter feed. The algorithm would go as follows:
1.	Get the top 250 TSX listed stocks (Some really high priced stocks were filtered out since I was not going to trade with that much capital). This step was only computed once in the beginning2.	TSX opens at 930AM. At 10AM, get all tweets for each stock from 12AM (start of day) to present (10AM). This would include premarket chatter and the first half hour of market open.
3.	For each stock, run all the tweets gathered through the sentiment analyzer of choice (vader or flair) and calculate the sentiment.
4.	Rank the stocks based on who has the most count of positive tweets
5.	Buy the top three ranked stocks on the list (equal weightage across all three)
6.	Sell all positions 10 minutes before market close.

To get the price data for the stocks, yfinance library was used. It seemed easy to use and quite reliable since it pulls data directly from Yahoo Finance.
This strategy was naïve since, there was minimal preprocessing done on the tweets. Ideally stop words should have been removed and word stemming should have been performed. Also there were no commission fees that were considered, since there are various platforms that charge various commissions, and there are also ones that don’t charge any.
Another factor that was not considered was slippage, although for our case since we are not trying to sell at certain price point, the script just sells whatever we have at market close, it would still be worthwhile to explore in the future. 
I completed and deployed the bots in August and gave each one a starting capital of $10,000 and let this bot do its thing since August 13, 2022 untill December 16, 2022. The results were as follows:

<p align="center">
  <img src="https://github.com/user-attachments/assets/0697407b-7feb-4e73-9310-9becf76c329e" alt="trading graph" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/d127a291-564a-485e-a408-837adafbeda8" alt="trading chart" />
</p>

The S&P buy and hold strategy turned out to be the best over time. Although the sentiment strategy using vader sentiment library was not far off. It should be noted that both sentiment strategies bought stocks irrelative of the market capitalization. Again, this is a very basic way of looking at the data. 

The difference in the results between the two sentiment libraries was quite a bit. This reinforced the idea that not all sentiment libraries are trained/created equally. One library might understand the financial jargon better then others. 
For the best result, I would have to create my own training, testing data using a large amount of twitter data which would be very time consuming but worth it since it would capture the modern financial jargon used these days e.g., “X stock going to the moon!”

If you would like to take a look at the code or to let me know how to improve it, please contact me.
