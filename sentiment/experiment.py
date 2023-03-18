import os
import re
from collections import Counter
import liwc
import pandas as pd


def tokenize(text):
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)

parse, category_names = liwc.load_token_parser('sentiment/LIWC2007_English080730.dic')


def get_emotion(string):
    # tokenize string
    tokens = tokenize(string)
    # now flatmap over all the categories in all of the tokens using a generator:
    counts = Counter(category for token in tokens for category in parse(token))
    print(counts)
    if counts['posemo']>counts['negemo']:
        print(string, 'positive')
    elif counts['posemo']==counts['negemo']:
        print(string, "cant decide")
    else:
        print(string, 'negative')

def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df

# gettysburg = '''Four score and seven years ago our fathers brought forth on
#   this continent a new nation, conceived in liberty, and dedicated to the
#   proposition that all men are created equal. Now we are engaged in a great
#   civil war, testing whether that nation, or any nation so conceived and so
#   dedicated, can long endure. We are met on a great battlefield of that war.
#   We have come to dedicate a portion of that field, as a final resting place
#   for those who here gave their lives that that nation might live. It is
#   altogether fitting and proper that we should do this.'''

# print(type(gettysburg))
# gettysburg_tokens = tokenize(gettysburg)
# # now flatmap over all the categories in all of the tokens using a generator:
# gettysburg_counts = Counter(category for token in gettysburg_tokens for category in parse(token))
# # and print the results:
# print(gettysburg_counts)

fl_tweets = pd.read_csv("sentiment/docs_clean_text.csv")['clean_text']

for t in fl_tweets[0:10]:
    get_emotion(t)