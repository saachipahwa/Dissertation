import os

import pandas as pd
from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups

def get_all_tweets(directories = None):
    df = pd.DataFrame()
    for directory in directories:
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            print(f)
            user_df = pd.read_csv(f, index_col=0)
            df = pd.concat([df, user_df], ignore_index=True)
    df.to_csv("data/all_tweets.csv")

directories =  ["nursetweets", "doctortweets", "teachertweets"]
# get_all_tweets(directories)

def get_topics_from(filename = "data/all_tweets.csv"):
    df = pd.read_csv(filename)
    tweet_text = df['text'].astype(str).tolist()

    topic_model = BERTopic(language="english",
                           calculate_probabilities=True,
                           verbose=True,
                           top_n_words=20,
                           n_gram_range=(1, 2)
                           # nr_topics = 20,
                           )

    topics, probabilities = topic_model.fit_transform(tweet_text)

    freq = topic_model.get_topic_info()
    print(type(freq))
    print(freq)

    details_list = []
    for i in freq['Topic']:
        if i>-1:
            details_list.append(topic_model.get_topic(i))
        else:
            details_list.append([])
    freq['details'] = details_list

    freq.to_csv('topics/tweets_topics.csv')

get_topics_from()