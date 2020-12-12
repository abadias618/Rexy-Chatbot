"""
Rexy
@author: abd
"""
import nltk
#nltk.download('punkt') #need for first time
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tensorflow as tf
from tensorflow import keras
import random 
import json

from app.input_processing import InputProcessing
from app.tdApiCalls import TdApiCalls
from app.bertTransferLearning import BertTransferLearning

class Intro_Bot():
    def __init__(self):
        with open("app/intro_data.json") as file:
            self.data = json.load(file)
        
        words = []
        labels = []
        docs_x = []
        docs_y = []
        #stemming
        for intent in self.data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])
                
            if intent["tag"] not in labels:
                labels.append(intent["tag"])
        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        self.words = sorted(list(set(words)))
        
        self.labels = sorted(labels)
        
        #load model
        self.model = keras.models.load_model("app/intro_rexy_saved_model")
        
    def bag_of_words(self, s, words):
        bag = [ 0 for _ in range(len(words))]
        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]
        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
        return np.array(bag)
    
    def chat(self, user_message):
        inp = user_message.lower()
        results = self.model.predict(self.bag_of_words(inp, self.words).reshape(-1,75))
        results_index = np.argmax(results)
        result = results[0][results_index]
        tag = self.labels[results_index]
        
        for tg in self.data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]
        print(result)
        print(tag)
        bot_response = ""
        if result < 0.6:
            bot_response += "I'm think that you are " + tag + " me. Can you rephrase a little so I can be sure?"
        elif tag == "asking a question to":
            inputProcessing = InputProcessing()
            optimized_usr_message = inputProcessing.optimizeForQuery(user_message)
            tdApiCalls = TdApiCalls()
            api_response = tdApiCalls.make_kb_search(optimized_usr_message)
            bot_response += tdApiCalls.find_answer(api_response, user_message)
        else:
            bot_response += random.choice(responses)
        return bot_response

            

 