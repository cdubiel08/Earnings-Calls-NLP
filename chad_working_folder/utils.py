import pandas as pd
import string
import unicodedata
import contractions
import re

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

wn = WordNetLemmatizer()

stop_words = stopwords.words('english')
stop_words.extend(['said', 'would', 'subject', 'use', 'also', 'like', 'know', 'well', 'could', 'thing', '...', 'want', 'yeah', 'look', 'take', 'make', 'think', 'okay', 'right', 'come', 'become', 'you.s', 'name', 'i.e', 'many', 'much'])

stop_words = set(stop_words)
    
def clean_word(token, stop_words, min_word_length):
    
    # clean up non-ascii terms and stem the word
    clean_token = unicodedata.normalize('NFKD', token).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # Lemmatize nouns and verbs
    clean_token = wn.lemmatize(clean_token, pos='n')
    clean_token = wn.lemmatize(clean_token, pos='v')
    
    # check if token is in punctuation, if it's a stopword, and if it meets the length requirements
    if ((clean_token not in string.punctuation) and (clean_token not in stop_words) and (len(clean_token) >= min_word_length)):    
        # if all requirements are met, stem the word and return it
        return clean_token

def preprocess_text(text, stop_words=stop_words, min_word_length=3):
    if isinstance(text, str):
        # clean up contractions
        text = contractions.fix(text)

        # lowercase text
        text = text.lower()
        
        # strip html from the text
        text = re.sub('<[^<]+?>', '', text)
        
        # strip out standalone digits
        text = re.sub(r'\b\d+\b', '', text)

        # tokenize text into individual terms
        tokens = word_tokenize(text)

        # pass each token through the function that determines if we keep it or not.
        clean_tokens = [clean_word(w, stop_words, min_word_length) for w in tokens]
        clean_tokens = list(filter(None, clean_tokens))
        return clean_tokens