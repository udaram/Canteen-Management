from textblob import TextBlob 

def analyse(text):
    s = TextBlob(text)
    p = s.sentiment.polarity
    if(p>0.5):
        return "POSITIVE"
    if(p==0.5):
        return 'NEUTRAL'
    else: 
        return "NEGATIVE"

