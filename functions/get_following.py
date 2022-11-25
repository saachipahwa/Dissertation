import json

import pandas as pd

from authpy import authpy
import datetime

today = datetime.date.today()

current_year = today.year

followers_file = "data/RCONfollowers.csv"
nurse_description_string = "nurse|nursing"


api = authpy('credentials.json')

try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')

def filter(description_string = nurse_description_string, df = None):
    #filter description
    df["description"] = df["description"].fillna(value="None")
    df = df[df["description"].str.contains(description_string)]

    #filter by rate of tweeting
    #get years since creation of account and total number of tweets
    #to get tweet per year
    df['year_created'] = df["created_at"].str[-4:]
    df['year_created'] = df['year_created'].astype(int)
    df['years_online'] = int(current_year) - df["year_created"]
    df['tweets_per_year'] = df['statuses_count'] / df['years_online']

    return df

def get_union_followers(user_id = "54506896", pagination = None):
    if pagination:
        onehundredfollowers, tokens = api.get_followers(user_id=user_id, cursor=pagination, count=100, skip_status=True)
    else:
        onehundredfollowers, tokens = api.get_followers(user_id=user_id, cursor=-1, count=100, skip_status=True)

    followers_data = [r._json for r in onehundredfollowers]
    try:
        followersdf = pd.read_csv(followers_file, index_col=0)
    except pd.errors.EmptyDataError:
        # followersdf = pd.DataFrame()
        followersdf = pd.DataFrame({'id':[], 'id_str':[], 'name':[], 'screen_name':[], 'description':[], 'statuses_count':[], 'tweets_per_year':[], 'location':[]})

    new_followers = pd.DataFrame(followers_data)
    followersdf = pd.concat([followersdf, new_followers], ignore_index=True)
    followersdf = filter(description_string=nurse_description_string, df=followersdf)
    followersdf.to_csv(followers_file)

    #get next token
    next_token = tokens[-1]
    return next_token

call_count = 0

next_token = get_union_followers(pagination=1750455016348240442)
call_count += 1

while next_token:
    next_token = get_union_followers(next_token)
    call_count += 1

    print("Just finished call " + str(call_count))
    print("Next token: " + str(next_token))

