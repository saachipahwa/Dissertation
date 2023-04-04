import pandas as pd
from bertopic import BERTopic
import os
import numpy as np
from matplotlib import pyplot as plt

directories = ["nursetweets", "doctortweets", "teachertweets",
               "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 2
directory_name = directories[directory_index]
profession_name = "teacher"
nr_topics = 10
work_topics = [1,7]

#TEACHER:
top_work_terms = ['holiday', 'week', 'summer', 'easter', 'bank', 'term', 'food', 'solidarity', 'school', 'recovery', 'money', 'funding', 'school', 'charity', 'donation', 'budget', 'fund', 'penny', 'cell', 'pocket']
topic_0 = ['tweet', 'twitter', 'account', 'people', 'reply']
topic_2 = ['morning', 'james', 'claire', 'paul', 'nicola']
topic_3 = ['enjoy', 'bird', 'today', 'theme', 'butterfly']
topic_4 = ['thanks', 'hope', 'look', 'care', 'sorry']
topic_5 = ['thank', 'kind', 'thanks', 'bridge', 'touch']
topic_6 = ['energy', 'price', 'bill', 'cost', 'water']
topic_8 = ['coffee', 'cake', 'chocolate', 'biscuit', 'sleep']
topic_9 = ['family', 'love', 'compassion', 'chair', 'thought']
all_terms = [top_work_terms, topic_0, topic_2, topic_3, topic_4, topic_5, topic_6, topic_8, topic_9]
topic_names = ["Twitter activity", #for teacherspy
                "School and  holidays",
                "Good mornings",
                "Nature",
                "Well wishes",
                "Thank you's",
                "Finances",
                "School funding",
                "Meals",
                "Loving wishes"]
# top_work_terms = ['shift', 'night', 'tonight', 'match', 'ward', 'sleep', 'game', 'bless', 'emotion', 'today']
# topic_0 = ['morning', 'hope', 'coffee', 'thing', 'weekend']
# topic_1 = ['thank', 'enjoy', 'brilliant', 'support', 'thankyou']
# topic_3 = ['congratulation', 'luck', 'award', 'jenny', 'achievement']
# topic_4 = ['thanks', 'follow', 'work', 'welcome', 'wait']
# topic_5 = ['birthday', 'heart', 'dance', 'treat', 'miss']
# topic_6 = ['week', 'mile', 'start', 'monday', 'hill']
# topic_7 = ['time', 'girl', 'something', 'article', 'kind']
# topic_8 = ['food', 'school', 'life', 'meal', 'child']
# topic_9 = ['friend', 'kenny', 'home', 'point', 'morning']
# all_terms = [top_work_terms, topic_0, topic_1, topic_3, topic_4, topic_5, topic_6, topic_7, topic_8, topic_9]
# topic_names = ["Good morning",
#                   "Thank you's",
#                       "WORK",
#                   "Congratulations",
#                   "Expressions",
#                   "Happy birthday",
#                   "Exercise",
#                   "Miscellaneous",
#                   "General life",
#                   "Friends & people",
#                     ]

before1 = pd.read_csv(f"graphs/{profession_name}s/before_first_lockdown.csv")
during1 = pd.read_csv(f"graphs/{profession_name}s/first_lockdown.csv")
after1 = pd.read_csv(f"graphs/{profession_name}s/after_first_lockdown.csv")
before2 = pd.read_csv(f"graphs/{profession_name}s/before_second_lockdown.csv")
during2 = pd.read_csv(f"graphs/{profession_name}s/second_lockdown.csv")
after2 = pd.read_csv(f"graphs/{profession_name}s/after_second_lockdown.csv")
before3 = pd.read_csv(f"graphs/{profession_name}s/before_third_lockdown.csv")
during3 = pd.read_csv(f"graphs/{profession_name}s/third_lockdown.csv")
after3 = pd.read_csv(f"graphs/{profession_name}s/after_third_lockdown.csv")

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
#
# def freq_change_plot(df1, df2, which_lockdown, df1_label, df2_label):
#     initial_work_change, initial_life_change = frequency_change(df1, df2) #pre filtering using 0.005 threshold
#     initial_terms = get_all_terms()
#     print(initial_work_change)
#     work_change = []
#     life_change = []
#     terms = []
#     for i in range(0, len(terms)):
#         if abs(initial_work_change[i])>0.005 or abs(initial_life_change[i])>0.005:
#             work_change.append(work_change[i])
#             life_change.append(life_change[i])
#             terms.append(terms[i])
#     print("work", work_change)
#     print("terms", terms)
#
#     workdict = {terms[i]: work_change[i] for i in range(len(terms))}
#     lifedict = {terms[i]: life_change[i] for i in range(len(terms))}
#     workdict = dict(sorted(workdict.items(), key=lambda item: item[1]))
#     # lifedict= dict(sorted(lifedict.items(), key=lambda item: item[1]))
#
#     work = plt.scatter(y=list(workdict.keys()), x = list(workdict.values()), color = "blue")
#     life = plt.scatter(y=list(lifedict.keys()), x=list(lifedict.values()), color = "orange")
#     plt.legend((work, life),
#                ('Work', 'Life'),
#                loc='best',
#                fontsize=12)
#     plt.title(f"Frequency change {df1_label} and {df2_label} the {which_lockdown} lockdown")
#     plt.xlabel("Frequency gain")
#     plt.ylabel("Term")
#     plt.grid()
#     plt.show()

def freq_change_plot(df1, df2, which_lockdown, df1_label, df2_label):
    initial_work_change, initial_life_change = frequency_change(df1, df2) #pre filtering using 0.005 threshold
    initial_terms = get_all_terms()
    work_change = []
    life_change = []
    terms = []
    for i in range(0, len(initial_terms)):
        if abs(initial_work_change[i])>0.005 or abs(initial_life_change[i])>0.005:
            # print(initial_terms[i], initial_work_change[i], initial_life_change[i])
            work_change.append(initial_work_change[i])
            life_change.append(initial_life_change[i])
            terms.append(initial_terms[i])
    # print('life', life_change)
    # print("work", work_change)
    # print("terms", terms)

    workdict = {terms[i]: work_change[i] for i in range(len(terms))}
    lifedict = {terms[i]: life_change[i] for i in range(len(terms))}
    # workdict = dict(sorted(workdict.items(), key=lambda item: item[1]))
    # lifedict= dict(sorted(lifedict.items(), key=lambda item: item[1]))

    work = plt.scatter(y=list(workdict.keys()), x = list(workdict.values()), color = "blue")
    life = plt.scatter(y=list(lifedict.keys()), x=list(lifedict.values()), color = "orange")
    plt.legend((work, life),
           ('Work', 'Life'),
           loc='best',
           fontsize=12)
    plt.title(f"Frequency change {df1_label} and {df2_label} the {which_lockdown} lockdown")
    plt.xlabel("Frequency change")
    plt.ylabel("Term")
    plt.grid()
    plt.show()

# freq_change_plot(before1, during1, which_lockdown="first", df1_label = "before", df2_label = "during")
# freq_change_plot(before2, during2, which_lockdown="second", df1_label = "before", df2_label = "during")
# freq_change_plot(before2, during2, which_lockdown="third", df1_label = "before", df2_label = "during")
# freq_change_plot(during1, after1, which_lockdown="first", df1_label = "during", df2_label = "after")
# freq_change_plot(during2, after2, which_lockdown="second", df1_label = "during", df2_label = "after")
# freq_change_plot(during3, after3, which_lockdown="third", df1_label = "during", df2_label = "after")

def compare_life_work(df1, df2, which_lockdown, df1_label, df2_label):
    # first lockdown
    df1_counts = df1['label'].value_counts()
    df1_array = [df1_counts["Life"]/len(df1), df1_counts["Work"]/len(df1)]

    df2_counts = df2['label'].value_counts()
    df2_array = [df2_counts["Life"]/len(df1), df2_counts["Work"]/len(df1)]

    categories = ["Life", "Work"]

    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))


    # Set position of bar on X axis
    br1 = np.arange(len(df1_array))
    br2 = [x + barWidth for x in br1]

    # Make the plot
    plt.bar(br1, df1_array, color ='r', width = barWidth,
            edgecolor ='grey', label = f"{df1_label} the {which_lockdown} lockdown")
    plt.bar(br2, df2_array, color ='g', width = barWidth,
            edgecolor ='grey', label = f"{df2_label} the {which_lockdown} lockdown")

    # Adding Xticks
    plt.xlabel("Topic label", fontweight ='bold', fontsize = 15)
    plt.ylabel("Percentage of tweets", fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(df1_array))],
               categories)

    plt.legend()
    plt.show()

# compare_life_work(during2, after2, "second", "During", "After")

#colour for before = red
#colour for during = green
#colour for after = blue
def compare_topics(df1, df2, topics, which_lockdown, df1_label, df2_label, colour_label1, colour_label2):
    #Add percentage values to arrays
    df1_counts = df1['Topic'].value_counts()
    df1_array=[]
    for i in topics:
        df1_array.append((df1_counts[i]/len(df1))*100)
    print("df1", df1)

    df2_counts = df2['Topic'].value_counts()
    df2_array=[]
    for j in topics:
        df2_array.append((df2_counts[j]/len(df2))*100)
    print("df2", df2)

    #add work at end
    for k in work_topics:
        df1_array.append((df1_counts[k]/len(df1))*100)
        df2_array.append((df2_counts[k]/len(df2))*100)

    categories=[]
    for l in topics:
        categories.append(topic_names[l])
    
    for m in work_topics:
        categories.append(topic_names[m]) # add work at end

    barWidth = 0.25
    fig = plt.subplots(figsize =(15, 8))

    br1 = np.arange(len(df1_array))
    br2 = [x + barWidth for x in br1]

    # Make the plot
    print("df1 array", df1_array)
    print("df2 array", df2_array)
    plt.bar(br1, df1_array, color =colour_label1, width = barWidth,
            edgecolor ='grey', label = f"{df1_label} the {which_lockdown} lockdown")
    plt.bar(br2, df2_array, color =colour_label2, width = barWidth,
            edgecolor ='grey', label = f"{df2_label} the {which_lockdown} lockdown")

    # Adding Xticks
    plt.xlabel("Topic number and name", fontweight ='bold', fontsize = 15)
    plt.ylabel("Percentage of tweets", fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(df1_array))],
               categories)

    plt.title(f"Distribution of topics discussed {df1_label} compared to {df2_label} the {which_lockdown} lockdown")
    plt.legend()
    plt.show()

topics = [2,3,4,5,6,8]
compare_topics(before1, during1, topics, 'First', 'Before', 'During', 'r', 'g')
compare_topics(before2, during2, topics, 'Second', 'Before', 'During', 'r', 'g')
compare_topics(before3, during3, topics, 'Third', 'Before', 'During', 'r', 'g')

compare_topics(during1, after1,  topics, 'First', 'During', 'After', 'g', 'b')
compare_topics(during2, after2,  topics, 'Second', 'During', 'After', 'g', 'b')
compare_topics(during3, after3,  topics, 'Third', 'During', 'After', 'g', 'b')


