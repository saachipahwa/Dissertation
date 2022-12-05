import os
import re
import string

import numpy as np
import pandas as pd
import nltk #lib used for stop words
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def remove_RT(directory = "nursetweets"):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            df = pd.read_csv(f)
            print("Length of df: " + str(len(df)))
            df = df[df['text'].str.startswith('RT ')==True]
            # df['text'] = df['text'].loc[~df['text'].str.startswith('RT ', na=False)] #remove RT's
            df.to_csv(f)
            print("Length of df: " + str(len(df)))

def remove_empty_tweets(directory = "doctortweets"):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            df = pd.read_csv(f)
            df['text'].replace('', np.nan, inplace=True)
            df.dropna(subset=['text'], inplace=True)
            df.to_csv(f)

# remove_empty_tweets()
words = set(nltk.corpus.words.words())

def nonenglish(text):
    for word in text:
        if word.lower() in words or not word.isalpha():
            return True
    return False

def remove_nonenglish(directory = "nursetweets"):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            df = pd.read_csv(f)
            df['text'] = df[~nonenglish(df.text)]
            df.to_csv(f)

remove_nonenglish()

#Text preprocessing
#REFERENCE: https://www.analyticsvidhya.com/blog/2021/06/text-preprocessing-in-nlp-with-python-codes/

#Helper function removing punctuations like . , ! $( ) * % @
def remove_punctuation_string(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

# Removing URLs
def remove_URL(text):
    """Remove URLs from a sample string"""
    return re.sub(r"http\S+", "", text)

# Removing hashtags
def remove_hashtags_mentions(text):
    clean_tweet = re.sub("@[A-Za-z0-9_]+","", text)
    clean_tweet = re.sub("#[A-Za-z0-9_]+","", clean_tweet)
    return clean_tweet

# Helper function removing Stop words
stopwords = nltk.corpus.stopwords.words('english')
def remove_stopwords(text):
    output= [i for i in text if i not in stopwords]
    return output

# Tokenization
# Stemming
# porter_stemmer = PorterStemmer()
# def stemming(text):
#     stem_text = [porter_stemmer.stem(word) for word in text]
#     return stem_text

#Tokenization
def tokenization(text):
    tokens = re.split('W+',text)
    return tokens

# Lemmatization
wordnet_lemmatizer = WordNetLemmatizer()
def lemmatizer(text):
    text = tokenization(text)
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return ' '.join(lemm_text)

#Remove words not in english

def text_preprocessing():
    df = pd.read_csv("nursetweets/150751978.csv")

    # #remove RT's
    # df = df[df['text'].str.startswith('RT ')==True]
    #
    # #remove empty tweets
    # df['text'].replace('', np.nan, inplace=True)
    # df.dropna(subset=['text'], inplace=True)

    df['clean_text'] = df['text']

    #remove urls
    df['clean_text']= df['clean_text'].apply(lambda x:remove_URL(x))

    #remove hashtage
    df['clean_text']= df['clean_text'].apply(lambda x:remove_hashtags_mentions(x))

    #remove punctuation
    df['clean_text'] = df['clean_text'].apply(lambda x:remove_punctuation_string(x))

    #lower case
    df['clean_text'] = df['clean_text'].apply(lambda x: x.lower())

    #lemmatizing
    df['clean_text']=df['clean_text'].apply(lambda x:lemmatizer(x))

    # #remove stopwords
    # df['clean_text']= df['clean_text'].apply(lambda x:remove_stopwords(x))

    df.to_csv("nursetweets/150751978.csv")

text_preprocessing()
