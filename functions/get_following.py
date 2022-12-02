import json

import pandas as pd
from authpy import authpy
import datetime

followers_file = "data/NEUfollowers.csv"
api = authpy('credentials.json')
RCON_ID = 54506896
NEU_ID = 884369177368199168
BMA_ID = 14243046 #BMA call 361+186: 1520753044442708727
UNION_ID = NEU_ID

def store_log(message):
    print(message)
    with open("store_log.txt", "a+") as file:
        file.write(message + "\n")

try:
    api.verify_credentials()
    store_log('Successful Authentication')
except:
    store_log('Failed authentication')

def get_union_followers(pagination = None):
    if pagination:
        twohundredfollowers, tokens = api.get_followers(user_id=UNION_ID, cursor=pagination, count=200, skip_status=True)
    else:
        twohundredfollowers, tokens = api.get_followers(user_id=UNION_ID, cursor="-1", count=200, skip_status=True)

    store_log("Got " + str(len(twohundredfollowers)) + " followers")
    followers_data = [r._json for r in twohundredfollowers]

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

while next_token:
    next_token = get_union_followers(next_token)
    call_count += 1

    store_log("Just finished call " + str(call_count))
    store_log("Next token: " + str(next_token))

