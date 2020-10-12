# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 09:42:56 2018

@author: A103932
"""

import json

import http.client

import pandas as pd

tmdb = pd.read_csv('movie_tmdb.csv')

class Movie(object):
    def __init__(self, n):
        try:
            self.id = tmdb.loc[tmdb['Title']==n, "Tmdb_id"].values[0]
        except:
            self.id = None
    def get_result(self, use_static=1, api_key = '92e447debf2441468e90b59d45b39608'):
        if self.id is None:
            return 0,0,False
        if use_static == 1:
            self.vote_average = tmdb.loc[tmdb['Tmdb_id']==self.id, "vote_average"].values[0]
            self.vote_count = tmdb.loc[tmdb['Tmdb_id']==self.id, "vote_count"].values[0]
            self.popularity = tmdb.loc[tmdb['Tmdb_id']==self.id, "popularity"].values[0]
        else:
            conn = http.client.HTTPSConnection("api.themoviedb.org")
            payload = "{}"
            url = "/3/movie/"+str(self.id)+"?language=en-US&api_key="+str(api_key)
            conn.request("GET", url, payload)
            res = conn.getresponse()
            data = res.read()
            self.vote_average = json.loads(data)['vote_average']
            self.vote_count = json.loads(data)['vote_count']
            self.popularity = json.loads(data)['popularity']
        return self.vote_average,self.popularity,True

    
    


