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
        if w not in stop_words and w[0] != "@" and w[0] != ":" and "//t.co/" not in w and "https" not in w: 
            filtered_sentence += w + " " 
    
    return filtered_sentence

def get_user_text(api, id):
    text = ""
    try:
        feed = api.user_timeline(id)
        # feed += api.favorites(id)
    except Exception as e:
        print(e)
        return ""
    else:
        for s in feed:
            text += s.text + " "
        return clean(text)

def analyze(api, id):
    self_text = get_user_text(api, id)
    self_score = TextBlob(self_text)
    # print(self_text)
    # print(id, self_score.sentiment)

    friends = api.friends_ids(id)
    friends_text = ""
    for f_id in friends:
        friends_text += get_user_text(api, f_id) + " "
    friends_score = TextBlob(friends_text)
    # print("friend", friends_score.sentiment)

    keywords = most_frequent(self_text + friends_text)
    return self_score, friends_score, keywords

def most_frequent(text):
    str_list = text.lower().split()
    wordcount = {}
    for word in str_list:
        word = word.replace(".","").replace("?","").replace(" ","").replace(",","").replace(":","").replace("\"","").replace("!","").replace("â€œ","").replace("â€˜","").replace("*","")
        
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1

    word_counter = collections.Counter(wordcount)
    significant = ""
    for word, count in word_counter.most_common(300):
        if len(word) > 4:
            # print(word, ": ", count)
            significant += " " + word

    return significant