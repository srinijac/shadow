from textblob import TextBlob
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

stop_words = set(stopwords.words('english')) 

def analyze(api, id):
    text = ""
    feed = api.user_timeline(id)
    feed += api.mentions_timeline()
    for s in feed:
        text += s.text + " "
    
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    
    filtered_sentence = ""
    for w in word_tokens: 
        if w not in stop_words and w[0] != "@": 
            filtered_sentence += w + " "   

    score = TextBlob(filtered_sentence)
    # print(id, score.sentiment)
    return score