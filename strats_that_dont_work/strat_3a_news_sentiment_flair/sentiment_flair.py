from itertools import count
import requests
import pandas as pd
import json
import time
import flair

flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
url = "https://free-news.p.rapidapi.com/v1/search"
headers = {"X-RapidAPI-Host": "free-news.p.rapidapi.com", "X-RapidAPI-Key": "c6d1c19cf7msh10678c12b509254p1cd52cjsnf4b65b33233d"}
finance_websites = ['marketwatch.com', 'investopedia.com', 'seekingalpha.com', 'xe.com', 'thestreet.com', 'financialpost.com', 'lesechos.fr', 'investing.com', 'kiplinger.com', 'benzinga.com', 'thisismoney.co.uk', 'cityam.com', 'latribune.fr', 'daveramsey.com', 'finanznachrichten.de', 'fin24.com', 'challenges.fr', 'smartasset.com', 'finanzen.net', 'investorplace.com', 'institutionalinvestor.com', 'ritholtz.com', 'marketrealist.com', 'pionline.com', 'wallstreet-online.de', 'efinancialcareers.com', 'marketoracle.co.uk', 'moneymorning.com', 'financial-planning.com', 'citywire.co.uk', 'wealthmanagement.com', 'investmentwatchblog.com', 'moneytalksnews.com', 'morningstar.co.uk', 'insidermonkey.com', 'risk.net', 'alternatives-economiques.fr', 'realclearmarkets.com', 'financialsamurai.com', 'worldfinance.com', 'armstrongeconomics.com', 'savingadvice.com', 'fool.co.uk', 'elliottwave.com', 'simplywall.st', 'kitces.com', 'etfdailynews.com', 'investmentweek.co.uk', 'globalcapital.com', 'lenouveleconomiste.fr', 'interest.co.nz', 'ai-cio.com', 'fool.ca', 'learnbonds.com', 'etnet.com.hk', 'wallstreetdaily.com', 'abladvisor.com', 'fool.com.au', 'investmentexecutive.com', 'investmentu.com', 'finanzen.ch', 'finews.ch', 'financeasia.com', 'mybudget360.com', 'wallstreetpit.com', 'deraktionaer.de', 'swfinstitute.org', 'wealthdaily.com', 'waterstechnology.com', 'smallcaps.com.au', 'dasinvestment.com', 'finews.asia', 'marketsmedia.com', 'moneymanagement.com.au', 'smarteranalyst.com', 'moneyobserver.com', 'trustnet.com', 'themiddlemarket.com', 'finews.com', 'insidefutures.com', 'stockmarketwire.com', 'dailyreckoning.com.au', 'thetradenews.com', 'mesec.cz', 'equitymaster.com', 'financialreporter.co.uk', 'insideparadeplatz.ch', 'ringgitplus.com', 'hedgeco.net', 'brokernews.com.au', 'theadviser.com.au', 'patria.cz', 'finance-investissement.com', 'cnafinance.com', 'asianinvestor.net', 'la-chronique-agora.com', 'dailyalts.com']

def get_sentiment_flair(sentence): 
    sentiment = flair.data.Sentence(sentence)
    flair_sentiment.predict(sentiment)
    return sentiment.labels[0].to_dict()['value']

def get_news_articles(company_name):
    querystring = {"q":'"{}"'.format(company_name)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    time.sleep(2)
    result_json = json.loads(response.text)

    if result_json['status'] == "ok":
        total_pages = result_json['total_pages']
        if total_pages >= 1:
            count = 1
            for i in range(total_pages):
                querystring = {"q":"'{}'".format(company_name), "page":"{}".format(count)}
                count = count+1
                response = requests.request("GET", url, headers=headers, params=querystring)
                time.sleep(2)
                result_json = json.loads(response.text)
                if i == 0:
                    df_master = pd.DataFrame(result_json['articles'])
                else:
                    df = pd.DataFrame(result_json['articles'])
                    df_master = pd.concat([df_master, df], ignore_index = True)
                    print(df.shape)
                    print(df_master.shape)
            
        filtered_df = df_master[df_master['clean_url'].isin(finance_websites)]
        return filtered_df
    else:
        print('No news results for the query')
        return pd.DataFrame()

    
def get_news_sentiment(company):
    print(company)
    filtered_df = get_news_articles(company)
    if not filtered_df.empty:
        filtered_df['sentiment'] = filtered_df.apply(lambda x: get_sentiment_flair(x['title']), axis = 1)
        count_total_reviews = len(filtered_df)
        count_pos_reviews = len(filtered_df[filtered_df['sentiment'] == 'POSITIVE'])
    else:
        count_total_reviews = 0
        count_pos_reviews = 0
    
    print('pos_rev: {}'.format(count_pos_reviews))
    print('tot rev: {}'.format(count_total_reviews))
    return count_total_reviews, count_pos_reviews 
