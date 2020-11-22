import json
from textblob import TextBlob
import random

notes = ["enjoy!", "for you:", "check this out!", "you might like this!", "take a look:"]

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
        response += "right now, the text on your feed looks positive! "
    elif polarity < 0:
        response += "right now, the text on your feed looks negative :( "
    else:
        response += "right now, your feed is neutral. "

    response += "on a scale of 0 to 10 (0 being most negative, 10 as most positive), your feed scores a "
    scaled = polarity * 5 + 5
    response += str(round(scaled, 2)) + "."
    # api.send_direct_message(id, response)
    print(response)

    response = "we also looked at how personal your feed seemed to be."
    # api.send_direct_message(id, response)
    # print(response)

    response = "on a scale of 0 to 10 (0 being most impersonal, 10 as most personal), your feed scores a "
    scaled = score.sentiment[1] * 10
    response += str(round(scaled, 2)) + "."
    # api.send_direct_message(id, response)
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
        tweet_text = "@" + str(user.screen_name) + " " + random.choice(notes) + "\n" + str(url)
        tweet = api.update_status(tweet_text)

        count += 1

    return