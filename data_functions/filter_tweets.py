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

#Helper function removing punctuations like . , ! $( ) * % @
# def remove_punctuation_string(text):
#     punctuationfree="".join([i for i in text if i not in string.punctuation])
#     return punctuationfree

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

# # Removing numbers
# def remove_numbers(text):
#     return ''.join((x for x in text if not x.isdigit()))

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

def remove_less_5_words(df):
    df['too_short'] = df['clean_text'].apply(lambda x:str(too_short(x)))
    df = df[df['too_short'].str.contains('False') == True]
    df = df.drop('too_short', axis=1)
    return df

# Stemming
# porter_stemmer = PorterStemmer()
# def stemming(text):
#     stem_text = [porter_stemmer.stem(word) for word in text]
#     return stem_text

# Lemmatization
wordnet_lemmatizer = WordNetLemmatizer()
def lemmatizer(text):
    tokens = text.split()
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in tokens]
    return(' '.join(lemm_text))

#Remove words not in english
words = set(nltk.corpus.words.words())
def nonenglish(text):
    try:
        lang = detect(str(text))
        if lang == "en":
            return str(False)
        else:
            print("not english", text, lang)
            print(text, detect_langs(text))
        return str(True)
    except:
        print(text, "throws an error")
        return None

# def return_non_english(text):
#     return " ".join(w for w in nltk.wordpunct_tokenize(text) \
#              if w.lower() in words or not w.isalpha())

# print(nonenglish(" me too freddie xx"))
# print(nonenglish(" i see my good friend"))

def delete_whitespace_tweets(df):
    df['whitespace'] = df['clean_text'].apply(lambda x:str(str(x).isspace()))
    df = df[df['whitespace'].str.contains('False') == True]
    df = df.drop('whitespace', axis=1)
    return df


def text_preprocessing(directory = "journalisttweets"):
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

            # df = remove_less_5_words(df)

            #lower case
            df['clean_text'] = df['clean_text'].apply(lambda x: x.lower())

            #remove non english tweets
            df['non_english'] = df['clean_text']
            df['non_english'] = df['non_english'].apply(lambda x:nonenglish(x))

            # df = df[df['non_english'].str.contains('False') == True]

            #lemmatizing
            df['clean_text'] = df['clean_text'].apply(lambda x:lemmatizer(str(x)))

            # #remove stopwords
            df['clean_text'] = df['clean_text'].apply(lambda x:remove_stopwords(str(x)))

            # #remove 2 char words
            df['clean_text'] = df['clean_text'].apply(lambda x:remove_2char_words(str(x)))

            #remove now empty tweets
            df['clean_text'].replace('', np.nan, inplace=True)
            df = delete_whitespace_tweets(df)
            df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'], axis=1,  inplace=True,  errors='ignore')
            df.to_csv(f, index=False)

#run remove_empty before this
text_preprocessing()
#run remove_empty after this

def get_nouns(text):
    text = word_tokenize(text)
    tags = nltk.pos_tag(text)
    new_text = ""
    for a,b in tags:
        print(b)
        if b=="NN":
            new_text = new_text + a + " "
    return new_text

def nouns_column(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file

        if os.path.isfile(f):
            print(f)
            df = pd.read_csv(f)
            # df['nouns'] = df['clean_text']
            df['nouns'] = df['clean_text'].apply(lambda x:get_nouns(str(x)))
            df.to_csv(f, index=False)

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



