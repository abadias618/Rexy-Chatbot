"""
Rexy
@author: abd
"""
import requests
import json
import re
from fuzzywuzzy import fuzz
class TdApiCalls():
    def __init__(self):
        self.credentials = {'username': 'abadias', 'password':'Menphis16$'}
        self.td_url = "https://td.byui.edu/TDWebApi/api/auth"
        # this line is commented out since we don't want to get a token each time
        # it is valid for 24 hours
        #self.bearer_token = requests.post(td_url, data = credentials)
        self.bearer_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1bmlxdWVfbmFtZSI6ImFiYWRpYXMiLCJ0ZHhfZW50aXR5IjoiMSIsInRkeF9wYXJ0aXRpb24iOiIwIiwiaXNzIjoiVEQiLCJhdWQiOiJodHRwczovL3d3dy50ZWFtZHluYW1peC5jb20vIiwiZXhwIjoxNjA3Nzc3NjQxLCJuYmYiOjE2MDc2OTEyNDF9.Z3qXbUTb5JyMiYYVWnnli_FSdBFxOnevMMfOMHgGq1o"
        self.query_url = "https://td.byui.edu/TDWebApi/api/75/knowledgebase/search"
        self.query_headers = {'Content-Type': 'application/json; charset=utf-8',
                     'Authorization': 'Bearer ' + self.bearer_token} # add .text when using new bearer token
        
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

