"""
Rexy
@author: abd
"""
import nltk
# nltk.download('averaged_perceptron_tagger') #need for first time
from nltk.tokenize import word_tokenize
import numpy as np

from fuzzywuzzy import fuzz

class InputProcessing():
    def optimizeForQuery(self, my_str):
        my_str = my_str.lower()
        # remove symbols, except question mark
        my_clean_str = ""
        for char in my_str:
            if char not in ["?","\\",".",",",":","\"","(",")","-","+","\'",";","{","}"]:
                my_clean_str += char
        
        # convert each word into a pos-tagged tuple
        tokenized_str = word_tokenize(my_clean_str)
        pos_tagged_str = nltk.pos_tag(tokenized_str)
        
        #extract only nouns and verbs
        final_str_array = []
        for tupl in pos_tagged_str:
            if tupl[1] in ["WRB","WDT","NN","NNS","NNP","NNPS","VB","VBD","VBG","VBN","VBP","VBZ","JJ"]:
                final_str_array.append(tupl[0])
        final_str = " ".join(final_str_array)
        return final_str
        
        
