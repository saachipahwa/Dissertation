
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


# def work_term_frequency():
#     original_top10terms_work = ['time', 'year', 'nurse', 'today', 'people', 'thank', 'nursing', 'care', 'morning', 'work']
#     top10terms_work = ['time', 'nurse', 'morning', 'thank', 'today', 'year', 'people', 'week', 'work', 'care']
#     first_lockdown_df = pd.read_csv("Dissertation/graphs/first_lockdown.csv", error_bad_lines=False)
#     second_lockdown_df = pd.read_csv("Dissertation/graphs/second_lockdown.csv", error_bad_lines=False)
#     third_lockdown_df = pd.read_csv("Dissertation/graphs/third_lockdown.csv", error_bad_lines=False)
#
#     #ønly use work tweets
#     work_df_1 = first_lockdown_df[first_lockdown_df['label']=="Work"]
#     work_df_2 = second_lockdown_df[second_lockdown_df['label']=="Work"]
#     work_df_3 = third_lockdown_df[third_lockdown_df['label']=="Work"]
#
#     work_text_1 = ' '.join(work_df_1["Document"])
#     work_text_2 = ' '.join(work_df_2["Document"])
#     work_text_3 = ' '.join(work_df_3["Document"])
#
#     # work_df_2["Document"].to_csv("Dissertation/graphs/worktext2.csv")
#
#     work_words_1 = work_text_1.split()
#     work_words_2 = work_text_2.split()
#     work_words_3 = work_text_3.split()
#
#     word_count_1 = pd.value_counts(np.array(work_words_1))
#     word_count_2 = pd.value_counts(np.array(work_words_2))
#     word_count_3 = pd.value_counts(np.array(work_words_3))
#
#     terms_count_1 = []
#     terms_count_2 = []
#     terms_count_3 = []
#
#     for w in top10terms_work:
#         terms_count_1.append(word_count_1[w]/len(work_words_1))
#         terms_count_2.append(word_count_2[w]/len(work_words_2))
#         terms_count_3.append(word_count_3[w]/len(work_words_3))
#
#     print("work\n", terms_count_1, terms_count_2, terms_count_3)
#
# # work_term_frequency()
#
# def life_term_frequency_lockdowns():
#     original_top10terms_life = ['time', 'thank', 'nurse', 'morning', 'today', 'year', 'people', 'work', 'week', 'care']
#     top10terms_life = ['time', 'thank', 'today', 'morning', 'people', 'year', 'nurse', 'work', 'health', 'week']
#     first_lockdown_df = pd.read_csv("Dissertation/graphs/first_lockdown.csv", error_bad_lines=False)
#     second_lockdown_df = pd.read_csv("Dissertation/graphs/second_lockdown.csv", error_bad_lines=False)
#     third_lockdown_df = pd.read_csv("Dissertation/graphs/third_lockdown.csv", error_bad_lines=False)
#
#     #ønly use life tweets
#     life_df_1 = first_lockdown_df[first_lockdown_df['label']=="Life"]
#     life_df_2 = second_lockdown_df[second_lockdown_df['label']=="Life"]
#     life_df_3 = third_lockdown_df[third_lockdown_df['label']=="Life"]
#
#     life_text_1 = ' '.join(life_df_1["Document"])
#     life_text_2 = ' '.join(life_df_2["Document"])
#     life_text_3 = ' '.join(life_df_3["Document"])
#
#     life_words_1 = life_text_1.split()
#     life_words_2 = life_text_2.split()
#     life_words_3 = life_text_3.split()
#
#     life_count_1 = pd.value_counts(np.array(life_words_1))
#     life_count_2 = pd.value_counts(np.array(life_words_2))
#     life_count_3 = pd.value_counts(np.array(life_words_3))
#
#     terms_count_1 = []
#     terms_count_2 = []
#     terms_count_3 = []
#
#     for w in top10terms_life:
#         try:
#             terms_count_1.append(life_count_1[w]/len(life_words_1))
#         except Exception as e:
#             terms_count_1.append(0)
#         try:
#             terms_count_2.append(life_count_2[w]/len(life_words_2))
#         except Exception as e:
#             terms_count_2.append(0)
#         try:
#             terms_count_3.append(life_count_3[w]/len(life_words_3))
#         except Exception as e:
#             terms_count_3.append(0)
#
#     print("life\n", terms_count_1, "\n", terms_count_2, "\n", terms_count_3)
#
# # life_term_frequency_lockdowns()
#
# #Before running, this get terms and lockdown counts from functions above
# def plot_term_frequency_lockdowns(label = None,
#                         terms = None,
#                         lockdown1_counts=None, lockdown2_counts=None, lockdown3_counts=None):
#     #set width of bar
#     barWidth = 0.25
#     fig = plt.subplots(figsize =(12, 8))
#
#     # Set position of bar on X axis
#     br1 = np.arange(len(lockdown1_counts))
#     br2 = [x + barWidth for x in br1]
#     br3 = [x + barWidth for x in br2]
#
#     # Make the plot
#     plt.bar(br1, lockdown1_counts, color ='r', width = barWidth,
#             edgecolor ='grey', label = "First lockdown (26th March 2020 to 10th May 2020)")
#     plt.bar(br2, lockdown2_counts, color ='g', width = barWidth,
#             edgecolor ='grey', label = "Second lockdown (5th November to 2nd December 2020)")
#     plt.bar(br3, lockdown3_counts, color ='b', width = barWidth,
#             edgecolor ='grey', label = "Third lockdown (6th January to 8th March 2021)")
#
#     # Adding Xticks
#     plt.xlabel("Term", fontweight ='bold', fontsize = 15)
#     plt.ylabel(f"Percentage of tweets containing {label} terms", fontweight ='bold', fontsize = 15)
#     plt.xticks([r + barWidth for r in range(len(lockdown1_counts))],
#                terms)
#
#     plt.legend()
#     plt.show()

# plot_term_frequency(label="Work",
#                     terms = ['time', 'nurse', 'morning', 'thank', 'today', 'year', 'people', 'week', 'work', 'care'],
#                     lockdown1_counts = [0.01664132454806555, 0.005575266092245312, 0.008109477952356817, 0.008025004223686433, 0.011572900827842542, 0.013515796587261361, 0.002196316945429971, 0.005575266092245312, 0.0033789491468153403, 0.007856056766345666],
#                     lockdown2_counts= [0.014565596471432967, 0.009847163811672992, 0.012924402502820802, 0.008411119089137347, 0.010565186172940815, 0.00912914145040517, 0.0034875371833008512, 0.0124115293876295, 0.004205559544568673, 0.006359626628372141],
#                     lockdown3_counts=[0.012965186074429771, 0.009981135311267365, 0.010358429085920082, 0.008266163608300464, 0.011490310409878237, 0.008060367003944436, 0.00329274566969645, 0.007820270965529069, 0.005282112845138055, 0.008780655119190533])
# plot_term_frequency(label="Life",
#                     terms=['time', 'thank', 'nurse', 'morning', 'today', 'year', 'people', 'work', 'week', 'care'],
#                     lockdown1_counts = [0.023994811932555125, 0.05512321660181582, 0.00324254215304799, 0.009079118028534372, 0.007782101167315175, 0.005188067444876783, 0.013618677042801557, 0.007133592736705577, 0.019455252918287938, 0.005188067444876783] ,
#                     lockdown2_counts=  [0.0273224043715847, 0.040983606557377046, 0.00273224043715847, 0.01639344262295082, 0.007285974499089253, 0.007285974499089253, 0.007285974499089253, 0.01092896174863388, 0.017304189435336976, 0.00273224043715847] ,
#                     lockdown3_counts = [0.02161681966242227, 0.04471424341131182, 0.0038495706248149247, 0.018359490672194254, 0.0071068996150429374, 0.009179745336097127, 0.01599052413384661, 0.013029315960912053, 0.014213799230085875, 0.00414569144210838])
