import os
import re
import string

import numpy as np
import pandas as pd
import nltk #lib used for stop words
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from langdetect import detect, detector_factory, detect_langs
from nltk.probability import FreqDist
from nltk.corpus import treebank

#Text preprocessing
#REFERENCE: https://www.analyticsvidhya.com/blog/2021/06/text-preprocessing-in-nlp-with-python-codes/



detector_factory.seed = 30

# Removing URLs
def remove_URL(text):
    """Remove URLs from a sample string"""
    return re.sub(r"http\S+", "", text)

# Removing hashtags
def remove_hashtags_mentions(text):
    clean_tweet = re.sub("@[A-Za-z0-9_]+","", text)
    clean_tweet = re.sub("#[A-Za-z0-9_]+","", clean_tweet)
    return clean_tweet


def remove_nonalphabet(text):
    regex = re.compile('[^a-zA-Z\s\']')
    return regex.sub('', text)

# Removing Stop words
stopwords = nltk.corpus.stopwords.words('english')
def remove_stopwords(text):
    wordslist = text.split()
    output= [i for i in wordslist if i not in stopwords]
    return ' '.join(output)

def remove_2char_words(text):
    wordslist = text.split()
    output= [i for i in wordslist if not len(i)<3]
    return ' '.join(output)

def too_short(text):
    wordslist = text.split()
    if len(wordslist)<5:
        return True
    return False

# Lemmatization
wordnet_lemmatizer = WordNetLemmatizer()
def lemmatizer(text):
    tokens = text.split()
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in tokens]
    return(' '.join(lemm_text))

def delete_whitespace_tweets(df):
    df['whitespace'] = df['clean_text'].apply(lambda x:str(str(x).isspace()))
    df = df[df['whitespace'].str.contains('False') == True]
    df = df.drop('whitespace', axis=1)
    return df

def get_nouns(text):
    text = word_tokenize(text)
    tags = nltk.pos_tag(text)
    new_text = ""
    for a,b in tags:
        print(b)
        if b=="NN":
            new_text = new_text + a + " "
    return new_text

def text_preprocessing(directory = "railtweets"):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file

        if os.path.isfile(f):
            print(f)
            df = pd.read_csv(f)

            #make RT's empty
            df['text'] = df['text'].loc[~df['text'].str.startswith('RT ', na=False)] #remove RT's
            #remove empty tweets
            df['text'].replace('', np.nan, inplace=True)
            df.dropna(subset=['text'], inplace=True)

            df['clean_text'] = df['text']

            #remove urls
            df['clean_text'] = df['clean_text'].apply(lambda x:remove_URL(x))

            #remove hashtage
            df['clean_text'] = df['clean_text'].apply(lambda x:remove_hashtags_mentions(x))

            #remove non alphabet chars
            df['clean_text'] = df['clean_text'].apply(lambda x:remove_nonalphabet(x))


            #lower case
            df['clean_text'] = df['clean_text'].apply(lambda x: x.lower())

            #lemmatizing
            df['clean_text'] = df['clean_text'].apply(lambda x:lemmatizer(str(x)))

            # #remove stopwords
            df['clean_text'] = df['clean_text'].apply(lambda x:remove_stopwords(str(x)))

            # #remove 2 char words
            df['clean_text'] = df['clean_text'].apply(lambda x:remove_2char_words(str(x)))

            #remove now empty tweets

            df['clean_text'].replace('', np.nan, inplace=True)
            df.dropna(subset=['clean_text'], inplace=True)

            try:
                df = delete_whitespace_tweets(df)
            except Exception as e:
                print("couldn't delete whitespace tweets. error:", e)

            df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'], axis=1,  inplace=True,  errors='ignore')

            #add column of only nouns
            df['nouns'] = df['clean_text'].apply(lambda x:get_nouns(str(x)))
            df.to_csv(f, index=False)

#run remove_empty before this
text_preprocessing()
#run remove_empty after this


#
# def nouns_column(directory):
#     for filename in os.listdir(directory):
#         f = os.path.join(directory, filename)
#         # checking if it is a file
#
#         if os.path.isfile(f):
#             print(f)
#             df = pd.read_csv(f)
#             # df['nouns'] = df['clean_text']
#             df['nouns'] = df['clean_text'].apply(lambda x:get_nouns(str(x)))
#             df.to_csv(f, index=False)

def remove_empty_tweets(directory = "doctortweets"):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            df = pd.read_csv(f)
            df['text'].replace('', np.nan, inplace=True)
            df.dropna(subset=['text'], inplace=True)
            df.to_csv(f, index=False)



