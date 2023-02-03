import os

import pandas as pd
from bertopic import BERTopic

model = BERTopic.load("nursetweets_10_1_model")

def get_all_tweets(directory = None):
    df = pd.DataFrame()
    for filename in os.listdir("Dissertation/"+directory):
        f = os.path.join("Dissertation/"+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df


print("all tweets", get_all_tweets("nursetweets")['nouns'])

print("docs", model.get_document_info(get_all_tweets("nursetweets")['nouns']))


