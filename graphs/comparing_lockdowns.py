import pandas as pd
from bertopic import BERTopic
import os
import numpy as np

from matplotlib import pyplot as plt

directories = ["nursetweets", "doctortweets", "teachertweets",
               "railtweets", "journalisttweets", "musiciantweets"]
directory_index = 0
directory_name = directories[directory_index]
profession_name = "nurse"
nr_topics = 10
# topic_dict = { 0: "Twitter activity", #for teachers
#                 1: "School and school holidays",
#                 2: "Good mornings and people",
#                 3: "Nature",
#                 4: "Well wishes",
#                 5: "Thank you's",
#                 6: "Finances",
#                 7: "School funding",
#                 8: "Meals",
#                 9: "Loving wishes"}
#
# topic_strings = {"0: Twitter activity", #for teachers
#                    "1: School and  holidays",
#                    "2: Good mornings",
#                    "3: Nature",
#                    "4: Well wishes",
#                    "5: Thank you's",
#                    "6: Finances",
#                    "7: School funding",
#                    "8: Meals",
#                    "9: Loving wishes"}

topic_dict = {0: "Good morning", #for nurses
              1: "Thank you's",
              3: "Congratulations",
              4: "Expressions",
              5: "Happy birthday",
              6: "Exercise",
              7: "Miscellaneous",
              8: "General life",
              9: "Friends & people"}

topic_strings = ["0: Good morning",
              "4: Expressions",
              "6: Exercise",
              "8: General life",
              "9: Friends & people"]

chosen_topics = [0,4,6,8,9]
work_topics = [2]

first_lockdown_df = pd.read_csv(f"graphs/{profession_name}s/first_lockdown.csv", error_bad_lines=False)
second_lockdown_df = pd.read_csv(f"graphs/{profession_name}s/second_lockdown.csv", error_bad_lines=False)
third_lockdown_df = pd.read_csv(f"graphs/{profession_name}s/third_lockdown.csv", error_bad_lines=False)
control1_df = pd.read_csv(f"graphs/{profession_name}s/control1.csv", error_bad_lines=False)
control2_df = pd.read_csv(f"graphs/{profession_name}s/control2.csv", error_bad_lines=False)
control3_df = pd.read_csv(f"graphs/{profession_name}s/control3.csv", error_bad_lines=False)


def get_all_tweets(directory=None):
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        user_df = pd.read_csv(f, index_col=0, error_bad_lines=False)
        df = pd.concat([df, user_df], ignore_index=True)
    return df

def get_before_lockdown():
    df = pd.read_csv(f"graphs/{profession_name}s/topics_with_dates.csv")

    # #get index range for 46 days before first lockdown
    # df_startdate = df[df['created_at'].str.match("2020-02-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-03-25")]
    # print(df_enddate)
    #
    # #get index range for 27 days before second lockdown
    # df_startdate = df[df['created_at'].str.match("2020-10-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-11-04")]
    # print(df_enddate)
    #
    # #get index range for 62 days before third lockdown
    # df_startdate = df[df['created_at'].str.match("2020-11-06")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-01-05")]
    # print(df_enddate)

    # make docs csv of first lockdown 8185 to 9735
    before_first_lockdown = df.iloc[8185:9736]
    before_first_lockdown.to_csv(f"graphs/{profession_name}s/before_first_lockdown.csv")

    # make docs csv of second lockdown 19287 to 20466
    before_second_lockdown = df.iloc[19287:20467]
    before_second_lockdown.to_csv(f"graphs/{profession_name}s/before_second_lockdown.csv")

    # make docs csv of third lockdown 20509 to 21480
    before_third_lockdown = df.iloc[20510:21481]
    before_third_lockdown.to_csv(f"graphs/{profession_name}s/before_third_lockdown.csv")

# get_before_lockdown()

def get_lockdown_tweets():
    df = pd.read_csv(f"graphs/{profession_name}s/topics_with_dates.csv")
    #dropping columns
    # df.drop(['tier', 'Unnamed: 0', 'Unnamed: 0.1.1.1'], axis=1, inplace=True,
    #         errors='ignore')
    # df.to_csv(f"graphs/{profession_name}s/topics_with_dates.csv")

    #sorting by date and adding new index
    # df.sort_values(by='created_at', inplace=True)
    # df.reset_index(drop=True, inplace=True)
    # df.to_csv(f"graphs/{profession_name}s/topics_with_dates.csv")

    #find indexes for start and end dates of lockdown periods
    #confirm first lockdown indexes
    df_startdate = df[df['created_at'].str.match("2020-03-26")]
    print(df_startdate)
    df_enddate = df[df['created_at'].str.match("2020-05-10")] #46 days
    print(df_enddate)

    #confirm second lockdown indexes
    df_startdate = df[df['created_at'].str.match("2020-11-05")]
    print(df_startdate)
    df_enddate = df[df['created_at'].str.match("2020-12-02")] #28 days
    print(df_enddate)

    #confirm third lockdown indexes
    df_startdate = df[df['created_at'].str.match("2021-01-06")]
    print(df_startdate)
    df_enddate = df[df['created_at'].str.match("2021-03-08")] #62 days
    print(df_enddate)

    # # first lockdown 9736 to 11853
    first_lockdown = df.iloc[9736:11854]
    first_lockdown.to_csv(f"graphs/{profession_name}s/first_lockdown.csv")

    # #second lockdown 20467 to 21793
    second_lockdown = df.iloc[20467:21794]
    second_lockdown.to_csv(f"graphs/{profession_name}s/second_lockdown.csv")

    # #third lockdown label 24181 to 29299
    third_lockdown = df.iloc[24181:29300]
    third_lockdown.to_csv(f"graphs/{profession_name}s/third_lockdown.csv")

# get_lockdown_tweets()

def get_after_lockdown():
    df = pd.read_csv(f"graphs/{profession_name}s/topics_with_dates.csv")

    # #get index range for 46 days after first lockdown
    # df_startdate = df[df['created_at'].str.match("2020-05-11")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-06-18")]
    # print(df_enddate)
    #
    # #get index range for 27 days after second lockdown
    # df_startdate = df[df['created_at'].str.match("2020-12-03")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-12-29")]
    # print(df_enddate)
    #
    # #get index range for 62 days after third lockdown
    # df_startdate = df[df['created_at'].str.match("2021-03-09")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-06-09")]
    # print(df_enddate)

    # make docs csv of first lockdown 11854 to 13688
    before_first_lockdown = df.iloc[11854:13689]
    before_first_lockdown.to_csv(f"graphs/{profession_name}s/after_first_lockdown.csv")

    # make docs csv of second lockdown 21794 to 23257
    before_second_lockdown = df.iloc[21794:23258]
    before_second_lockdown.to_csv(f"graphs/{profession_name}s/after_second_lockdown.csv")

    # make docs csv of third lockdown 29300 to 36061
    before_third_lockdown = df.iloc[29300:36062]
    before_third_lockdown.to_csv(f"graphs/{profession_name}s/after_third_lockdown.csv")

# get_after_lockdown()

def get_lockdown_control():
    #find indexes for start and end dates of lockdown periods
    #confirm first lockdown indexes
    df = pd.read_csv(f"graphs/{profession_name}s/topics_with_dates.csv")
    #
    # df_startdate = df[df['created_at'].str.match("2019-03-26")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2019-05-10")] #46 days
    # print(df_enddate)
    #
    # #confirm second lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2019-11-05")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2019-12-02")] #28 days
    # print(df_enddate)
    #
    # #confirm third lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-01-06")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-03-08")] #62 days
    # print(df_enddate)

    # make docs csv of first lockdown 430 to 1731
    control1 = df.iloc[430:1732]
    control1.to_csv(f"graphs/{profession_name}s/control1.csv")
    #
    # # make docs csv of second lockdown 5892 to 6516
    control2 = df.iloc[5892:6517]
    control2.to_csv(f"graphs/{profession_name}s/control2.csv")
    #
    # # make docs csv of first lockdown 7314 to 9044
    control3 = df.iloc[7314:9045]
    control3.to_csv(f"graphs/{profession_name}s/control3.csv")

# get_lockdown_control()

def lockdown_Life_Work():
    # first lockdown
    fl_counts_df = first_lockdown_df['label'].value_counts()
    fl_total_life_work = fl_counts_df["Life"]+fl_counts_df["Work"]
    first_lockdown = [fl_counts_df["Life"]/fl_total_life_work, fl_counts_df["Work"]/fl_total_life_work]
    print("first", first_lockdown)

    sl_counts_df = second_lockdown_df['label'].value_counts()
    sl_total_life_work = sl_counts_df["Life"]+sl_counts_df["Work"]
    second_lockdown = [sl_counts_df["Life"]/sl_total_life_work, sl_counts_df["Work"]/sl_total_life_work]
    print("second", second_lockdown)

    tl_counts_df = third_lockdown_df['label'].value_counts()
    tl_total_life_work = tl_counts_df["Life"]+tl_counts_df["Work"]
    third_lockdown = [tl_counts_df["Life"]/tl_total_life_work, tl_counts_df["Work"]/tl_total_life_work]
    print("third", third_lockdown)

    c1_counts_df = control1_df['label'].value_counts()
    c1_total_life_work = c1_counts_df["Life"]+c1_counts_df["Work"]
    control1 = [c1_counts_df["Life"]/c1_total_life_work, c1_counts_df["Work"]/c1_total_life_work]
    print("control1", control1)

    c2_counts_df = control2_df['label'].value_counts()
    c2_total_life_work = c2_counts_df["Life"]+c2_counts_df["Work"]
    control2 = [c2_counts_df["Life"]/c2_total_life_work, c2_counts_df["Work"]/c2_total_life_work]
    print("control2", control2)

    c3_counts_df = control3_df['label'].value_counts()
    c3_total_life_work = c3_counts_df["Life"]+c3_counts_df["Work"]
    control3 = [c3_counts_df["Life"]/c3_total_life_work, c3_counts_df["Work"]/c3_total_life_work]
    print("control3", control3)

    lockdowns = ["Control for First Lockdown",
                 "First Lockdown",
                 "Control for Second Lockdown",
                 "Second Lockdown",
                 "Control for Third Lockdown",
                 "Third Lockdown"]

    values = { "Work": [control1[1], first_lockdown[1], control2[1], second_lockdown[1], control3[1], third_lockdown[1]],
        "Life": [control1[0], first_lockdown[0], control2[0], second_lockdown[0], control3[0], third_lockdown[0]]}

    for i in range(0, len(values["Work"])):
        values["Work"][i] = values["Work"][i] * 100
    for j in range(0, len(values["Life"])):
        values["Life"][j] = values["Life"][j] * 100

    # set width of bar
    barWidth = 0.25


    fig, ax = plt.subplots()
    bottom = np.zeros(6)

    for category, value in values.items():
        p = ax.bar(lockdowns, value, barWidth, label=category, bottom=bottom)
        bottom += value

    ax.set_title(f"How much did {profession_name}s tweet about Work vs Life in each lockdown (compared to the year prior)")
    ax.legend(loc="upper right")


    # Adding Xticks
    plt.xlabel("Lockdown", fontweight ='bold', fontsize = 15)
    plt.ylabel("Percentage of tweets", fontweight ='bold', fontsize = 15)

    plt.show()

# lockdown_Life_Work()

def lockdown_Life_Work_None():
    # first lockdown
    fl_counts_df = first_lockdown_df['label'].value_counts()
    first_lockdown = [fl_counts_df["Life"]/len(first_lockdown_df), fl_counts_df["Work"]/len(first_lockdown_df), fl_counts_df["None"]/len(first_lockdown_df)]
    print("first", first_lockdown)

    sl_counts_df = second_lockdown_df['label'].value_counts()
    second_lockdown = [sl_counts_df["Life"]/len(second_lockdown_df), sl_counts_df["Work"]/len(second_lockdown_df), sl_counts_df["None"]/len(second_lockdown_df)]
    print("second", second_lockdown)

    tl_counts_df = third_lockdown_df['label'].value_counts()
    third_lockdown = [tl_counts_df["Life"]/len(third_lockdown_df), tl_counts_df["Work"]/len(third_lockdown_df), tl_counts_df["None"]/len(third_lockdown_df)]
    print("third", third_lockdown)

    c1_counts_df = control1_df['label'].value_counts()
    control1 = [c1_counts_df["Life"]/len(control1_df), c1_counts_df["Work"]/len(control1_df), c1_counts_df["None"]/len(control1_df)]
    print("control1", control1)

    c2_counts_df = control2_df['label'].value_counts()
    control2 = [c2_counts_df["Life"]/len(control2_df), c2_counts_df["Work"]/len(control2_df), c2_counts_df["None"]/len(control2_df)]
    print("control2", control2)

    c3_counts_df = control3_df['label'].value_counts()
    control3 = [c3_counts_df["Life"]/len(control3_df), c3_counts_df["Work"]/len(control3_df), c3_counts_df["None"]/len(control3_df)]
    print("control3", control3)

    lockdowns = ["Control for First Lockdown",
                 "First Lockdown",
                 "Control for Second Lockdown",
                 "Second Lockdown",
                 "Control for Third Lockdown",
                 "Third Lockdown"]

    values = {
              "Work": [control1[1], first_lockdown[1], control2[1], second_lockdown[1], control3[1], third_lockdown[1]],
                "Life": [control1[0], first_lockdown[0], control2[0], second_lockdown[0], control3[0], third_lockdown[0]],
              "Neither": [control1[2], first_lockdown[2], control2[2], second_lockdown[2], control3[2], third_lockdown[2]]}

    for i in range(0, len(values["Work"])):
        values["Work"][i] = values["Work"][i] * 100
    for j in range(0, len(values["Life"])):
        values["Life"][j] = values["Life"][j] * 100
    for k in range(0, len(values["Neither"])):
        values["Neither"][k] = values["Neither"][k] * 100

    # set width of bar
    barWidth = 0.25

    fig, ax = plt.subplots()
    bottom = np.zeros(6)
    # print(lockdowns)
    # print(values)
    for category, value in values.items():
        p = ax.bar(lockdowns, value, barWidth, label=category, bottom=bottom)
        bottom += value

    ax.set_title(f"How much did {profession_name}s tweet about Work vs Life vs Neither in each lockdown?")
    ax.legend(loc="upper right")


    # Adding Xticks
    plt.xlabel("Lockdown", fontweight ='bold', fontsize = 15)
    plt.ylabel("Percentage of tweets", fontweight ='bold', fontsize = 15)

    plt.show()

# lockdown_Life_Work_None()

def lockdown_topics_pie():
    categories = topic_dict.copy()
    fl_counts = first_lockdown_df['Topic'].value_counts()
    fl_counts = fl_counts[1:11]
    fl_values = list(dict(sorted(fl_counts.items())).values())
    for t in work_topics:
        del fl_values[t]
        del categories[t]
    list_categories = list(categories.values())
    fl_df = pd.DataFrame(data=fl_values, index=list_categories)
    plot = pd.DataFrame(fl_df).plot.pie(y=0, legend=False)
    plt.title(f"Distribution of tweets about life topics for {profession_name}s during the first lockdown")
    plt.show()

    sl_values = second_lockdown_df['Topic'].value_counts()
    sl_values = sl_values[1:11]
    sl_values = list(dict(sorted(sl_values.items())).values())
    for u in work_topics:
        del sl_values[u]
    sl_df = pd.DataFrame(data=sl_values, index=list_categories)
    plot2 = pd.DataFrame(sl_df).plot.pie(y=0, legend=False)
    plt.title(f"Distribution of tweets about life topics for {profession_name}s during the second lockdown")
    plt.show()

    third_lockdown_df = pd.read_csv(f"graphs/{profession_name}s/third_lockdown.csv", error_bad_lines=False)
    tl_values = third_lockdown_df['Topic'].value_counts()
    tl_values = tl_values[1:11]
    tl_values = list(dict(sorted(tl_values.items())).values())
    for v in work_topics:
        del tl_values[v]
    tl_df = pd.DataFrame(data=tl_values, index=list_categories)
    plot3 = pd.DataFrame(tl_df).plot.pie(y=0, legend=False)
    plt.title(f"Distribution of tweets about life topics for {profession_name}s during the third lockdown")
    plt.show()

# lockdown_topics_pie()

def lockdown_topics_bar():
    # first lockdown
    fl_counts_df = first_lockdown_df['Topic'].value_counts()
    first_lockdown=[]
    for i in chosen_topics:
        first_lockdown.append((fl_counts_df[i]/len(first_lockdown_df))*100)
    print("first", first_lockdown)

    #second lockdown
    sl_counts_df = second_lockdown_df['Topic'].value_counts()
    second_lockdown=[]
    for i in chosen_topics:
        second_lockdown.append((sl_counts_df[i]/len(second_lockdown_df))*100)
    print("second", second_lockdown)

    #third lockdown
    tl_counts_df = third_lockdown_df['Topic'].value_counts()
    third_lockdown=[]
    for i in chosen_topics:
        third_lockdown.append((tl_counts_df[i]/len(third_lockdown_df))*100)
    print("third", third_lockdown)

    categories = topic_strings.copy()

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
    plt.xlabel("Topic", fontweight ='bold', fontsize = 15)
    plt.ylabel("Percentage of tweets relating to this topic", fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(first_lockdown))],
               categories)
    plt.title(f"How much did {profession_name}s talk about each Home-life topic in each lockdown?")
    plt.legend()
    plt.show()

# lockdown_topics_bar()
