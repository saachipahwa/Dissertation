#Used to get usernames from ID's in nurses.csv

import json
import os

import pandas as pd
import requests

#Ensure to export these values using the terminal e.g. the following line
#export 'BEARER_TOKEN'='<your_bearer_token>'

# consumer_key = os.environ.get("CONSUMER_KEY")
# consumer_secret = os.environ.get("CONSUMER_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")

def create_url():
    # Replace with user ID below
    print("Step 1")
    user_id = 54506896
    return "https://api.twitter.com/2/users".format(user_id)

def get_params(pagination=None):
    print("Step 2")
    if pagination:
        return {"user.fields": "id,username,description,created_at", "pagination_token": "{}".format(pagination)}
    return {"user.fields": "id,username,description,created_at"}

def bearer_oauth(r):
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

