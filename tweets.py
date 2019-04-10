#!/usr/bin/env python

import sys
import config
import tweepy
import time
import operator
import re
import pprint

# setup
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)
result = ""
search_terms = ["Apple", "apple"]
filename = "apple.txt"
tweet_count = 300

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

class StreamListener(tweepy.StreamListener):
    def __init__(self):
        self.saveFile = open(filename, 'a')
        self.count = 0
        super(StreamListener, self).__init__()

    def on_status(self, status):
        if (self.count <= tweet_count):
            text = status._json['text']
            text = re.sub(r'https:\/\/.*[\s\r\n]*', '', text, flags=re.MULTILINE)
            text = text.lower().rstrip("\n\r\t")
            if  (isEnglish(text)) and \
                (not status.retweeted) and \
                (text.startswith('rt ')) and\
                len(text) > len(search_terms[0]):
                if any(word in text for word in search_terms):
                    print(text)
                    self.saveFile.write(text)
                    self.saveFile.write('\n')
                    self.count += 1
            return True
        else:
            self.saveFile.close()
            return False
    def on_error(self, status_code):
        if status_code == 420:
            return False

# start stream
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=search_terms, encoding="ascii")
