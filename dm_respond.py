import json

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

    global sent

    for s in senders and s not in sent:
        api.send_direct_message(int(s), "hello")
        sent.append(s)

    return sent

def report(api, id, score):
    response = ""
    polarity = score.sentiment[0]
    if polarity > 0:
        response += "right now, the text on your feed looks positive! "
    elif polarity < 0:
        response += "right now, the text on your feed looks negative :( "
    else:
        response += "right now, your feed is neutral. "

    response += "on a scale of 0 to 10 (0 being most negative, 10 as most positive), your feed scores a "
    scaled = polarity * 5 + 5
    response += str(round(scaled, 2)) + "."
    api.send_direct_message(id, response)
    # print(response)

    response = "we also looked at how personal your feed seemed to be."
    api.send_direct_message(id, response)
    # print(response)

    response = "on a scale of 0 to 10 (0 being most impersonal, 10 as most personal), your feed scores a "
    scaled = score.sentiment[1] * 10
    response += str(round(scaled, 2)) + "."
    api.send_direct_message(id, response)
    # print(response)

    return