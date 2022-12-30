import twint
import nest_asyncio
import pandas as pd
import flair
flair_sentiment = flair.models.TextClassifier.load('en-sentiment')



def check_tsx_sentiment(dataframe, todays_date):

    nest_asyncio.apply()  # reiniate a nest loop required for twint to run properly
    # create a configuration object
    c = twint.Config()
    # configuration paramenters to filter for tweets more found at: https://github.com/twintproject/twint/wiki/Configuration
    c.Show_cashtags = True
    c.Since = todays_date  # format e.g. '2022-05-16'
    c.Lang = 'en'
    c.Hide_output = True
    c.Pandas = True  # this needs to be true to save to pandas dataframes

    ticker_list = dataframe
    ticker_list['pos_rev'] = 0

    row = 0
    for ticker in ticker_list['ticker_search']:
        ticker_cashtag = '%24' + ticker
        c.Search = ticker_cashtag
        twint.run.Search(c)
        tweets_df = twint.storage.panda.Tweets_df
        print('Received tweets for: ' + ticker)

        if not tweets_df.empty:
            # that dont have cashtags
            filtered_tweets = tweets_df[tweets_df['cashtags'] != "null"]

            positive_reviews = 0
            if not filtered_tweets.empty:
                for tweet in filtered_tweets['tweet']:
                    sentiment = flair.data.Sentence(tweet)
                    flair_sentiment.predict(sentiment)
                    if sentiment.labels[0].to_dict()['value'] == 'POSITIVE':
                        positive_reviews = positive_reviews + 1

                ticker_list['pos_rev'][row] = positive_reviews
                row = row+1

            print("number of postitive reviews for {} are: {}".format(
                ticker, positive_reviews))
            print("% of tickers completed: ")
            print(row/len(ticker_list)*100)

    # save a csv file with ticker and sentiment data
    ticker_list.to_csv('A://Projects/Ultimate Trader/strat_1b_twitter_sentiment_flair/ticker_w_sentiment.csv')
