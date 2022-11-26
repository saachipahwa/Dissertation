import json

import pandas as pd

from authpy import authpy
import datetime

followers_file = "data/RCONfollowers.csv"
api = authpy('credentials.json')

try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')


def get_union_followers(pagination = None):
    if pagination:
        onehundredfollowers, tokens = api.get_followers(user_id=54506896, cursor=pagination, count=100, skip_status=True)
    else:
        onehundredfollowers, tokens = api.get_followers(user_id=54506896, cursor="-1", count=100, skip_status=True)

    followers_data = [r._json for r in onehundredfollowers]

    try:
        followersdf = pd.read_csv(followers_file, index_col=0)
    except pd.errors.EmptyDataError:
        followersdf = pd.DataFrame({'id':[], 'id_str':[], 'name':[], 'screen_name':[], 'description':[],  'years_online':[], 'statuses_count':[], 'tweets_per_year':[], 'location':[]})

    new_followers_df = pd.DataFrame(followers_data)
    followersdf = pd.concat([followersdf, new_followers_df], ignore_index=True)
    followersdf.to_csv(followers_file)

    #get next token
    next_token = tokens[-1]
    return next_token

call_count = 0

next_token = get_union_followers()
call_count += 1

while call_count<2:
    next_token = get_union_followers(next_token)
    call_count += 1

    print("Just finished call " + str(call_count))
    print("Next token: " + str(next_token))

