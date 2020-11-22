import json
from textblob import TextBlob
import random

notes = ["enjoy!", "for you:", "check this out!", "you might like this!", "take a look:", "looking for this?", "your shadow tells me you might like this", "from your shadow,"]

negative_pl = ["https://open.spotify.com/playlist/5FmmxErJczcrEwIFGIviYo", 
"https://open.spotify.com/playlist/37i9dQZF1DX2yvmlOdMYzV", 
"https://open.spotify.com/playlist/37i9dQZF1DWTQwRw56TKNc",  
"https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn",  
"https://open.spotify.com/playlist/37i9dQZF1DWTx0xog3gN3q", 
"https://open.spotify.com/playlist/37i9dQZF1DXdbXrPNafg9d", 
"https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO", 
"https://www.youtube.com/watch?v=g8NVwN0_mks&ab_channel=knoPianoMusic"]
neutral_pl = ["https://open.spotify.com/playlist/37i9dQZF1DX4UtSsGT1Sbe",
"https://open.spotify.com/album/0WSpHK6tinGHU4gvP8fHih", 
"https://open.spotify.com/album/0k6vua6Xz4B14Lwl7VBonP", 
"https://open.spotify.com/playlist/7jnm4kGjsaT08AbVB5798m", 
"https://open.spotify.com/playlist/0rZJqZmX61rQ4xMkmEWQar", 
"https://open.spotify.com/artist/3WrFJ7ztbogyGnTHbHJFl2", 
"https://open.spotify.com/playlist/37i9dQZF1DX5Ejj0EkURtP", ]
positive_pl = ["https://www.youtube.com/watch?v=p1IChPfD2-s&ab_channel=HappyMusic",
"https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4", 
"https://open.spotify.com/playlist/37i9dQZF1DX9wC1KY45plY",  
"https://open.spotify.com/artist/3fMbdgg4jU18AjLCKBhRSm", 
"https://open.spotify.com/playlist/37i9dQZF1DXa2PvUpywmrr", 
"https://open.spotify.com/playlist/37i9dQZF1DWY4xHQp97fN6", 
"https://open.spotify.com/playlist/37i9dQZF1DWWXrKtH3fzUd", 
"https://open.spotify.com/playlist/37i9dQZF1DX4dyzvuaRJ0n",]

def respond_hello(api):
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
    # global sent

    for s in senders:
        api.send_direct_message(int(s), "hello")
        # sent.append(s)

    return

def report(api, id, score):
    response = ""

    friend_score = score[-1]
    friend_polarity = friend_score.sentiment[0]

    score = score[0]
    polarity = score.sentiment[0]
    
    polarity = 0.2 * polarity + 0.8 * friend_polarity

    if polarity > 0:
        response += "right now, your feed looks positive! "
        playlist = positive_pl
    elif polarity < 0:
        response += "right now, your feed looks negative :( "
        playlist = negative_pl
    else:
        response += "right now, your feed is neutral. "
        playlist = neutral_pl

    response += "on a scale of 0 to 10 (0 being most negative, 10 as most positive), your feed scores a "
    scaled = polarity * 5 + 5
    response += str(round(scaled, 2)) + "."
    api.send_direct_message(id, response)
    print(response)

    response = "we also looked at how personal your feed seemed to be. on a scale of 0 to 10 (0 being most impersonal, 10 as most personal), your feed scores a "
    scaled = score.sentiment[1] * 10
    response += str(round(scaled, 2)) + "."
    api.send_direct_message(id, response)
    print(response)

    response = "here's something to listen to that might fit your mood: " + random.choice(playlist)
    api.send_direct_message(id, response)
    print(response)

    return

def recommend(api, id, keywords):
    positive = keywords.split()
    positive.sort(key = lambda w: TextBlob(w).sentiment[0], reverse = True)
    print(positive)
    
    count = 0
    while count < 3 and len(positive) > 3:
        query = positive.pop(0) + " " + positive.pop(0) + " " + positive.pop(0)
        result = api.search(query, result_type="popular", count=1)
        
        print(query)
        for r in result:
            screen_name = r.user.screen_name
            tweet_id = r.id_str
            url = "https://twitter.com/" + screen_name + "/status/" + tweet_id
        
        user = api.get_user(id)
        try:
            tweet_text = "@" + str(user.screen_name) + " " + random.choice(notes) + "\n" + str(url)
            tweet = api.update_status(tweet_text)
        except Exception as e:
            print(e)
        count += 1

    return