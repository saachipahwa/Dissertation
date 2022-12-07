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

from langdetect import detect

#Text preprocessing
#REFERENCE: https://www.analyticsvidhya.com/blog/2021/06/text-preprocessing-in-nlp-with-python-codes/

#Helper function removing punctuations like . , ! $( ) * % @
# def remove_punctuation_string(text):
#     punctuationfree="".join([i for i in text if i not in string.punctuation])
#     return punctuationfree

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
#
# def remove_emojis(text):
#     emoji_pattern = re.compile("["
#                                u"\U0001F600-\U0001F64F"  # emoticons
#                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
#                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                                u"\U00002500-\U00002BEF"  # chinese char
#                                u"\U00002702-\U000027B0"
#                                u"\U00002702-\U000027B0"
#                                u"\U000024C2-\U0001F251"
#                                u"\U0001f926-\U0001f937"
#                                u"\U00010000-\U0010ffff"
#                                u"\u2640-\u2642"
#                                u"\u2600-\u2B55"
#                                u"\u200d"
#                                u"\u23cf"
#                                u"\u23e9"
#                                u"\u231a"
#                                u"\ufe0f"  # dingbats
#                                u"\u3030"
#                                "]+", re.UNICODE)
#
#     return(emoji_pattern.sub(r'', text)) # no emoji

def remove_nonalphabet(text):
    regex = re.compile('[^a-zA-Z\s\']')
    return regex.sub('', text)

# Removing Stop words
stopwords = nltk.corpus.stopwords.words('english')
def remove_stopwords(text):
    wordslist = text.split()
    output= [i for i in wordslist if i not in stopwords]
    return ' '.join(output)

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
    # for word in text:
    #     if str(word).lower() in words or not str(word).isalpha():
    #         return True
    # return False
    if detect(str(text))=="en":
        return str(False)
    else:
        return str(True)

# def return_non_english(text):
#     return " ".join(w for w in nltk.wordpunct_tokenize(text) \
#              if w.lower() in words or not w.isalpha())

def delete_whitespace_tweets(df):
    df['whitespace'] = df['clean_text'].apply(lambda x:str(str(x).isspace()))
    df = df[df['whitespace'].str.contains('False') == True]
    df = df.drop('whitespace', axis=1)
    return df

def text_preprocessing(directory = "nursetweets"):
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

            #remove non english tweets
            df['non_english'] = nonenglish(df['text'])
            df = df[df['non_english'].str.contains('False') == True]

            #lower case
            df['clean_text'] = df['clean_text'].apply(lambda x: x.lower())

            #lemmatizing
            df['clean_text'] = df['clean_text'].apply(lambda x:lemmatizer(str(x)))

            # #remove stopwords
            df['clean_text'] = df['clean_text'].apply(lambda x:remove_stopwords(str(x)))

            #remove now empty tweets
            df['clean_text'].replace('', np.nan, inplace=True)
            df = delete_whitespace_tweets(df)
            print(len(df))
            df.drop([ 'Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'], axis=1,  inplace=True,  errors='ignore')
            df.to_csv(f, index=False)

#run remove_empty before this
text_preprocessing()
#run remove_empty after this


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
