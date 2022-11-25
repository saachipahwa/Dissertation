import json
import os

import pandas as pd
import requests

#Ensure to export these values using the terminal e.g. the following line
# export 'BEARER_TOKEN'='AAAAAAAAAAAAAAAAAAAAAP46jQEAAAAAXX7xy9q80JEZRBqAE%2FxD7WxSlp4%3Dt77E05zPiYq7DevlPiiQohTK9T2BXnZlqWgX3PGtrDDBrZPX7b'
# consumer_key = os.environ.get("CONSUMER_KEY")
# consumer_secret = os.environ.get("CONSUMER_SECRET")
from requests_oauthlib import OAuth1Session

bearer_token = os.environ.get("BEARER_TOKEN")
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
request_token_url = "https://api.twitter.com/oauth/request_token"

def create_url():
    # Replace with user ID below
    print("Step 1")
    user_id = 54506896
    return "https://api.twitter.com/2/users/{}/followers".format(user_id)

def get_params(pagination=None):
    print("Step 2")
    if pagination:
        return {"user.fields": "id,username,description,created_at,public_metrics", "pagination_token": "{}".format(pagination)}
    return {"user.fields": "id,username,description,created_at"}

def oauth(r):
    """
    Method required by bearer token authentication.
    """

    print("Step 3")
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r

def connect_to_endpoint(url, params):
    print("Step 4")
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def callAPIgetJson(pagination=None):
    url = create_url()
    params = get_params(pagination)
    json_response = connect_to_endpoint(url, params)
    # return json_response
    print(json.dumps(json_response, indent=4, sort_keys=True))

    try:
        #file.csv is an empty csv file
        current_df = pd.read_csv("data/followingRCON.csv", index_col=0)
    except pd.errors.EmptyDataError:
        current_df = pd.DataFrame()

    data = json_response.get("data")

    #turn tweets into dataframe
    data = json.loads(json.dumps(data))
    new_df = pd.DataFrame(data)
    current_df = pd.concat([current_df, new_df], ignore_index=True)

    current_df.to_csv("data/followingRCON.csv")

    #get next token
    next_token = json_response.get("meta").get("next_token")
    next_token = json.loads(json.dumps(next_token))
    return next_token

next_token = callAPIgetJson(pagination="0N7OC4BUC131GZZZ")
i = 0
while i < 9:
    next_token = callAPIgetJson(pagination=next_token)
    with open("tokens.txt", "a+") as f:
        f.write(next_token)
    i += 1
print(next_token)


def filter4nurses(csv_file = "data/followingRCON.csv"):
    df = pd.read_csv(csv_file)
    df["description"] = df["description"].fillna(value="None")
    df = df[df["description"].str.contains("nurse|nursing")]
    df.to_csv(csv_file)

# filter4nurses()
