import os
from io import StringIO
import pandas as pd
from pandas import read_csv
from searchtweets import ResultStream, load_credentials, collect_results, gen_request_parameters
import json

def separate_metrics(big_df):
    #turn public metrics into separate columns
    big_df = pd.concat([big_df, big_df['public_metrics'].apply(pd.Series)], axis=1)
    big_df = big_df.drop(columns = "public_metrics")

    return big_df

csv_file = "../data/healthcareworkertweets.csv"

nurse_hashtags = ["#nursethings", "#lifeasanurse", "#nurselife"]
healthcare_hashtags=["#healthcareworker", "#healthcareprofessional", "#nohealthcarewithoutselfcare"]
teacher_hashtags=["#teacher5oclockclub", "#teachertwitter", "#edchat", "#t2tchat"]
desired_hashtags = healthcare_hashtags

#API call
search_args=load_credentials("~/.twitter_keys.yaml",
                             yaml_key="search_tweets_v2",
                             env_overwrite=False)
tweets = []
for ht in desired_hashtags:
    query = gen_request_parameters("{} -is:retweet -is:nullcast".format(ht), None, results_per_call=500, start_time='2019-02-01T00:00', end_time='2022-09-01T00:00', user_fields='username, public_metrics',expansions='author_id')

    rs = ResultStream(request_parameters=query,
                      max_results=3000,
                      max_pages=1,
                      **search_args)

    tweets = tweets + list(rs.stream())

# [print(tweet) for tweet in nursetweets[0:10]]

big_df = pd.DataFrame()

print(len(tweets))

for call in tweets:
    data = call.get("data")
    user_fields = call.get("includes").get("users")

    #turn nursetweets into dataframe
    data = json.loads(json.dumps(data))
    text_df = pd.DataFrame(data)

    #turn user fields into dataframe
    user_fields = json.loads(json.dumps(user_fields))
    user_df = pd.DataFrame(user_fields).drop(columns = ['username', 'name'])

    user_df.rename(columns = {'id' : 'author_id'},  inplace=True)

    #join both df's together
    joint_df = pd.DataFrame.merge(text_df, user_df, how="inner", on=["author_id"])

    # join all the calls to the same dataframe
    big_df = pd.concat([big_df, joint_df], ignore_index=True)

big_df = separate_metrics(big_df)

#remove rows with less than ten followers or ten following
big_df = big_df.loc[big_df['following_count'] > 10]
big_df = big_df.loc[big_df['followers_count'] > 10]

#drops nursetweets that i've called more than once
big_df.drop_duplicates('id', ignore_index=True)
big_df.drop_duplicates('text', ignore_index=True)

big_df.to_csv(csv_file)



