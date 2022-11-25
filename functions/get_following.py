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

def filter(description_string = nurse_description_string, df = None, csv_file = None):
    if csv_file:
        df = pd.read_csv(csv_file)

    #filter description
    df["description"] = df["description"].fillna(value="None")
    df = df[df["description"].str.contains(description_string)]

    #filter tweetcount
    df['years_online'] = current_year - df["created_at"][:-4]
    df['tweets_per_year'] = df['statuses_count']/df['ye ars_online']
    df.to_csv(csv_file)

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
        followersdf = pd.DataFrame({'id':[], 'id_str':[], 'name':[], 'screen_name':[], 'description':[], 'statuses_count':[],'location':[]})


    new_followers = pd.DataFrame(followers_data)
    followersdf = pd.concat([followersdf, new_followers], ignore_index=True)
    followersdf.to_csv(followers_file)

    #get next token
    next_token = tokens[-1]
    return next_token

next_token = get_union_followers()
while next_token:
    next_token = get_union_followers()