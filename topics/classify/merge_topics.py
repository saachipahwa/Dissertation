import os

import pandas as pd
from bertopic import BERTopic


def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir("Dissertation/"+directory):
        f = os.path.join("Dissertation/"+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df


model = BERTopic.load("nursetweets_10_1_model_copy")
docs = get_all_tweets("nursetweets")['nouns']


model.merge_topics(get_all_tweets("nursetweets")['nouns'],
                   [[-1, 2], [0, 1, 3, 4, 5, 6, 7, 8, 9]])

topic_distr, topic_token_distr = model.approximate_distribution(
    docs, calculate_tokens=True)

model.visualize_approximate_distribution(docs[1], topic_token_distr[1])
