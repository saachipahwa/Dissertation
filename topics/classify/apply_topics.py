import os

import pandas as pd
from bertopic import BERTopic


def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir("Dissertation/"+directory):
        f = os.path.join("Dissertation/"+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0, error_bad_lines=False)
        df = pd.concat([df, user_df], ignore_index=True)
    return df


def get_docs_topics(modelname, directory, profession):
    model = BERTopic.load(modelname)
    df = model.get_document_info(get_all_tweets(directory)['nouns'])
    df["original_text"] = get_all_tweets(directory)['text']
    df.to_csv(f"Dissertation/topics/{profession}_docs/docs_topics.csv")


get_docs_topics(modelname="journalisttweets_15_1_model", directory="journalisttweets", profession="journalist")


def get_sample_tweets(profession):
    df = pd.read_csv(f"Dissertation/topics/{profession}_docs/docs_topics.csv")
    for i in range(-1, 10):
        df_topic = df[df['Topic'] == i]
        df_topic = df_topic.sample(n=40, replace=False, random_state=1)
        df_topic.to_csv(
            "Dissertation/topics/{}_docs/samples/topic_{}_sample.csv".format(profession, i))

get_sample_tweets(profession="journalist")