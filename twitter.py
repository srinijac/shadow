import tweepy
from time import sleep
from credentials import *
import os
import json
from collections import defaultdict

# login to twitter account api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

self_obj = api.me()
self_info = json.loads(json.dumps(self_obj._json))
self_id = self_info["id"]
print("self", self_id)

messages = api.list_direct_messages()
senders = []
for dm_obj in messages:
    dm_obj = str(json.dumps(dm_obj._json))
    dm_json = json.loads(dm_obj)
    sender = dm_json["message_create"]["sender_id"]

    if sender not in senders and str(sender) != str(self_id):
        senders.append(sender)

print(senders)

for s in senders:
    api.send_direct_message(int(s), "hello")