import pandas as pd
from bertopic import BERTopic
import os
df = pd.DataFrame(columns=['original_tweet', 'date', ''])


def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir("Dissertation/"+directory):
        f = os.path.join("Dissertation/"+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df


def get_topics_with_dates():
    model = BERTopic.load("nursetweets_10_1_model")
    df = model.get_document_info(get_all_tweets("nursetweets")['nouns'])
    df["original_text"] = get_all_tweets("nursetweets")['text']
    df["created_at"] = get_all_tweets("nursetweets")['created_at']

    df.to_csv("Dissertation/graphs/topics_with_dates.csv")


get_topics_with_dates()
