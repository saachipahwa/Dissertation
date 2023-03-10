import pandas as pd
from bertopic import BERTopic
import os
import numpy as np
from matplotlib import pyplot as plt


top_work_terms = ['shift', 'night', 'tonight', 'match', 'ward', 'sleep', 'game', 'bless', 'emotion', 'today']
topic_0 = ['morning', 'hope', 'coffee', 'thing', 'weekend']
topic_1 = ['thank', 'enjoy', 'brilliant', 'support', 'thankyou']
topic_3 = ['congratulation', 'luck', 'award', 'jenny', 'achievement']
topic_4 = ['thanks', 'follow', 'work', 'welcome', 'wait']
topic_5 = ['birthday', 'heart', 'dance', 'treat', 'miss']
topic_6 = ['week', 'mile', 'start', 'monday', 'hill']
topic_7 = ['time', 'girl', 'something', 'article', 'kind']
topic_8 = ['food', 'school', 'life', 'meal', 'child']
topic_9 = ['friend', 'kenny', 'home', 'point', 'morning']

all_terms = [top_work_terms, topic_0, topic_1, topic_3, topic_4, topic_5, topic_6, topic_7, topic_8, topic_9]

before1 = pd.read_csv("graphs/before_first_lockdown.csv")
during1 = pd.read_csv("graphs/first_lockdown.csv")
after1 = pd.read_csv("graphs/after_first_lockdown.csv")
before2 = pd.read_csv("graphs/before_second_lockdown.csv")
during2 = pd.read_csv("graphs/second_lockdown.csv")
after2 = pd.read_csv("graphs/after_second_lockdown.csv")
before3 = pd.read_csv("graphs/before_third_lockdown.csv")
during3 = pd.read_csv("graphs/third_lockdown.csv")
after3 = pd.read_csv("graphs/after_third_lockdown.csv")

def get_all_terms():
    array = []
    for topic in all_terms:
        for term in topic:
            array.append(term)
    return array

def get_freq_gain(df1, df2):
    #return array of frequency gain between df1 and df2 for each term
    df1_words = ' '.join(df1["Document"]).split()
    df2_words = ' '.join(df2["Document"]).split()
    df1_word_counts = pd.value_counts(np.array(df1_words))
    df2_word_counts = pd.value_counts(np.array(df2_words))
    df1_freq = []
    df2_freq = []
    terms = get_all_terms()
    print("number of terms", len(terms))

    for term in terms:
        try:
            df1_freq.append(df1_word_counts[term]/len(df1_words))
        except Exception as e:
            df1_freq.append(0)
        try:
            df2_freq.append(df2_word_counts[term]/len(df2_words))
        except Exception as e:
            df2_freq.append(0)

    freq_change =[]

    for i in range(0, len(terms)):
        freq_change.append(df2_freq[i]-df1_freq[i])

    print("df1_freq length", len(df1_freq))
    print("df1_freq length", len(df2_freq))
    print("freq change length", len(freq_change))

    return freq_change       
    

def frequency_change(df1, df2):
    df1_work = df1[df1['label']=="Work"]
    df1_life = df1[df1['label']=="Life"]
    df2_work = df2[df2['label']=="Work"]
    df2_life = df2[df2['label']=="Life"]
    work_gain = get_freq_gain(df1_work, df2_work)
    life_gain = get_freq_gain(df1_life, df2_life)
    return work_gain, life_gain

# frequency_change()

def freq_change_plot(df1, df2, which_lockdown, df1_label, df2_label):
    work_change, life_change = frequency_change(df1, df2)
    terms = get_all_terms()
    workdict = {terms[i]: work_change[i] for i in range(len(terms))}
    lifedict = {terms[i]: life_change[i] for i in range(len(terms))}
    # workdict_sorted = dict(sorted(workdict.items(), key=lambda item: item[1]))
    # life_dict_sorted = dict(sorted(lifedict.items(), key=lambda item: item[1]))

    work = plt.scatter(y=list(workdict.keys()), x = list(workdict.values()), color = "blue")
    life = plt.scatter(y=list(lifedict.keys()), x=list(lifedict.values()), color = "orange")
    plt.legend((work, life),
           ('Work', 'Life'),
           loc='best',
           fontsize=12)
    plt.title(f"Frequency change {df1_label} and {df2_label} the {which_lockdown} lockdown")
    plt.xlabel("Frequency gain")
    plt.ylabel("Term")
    plt.grid()
    plt.show()

freq_change_plot(during3, after3, which_lockdown="third", df1_label = "during", df2_label = "after")
