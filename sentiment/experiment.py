import os
import re
from collections import Counter

import pandas as pd


def tokenize(text):
    # you may want to use a smarter tokenizer
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)

import liwc
parse, category_names = liwc.load_token_parser('sentiment/LIWC2007_English080730.dic')

def get_emotion(string):
    # tokenize string
    tokens = string.tokenize()
    # now flatmap over all the categories in all of the tokens using a generator:
    counts = Counter(category for token in tokens for category in parse(token))
    if counts['posemo']>counts['negemo']:
        print(string, 'positive')
    elif counts['posemo']==counts['negemo']:
        print(string, "cant decide")
    else:
        print(string,'negative')

def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df

fl_tweets = pd.read_csv("graphs/first_lockdown.csv")['text']

for t in fl_tweets[0:10]:
    get_emotion(t)