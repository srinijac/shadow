from textblob import TextBlob
import collections
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

stop_words = set(stopwords.words('english')) 

def clean(text):
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    
    filtered_sentence = ""
    for w in word_tokens: 
        if w not in stop_words and w[0] != "@": 
            filtered_sentence += w + " " 
    
    return filtered_sentence

def get_user_text(api, id):
    text = ""
    feed = api.user_timeline(id)
    feed += api.mentions_timeline()
    for s in feed:
        text += s.text + " "
    return clean(text)

def analyze(api, id):
    self_text = get_user_text(api, id)
    self_score = TextBlob(self_text)
    # print(id, self_score.sentiment)

    friends = api.friends_ids(id)
    friends_text = ""
    for f_id in friends:
        friends_text += get_user_text(api, f_id) + " "
    friends_text.trim()
    friends_score = TextBlob(friends_text)

    most_frequent(self_text + friends_text)
    return (self_score * 0.8) + (friends_score * 0.2)

def most_frequent(text):
    str_list = text.lower().split()
    wordcount = {}
    for word in str_list:
        word = word.replace(".","")
        word = word.replace("?","")
        word = word.replace(" ","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace("\"","")
        word = word.replace("!","")
        word = word.replace("â€œ","")
        word = word.replace("â€˜","")
        word = word.replace("*","")
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1

    word_counter = collections.Counter(wordcount)
    for word, count in word_counter.most_common(10):
        print(word, ": ", count)

    # print(most_occur) 

    return