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
    df.to_csv("data/healthcare_tweets.csv")

directories =  ["nursetweets", "doctortweets"]
# get_all_tweets(directories)

def get_topics_from(filename = "data/healthcare_tweets.csv"):
    df = pd.read_csv(filename)
    tweet_text = df['text'].astype(str).tolist()

    topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)

    topics, probs = topic_model.fit_transform(tweet_text)

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

    freq.to_csv('topics/healthcare_topics.csv')

    # similar_topics, similarity = topic_model.find_topics("wellbeing", top_n=5); similar_topics

get_topics_from()