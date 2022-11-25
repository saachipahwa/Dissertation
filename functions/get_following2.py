import tweepy
from authpy import authpy
api = authpy('credentials.json')

try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')