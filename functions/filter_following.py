from datetime import datetime

import pandas as pd

followers_file = "data/RCONfollowers.csv"
nurse_description_string = "nurse|nursing"
today = datetime.today()
current_year = today.year

def filter(description_string = nurse_description_string, df = None):
    #filter description
    df["description"] = df["description"].fillna(value="None")
    df = df[df["description"].str.contains(description_string)]

    #filter by rate of tweeting
    #get years since creation of account and total number of tweets
    #to get tweet per year
    df["year_created"] = df["created_at"]
    df["year_created"] = df.year_created.str[-4:]
    df["year_created"] = df["year_created"].astype(int)
    df = df[df["year_created"]<2019]
    df["years_online"] = int(current_year) - df["year_created"]
    df["tweets_per_year"] = df["statuses_count"] / df["years_online"]

    return df


followersdf = pd.read_csv(followers_file, index_col=0)
followersdf = filter(nurse_description_string,df=followersdf)
followersdf.to_csv(followers_file)

