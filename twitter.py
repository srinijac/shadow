import tweepy
from credentials import *
from dm_respond import *
from sentiment import *

# login to twitter account api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

sent = []
sent = respond_hello(api)

def main():
    shadowing = api.followers_ids() 
    for id in shadowing: # can use mentions_timeline?
        report(api, id, analyze(api, id))

main()