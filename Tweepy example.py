# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 11:17:17 2021

@author: ryanp
"""

import tweepy
import json
#%% import json token file
with open(r'C:\Users\ryanp\OneDrive\Documents\NIU\MST 691 Data Science Tools and Techniques\Code\tweepy_tokens.json') as json_file:
    token = json.load(json_file)
#%% set up tweepy
auth = tweepy.OAuthHandler(token['consumer_key'], token['consumer_secret'])
auth.set_access_token(token['access_token'], token['access_token_secret'])
api = tweepy.API(auth)
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
#%% 
# Get the User object for twitter...
user = api.get_user('twitter')
user.screen_name
user.followers_count
#dir(user)
for friend in user.friends():
    print(friend.screen_name)