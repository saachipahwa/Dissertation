import os
from collections import Counter

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

before1 = pd.read_csv("sentiment/csvs/before_first_lockdown.csv")
during1 = pd.read_csv("sentiment/csvs/first_lockdown.csv")
after1 = pd.read_csv("sentiment/csvs/after_first_lockdown.csv")
before2 = pd.read_csv("sentiment/csvs/before_second_lockdown.csv")
during2 = pd.read_csv("sentiment/csvs/second_lockdown.csv")
after2 = pd.read_csv("sentiment/csvs/after_second_lockdown.csv")
before3 = pd.read_csv("sentiment/csvs/before_third_lockdown.csv")
during3 = pd.read_csv("sentiment/csvs/third_lockdown.csv")
after3 = pd.read_csv("sentiment/csvs/after_third_lockdown.csv")

def get_freq_change(df1, df2):
    df1counts = df1['sentiment'].value_counts()
    df2counts = df2['sentiment'].value_counts()

    print("positive 2", df2counts["Positive"])
    print("negative 2", df2counts["Negative"])
    print("none 2", df2counts["None"])
    print("length 2", len(df2), "\n")
    print("positive 1", df1counts["Positive"])
    print("negative 1", df1counts["Negative"])
    print("none 1", df1counts["None"])
    print("length 1", len(df1), "\n")

    pos_change = ((df2counts["Positive"]/len(df2))-(df1counts['Positive']/len(df1)))*100
    neg_change = ((df2counts["Negative"]/len(df2))-(df1counts['Negative']/len(df1)))*100
    none_change = ((df2counts["None"]/len(df2))-(df1counts['None']/len(df1)))*100
    change_dict = {"positive":pos_change, "negative":neg_change, "none": none_change}
    print(change_dict)
    return change_dict

def get_frequency_change(df1, df2):
    #TODO: add threhsold
    df1_work = df1[df1['label']=="Work"]
    df1_life = df1[df1['label']=="Life"]
    df2_work = df2[df2['label']=="Work"]
    df2_life = df2[df2['label']=="Life"]
    workdict = get_freq_change(df1_work, df2_work)
    lifedict = get_freq_change(df1_life, df2_life)
    return workdict, lifedict


def make_plot():
    labels = [["Before", "During", "first"], [ "Before", "During", "second"], ["Before", "During", "third"],
              ["During", "After", "first"], ["During", "After", "second"], ["During", "After", "third"]]
    print("first lockdown beforeduring")
    work1a, life1a = get_frequency_change(before1, during1)
    print("second lockdown beforeduring")
    work2a, life2a = get_frequency_change(before2, during2)
    print("third lockdown beforeduring")
    work3a, life3a = get_frequency_change(before3, during3)
    print("first lockdown duringafter")
    work1b, life1b = get_frequency_change(during1, after1)
    print("second lockdown duringafter")
    work2b, life2b = get_frequency_change(during2, after2)
    print("third lockdown duringafter")
    work3b, life3b = get_frequency_change(during3, after3)
    x_names = ["Classes", "Before vs During LD1", "During vs After LD1", "Before vs During LD2", "During vs After LD2", "Before vs During LD3", "During vs After LD4"]

    #WORK DF
    work_df = pd.DataFrame(columns=x_names)
    work_df["Classes"] = ["positive", "negative", "none"]
    work_df.set_index('Classes')

    # all_dicts = [work1a, life1a, work1b, life1b, work2a, life2a, work2b, life2b, work3a, life3a, work3b, life3b]
    workdicts = [work1a, work1b, work2a, work2b, work3a, work3b]
    for i in range(0, len(workdicts)):
        work_df[x_names[i+1]] = workdicts[i].values()
    print(work_df)

    #LIFEDF
    life_df = pd.DataFrame(columns=x_names)
    life_df["Classes"] = ["positive", "negative", "none"]
    life_df.set_index('Classes')

    # all_dicts = [work1a, life1a, work1b, life1b, work2a, life2a, work2b, life2b, work3a, life3a, work3b, life3b]
    lifedicts = [life1a, life1b, life2a, life2b, life3a, life3b]
    for i in range(0, len(lifedicts)):
        life_df[x_names[i+1]] = lifedicts[i].values()
    print(life_df)
    fig, ax = plt.subplots(figsize=(13,3))
    pd.plotting.parallel_coordinates(work_df, 'Classes', color=['green', 'red', 'blue'], ls='', marker='o')
    ax.legend(bbox_to_anchor=(1.01, 1.02), loc='upper left')
    plt.title("Frequency change comparing periods before, during and after each lockdown: Work tweets")
    plt.xlabel("Comparison")
    plt.ylabel("Percentage change")
    plt.tight_layout()
    plt.show()

    fig2, ax2 = plt.subplots(figsize=(13,3))
    pd.plotting.parallel_coordinates(life_df, 'Classes', color=['green', 'red', 'blue'], ls='', marker='o')
    ax2.legend(bbox_to_anchor=(1.01, 1.02), loc='upper left')
    plt.title("Frequency change comparing periods before, during and after each lockdown: Life tweets")
    plt.xlabel("Comparison")
    plt.ylabel("Percentage change")
    plt.tight_layout()
    plt.show()

make_plot()
