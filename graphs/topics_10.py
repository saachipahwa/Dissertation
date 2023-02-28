import pandas as pd
from bertopic import BERTopic
import os


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


# get_topics_with_dates()

def dynamic_topic_modelling():
    dates_df = pd.read_csv("Dissertation/graphs/topics_with_dates.csv")
    model_copy = BERTopic.load("nursetweets_10_1_model_copy")
    model_copy.merge_topics(get_all_tweets("nursetweets")['nouns'],
                            [[-1, 2], [0, 1, 3, 4, 5, 6, 7, 8, 9]])
    model_copy.set_topic_labels({-1: "Work", 0: "Life"})
    print(model_copy.get_topic_info())
    topics_over_time = model_copy.topics_over_time(
        dates_df['Document'], dates_df['created_at'], datetime_format="%Y-%m-%d %H:%M:%S+00:00", nr_bins=30)
    fig = model_copy.visualize_topics_over_time(
        topics_over_time, topics=[-1, 0], custom_labels=True)
    fig.show()


# dynamic_topic_modelling()

def words_per_topic():
    model_copy = BERTopic.load("nursetweets_10_1_model_copy")
    model_copy.merge_topics(get_all_tweets("nursetweets")['nouns'],
                            [[-1, 2], [0, 1, 3, 4, 5, 6, 7, 8, 9]])
    model_copy.set_topic_labels({-1: "Work", 0: "Life"})

    fig = model_copy.visualize_barchart(topics=[-1, 0], custom_labels=True)
    fig.show()


words_per_topic()
