import sys
import config
import tweepy
import time
import operator
# import pprint

# setup
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)
fullStream=""
hashtags = {}
numSecs = 600


