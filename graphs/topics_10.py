import pandas as pd
from bertopic import BERTopic
import os
import numpy as np
import matplotlib.pyplot as plt


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
    # df.sort_values(by='created_at', inplace=True)
    # df.drop("Unnamed", "Unnamed: 0", "Unnamed: 0.1", "Unnamed: 0.2")
    # df.reset_index(drop=True, inplace=True)
    # df.to_csv("Dissertation/graphs/topics_with_dates.csv")
    print(len(df))
    # first_lockdown.to_csv("Dissertation/graphs/first_lockdown.csv")


dynamic_box_plot()

# def lockdown_tweets():
# df = pd.read_csv("graphs/topics_with_dates.csv")
# dropping columns
# df.drop(['tier', 'Unnamed: 0', 'Unnamed: 0.1.1.1'], axis=1, inplace=True,
#         errors='ignore')
# df.to_csv("graphs/topics_with_dates.csv")

# sorting bhy date and adding new index
# df.sort_values(by='created_at', inplace=True)
# df.reset_index(drop=True, inplace=True)
# df.to_csv("graphs/topics_with_dates.csv")

# find indexes for start and end dates of lockdown periods
# df_startdate = df[df['created_at'].str.match("2021-01-06")]
# print(df_startdate)
# df_enddate = df[df['created_at'].str.match("2021-03-08")]
# print(df_enddate)

# first lockdown 10839 to 13703
# first_lockdown = df.iloc[10839:13703]
# print(first_lockdown)
# first_lockdown.to_csv("graphs/first_lockdown.csv")

# second lockdown 25517 to 27893
# second_lockdown = df.iloc[25517:27893]
# second_lockdown.to_csv("graphs/second_lockdown.csv")

# third lockdown 30529 to 37921
# third_lockdown = df.iloc[30529:37921]
# third_lockdown.to_csv("graphs/third_lockdown.csv")

# lockdown_tweets()


def box_plot():
    # first lockdown
    first_lockdown_df = pd.read_csv(
        "graphs/first_lockdown.csv", error_bad_lines=False)
    fl_counts_df = first_lockdown_df['label'].value_counts()
    first_lockdown = [fl_counts_df["Life"] /
                      len(first_lockdown_df), fl_counts_df["Work"]/len(first_lockdown_df)]
    print("first", first_lockdown)

    second_lockdown_df = pd.read_csv(
        "graphs/second_lockdown.csv", error_bad_lines=False)
    sl_counts_df = second_lockdown_df['label'].value_counts()
    second_lockdown = [sl_counts_df["Life"] /
                       len(second_lockdown_df), sl_counts_df["Work"]/len(second_lockdown_df)]
    print("second", second_lockdown)

    third_lockdown_df = pd.read_csv(
        "graphs/third_lockdown.csv", error_bad_lines=False)
    tl_counts_df = third_lockdown_df['label'].value_counts()
    third_lockdown = [tl_counts_df["Life"] /
                      len(third_lockdown_df), tl_counts_df["Work"]/len(third_lockdown_df)]
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
    fig = plt.subplots(figsize=(12, 8))

    # Set position of bar on X axis
    br1 = np.arange(len(first_lockdown))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    # Make the plot
    plt.bar(br1, first_lockdown, color='r', width=barWidth,
            edgecolor='grey', label="First lockdown (26th March 2020 to 10th May 2020)")
    plt.bar(br2, second_lockdown, color='g', width=barWidth,
            edgecolor='grey', label="Second lockdown (5th November to 2nd December 2020)")
    plt.bar(br3, third_lockdown, color='b', width=barWidth,
            edgecolor='grey', label="Third lockdown (6th January to 8th March 2021)")

    # Adding Xticks
    plt.xlabel("Topic label", fontweight='bold', fontsize=15)
    plt.ylabel("Percentage of tweets", fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(first_lockdown))],
               categories)

    plt.legend()
    plt.show()


box_plot()

# def words_per_topic():
#     model_copy = BERTopic.load("nursetweets_10_1_model_copy")
#     model_copy.merge_topics(get_all_tweets("nursetweets")['nouns'],
#                             [[-1, 2], [0, 1, 3, 4, 5, 6, 7, 8, 9]])
#     model_copy.set_topic_labels({-1: "Work", 0: "Life"})

#     fig = model_copy.visualize_barchart(topics=[-1, 0], custom_labels=True)
#     fig.show()

# words_per_topic()
