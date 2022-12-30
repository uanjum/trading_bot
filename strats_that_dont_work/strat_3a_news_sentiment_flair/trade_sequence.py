import requests
import pandas as pd
import json
import time
import flair
import sentiment_flair

tsx = pd.read_csv('tsx_index.csv')

print(tsx)

reviews = tsx.apply(lambda x: sentiment_flair.get_news_sentiment(x['company']), axis = 1, result_type='expand')
reviews.rename(columns = {'0':'total_reviews', '1':'pos_reviews'}, inplace = True)
tsx = pd.concat([tsx, reviews], axis = 'columns')

tsx.to_csv('tsx_with_reviews.csv')