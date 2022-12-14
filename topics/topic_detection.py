import os

import pandas as pd
from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups

def get_all_tweets(directory = None):
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df

def get_topics_from(df=None, directory_name = "nursetweets"):
    tweet_text = df['text'].astype(str).tolist()
    print("got df")
    topic_model = BERTopic(language="english",
                           calculate_probabilities=True,
                           verbose=True,
                           # top_n_words=10,
                           # n_gram_range=(1, 2)
                           # nr_topics = 20,
                           )
    print("set up topic model. about to fit model")
    topics, probabilities = topic_model.fit_transform(tweet_text)
    topic_model.save("{}_model".format(directory_name))
    print("fit model")
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

    freq.to_csv('topics/{}_topics.csv'.format(directory_name))
    print("saved to csv")

directories =  ["nursetweets", "doctortweets", "teachertweets", "railtweets", "journalisttweets", "musiciantweets"]

# for directory in directories:
df = get_all_tweets("nursetweets")
print("got all tweets")

try:
    get_topics_from(df, "nursetweets")
except Exception as e:
    print(str(e))