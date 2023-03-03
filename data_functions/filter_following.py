import os
from datetime import datetime
import pandas as pd

followers_file = "data/NUJfollowers.csv"
filtered_file = "data/filteredNUJfollowers2.csv"
nurse_description_string = "nurse|nursing"
teacher_description_string = "teacher"
doctor_description_string = "doctor|surgeon|general practicioner"
journalist_description_string = "journalist"
railworker_description_string = "rail|train |maritime"
musician_description_string = "music|musician"
description_string = journalist_description_string
today = datetime.today()
current_year = today.year

def filter(df = None):
    print("length before filtering: " + str(len(df)))

    #filter description
    df["description"] = df["description"].fillna(value="None")
    df = df[df["description"].str.contains(description_string)]
    df = df[~df["description"].str.contains("doctorate")]
    #Should've been online before 2019
    df["year_created"] = df["created_at"]
    df["year_created"] = df.year_created.str[-4:]
    df['year_created'] = pd.to_numeric(df['year_created'], errors='coerce')
    df = df.dropna(subset=['created_at'])
    df['year_created']=df['year_created'].astype(str)
    df['year_created']=df['year_created'].astype(float)
    df = df[df["year_created"]<=float(2019)]

    #filter by rate of tweeting
    #get years since creation of account and total number of nursetweets
    #to get tweet per year
    df["years_online"] = int(current_year) - df["year_created"]
    df['statuses_count']=df['statuses_count'].astype(str)
    df['statuses_count']=df['statuses_count'].astype(float)
    df = df[(df[['statuses_count']] != 0).all(axis=1)]
    df = df[(df[['years_online']] != 0).all(axis=1)]
    df["tweets_per_year"] = df["statuses_count"] / df["years_online"]

    df = df[(df[['tweets_per_year']] != 0).all(axis=1)]
    df = df[df["tweets_per_year"]>float(2000)]

    #remove bots
    df['friend_ratio'] = df['followers_count'] / df['friends_count'] #get follower to friend ratio
    # df = df.loc[(df["followers_count"]>4000) & (df["friend_ratio"]<1)] #USE TO GET BOTS
    # df = df.loc[(df["followers_count"] < 4000) | ((df["followers_count"] >= 4000) & (df["friend_ratio"]>=1))] #USE TO REMOVE BOTS #FOR MU i replaced 1 with 0.6

    #remove famous accounts for musicians union followers
    # df = df.loc[~(df["friend_ratio"]>2)] #MU
    # df = df.loc[~(df["followers_count"]>50000)] #MU

    # df = df.loc[~(df["followers_count"]>10000)] #for trains

    #remove private accounts
    df['protected'] = df['protected'].astype(str)
    df = df[~df["protected"].str.contains("True")]

    print("length after filtering " + str(len(df)))
    return df

# followersdf = pd.read_csv(followers_file, index_col=0)
# followersdf = filter(df=followersdf)
# followersdf.to_csv(filtered_file)

def second_filter(followers_df_name = "data/filteredNUJfollowers.csv", directory = "journalisttweets"):
    # Use after filtering tweets
    # How many users can we analyse?
    two_count = 0
    one_count = 0
    followers_df = pd.read_csv(followers_df_name)
    followers_df["no_tweets_after_filter"] = None
    for index, row in followers_df.iterrows():
        f = "{}/{}.csv".format(directory, str(int(row["id"])))
        if os.path.isfile(f):
            df = pd.read_csv(f)
            if len(df)>=2000:
                two_count+=1
                one_count+=1
            elif len(df)>=1000:
                one_count+=1
            followers_df.loc[index, "no_tweets_after_filter"] = len(df)
        else:
            print("count not find", f)
            followers_df.drop(index=index, inplace=True)
    followers_df.to_csv(followers_df_name)
    print("number of users who survived filtering", len(followers_df))
    print("number of users with >1000 tweets left", one_count)
    print("number of users with >2000 tweets left", two_count)

# second_filter()


def third_filter(followers_df_name = "data/filteredRMTfollowers.csv", directory = "railtweets"):
    #after filtering tweets, ensure all followers have >1000 tweets
    followers_df = pd.read_csv(followers_df_name)
    for index, row in followers_df.iterrows():
        f = "{}/{}.csv".format(directory, str(int(row["id"])))
        if os.path.isfile(f):
            df = pd.read_csv(f)
            if len(df)<1000:
                os.remove(f)
                followers_df.drop(index=[index], axis=0, inplace=True)
    followers_df.to_csv(followers_df_name)

third_filter()