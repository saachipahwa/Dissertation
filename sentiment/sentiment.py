import re
from collections import Counter
import liwc
import numpy as np
import pandas as pd
import os
import re
from collections import Counter
import liwc
import pandas as pd

#Getting sentiment
def tokenize(text):
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)

parse, category_names = liwc.load_token_parser('sentiment/LIWC2007_English080730.dic')

def get_emotion(string):
    # tokenize string
    tokens = tokenize(string)
    # now flatmap over all the categories in all the tokens using a generator:
    counts = Counter(category for token in tokens for category in parse(token))

    if counts['posemo']>counts['negemo']:
        return 1 #positive
    elif counts['posemo']==counts['negemo']:
        return 0 #neither
    else:
        return 2 #negative

def add_sentiment():
    docs = pd.read_csv("sentiment/docs_clean_text.csv")
    docs['sentiment_index'] = docs['clean_text'].apply(lambda x: get_emotion(x))
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