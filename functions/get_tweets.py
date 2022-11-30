import json
import os
import pandas as pd
import datetime as datetime
import tweepy
from pytz import utc
from authpy import authpy

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

def get_tweets(id):
    id_file = "tweets/{}.csv".format(id)

    with open(id_file, "a+") as f:
            try:
                currenttweetsdf = pd.read_csv(id_file, index_col=0)
            except pd.errors.EmptyDataError:
                currenttweetsdf = pd.DataFrame({'id':[], 'created_at':[]})

    call = client.get_users_tweets(id=id, start_time=startDate, end_time=endDate, tweet_fields=['created_at'])

    data = call.data
    meta = call.meta
    store_log(str(meta))

    newtweetsdf = pd.DataFrame(data)

    # join all the calls to the same dataframe
    currenttweetsdf = pd.concat([currenttweetsdf, newtweetsdf], ignore_index=True)

    currenttweetsdf.to_csv(id_file)

    return meta.get('next_token')

followers_file = "data/filteredRCONfollowers.csv"
followerdf = pd.read_csv(followers_file)
for id in followerdf['id']:
    count=0
    store_log(id)
    store_log(count)
    next_token = get_tweets(int(id))
    store_log(next_token)
    while next_token:
        count+=1
        next_token = get_tweets(int(id))
        store_log(next_token)
        store_log(count)

# def get_tweets(id):
#     id_file = "tweets/{}.json".format(id)
#
#     tweets = []
#     tmpTweets = api.user_timeline(user_id=id, exclude_replies=False, include_rts=False)
#     print(tmpTweets)
#
#     for tweet in tmpTweets:
#         if endDate > tweet.created_at > startDate:
#             tweets.append(tweet._json)
#             print("1")
#             print(tweet)
#
#     print("Last in list created at: " + str(tmpTweets[-1].created_at))
#
#     while tmpTweets[-1].created_at > startDate:
#         tmpTweets = api.user_timeline(user_id=id, max_id = tmpTweets[-1].id, exclude_replies=False,include_rts=False)
#         for tweet in tmpTweets:
#             if endDate > tweet.created_at > startDate:
#                 tweets.append(tweet._json)
#                 print("2")
#                 print(tweet)
#
#     #WRITE TO CSV
#     with open(id_file, "a+") as f:
#         try:
#             tweetdf = pd.read_csv(id_file, index_col=0)
#         except pd.errors.EmptyDataError:
#             tweetdf = pd.DataFrame({'id':[], 'created_at':[]})
#
#         newtweetdf = pd.DataFrame(tweets)
#         tweetdf = pd.concat([tweetdf, newtweetdf], ignore_index=True)
#         tweetdf.to_csv(id_file)
#
#     #WRITING TO JSON
#     # for t in tmpTweets:
#     #     json_string = json.dumps(t._json)
#     #     with open("{}.json".format(20465706), "a+") as f:
#     #         f.write(json_string + "\n")
#     #         print("wrote it")
#
#
# get_tweets(20465706)

