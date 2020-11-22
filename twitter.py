import tweepy
from credentials import *
from message import *
from sentiment import *

# login to twitter account api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

sent = []
sent = respond_hello(api)

def main():
    shadowing = api.followers_ids() 
    for id in shadowing:
        self_score, friends_score, keywords = analyze(api, id)
        report(api, id, [self_score, friends_score])
        recommend(api, id, keywords)

main()