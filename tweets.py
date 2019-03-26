#!/usr/bin/env python

#-----------------------------------------------------------------------
# twitter-stream-format:
#  - ultra-real-time stream of twitter's public timeline.
#    does some fancy output formatting.
#-----------------------------------------------------------------------

from twitter import *
import re

search_term = "Google,google"

#-----------------------------------------------------------------------
# import a load of external features, for text display and date handling
# you will need the termcolor module:
#
# pip install termcolor
#-----------------------------------------------------------------------
from time import strftime
from textwrap import fill
from termcolor import colored
from email.utils import parsedate

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
import sys
sys.path.append(".")
import config
import codecs

#-----------------------------------------------------------------------
# create twitter streaming API object
#-----------------------------------------------------------------------
auth = OAuth(config.access_key,
             config.access_secret,
             config.consumer_key,
             config.consumer_secret)
stream = TwitterStream(auth = auth, secure = True)

#-----------------------------------------------------------------------
# iterate over tweets matching this filter text
#-----------------------------------------------------------------------
tweet_iter = stream.statuses.filter(track = search_term,language="en",encoding="ascii")

pattern = re.compile("%s" % search_term, re.IGNORECASE)
file= open("google.txt","w")
i=0
for tweet in tweet_iter:
    #if 'lang' in tweet and tweet['lang']=='en':
    # turn the date string into a date object that python can handle
    timestamp = parsedate(tweet["created_at"])

    # now format this nicely into HH:MM:SS format
    timetext = strftime("%H:%M:%S", timestamp)

    # colour our tweet's time, user and text
    time_colored = colored(timetext, color = "white", attrs = [ "bold" ])
    user_colored = colored(tweet["user"]["screen_name"], "green")
    text_colored = tweet["text"]

    # replace each instance of our search terms with a highlighted version
    #text_colored = pattern.sub(colored(search_term.upper(), "yellow"), text_colored)

    # add some indenting to each line and wrap the text nicely
    #indent = " " * 11
    #text_colored = fill(text_colored, 80, initial_indent = indent, subsequent_indent = indent)

    # now output our tweet
    #sa= str(text_colored)
    st = ' @'+ tweet["user"]["screen_name"] + '\t'+ tweet["text"]
    #st = str(st)
    st= st.encode("utf-8","replace")
    #st = unicode(st, "utf-8", errors="ignore")
    #st = (str(text_colored)+ ' @'+ str(user_colored)).encode('ascii','ignore')
    file.write(st + '\n')
    #print("(%s) @%s" % (time_colored, user_colored))
    #print("%s" % (text_colored))
    if(i > 300):
        break
    i= i+1
file.close()
