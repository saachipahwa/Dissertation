from datetime import datetime

import pandas as pd

followers_file = "data/RCONfollowers.csv"
nurse_description_string = "nurse|nursing"
teacher_description_string = "teacher"
doctor_description_string = "doctor|surgeon|general practicioner"
description_string = nurse_description_string
today = datetime.today()
current_year = today.year

def filter(df = None):
    print("length before filtering: " + str(len(df)))

    #filter description
    df["description"] = df["description"].fillna(value="None")
    df = df[df["description"].str.contains(description_string)]

    #filter by rate of tweeting
    #get years since creation of account and total number of tweets
    #to get tweet per year
    df["year_created"] = df["created_at"]
    df["year_created"] = df.year_created.str[-4:]
    df['year_created'] = pd.to_numeric(df['year_created'], errors='coerce')
    df = df.dropna(subset=['created_at'])
    df['year_created']=df['year_created'].astype(str)
    df['year_created']=df['year_created'].astype(float)
    df = df[df["year_created"]<float(2019)]
    df["years_online"] = int(current_year) - df["year_created"]
    df['statuses_count']=df['statuses_count'].astype(str)
    df['statuses_count']=df['statuses_count'].astype(float)
    df = df[(df[['statuses_count']] != 0).all(axis=1)]
    df = df[(df[['years_online']] != 0).all(axis=1)]
    df["tweets_per_year"] = df["statuses_count"] / df["years_online"]
    df = df[(df[['tweets_per_year']] != 0).all(axis=1)]
    df = df[df["tweets_per_year"]>float(2000)]

    print("length after filtering " + str(len(df)))
    return df


followersdf = pd.read_csv(followers_file, index_col=0)
followersdf = filter(df=followersdf)
followersdf.to_csv("data/BMAfollowers.csv")

