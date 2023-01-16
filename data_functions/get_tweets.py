import json
import os
import pandas as pd
import datetime as datetime
import tweepy
from pytz import utc
from authpy import authpy

journalist_directory = "journalisttweets"
journalist_followers_file = "data/filteredNUJfollowers.csv"
rail_directory = "railtweets"
rail_followers_file = "data/filteredRMTfollowers.csv"
musicians_directory = "musiciantweets"
musicians_followers_file = "data/filteredMUfollowers.csv"
musiciansfollowerdf = pd.read_csv(musicians_followers_file)
journalistsfollowerdf = pd.read_csv(journalist_followers_file)
railworkersfollowerdf = pd.read_csv(rail_followers_file)

def store_log(message):
    print(message)
    with open("gettweetsstorelog.txt", "a+") as file:
        file.write(str(message) + "\n")

client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAP46jQEAAAAAAFDtxA94KI%2B21x1LrlCLfEwkK1w%3DknqlAAkiTjZBMul2hnhbKEvEasHTPLXMiv4o9LiXgzdei1a1c0',
                       consumer_key='U2Qvj02fgz61HtzRJb92GRK6D',
                       consumer_secret='fUGXSZiChK3mKAjt3ascUEzfZa0y3bQJ6NdpbyktAenv6Wpwhw',
                       access_token_secret='erQnd9fLb20TrodIQJztsZngI26K1EaYphXVc6Xf2Wigs',
                       access_token='1582717564353904640-HhB6jWVTq1mWCOoNgX8IPYQ4uehW4C',
                       wait_on_rate_limit=True)

startDate = utc.localize(datetime.datetime(2019, 2, 1, 0, 0, 0))
endDate = utc.localize(datetime.datetime(2022, 9, 1, 0, 0, 0))

def get_tweets(id, directory = None, pagination=None):
    id_file = "{}/{}.csv".format(directory, id)

    with open(id_file, "a+") as f:
            try:
                currenttweetsdf = pd.read_csv(id_file, index_col=0)
            except pd.errors.EmptyDataError:
                currenttweetsdf = pd.DataFrame({'id':[], 'created_at':[]})

    if pagination:
        call = client.get_users_tweets(id=id, start_time=startDate, end_time=endDate, tweet_fields=['created_at'], pagination_token=pagination)
    else:
        call = client.get_users_tweets(id=id, start_time=startDate, end_time=endDate, tweet_fields=['created_at'])

    data = call.data
    meta = call.meta
    store_log(str(meta))

    newtweetsdf = pd.DataFrame(data)

    # join all the calls to the same dataframe
    currenttweetsdf = pd.concat([currenttweetsdf, newtweetsdf], ignore_index=True)

    currenttweetsdf.to_csv(id_file)

    return meta.get('next_token')


def call_get_tweets(followerdf = None, directory = None):
    for id in followerdf['id']:
        store_log("ID" + str(id))
        count=0
        next_token = get_tweets(int(id), directory)
        store_log("COUNT" + str(count))
        store_log("NEXT_TOKEN" + str(next_token))
        while next_token:
            count+=1
            next_token = get_tweets(int(id), directory, pagination = next_token)
            store_log("NEXT_TOKEN" + str(next_token))
            store_log("COUNT" + str(count))

    store_log("Finished - I got all the tweets!!")

# call_get_tweets(musiciansfollowerdf, musicians_directory)
# call_get_tweets(railworkersfollowerdf, rail_directory)
call_get_tweets(journalistsfollowerdf, journalist_directory)
