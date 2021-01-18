import pandas as pd
import string
import unicodedata
import contractions
import re

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import matplotlib.pyplot as plt
import numpy as np

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
    

# Custom plotting function to capture the top n most influential coefficients for a trained model
def getTopCoefs(num_terms, model, class_labels, feature_names):

    # Pull the coefficient values for the regression
    coef_vals = model.coef_

    # set a few variables
    tmp_weights=[]
    terms=[]
    group = []
    vals = []
    color_grid = np.full((num_terms*len(coef_vals),len(coef_vals)), 'w', object)
    
    counter=0
    # loop through the coefficient values
    for i in range(len(coef_vals)):
        weights = list(coef_vals[i])

        # Reverse sort the coefficient weights and pull out the top values
        max_coef_weights = sorted(weights, reverse=True)[:num_terms]

        # Append the label name to a list
        group.append(class_labels[i])

        # Within each label group, loop through the top coefficients
        for j in max_coef_weights:
            color_grid[counter, i] = 'orange'
            counter += 1
            
            coef = weights.index(j)
            
            # Create a list of the label name and the cofficient name
            terms.append(group[i] + " - " + feature_names[coef])

            # Within each coefficient, pull the weights for the other labels
            for k in range(len(coef_vals)):
                other_weights = list(coef_vals[k])

                #Create a list of the weights (rounded to 3 decimal places)
                tmp_weights.append(round(other_weights[coef],3))

            # append the list of weights to a list of weight lists
            vals.append(tmp_weights)

            # before moving to the next coefficient, reset the weights list
            tmp_weights=[]

    # I decided to use matplotlib to create my table of coeffient weights
    # To do this, I turned off all of the actual plot lines
    ax = plt.subplot(frame_on=False)

    # Hide axes
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False)
    table = plt.table(cellText=vals,
              colLabels=group,
              rowLabels=terms,
              loc='top',
              cellColours = color_grid
             )
    # increase font size
    table.set_fontsize(20)
    table.scale(2,2)
    plt.show()