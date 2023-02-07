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

# topics_life = [2, 4, 5, 6, 8, 8]
# topics_work = [-1, 1]
# topics_other = [0, 3, 7]
# topics_to_merge = [topics_work, topics_life, topics_other]
# model.merge_topics(docs, topics_to_merge)

topic_distr, topic_token_distr = model.approximate_distribution(
    docs, calculate_tokens=True)

df = model.visualize_approximate_distribution(docs[1], topic_token_distr[1])
