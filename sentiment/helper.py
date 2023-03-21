import numpy as np
from bertopic import BERTopic

import os

import pandas as pd
import re
from collections import Counter
import liwc
import numpy as np
import pandas as pd
import os
import re
from collections import Counter
import liwc
import pandas as pd

def get_all_tweets(directory=None):
    directory = "Dissertation/"+directory #remove when running locally
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df

#Setting up docs
def get_original_tweets():
    model = BERTopic.load("nursetweets_10_1_model")
    df = model.get_document_info(get_all_tweets("nursetweets")['nouns'])
    df["original_text"] = get_all_tweets("nursetweets")['text']
    df["clean_text"] = get_all_tweets("nursetweets")['clean_text']
    df["created_at"] = get_all_tweets("nursetweets")['created_at']
    df.to_csv("Dissertation/sentiment/docs_clean_text.csv")

# get_original_tweets()

def reset_index(path = "sentiment/docs_clean_text.csv"):
    df = pd.read_csv(path)
    df.sort_values(by='created_at', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(path)

# reset_index()

def add_topic_label():
    df = pd.read_csv("sentiment/docs_clean_text.csv")
    conditions = [
        (df['Topic'] == 2),
        (df['Topic'] == -1)
    ]
    values = ["Work", "None"]
    df.drop(['tier', 'Unnamed: 0', 'Unnamed: 0.1.1.1', 'Unnamed: 0.4', 'Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1'], axis=1, inplace=True,
            errors='ignore')
    df['label'] = np.select(conditions, values, default="Life")
    df.to_csv("sentiment/docs_clean_text.csv")
    print(df.head())

# add_topic_label()

#Getting sentiment
def tokenize(text):
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)

parse, category_names = liwc.load_token_parser('sentiment/LIWC2007_English080730.dic')

def get_emotion(string):
    # tokenize string
    tokens = tokenize(string)
    # now flatmap over all the categories in all the tokens using a generator:
    counts = Counter(category for token in tokens for category in parse(token))

    if counts['posemo']>counts['negemo']:
        return 1 #positive
    elif counts['posemo']==counts['negemo']:
        return 0 #neither
    else:
        return 2 #negative

def add_sentiment():
    docs = pd.read_csv("sentiment/docs_clean_text.csv")
    docs['sentiment_index'] = docs['clean_text'].apply(lambda x: get_emotion(x))
    conditions = [
        (docs['sentiment_index'] == 0),
        (docs['sentiment_index'] == 1),
        (docs['sentiment_index'] == 2)
    ]
    values = ["None", "Positive", "Negative"]
    docs.drop(['tier', 'Unnamed: 0', 'Unnamed: 0.1.1.1', 'Unnamed: 0.4', 'Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1'], axis=1, inplace=True,
              errors='ignore')
    docs['sentiment'] = np.select(conditions, values)
    docs.to_csv("sentiment/docs_sentiment.csv")

add_sentiment()

#Getting docs for different time periods
def get_before_lockdown():
    df = pd.read_csv("sentiment/docs_sentiment.csv")

    #get index range for 46 days before first lockdown
    # df_startdate = df[df['created_at'].str.match("2020-02-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-03-25")]
    # print(df_enddate)

    # make docs csv of first lockdown 8938 to 10838
    before_first_lockdown = df.iloc[8938:10839]
    before_first_lockdown.to_csv("sentiment/csvs/before_first_lockdown.csv")

    #get index range for 27 days before second lockdown
    # df_startdate = df[df['created_at'].str.match("2020-10-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-11-04")]
    # print(df_enddate)

    # make docs csv of second lockdown 23578 to 25516
    before_second_lockdown = df.iloc[23578:25517]
    before_second_lockdown.to_csv("sentiment/csvs/before_second_lockdown.csv")

    #get index range for 62 days before third lockdown
    # df_startdate = df[df['created_at'].str.match("2020-11-06")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-01-05")]
    # print(df_enddate)

    # make docs csv of third lockdown 25613 to 30528
    before_third_lockdown = df.iloc[25613:30529]
    before_third_lockdown.to_csv("sentiment/csvs/before_third_lockdown.csv")

get_before_lockdown()

def get_lockdown_tweets():
    df = pd.read_csv("sentiment/docs_sentiment.csv")

    #sorting by date and adding new index
    # df.sort_values(by='created_at', inplace=True)
    # df.reset_index(drop=True, inplace=True)
    # df.to_csv("Dissertation/graphs/topics_with_dates.csv")

    #find indexes for start and end dates of lockdown periods
    #confirm first lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-03-26")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-05-10")] #46 days
    # print(df_enddate)

    #confirm second lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-11-05")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-12-02")] #28 days
    # print(df_enddate)

    #confirm third lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2021-01-06")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-03-08")] #62 days
    # print(df_enddate)

    # first lockdown 10839 to 13703
    first_lockdown = df.iloc[10839:13704]
    first_lockdown.to_csv("sentiment/csvs/first_lockdown.csv")
    #
    # #second lockdown 25517 to 27893
    second_lockdown = df.iloc[25517:27894]
    second_lockdown.to_csv("sentiment/csvs/second_lockdown.csv")
    #
    # #third lockdown 30529 to 37921
    third_lockdown = df.iloc[30529:37922]
    third_lockdown.to_csv("sentiment/csvs/third_lockdown.csv")
    # print(third_lockdown[third_lockdown['Topic']==2])

get_lockdown_tweets()

def get_after_lockdown():
    df = pd.read_csv("sentiment/docs_sentiment.csv")

    #get index range for 46 days after first lockdown
    # df_startdate = df[df['created_at'].str.match("2020-05-11")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-06-18")]
    # print(df_enddate)

    # make docs csv of first lockdown 13704 to 16139
    before_first_lockdown = df.iloc[13704:16140]
    before_first_lockdown.to_csv("sentiment/csvs/after_first_lockdown.csv")

    #get index range for 27 days after second lockdown
    # df_startdate = df[df['created_at'].str.match("2020-12-03")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-12-29")]
    # print(df_enddate)

    # make docs csv of second lockdown 27894 to 29883
    before_second_lockdown = df.iloc[27894:29884]
    before_second_lockdown.to_csv("sentiment/csvs/after_second_lockdown.csv")

    #get index range for 62 days after third lockdown
    # df_startdate = df[df['created_at'].str.match("2021-03-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-06-09")]
    # print(df_enddate)
    #
    # make docs csv of third lockdown 37922 to 47140
    before_third_lockdown = df.iloc[37922:47141]
    before_third_lockdown.to_csv("sentiment/csvs/after_third_lockdown.csv")

get_after_lockdown()

