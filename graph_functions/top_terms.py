import pandas as pd
from bertopic import BERTopic
import os
import numpy as np
from matplotlib import pyplot as plt

directories = ["nursetweets", "doctortweets", "teachertweets",
               "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 0
directory_name = directories[directory_index]
profession_name = "nurse"
nr_topics = 10
work_topics = [2] #change add_topic_label function too
other_topics = [0,1,3,4,5,6,7,8,9]


def get_all_tweets(directory=None):
    directory = "Dissertation/"+directory #remove when running locally
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0, error_bad_lines=False)
        df = pd.concat([df, user_df], ignore_index=True)
    return df


def get_topics_with_dates(path = f"Dissertation/graphs/{profession_name}s/topics_with_dates.csv"):
    model = BERTopic.load(f"{directory_name}_{nr_topics}_1_model")
    df = model.get_document_info(get_all_tweets(directory_name)['nouns'])
    df["original_text"] = get_all_tweets(directory_name)['text']
    df["created_at"] = get_all_tweets(directory_name)['created_at']
    df.to_csv(path)

# get_topics_with_dates()


def add_topic_label(path = f"graphs/{profession_name}s/topics_with_dates.csv"):
    df = pd.read_csv(path)
    conditions = [
        #CHANGE FOR NEW WORKER GROUP
        (df['Topic'] == 2),
        (df['Topic'] == -1)
    ]
    values = ["Work", "None"]
    df.drop(['tier', 'Unnamed: 0', 'Unnamed: 0.1.1.1', 'Unnamed: 0.4', 'Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1'], axis=1, inplace=True,
            errors='ignore')
    df['label'] = np.select(conditions, values, default="Life")
    df.to_csv(path)
    print(df.head())

# add_topic_label()


def reset_index(path = "graphs/{}s/topics_with_dates.csv".format(profession_name)):
    df = pd.read_csv(path)
    df.sort_values(by='created_at', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(path)

# reset_index()

def top_terms():
    model = BERTopic.load(f"{directory_name}_{nr_topics}_1_model")
    print(model.get_topic_info())
    fig = model.visualize_barchart(topics=work_topics, n_words = 10)
    fig.show()
    fig = model.visualize_barchart(topics=other_topics, n_words = 5)
    fig.show()

top_terms()
