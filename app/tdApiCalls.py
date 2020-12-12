"""
Rexy
@author: abd
"""
import requests
import json
import re
from fuzzywuzzy import fuzz
from app.bertTransferLearning import BertTransferLearning
class TdApiCalls():
    def __init__(self):
        self.credentials = {'username': 'abadias', 'password':'Menphis16$'}
        self.td_url = "https://td.byui.edu/TDWebApi/api/auth"
        # this line is commented out since we don't want to get a token each time
        # it is valid for 24 hours
        #self.bearer_token = requests.post(td_url, data = credentials)
        self.bearer_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1bmlxdWVfbmFtZSI6ImFiYWRpYXMiLCJ0ZHhfZW50aXR5IjoiMSIsInRkeF9wYXJ0aXRpb24iOiIwIiwiaXNzIjoiVEQiLCJhdWQiOiJodHRwczovL3d3dy50ZWFtZHluYW1peC5jb20vIiwiZXhwIjoxNjA3ODg5ODY0LCJuYmYiOjE2MDc4MDM0NjR9.Hzl4O0y2zw0JM7TkOJ3DJ52VvgmPmWx4Ods01kIDaIU"
        self.query_url = "https://td.byui.edu/TDWebApi/api/75/knowledgebase/search"
        self.query_headers = {'Content-Type': 'application/json; charset=utf-8',
                     'Authorization': 'Bearer ' + self.bearer_token} # add .text when using new bearer token
        # for some of our functions to work we need to initialize the BERT class
        self.bertTransferLearning = BertTransferLearning()
        
    def make_kb_search(self, query_str):
        # object of type TeamDynamix.Api.KnowledgeBase.ArticleSearch
        query_body = {'Status': 3,
              'CustomAttributes': None,
              'SearchText': query_str,
              'CategoryID': None,
              'IsPublished': 'true',
              'IsPublic': None,
              'AuthorUID': None,
              'ReturnCount': 10,
              'IncludeArticleBodies': 'true',
              'IncludeShortcuts': 'false'}
        query = requests.post(self.query_url, json = query_body, headers = self.query_headers)
        return query.text
    def find_article_where_answer_might_be(self, query, query_str):
        raw_json = json.loads(query)
        most_likely_article = None
        most_likely_score = 0
        tag_regex = re.compile('<.*?>|\r|\n|&nbsp;|&quot;|&ndash;|&mdash;')
        clean_array = []
        for i in range(len(raw_json)):
            html_free_str = re.sub(tag_regex,'',raw_json[i]['Body'])
            html_free_str = re.sub(r"\s{2,}"," ", html_free_str)
            clean_array.append(html_free_str)
            score = fuzz.partial_ratio(query_str, html_free_str)
            if (score > most_likely_score):
                most_likely_score = score
                most_likely_article = i
        return(clean_array[most_likely_article], re.sub(r"\r|\n|\t","",raw_json[most_likely_article]['Body']))

    def splitter(self, n, splitted_string):
        splitted_string_array = []
        for i in range(0, len(splitted_string), n):
            splitted_string_array.append(" ".join(splitted_string[i:i+n]))
        return splitted_string_array
               
    def find_answer(self, query, query_str):
        raw_json = json.loads(query)
        tag_regex = re.compile('<.*?>|\r|\n|&nbsp;|&quot;|&ndash;|&mdash;')
        space_regex = re.compile('\s{2,}')
        answer = ""
        no_answer = False
        for i in range(len(raw_json)):
            html_free = re.sub(tag_regex," ",raw_json[i]['Body'])
            double_space_free = re.sub(space_regex," ", html_free)
            splitted_string = double_space_free.split()
            if len(splitted_string) > 380:
                for fragment in self.splitter(380, splitted_string):
                    prediction = self.bertTransferLearning.predict_answer(query_str, fragment)
                    if "[CLS]" not in prediction:
                        answer += prediction + "<br>"
                        no_answer = True
                
            else:
                prediction = self.bertTransferLearning.predict_answer(query_str, double_space_free)
                if "[CLS]" not in prediction:
                        answer += prediction + "<br>"
                        no_answer = True
                
        if no_answer == False:
            answer += "Sorry!, I wasn't able to find an answer to your question."
            
        return answer
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
