
import numpy as np
import re
from collections import Counter
import liwc
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
    docs = pd.read_csv("sentiment/docs_clean_text.csv")
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
    docs.to_csv("sentiment/docs_sentiment.csv")

add_sentiment()

# sentiment_scores("I hope nobody dies")