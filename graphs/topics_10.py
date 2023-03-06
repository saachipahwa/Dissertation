import pandas as pd
from bertopic import BERTopic
import os
import numpy as np

from matplotlib import pyplot as plt

def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir("Dissertation/"+directory):
        f = os.path.join("Dissertation/"+directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df


def get_topics_with_dates():
    model = BERTopic.load("nursetweets_10_1_model")
    df = model.get_document_info(get_all_tweets("nursetweets")['nouns'])
    df["original_text"] = get_all_tweets("nursetweets")['text']
    df["created_at"] = get_all_tweets("nursetweets")['created_at']

    df.to_csv("Dissertation/graphs/topics_with_dates.csv")


# get_topics_with_dates()

def box_plot():
    # first lockdown
    first_lockdown_df = pd.read_csv("Dissertation/graphs/first_lockdown.csv", error_bad_lines=False)
    fl_counts_df = first_lockdown_df['label'].value_counts()
    first_lockdown = [fl_counts_df["Life"]/len(first_lockdown_df), fl_counts_df["Work"]/len(first_lockdown_df)]
    print("first", first_lockdown)

    second_lockdown_df = pd.read_csv("Dissertation/graphs/second_lockdown.csv", error_bad_lines=False)
    sl_counts_df = second_lockdown_df['label'].value_counts()
    second_lockdown = [sl_counts_df["Life"]/len(second_lockdown_df), sl_counts_df["Work"]/len(second_lockdown_df)]
    print("second", second_lockdown)

    third_lockdown_df = pd.read_csv("Dissertation/graphs/third_lockdown.csv", error_bad_lines=False)
    tl_counts_df = third_lockdown_df['label'].value_counts()
    third_lockdown = [tl_counts_df["Life"]/len(third_lockdown_df), tl_counts_df["Work"]/len(third_lockdown_df)]
    print("third", third_lockdown)

    categories = ["Life", "Work"]
    # fig, ax = plt.subplots()
    # ax.bar(categories, first_lockdown, label = "First lockdown (26th March 2020 to 10th May 2020)")
    # data = [first_lockdown,
    #     second_lockdown,
    #     third_lockdown]
    #
    # ax.legend()
    # ax.set_xlabel("Topic label")
    # ax.set_ylabel("Percentage of tweets")
    # ax.set_ylim(0, 1)
    # plt.show()

    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))


    # Set position of bar on X axis
    br1 = np.arange(len(first_lockdown))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    # Make the plot
    plt.bar(br1, first_lockdown, color ='r', width = barWidth,
            edgecolor ='grey', label = "First lockdown (26th March 2020 to 10th May 2020)")
    plt.bar(br2, second_lockdown, color ='g', width = barWidth,
            edgecolor ='grey', label = "Second lockdown (5th November to 2nd December 2020)")
    plt.bar(br3, third_lockdown, color ='b', width = barWidth,
            edgecolor ='grey', label = "Third lockdown (6th January to 8th March 2021)")

    # Adding Xticks
    plt.xlabel("Topic label", fontweight ='bold', fontsize = 15)
    plt.ylabel("Percentage of tweets", fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(first_lockdown))],
               categories)

    plt.legend()
    plt.show()

# box_plot()

def lockdown_tweets():
    df = pd.read_csv("Dissertation/graphs/topics_with_dates.csv")
    #dropping columns
    df.drop(['tier', 'Unnamed: 0', 'Unnamed: 0.1.1.1'], axis=1, inplace=True,
            errors='ignore')
    df.to_csv("Dissertation/graphs/topics_with_dates.csv")

    #sorting by date and adding new index
    # df.sort_values(by='created_at', inplace=True)
    # df.reset_index(drop=True, inplace=True)
    # df.to_csv("Dissertation/graphs/topics_with_dates.csv")

    #find indexes for start and end dates of lockdown periods
    #confirm first lockdown dates
    # df_startdate = df[df['created_at'].str.match("2020-03-26")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-05-10")]
    # print(df_enddate)

    #confirm second lockdown dates
    # df_startdate = df[df['created_at'].str.match("2020-11-05")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-12-02")]
    # print(df_enddate)

    #confirm third lockdown dates
    # df_startdate = df[df['created_at'].str.match("2021-01-06")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-03-08")]
    # print(df_enddate)

    #first lockdown 10839 to 13703
    # first_lockdown = df.iloc[10839:13703]
    # first_lockdown.to_csv("Dissertation/graphs/first_lockdown.csv")

    # #second lockdown 25517 to 27893
    # second_lockdown = df.iloc[25517:27893]
    # second_lockdown.to_csv("Dissertation/graphs/second_lockdown.csv")

    # #third lockdown 30529 to 37921
    # third_lockdown = df.iloc[30529:37921]
    # third_lockdown.to_csv("Dissertation/graphs/third_lockdown.csv")

# lockdown_tweets()

def dynamic_topic_modelling():
    dates_df = pd.read_csv("Dissertation/graphs/topics_with_dates.csv")
    model_copy = BERTopic.load("nursetweets_10_1_model_copy")
    model_copy.merge_topics(get_all_tweets("nursetweets")['nouns'],
                            [[2], [0, 1, 3, 4, 5, 6, 7, 8, 9]])
    model_copy.set_topic_labels({-1: "Work", 0: "Life"})
    print(model_copy.get_topic_info())
    topics_over_time = model_copy.topics_over_time(
        dates_df['Document'], dates_df['created_at'], datetime_format="%Y-%m-%d %H:%M:%S+00:00", nr_bins=30)
    fig = model_copy.visualize_topics_over_time(
        topics_over_time, topics=[0, 1], custom_labels=True)
    fig.show()


# dynamic_topic_modelling()


def add_topic_label():
    df = pd.read_csv("Dissertation/graphs/topics_with_dates.csv")

    conditions = [
        (df['Topic'] != -1) & (df['Topic'] != 2),
        (df['Topic'] == -1),
        (df['Topic'] == 2)
    ]

    values = ["Life", "None", "Work"]
    df['label'] = np.select(conditions, values)
    df.to_csv("Dissertation/graphs/topics_with_dates.csv")
    print(df.head())


# add_topic_label()

def dynamic_box_plot():
    df = pd.read_csv("Dissertation/graphs/topics_with_dates.csv")
    df.sort_values(by='created_at', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv("Dissertation/graphs/topics_with_dates.csv")

    # first_lockdown.to_csv("Dissertation/graphs/first_lockdown.csv")


# dynamic_box_plot()

# def words_per_topic():
#     model_copy = BERTopic.load("nursetweets_10_1_model_copy")
#     model_copy.merge_topics(get_all_tweets("nursetweets")['nouns'],
#                             [[-1, 2], [0, 1, 3, 4, 5, 6, 7, 8, 9]])
#     model_copy.set_topic_labels({-1: "Work", 0: "Life"})

#     fig = model_copy.visualize_barchart(topics=[-1, 0], custom_labels=True)
#     fig.show()

# words_per_topic()

def top_terms_normal():
    model = BERTopic.load("old_nurse_model/nursetweets_10_1_model_old")
    print(model.get_topic_info())
    fig = model.visualize_barchart(topics=[0,1,2,3,4,5,6,7,8,9])    
    fig.show()

# top_terms_normal()

def top_terms_merged():
    model = BERTopic.load("old_nurse_model/merged")
    model.merge_topics(get_all_tweets("nursetweets")['nouns'],
                   [[0, 1, 3, 4, 5, 6, 7, 8, 9]])
    model.set_topic_labels({-1: "None", 0: "Life", 1: "Work"})

    print(model.get_topic_info())

    fig = model.visualize_barchart(topics=[-1,0,1],n_words=20, custom_labels=True)    
    fig.show()


def work_term_frequency():
    top10terms_work = ['time', 'year', 'nurse', 'today', 'people', 'thank', 'nursing', 'care', 'morning', 'work']
    first_lockdown_df = pd.read_csv("graphs/first_lockdown.csv", error_bad_lines=False)
    second_lockdown_df = pd.read_csv("graphs/second_lockdown.csv", error_bad_lines=False)
    third_lockdown_df = pd.read_csv("graphs/third_lockdown.csv", error_bad_lines=False)
    
    #ønly use work tweets
    work_df_1 = first_lockdown_df[first_lockdown_df['label']=="Work"]
    work_df_2 = second_lockdown_df[second_lockdown_df['label']=="Work"]
    work_df_3 = third_lockdown_df[third_lockdown_df['label']=="Work"]

    work_text_1 = ' '.join(work_df_1["Document"])
    work_text_2 = ' '.join(work_df_2["Document"])
    work_text_3 = ' '.join(work_df_3["Document"])

    work_words_1 = work_text_1.split()
    work_words_2 = work_text_2.split()
    work_words_3 = work_text_3.split()

    word_count_1 = pd.value_counts(np.array(work_words_1))
    word_count_2 = pd.value_counts(np.array(work_words_2))
    word_count_3 = pd.value_counts(np.array(work_words_3))
    print(word_count_1)

    terms_count_1 = []
    terms_count_2 = []
    terms_count_3 = []

    for w in top10terms_work:
        terms_count_1.append(word_count_1[w]/len(work_words_1))
        terms_count_2.append(word_count_2[w]/len(work_words_2))
        terms_count_3.append(word_count_3[w]/len(work_words_3))

    return terms_count_1, terms_count_2, terms_count_3

def life_term_frequency():
    top10terms_work = ['time', 'thank', 'nurse', 'morning', 'today', 'year', 'people', 'work', 'week', 'care']
    first_lockdown_df = pd.read_csv("Dissertation/graphs/first_lockdown.csv", error_bad_lines=False)
    second_lockdown_df = pd.read_csv("Dissertation/graphs/second_lockdown.csv", error_bad_lines=False)
    third_lockdown_df = pd.read_csv("Dissertation/graphs/third_lockdown.csv", error_bad_lines=False)
    
    #ønly use life tweets
    life_df_1 = first_lockdown_df[first_lockdown_df['label']=="Life"]
    life_df_2 = second_lockdown_df[second_lockdown_df['label']=="Life"]
    life_df_3 = third_lockdown_df[third_lockdown_df['label']=="Life"]

    life_text_1 = ' '.join(life_df_1["Document"])
    life_text_2 = ' '.join(life_df_2["Document"])
    life_text_3 = ' '.join(life_df_3["Document"])

    life_words_1 = life_text_1.split()
    life_words_2 = life_text_2.split()
    life_words_3 = life_text_3.split()

    life_count_1 = pd.value_counts(np.array(life_words_1))
    life_count_2 = pd.value_counts(np.array(life_words_2))
    life_count_3 = pd.value_counts(np.array(life_words_3))

    terms_count_1 = []
    terms_count_2 = []
    terms_count_3 = []

    for w in top10terms_work:
        terms_count_1.append(life_count_1[w]/len(life_words_1))
        terms_count_2.append(life_count_2[w]/len(life_words_2))
        terms_count_3.append(life_count_3[w]/len(life_words_3))

    print(terms_count_1, "\n", terms_count_2, "\n", terms_count_3)

life_term_frequency()
def plot_term_frequency(label = None,
                        terms = None,
                        lockdown1_counts=None, lockdown2_counts=None, lockdown3_counts=None):
    #set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))

    # Set position of bar on X axis
    br1 = np.arange(len(lockdown1_counts))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    # Make the plot
    plt.bar(br1, lockdown1_counts, color ='r', width = barWidth,
            edgecolor ='grey', label = "First lockdown (26th March 2020 to 10th May 2020)")
    plt.bar(br2, lockdown2_counts, color ='g', width = barWidth,
            edgecolor ='grey', label = "Second lockdown (5th November to 2nd December 2020)")
    plt.bar(br3, lockdown3_counts, color ='b', width = barWidth,
            edgecolor ='grey', label = "Third lockdown (6th January to 8th March 2021)")

    # Adding Xticks
    plt.xlabel("Topic label", fontweight ='bold', fontsize = 15)
    plt.ylabel(f"Percentage of tweets containing {label} terms", fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(lockdown1_counts))],
               terms)

    plt.legend()
    plt.show()

plot_term_frequency(label="Work",
                    terms = ['time', 'year', 'nurse', 'today', 'people', 'thank', 'nursing', 'care', 'morning', 'work'],
                    lockdown1_counts = [0.01664132454806555, 0.005575266092245312, 0.008109477952356817, 0.008025004223686433, 0.011572900827842542, 0.013515796587261361, 0.002196316945429971, 0.005575266092245312, 0.0033789491468153403, 0.007856056766345666],
                    lockdown2_counts= [0.014565596471432967, 0.009847163811672992, 0.012924402502820802, 0.008411119089137347, 0.010565186172940815, 0.00912914145040517, 0.0034875371833008512, 0.0124115293876295, 0.004205559544568673, 0.006359626628372141],
                    lockdown3_counts=[0.012965186074429771, 0.009981135311267365, 0.010358429085920082, 0.008266163608300464, 0.011490310409878237, 0.008060367003944436, 0.00329274566969645, 0.007820270965529069, 0.005282112845138055, 0.008780655119190533])
plot_term_frequency(label="Life",
                    terms=['time', 'thank', 'nurse', 'morning', 'today', 'year', 'people', 'work', 'week', 'care'],
                    lockdown1_counts = [0.023994811932555125, 0.05512321660181582, 0.00324254215304799, 0.009079118028534372, 0.007782101167315175, 0.005188067444876783, 0.013618677042801557, 0.007133592736705577, 0.019455252918287938, 0.005188067444876783] ,
                    lockdown2_counts=  [0.0273224043715847, 0.040983606557377046, 0.00273224043715847, 0.01639344262295082, 0.007285974499089253, 0.007285974499089253, 0.007285974499089253, 0.01092896174863388, 0.017304189435336976, 0.00273224043715847] ,
                    lockdown3_counts = [0.02161681966242227, 0.04471424341131182, 0.0038495706248149247, 0.018359490672194254, 0.0071068996150429374, 0.009179745336097127, 0.01599052413384661, 0.013029315960912053, 0.014213799230085875, 0.00414569144210838])
