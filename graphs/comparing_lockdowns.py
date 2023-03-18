
import pandas as pd
from bertopic import BERTopic
import os
import numpy as np

from matplotlib import pyplot as plt

def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0)
        df = pd.concat([df, user_df], ignore_index=True)
    return df


def get_before_lockdown():
    df = pd.read_csv("graphs/topics_with_dates.csv")

    #get index range for 46 days before first lockdown 
    # df_startdate = df[df['created_at'].str.match("2020-02-09")] 
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-03-25")]
    # print(df_enddate)

    # make docs csv of first lockdown 8938 to 10838
    before_first_lockdown = df.iloc[8938:10839]
    before_first_lockdown.to_csv("graphs/before_first_lockdown.csv")

    #get index range for 27 days before second lockdown 
    # df_startdate = df[df['created_at'].str.match("2020-10-09")] 
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-11-04")]
    # print(df_enddate)

    # make docs csv of second lockdown 23578 to 25516
    before_second_lockdown = df.iloc[23578:25517]
    before_second_lockdown.to_csv("graphs/before_second_lockdown.csv")

    #get index range for 62 days before third lockdown
    # df_startdate = df[df['created_at'].str.match("2020-11-06")] 
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-01-05")]
    # print(df_enddate)

    # make docs csv of third lockdown 25613 to 30528
    before_third_lockdown = df.iloc[25613:30529]
    before_third_lockdown.to_csv("graphs/before_third_lockdown.csv")

# get_before_lockdown()

def get_lockdown_tweets():
    df = pd.read_csv("graphs/topics_with_dates.csv")
    #dropping columns
    # df.drop(['tier', 'Unnamed: 0', 'Unnamed: 0.1.1.1'], axis=1, inplace=True,
    #         errors='ignore')
    # df.to_csv("Dissertation/graphs/topics_with_dates.csv")

    #sorting by date and adding new index
    # df.sort_values(by='created_at', inplace=True)
    # df.reset_index(drop=True, inplace=True)
    # df.to_csv("Dissertation/graphs/topics_with_dates.csv")

    #find indexes for start and end dates of lockdown periods
    #confirm first lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-03-26")] 
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-05-10")] #46 days
    # print(df_enddate)

    #confirm second lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-11-05")] 
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-12-02")] #28 days
    # print(df_enddate)

    #confirm third lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2021-01-06")] 
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-03-08")] #62 days
    # print(df_enddate)

    # first lockdown 10839 to 13703
    first_lockdown = df.iloc[10839:13704]
    first_lockdown.to_csv("graphs/first_lockdown.csv")

    #second lockdown 25517 to 27893
    second_lockdown = df.iloc[25517:27894]
    second_lockdown.to_csv("graphs/second_lockdown.csv")

    #third lockdown 30529 to 37921
    third_lockdown = df.iloc[30529:37922]
    third_lockdown.to_csv("graphs/third_lockdown.csv")
    # print(third_lockdown[third_lockdown['Topic']==2])

# get_lockdown_tweets()
def get_after_lockdown():
    df = pd.read_csv("graphs/topics_with_dates.csv")

    #get index range for 46 days after first lockdown
    # df_startdate = df[df['created_at'].str.match("2020-05-11")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-06-18")]
    # print(df_enddate)

    # make docs csv of first lockdown 13704 to 16139
    # before_first_lockdown = df.iloc[13704:16140]
    # before_first_lockdown.to_csv("graphs/after_first_lockdown.csv")

    #get index range for 27 days after second lockdown
    # df_startdate = df[df['created_at'].str.match("2020-12-03")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-12-29")]
    # print(df_enddate)

    # make docs csv of second lockdown 27894 to 29883
    # before_second_lockdown = df.iloc[27894:29884]
    # before_second_lockdown.to_csv("graphs/after_second_lockdown.csv")

    #get index range for 62 days after third lockdown
    # df_startdate = df[df['created_at'].str.match("2021-03-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-06-09")]
    # print(df_enddate)
    #
    # make docs csv of third lockdown 37922 to 47140
    before_third_lockdown = df.iloc[37922:47141]
    before_third_lockdown.to_csv("graphs/after_third_lockdown.csv")

# get_after_lockdown()

def lockdown_Life_Work():
    # first lockdown
    first_lockdown_df = pd.read_csv("graphs/first_lockdown.csv", error_bad_lines=False)
    fl_counts_df = first_lockdown_df['label'].value_counts()
    fl_total_life_work = fl_counts_df["Life"]+fl_counts_df["Work"]
    first_lockdown = [fl_counts_df["Life"]/fl_total_life_work, fl_counts_df["Work"]/fl_total_life_work]
    print("first", first_lockdown)

    second_lockdown_df = pd.read_csv("graphs/second_lockdown.csv", error_bad_lines=False)
    sl_counts_df = second_lockdown_df['label'].value_counts()
    sl_total_life_work = sl_counts_df["Life"]+sl_counts_df["Work"]
    second_lockdown = [sl_counts_df["Life"]/sl_total_life_work, sl_counts_df["Work"]/sl_total_life_work]
    print("second", second_lockdown)

    third_lockdown_df = pd.read_csv("graphs/third_lockdown.csv", error_bad_lines=False)
    tl_counts_df = third_lockdown_df['label'].value_counts()
    tl_total_life_work = tl_counts_df["Life"]+tl_counts_df["Work"]
    third_lockdown = [tl_counts_df["Life"]/tl_total_life_work, tl_counts_df["Work"]/tl_total_life_work]
    print("third", third_lockdown)

    lockdowns = ["First lockdown (26th March 2020 to 10th May 2020)",
                  "Second lockdown (5th November to 2nd December 2020)",
                  "Third lockdown (6th January to 8th March 2021)"]
    values = {"Life": [first_lockdown[0], second_lockdown[0], third_lockdown[0]],
              "Work": [first_lockdown[1], second_lockdown[1], third_lockdown[1]]}

    # set width of bar
    barWidth = 0.25


    fig, ax = plt.subplots()
    bottom = np.zeros(3)

    for category, value in values.items():
        p = ax.bar(lockdowns, value, barWidth, label=category, bottom=bottom)
        bottom += value

    ax.set_title("How much did nurses tweet about Life vs Work in each lockdown?")
    ax.legend(loc="upper right")


    # Adding Xticks
    plt.xlabel("Lockdown", fontweight ='bold', fontsize = 15)
    plt.ylabel("Percentage of tweets", fontweight ='bold', fontsize = 15)

    plt.show()

# lockdown_Life_Work()

def lockdown_Life_Work_None():
    # first lockdown
    first_lockdown_df = pd.read_csv("graphs/first_lockdown.csv", error_bad_lines=False)
    fl_counts_df = first_lockdown_df['label'].value_counts()
    first_lockdown = [fl_counts_df["Life"]/len(first_lockdown_df), fl_counts_df["Work"]/len(first_lockdown_df), fl_counts_df["None"]/len(first_lockdown_df)]
    print("first", first_lockdown)

    second_lockdown_df = pd.read_csv("graphs/second_lockdown.csv", error_bad_lines=False)
    sl_counts_df = second_lockdown_df['label'].value_counts()
    second_lockdown = [sl_counts_df["Life"]/len(second_lockdown_df), sl_counts_df["Work"]/len(second_lockdown_df), sl_counts_df["None"]/len(second_lockdown_df)]
    print("second", second_lockdown)

    third_lockdown_df = pd.read_csv("graphs/third_lockdown.csv", error_bad_lines=False)
    tl_counts_df = third_lockdown_df['label'].value_counts()
    third_lockdown = [tl_counts_df["Life"]/len(third_lockdown_df), tl_counts_df["Work"]/len(third_lockdown_df), tl_counts_df["None"]/len(third_lockdown_df)]
    print("third", third_lockdown)

    lockdowns = ["First lockdown (26th March 2020 to 10th May 2020)",
                 "Second lockdown (5th November to 2nd December 2020)",
                 "Third lockdown (6th January to 8th March 2021)"]

    values = {"Life": [first_lockdown[0], second_lockdown[0], third_lockdown[0]],
              "Work": [first_lockdown[1], second_lockdown[1], third_lockdown[1]],
              "None": [first_lockdown[2], second_lockdown[2], third_lockdown[2]]}

    # set width of bar
    barWidth = 0.25


    fig, ax = plt.subplots()
    bottom = np.zeros(3)

    for category, value in values.items():
        p = ax.bar(lockdowns, value, barWidth, label=category, bottom=bottom)
        bottom += value

    ax.set_title("How much did nurses tweet about Life vs Work in each lockdown?")
    ax.legend(loc="upper right")


    # Adding Xticks
    plt.xlabel("Lockdown", fontweight ='bold', fontsize = 15)
    plt.ylabel("Percentage of tweets", fontweight ='bold', fontsize = 15)

    plt.show()


# lockdown_Life_Work_None()

def lockdown_topics_pie():
    categories = {0: "Good morning",
                  1: "Thank you's",
                  3: "Congratulations",
                  4: "Expressions",
                  5: "Happy birthday",
                  6: "Exercise",
                  7: "Miscellaneous",
                  8: "General life",
                  9: "Friends & people"}

    first_lockdown_df = pd.read_csv("graphs/first_lockdown.csv", error_bad_lines=False)
    fl_counts = first_lockdown_df['Topic'].value_counts()
    fl_counts = fl_counts[1:11]


    fl_values = list(dict(sorted(fl_counts.items())).values())
    del fl_values[2]
    list_categories = list(categories.values())
    fl_df = pd.DataFrame(data=fl_values, index=list_categories)
    plot = pd.DataFrame(fl_df).plot.pie(y=0, legend=False)
    plt.title("Distribution of tweets about life topics for nurses during the first lockdown")
    plt.show()

    second_lockdown_df = pd.read_csv("graphs/second_lockdown.csv", error_bad_lines=False)
    sl_values = second_lockdown_df['Topic'].value_counts()
    sl_values = sl_values[1:11]

    sl_values = list(dict(sorted(sl_values.items())).values())
    del sl_values[2]
    list_categories = list(categories.values())
    fl_df = pd.DataFrame(data=sl_values, index=list_categories)
    plot2 = pd.DataFrame(fl_df).plot.pie(y=0, legend=False)
    plt.title("Distribution of tweets about life topics for nurses during the second lockdown")
    plt.show()

    third_lockdown_df = pd.read_csv("graphs/third_lockdown.csv", error_bad_lines=False)
    tl_values = third_lockdown_df['Topic'].value_counts()
    tl_values = tl_values[1:11]

    tl_values = list(dict(sorted(tl_values.items())).values())
    del tl_values[2]
    list_categories = list(categories.values())
    fl_df = pd.DataFrame(data=tl_values, index=list_categories)
    plot3 = pd.DataFrame(fl_df).plot.pie(y=0, legend=False)
    plt.title("Distribution of tweets about life topics for nurses during the third lockdown")
    plt.show()

# lockdown_topics_pie()

def lockdown_topics_bar():
    # first lockdown
    first_lockdown_df = pd.read_csv("graphs/first_lockdown.csv", error_bad_lines=False)
    fl_counts_df = first_lockdown_df['Topic'].value_counts()
    first_lockdown=[]
    for i in [0,4,6,8,9]:
        first_lockdown.append(fl_counts_df[i]/len(first_lockdown_df))
    print("first", first_lockdown)

    #second lockdown
    second_lockdown_df = pd.read_csv("graphs/second_lockdown.csv", error_bad_lines=False)
    sl_counts_df = second_lockdown_df['Topic'].value_counts()
    second_lockdown=[]
    for i in [0,4,6,8,9]:
        second_lockdown.append(sl_counts_df[i]/len(second_lockdown_df))
    print("second", second_lockdown)

    #third lockdown
    third_lockdown_df = pd.read_csv("graphs/third_lockdown.csv", error_bad_lines=False)
    tl_counts_df = third_lockdown_df['Topic'].value_counts()
    third_lockdown=[]
    for i in [0,4,6,8,9]:
        third_lockdown.append(tl_counts_df[i]/len(third_lockdown_df))
    print("third", third_lockdown)

    # categories = ["0: Good morning",
    #               "1: Thank you's",
    #               "3: Congratulations",
    #               "4: Expressions",
    #               "5: Happy birthday",
    #               "6: Exercise",
    #               "7: Miscellaneous",
    #               "8: General life",
    #               "9: Friends & people"]
    categories = ["0: Good morning",
                  "4: Expressions",
                  "6: Exercise",
                  "8: General life",
                  "9: Friends & people"]
    print("numbers", categories)

    # set width of bar
    barWidth = 0.25

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
    plt.xlabel("Lockdown", fontweight ='bold', fontsize = 15)
    plt.ylabel("Percentage of tweets on this topic", fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(first_lockdown))],
               categories)
    plt.title("How much did nurses talk about each Home-life topic in each lockdown?")
    plt.legend()
    plt.show()

# lockdown_topics_bar()
