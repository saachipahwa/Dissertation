import os
import re
import string

import numpy as np
import pandas as pd
import nltk  # lib used for stop words
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from langdetect import detect, detector_factory, detect_langs
from nltk.probability import FreqDist
from nltk.corpus import treebank


# Text preprocessing
# REFERENCE: https://www.analyticsvidhya.com/blog/2021/06/text-preprocessing-in-nlp-with-python-codes/

# Removing URLs
def remove_URL(text):
    """Remove URLs from a sample string"""
    return re.sub(r"http\S+", "", text)


# Removing hashtags
def remove_hashtags_mentions(text):
    clean_tweet = re.sub("@[A-Za-z0-9_]+", "", text)
    clean_tweet = re.sub("#[A-Za-z0-9_]+", "", clean_tweet)
    return clean_tweet


def remove_nonalphabet(text):
    wordslist = text.split(' ')
    contraction_regex = re.compile(r"^[A-Za-z]+['|’][A-Za-z]+$")
    # start_quote_regex = re.compile(r"^[\"|'|‘][a-zA-Z\s]+[\"|'|‘]*$")
    # end_quote_regex = re.compile(r"^[\"|'|‘]*[a-zA-Z\s]+[\"|'|‘]$")
    contains_non_alphabet = re.compile('[a-zA-Z]*[^a-zA-z]+[a-zA-Z]*')
    non_alphabet = re.compile('[^a-zA-Z\s]')
    numbers = re.compile(r"[1-9]+")
    output = []
    for word in wordslist:
        if numbers.match(word):  # if there are numbers, remove them
            pass
        elif contraction_regex.match(word):  # keep contractions "can't" and "don't"
            output.append(word)
        elif contains_non_alphabet.match(word):  # if contains symbols, remove them and add
            output.append(non_alphabet.sub('', word))
        else:
            output.append(word)
    return ' '.join(output)


# Removing Stop words
stopwords = nltk.corpus.stopwords.words('english')


def remove_stopwords(text):
    wordslist = text.split()
    output = [i for i in wordslist if i not in stopwords]
    return ' '.join(output)


def remove_2char_words(text):
    wordslist = text.split()
    output = [i for i in wordslist if not len(i) < 3]
    return ' '.join(output)


def too_short(text):
    wordslist = text.split()
    if len(wordslist) < 5:
        return True
    return False


def lemmatizer(text):
    wordnet_lemmatizer = WordNetLemmatizer()
    tokens = text.split()
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in tokens]
    return (' '.join(lemm_text))


def remove_and_bug(text):
    wordslist = text.split()
    output = [i for i in wordslist if i != "&amp;"]
    pattern = re.compile("x+")
    output2 = [i for i in output if not pattern.match(i)]
    return ' '.join(output2)


def delete_whitespace_tweets(df):
    df['whitespace'] = df['clean_text'].apply(lambda x: str(str(x).isspace()))
    df = df[df['whitespace'].str.contains('False') == True]
    df = df.drop('whitespace', axis=1)
    return df


def get_nouns(text):
    text = text.split(" ")
    tags = nltk.pos_tag(text)
    new_text = ""
    haha_lol_omg = re.compile(r"^(ha)+$|lol(ol)*|omg(omg)*")
    contraction_regex = re.compile(r"^[A-Za-z]+['|’][A-Za-z]+$")

    for a, b in tags:
        if b == "NN" or b == "NNS" or b == "NNP" or b == "NNPS":
            if haha_lol_omg.match(a) or contraction_regex.match(a):
                pass
            else:
                new_text = new_text + a + " "
    return new_text


def remove_wordle(df):
    df['wordle'] = df['text'].apply(lambda x: str(True if 'Wordle' in x else False))
    df = df[df['wordle'].str.contains('False') == True]
    df = df.drop('wordle', axis=1)
    return df


def remove_empty_tweets(directory="nursetweets"):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            df = pd.read_csv(f)
            df['text'].replace('', np.nan, inplace=True)
            df.dropna(subset=['text'], inplace=True)
            df.to_csv(f, index=False)


def check_repeated_tweets(df):
    boolean = df['id'].duplicated(keep='last') # True
    return df[~boolean]

def text_preprocessing(directory="nursetweets"):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file

        if os.path.isfile(f):
            print(f)
            df = pd.read_csv(f)
            df = check_repeated_tweets(df)
            # remove tweets with 'wordle' in it
            df = remove_wordle(df)

            # make RT's empty
            df['text'] = df['text'].loc[~df['text'].str.startswith('RT ', na=False)]  # remove RT's

            # remove and bug where & turns into "&amp;"
            df['text'] = df['text'].apply(lambda x: remove_and_bug(x))

            # remove empty tweets
            df['text'].replace('', np.nan, inplace=True)
            df.dropna(subset=['text'], inplace=True)

            df['clean_text'] = df['text']

            # remove urls
            df['clean_text'] = df['clean_text'].apply(lambda x: remove_URL(x))

            # remove hashtage
            df['clean_text'] = df['clean_text'].apply(lambda x: remove_hashtags_mentions(x))

            # lower case
            df['clean_text'] = df['clean_text'].apply(lambda x: x.lower())

            # remove non alphabet chars
            df['clean_text'] = df['clean_text'].apply(lambda x: remove_nonalphabet(x))

            # remove now empty tweets
            df['clean_text'].replace('', np.nan, inplace=True)
            df.dropna(subset=['clean_text'], inplace=True)

            try:
                df = delete_whitespace_tweets(df)
            except Exception as e:
                print("couldn't delete whitespace tweets. error:", e)

            # add column of only nouns
            df['nouns'] = df['clean_text'].apply(lambda x: get_nouns(str(x)))

            #remove now empty tweets
            df['nouns'].replace('', np.nan, inplace=True)
            df.dropna(subset=['nouns'], inplace=True)


            # lemmatizing
            df['nouns'] = df['nouns'].apply(lambda x:lemmatizer(str(x)))

            # remove stopwords
            df['nouns'] = df['nouns'].apply(lambda x:remove_stopwords(str(x)))

            # #remove 2 char words
            df['nouns'] = df['nouns'].apply(lambda x:remove_2char_words(str(x)))

            df.drop(['lemm_nouns', 'non_english', 'Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'], axis=1, inplace=True,
                    errors='ignore')

            df.to_csv(f, index=False)

# run remove_empty before this
text_preprocessing()
# run remove_empty after this
