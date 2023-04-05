import os

import pandas as pd
from bertopic import BERTopic

directories = ["nursetweets", "doctortweets", "teachertweets",
               "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 1
directory = directories[directory_index]
profession = "doctor"
nr_topics = 10

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
    df.to_csv("Dissertation/topics/{}_docs/docs_topics.csv".format(profession))

get_docs_topics(modelname="{}_{}_1_model".format(directory, nr_topics), directory=directory, profession=profession)

def get_sample_tweets(profession, nr_topics):
    df = pd.read_csv("Dissertation/topics/{}_docs/docs_topics.csv".format(profession))
    for i in range(-1, nr_topics):
        df_topic = df[df['Topic'] == i]
        df_topic = df_topic.sample(n=40, replace=False, random_state=1)
        df_topic.to_csv(
            "Dissertation/topics/{}_docs/samples/topic_{}_sample.csv".format(profession, i))

get_sample_tweets(profession=profession, nr_topics=nr_topics)