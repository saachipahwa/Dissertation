import pandas as pd
from authpy import authpy

#Gets followers from union twitter account


#Files to store followers
NUJ_followers_file = "data/NUJfollowers.csv"
MU_followers_file =  "data/MUfollowers.csv"
RMT_followers_file = "data/RMTfollowers.csv"
f = open(NUJ_followers_file, "w+")


#Retrieves api keys
api = authpy('credentials.json')


#User ID's of union accounts
RCON_ID = 54506896
NEU_ID = 884369177368199168
BMA_ID = 14243046
NUJ_ID = 335177549
MU_ID = 116720443
RMT_ID = 26020906


def store_log(message):
    print(message)
    with open("store_log.txt", "a+") as file:
        file.write(message + "\n")


try:
    api.verify_credentials()
    store_log('Successful Authentication')
except:
    store_log('Failed authentication')


#Calls API once
def get_union_followers(pagination = None, UNION_ID = None, followers_file = None):
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


#Calls get_union_followers repeatedley. Handles pagination.
def call_get_following(UNION_ID = None, followers_file = None):
    call_count = 0

    next_token = get_union_followers(UNION_ID = UNION_ID, followers_file = followers_file)
    call_count += 1

    while next_token:
        next_token = get_union_followers(pagination = next_token, UNION_ID = UNION_ID, followers_file = followers_file)
        call_count += 1

        store_log("Just finished call " + str(call_count))
        store_log("Next token: " + str(next_token))

