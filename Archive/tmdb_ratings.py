# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 09:42:56 2018

@author: A103932
"""
import time

start = time.time()

#import sys

api_key = "92e447debf2441468e90b59d45b39608"#sys.argv[1]

"""Finding 300 most popular comedy movies relaeased 2000 or later"""

import json

import http.client

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

import numpy as np

import pandas as pd

movie_data = pd.read_csv('movie_tmdb.csv')

movie_ids = list(movie_data['Tmdb_id'].unique())

vote_average = []

vote_count = []

popularity = []

page = 1 #count for pages
req = 1 #count for requests

for movie_id in movie_ids:
    if req == 41:
        time.sleep(10)
        req = 1
    url = "/3/movie/"+str(movie_id)+"?language=en-US&api_key="+str(api_key)
    conn.request("GET", url, payload)
    res = conn.getresponse()
    data = res.read()
    vote_average.append(json.loads(data)['vote_average'])
    vote_count.append(json.loads(data)['vote_count'])
    popularity.append(json.loads(data)['popularity'])
    req += 1       

movie_details = pd.DataFrame({'movie_id':movie_ids, 'vote_average':vote_average, 'vote_count':vote_count,
                              'popularity':popularity})

end = time.time()

print('Start is : '+str(start)+', End is :'+str(end)+', Time taken:'+str(end-start))


