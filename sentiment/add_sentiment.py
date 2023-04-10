from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bertopic import BERTopic
import numpy as np
import os
import pandas as pd

directories = ["nursetweets", "doctortweets", "teachertweets",
               "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 4
directory_name = directories[directory_index]
profession_name = "journalist"
nr_topics = 15
#REMINDER TO SET WORK TOPICS in add_topic_label()

def get_all_tweets(directory=None):
    directory = "Dissertation/"+directory #remove when running locally
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0, error_bad_lines = False)
        df = pd.concat([df, user_df], ignore_index=True)
    return df

#Setting up docs
def get_original_tweets():
    model = BERTopic.load(f"{directory_name}_{nr_topics}_1_model")
    df = model.get_document_info(get_all_tweets(directory_name)['nouns'])
    df["original_text"] = get_all_tweets(directory_name)['text']
    df["clean_text"] = get_all_tweets(directory_name)['clean_text']
    df["created_at"] = get_all_tweets(directory_name)['created_at']
    df.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/docs_clean_text.csv")

get_original_tweets()

def reset_index(path = f"Dissertation/sentiment/{profession_name}s_csvs/docs_clean_text.csv"):
    df = pd.read_csv(path)
    df.sort_values(by='created_at', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(path)

reset_index()

def add_topic_label():
    df = pd.read_csv(f"Dissertation/sentiment/{profession_name}s_csvs/docs_clean_text.csv")
    conditions = [
        (df['Topic'] == 4),
        (df['Topic'] == -1)
    ]
    values = ["Work", "None"]
    df.drop(['tier', 'Unnamed: 0', 'Unnamed: 0.1.1.1', 'Unnamed: 0.4', 'Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1'], axis=1, inplace=True,
            errors='ignore')
    df['label'] = np.select(conditions, values, default="Life")
    df.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/docs_clean_text.csv")
    print(df.head())

add_topic_label()


def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    # print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    # print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    #
    # print("Sentence Overall Rated As", end = " ")

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        # print("Positive")
        return 1
    elif sentiment_dict['compound'] <= - 0.05 :
        # print("Negative")
        return 2
    else :
        # print("Neutral")
        return 0

def add_sentiment():
    docs = pd.read_csv(f"Dissertation/sentiment/{profession_name}s_csvs/docs_clean_text.csv")
    docs['sentiment_index'] = docs['clean_text'].apply(lambda x: sentiment_scores(x))
    conditions = [
        (docs['sentiment_index'] == 0),
        (docs['sentiment_index'] == 1),
        (docs['sentiment_index'] == 2)
    ]
    values = ["None", "Positive", "Negative"]
    docs.drop(['tier', 'Unnamed: 0', 'Unnamed: 0.1.1.1', 'Unnamed: 0.4', 'Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1'], axis=1, inplace=True,
              errors='ignore')
    docs['sentiment'] = np.select(conditions, values)
    docs.to_csv(f"Dissertation/sentiment/{profession_name}s_csvs/docs_sentiment.csv")

add_sentiment()

# sentiment_scores("I hope nobody dies")