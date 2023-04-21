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
work_topics = [2]
chosen_topics = [0,4,6,8,9]

#Use when plotting all topics in bar chart
# chosen_topics = list(range(0, nr_topics))
# for i in work_topics:
#     del chosen_topics[i]

topic_dict = {0: "Good morning", #for nurses
              1: "Thank you's",
              2: "Shifts",
              3: "Congratulations",
              4: "Expressions",
              5: "Happy birthday",
              6: "Exercise",
              7: "Miscellaneous",
              8: "General life",
              9: "Friends & people"}

topic_strings = ["0: Good morning", #for nurses
              "1: Thank you's",
              "2: Shifts",
              "3: Congratulations",
              "4: Expressions",
              "5: Happy birthday",
              "6: Exercise",
              "7: Miscellaneous",
              "8: General life",
              "9: Friends & people"]


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

    # make docs csv of first lockdown 4054 to 4847
    before_first_lockdown = df.iloc[4054:4848]
    before_first_lockdown.to_csv(f"graphs/{profession_name}s/before_first_lockdown.csv")

    # # make docs csv of second lockdown 10352 to 11154
    before_second_lockdown = df.iloc[10352:11155]
    before_second_lockdown.to_csv(f"graphs/{profession_name}s/before_second_lockdown.csv")
    #
    # # make docs csv of third lockdown 11188 to 13427
    before_third_lockdown = df.iloc[11188:13428]
    before_third_lockdown.to_csv(f"graphs/{profession_name}s/before_third_lockdown.csv")

# get_before_lockdown()

def get_lockdown_tweets():
    df = pd.read_csv(f"graphs/{profession_name}s/topics_with_dates.csv")

    # # find indexes for start and end dates of lockdown periods
    # # confirm first lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-03-26")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-05-10")] #46 days
    # print(df_enddate)
    #
    # #confirm second lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-11-05")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-12-02")] #28 days
    # print(df_enddate)
    #
    # #confirm third lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2021-01-06")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2021-03-08")] #62 days
    # print(df_enddate)

    # make docs csv of first lockdown 4848 to 5994
    first_lockdown = df.iloc[4848:5995]
    first_lockdown.to_csv(f"graphs/{profession_name}s/first_lockdown.csv")

    # make docs csv of second lockdown 11155 to 12122
    second_lockdown = df.iloc[11155:12123]
    second_lockdown.to_csv(f"graphs/{profession_name}s/second_lockdown.csv")

    # make docs csv of third lockdown 13428 to 15883
    third_lockdown = df.iloc[13428:15884]
    third_lockdown.to_csv(f"graphs/{profession_name}s/third_lockdown.csv")

# get_lockdown_tweets()

def get_after_lockdown():
    df = pd.read_csv(f"graphs/{profession_name}s/topics_with_dates.csv")

    # # get index range for 46 days after first lockdown
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

    # make docs csv of first lockdown 5995 to 7165
    before_first_lockdown = df.iloc[5995:7166]
    before_first_lockdown.to_csv(f"graphs/{profession_name}s/after_first_lockdown.csv")
    #
    # # make docs csv of second lockdown 12123 to 13150
    before_second_lockdown = df.iloc[12123:13151]
    before_second_lockdown.to_csv(f"graphs/{profession_name}s/after_second_lockdown.csv")
    #
    # # make docs csv of third lockdown 15884 to 20450
    before_third_lockdown = df.iloc[15884:20451]
    before_third_lockdown.to_csv(f"graphs/{profession_name}s/after_third_lockdown.csv")

# get_after_lockdown()

def get_lockdown_control():
    #find indexes for start and end dates of lockdown periods
    df = pd.read_csv(f"graphs/{profession_name}s/topics_with_dates.csv")

    #confirm first lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2019-03-28")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2019-04-04")] #46 days
    # print(df_enddate)
    #
    # # confirm second lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2019-11-05")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2019-12-02")] #28 days
    # print(df_enddate)
    #
    # # confirm third lockdown indexes
    # df_startdate = df[df['created_at'].str.match("2020-01-04")]
    # print(df_startdate)
    # df_enddate = df[df['created_at'].str.match("2020-03-08")] #62 days would start at 06/01 but no tweets
    # print(df_enddate)

    # make docs csv of first lockdown 582 to 681
    control1 = df.iloc[582:681]
    control1.to_csv(f"graphs/{profession_name}s/control1.csv")

    # make docs csv of second lockdown 3102 to 3351
    control2 = df.iloc[3102:3351]
    control2.to_csv(f"graphs/{profession_name}s/control2.csv")

    # make docs csv of first lockdown 3646 to 4462
    control3 = df.iloc[3646:4462]
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
    print("c1 counts", c1_counts_df)
    if "Life" in list(c1_counts_df.keys()) and "Work" in list(c1_counts_df.keys()):
        c1_total_life_work = c1_counts_df["Life"]+c1_counts_df["Work"]
        control1 = [c1_counts_df["Life"]/c1_total_life_work, c1_counts_df["Work"]/c1_total_life_work]
    elif "Life" in list(c1_counts_df.keys()):
        control1 = [1, 0]
    elif "Work" in list(c1_counts_df.keys()):
        control1 = [0,1]
    else:
        control1 = [0,0]
    print("control1", control1)

    c2_counts_df = control2_df['label'].value_counts()
    print("c2 counts", c2_counts_df)
    if "Life" in list(c2_counts_df.keys()) and "Work" in list(c2_counts_df.keys()):
        c2_total_life_work = c2_counts_df["Life"]+c2_counts_df["Work"]
        control2 = [c2_counts_df["Life"]/c2_total_life_work, c2_counts_df["Work"]/c2_total_life_work]
    elif "Life" in list(c2_counts_df.keys()):
        control2 = [1,0]
    elif "Work" in list(c2_counts_df.keys()):
        control2 = [0,1]
    else:
        control2 = [0,0]

    c3_counts_df = control3_df['label'].value_counts()
    print("c3 counts", c3_counts_df)
    if "Life" in list(c3_counts_df.keys()) and "Work" in list(c3_counts_df.keys()):
        c3_total_life_work = c3_counts_df["Life"]+c3_counts_df["Work"]
        control3 = [c3_counts_df["Life"]/c3_total_life_work, c3_counts_df["Work"]/c3_total_life_work]
    elif "Life" in list(c3_counts_df.keys()):
        control3 = [1,0]
    elif "Work" in list(c3_counts_df.keys()):
        control3 = [0,1]
    else:
        control3 = [0,0]
    print("control3", control3)

    lockdowns = [
                 "Control for Second Lockdown",
                 "Second Lockdown",
                 "Control for Third Lockdown",
                 "Third Lockdown"]

    values = { "Work": [control2[1], second_lockdown[1], control3[1], third_lockdown[1]],
        "Life": [control2[0], second_lockdown[0], control3[0], third_lockdown[0]]}

    for i in range(0, len(values["Work"])):
        values["Work"][i] = values["Work"][i] * 100
    for j in range(0, len(values["Life"])):
        values["Life"][j] = values["Life"][j] * 100

    # set width of bar
    barWidth = 0.25


    fig, ax = plt.subplots()
    bottom = np.zeros(4)

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
    c1_life_fraction = c1_counts_df["Life"]/len(control1_df) if "Life" in list(c1_counts_df.keys()) else 0
    c1_work_fraction = c1_counts_df["Work"]/len(control1_df) if "Work" in list(c1_counts_df.keys()) else 0
    c1_none_fraction = c1_counts_df["None"]/len(control1_df) if "None" in list(c1_counts_df.keys()) else 0
    control1 = [c1_life_fraction, c1_work_fraction, c1_none_fraction]
    print("control1", control1)

    c2_counts_df = control2_df['label'].value_counts()
    c2_life_fraction = c2_counts_df["Life"]/len(control2_df) if "Life" in list(c2_counts_df.keys()) else 0
    c2_work_fraction = c2_counts_df["Work"]/len(control2_df) if "Work" in list(c2_counts_df.keys()) else 0
    c2_none_fraction = c2_counts_df["None"]/len(control2_df) if "None" in list(c2_counts_df.keys()) else 0
    control2 = [c2_life_fraction, c2_work_fraction, c2_none_fraction]
    print("control2", control2)

    c3_counts_df = control3_df['label'].value_counts()
    c3_life_fraction = c3_counts_df["Life"]/len(control3_df) if "Life" in list(c3_counts_df.keys()) else 0
    c3_work_fraction = c3_counts_df["Work"]/len(control3_df) if "Work" in list(c3_counts_df.keys()) else 0
    c3_none_fraction = c3_counts_df["None"]/len(control3_df) if "None" in list(c3_counts_df.keys()) else 0
    control3 = [c3_life_fraction, c3_work_fraction, c3_none_fraction]
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

lockdown_Life_Work_None()

def lockdown_topics_pie():
    fl_counts = first_lockdown_df['Topic'].value_counts()
    fl_counts = dict(sorted(fl_counts.items()))
    del fl_counts[-1]
    fl_values = list(dict(sorted(fl_counts.items())).values())
    og_categories = list(topic_dict.copy().values())
    new_categories = []
    for tp in list(fl_counts.keys()):
        new_categories.append(og_categories[tp])
    for wt in work_topics:
        del fl_values[wt]
        del new_categories[wt]
    fl_df = pd.DataFrame(data=fl_values, index=new_categories)
    plot = pd.DataFrame(fl_df).plot.pie(y=0, legend=False)
    plt.title(f"Distribution of tweets about life topics for {profession_name}s during the first lockdown")
    plt.show()

    sl_counts = second_lockdown_df['Topic'].value_counts()
    sl_counts = dict(sorted(sl_counts.items()))
    del sl_counts[-1]
    sl_values = list(dict(sorted(sl_counts.items())).values())
    og_categories = list(topic_dict.copy().values())
    new_categories = []
    for tp in list(sl_counts.keys()):
        new_categories.append(og_categories[tp])
    for wt in work_topics:
        del sl_values[wt]
        del new_categories[wt]
    sl_df = pd.DataFrame(data=sl_values, index=new_categories)
    plot = pd.DataFrame(sl_df).plot.pie(y=0, legend=False)
    plt.title(f"Distribution of tweets about life topics for {profession_name}s during the second lockdown")
    plt.show()

    tl_counts = second_lockdown_df['Topic'].value_counts()
    tl_counts = dict(sorted(tl_counts.items()))
    del tl_counts[-1]
    tl_values = list(dict(sorted(tl_counts.items())).values())
    og_categories = list(topic_dict.copy().values())
    new_categories = []
    for tp in list(tl_counts.keys()):
        new_categories.append(og_categories[tp])
    for wt in work_topics:
        del tl_values[wt]
        del new_categories[wt]

    tl_df = pd.DataFrame(data=tl_values, index=new_categories)
    plot = pd.DataFrame(tl_df).plot.pie(y=0, legend=False)
    plt.title(f"Distribution of tweets about life topics for {profession_name}s during the third lockdown")
    plt.show()

# lockdown_topics_pie()

def lockdown_topics_bar():
    og_categories = topic_strings.copy()
    print(og_categories)
    new_categories = []
    # first lockdown
    fl_counts_df = first_lockdown_df['Topic'].value_counts()
    print(fl_counts_df)
    first_lockdown=[]
    for i in chosen_topics:
        print("topic", i)
        new_categories.append(og_categories[i])
        try:
            print("fl count", fl_counts_df[i])
            first_lockdown.append((fl_counts_df[i]/len(first_lockdown_df))*100)
        except Exception as e:
            print("not found, added 0")
            first_lockdown.append(0)
            print("new ", first_lockdown)
    print("first", first_lockdown)

    #second lockdown
    sl_counts_df = second_lockdown_df['Topic'].value_counts()
    second_lockdown=[]
    for i in chosen_topics:
        try:
            second_lockdown.append((sl_counts_df[i]/len(second_lockdown_df))*100)
        except Exception as e:
            second_lockdown.append(0)
    print("second", second_lockdown)

    #third lockdown
    tl_counts_df = third_lockdown_df['Topic'].value_counts()
    third_lockdown=[]
    for i in chosen_topics:
        try:
            third_lockdown.append((tl_counts_df[i]/len(third_lockdown_df))*100)
        except Exception as e:
            third_lockdown.append(0)
    print("third", third_lockdown)


    print("numbers", new_categories)

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
               new_categories)
    plt.title(f"How much did {profession_name}s talk about each Home-life topic in each lockdown?")
    plt.legend()
    plt.show()

# lockdown_topics_bar()
