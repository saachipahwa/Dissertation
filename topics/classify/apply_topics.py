import os

import pandas as pd
from bertopic import BERTopic

model = BERTopic.load("nursetweets_10_1_model")


def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir("Dissertation/"+directory):
        f = os.path.join("Dissertation/"+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df

def get_docs_topics():
    get_all_tweets("nursetweets")['text'].to_csv("Dissertation/topics/all_nurse_tweets.csv")
    df = model.get_document_info(get_all_tweets("nursetweets")['nouns'])
    df["original_text"] = get_all_tweets("nursetweets")['text']
    df.to_csv("Dissertation/topics/docs_topics.csv")

def get_docs_topics():
    get_all_tweets("nursetweets")['text'].to_csv(
        "Dissertation/topics/all_nurse_tweets.csv")
    df = model.get_document_info(get_all_tweets("nursetweets")['nouns'])
    df["original_text"] = get_all_tweets("nursetweets")['text']
    df.to_csv("Dissertation/topics/docs_topics.csv")


def get_sample_tweets():
    df = pd.read_csv("Dissertation/topics/chosen_docs/docs_topics.csv")
    for i in range(-1, 10):
        df_topic = df[df['Topic'] == i]
        df_topic = df_topic.sample(n=40, replace=False, random_state=1)
        df_topic.to_csv("Dissertation/topics/samples/topic_{}_sample.csv".format(i))

get_sample_tweets()