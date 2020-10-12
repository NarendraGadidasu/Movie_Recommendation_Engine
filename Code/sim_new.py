# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 23:38:10 2018

@author: sk953947
"""

import csv
import numpy as np
import scipy.sparse
import pandas as pd
import collections
import Movie_Class
import json

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = (value - leftMin) / leftSpan

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def Similarity(table):
    sA = scipy.sparse.csr_matrix(table)
    DotProducts = sA.dot(sA.T)       

    # kronecker product of row norms
    #NormKronecker = np.array([np.linalg.linalg.norm(table, axis=1)]) * np.array([np.linalg.linalg.norm(table, axis=1)]).T
    
    return DotProducts.toarray()

def getdata(data_path = 'all_movies_2000.csv'):
    #data = np.genfromtxt('sample.csv', dtype=int, delimiter=',', names=True) 
    with open(data_path, 'r', encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',')
        # get header from first row
        headers = next(reader)
        # get all the rows as a list
        data = list(reader)
        # transform data into numpy array
        data = np.array(data)
    print(headers)
    return data

def GetMoviesList(data_path = 'movie_list_updated.csv'):
    with open(data_path, 'r', encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',')
        # get header from first row
        headers = next(reader)
        # get all the rows as a list
        data = list(reader)
        # transform data into numpy array
        data = np.array(data)
    print(headers)
    return data
        
class MovieData(object):
    def __init__(self,data_path = 'all_movies_2000.csv',movie_path ='movie_list_updated.csv'):
        data = getdata(data_path)
        print(data.shape)
        
        movies_list = GetMoviesList(movie_path)
        
        movie_freq = collections.Counter(data[:,0])

        self.movie_key_dict = {}
        self.movie_idx_list = list(movie_freq.keys())
        
        for movie in movies_list:
            self.movie_key_dict[movie[1]] = int(movie[0])
            self.movie_idx_list[int(movie[0])] = movie[1]
            
        trope_freq = collections.Counter(data[:,1])
        
        self.trope_key_dict = {}
        self.trope_idx_list = list(trope_freq.keys())
        for idx,key in enumerate(trope_freq.keys()):
            self.trope_key_dict[key] = idx
        
        trope_freq_values = np.array(list(trope_freq.values()))
        trope_weight = translate(trope_freq_values,2,trope_freq_values.max(),1,0.5)
        
        self.trope_table = np.zeros((len(movie_freq),len(trope_freq)))
        self.trope_table_presense = np.zeros((len(movie_freq),len(trope_freq)))
        
        for item in data:
            self.trope_table[self.movie_key_dict[item[0]],self.trope_key_dict[item[1]]] = trope_weight[self.trope_key_dict[item[1]]]
            self.trope_table_presense[self.movie_key_dict[item[0]],self.trope_key_dict[item[1]]] = 1
    
#select some 5 randon movies
#user_movies_idx = np.random.randint(len(movie_idx_list), size=5)
#user_movies_idx = np.array([140,345,862])
    def getSimilarMovies(self,user_movies_idx,trope_weights):
        
        jsonresult = {}
        user_req_movies = {}
        similar_movies_dict = {}
        trope_weight_dict = {}
        
        user_movies_idx = np.array(user_movies_idx)
        user_movies_tropes = self.trope_table_presense[user_movies_idx,:].sum(axis=0)
        user_tropes_idx = (user_movies_tropes.argsort()[::-1])
        
        new_trope_table = self.trope_table * user_movies_tropes
        
        CosineSimilarityNew = Similarity(new_trope_table)

        #update the trope
        user_movies_tropes = new_trope_table[user_movies_idx,:].sum(axis=0)
        if trope_weights is not None:
            extra_weight = np.zeros_like(user_movies_tropes)
            extra_weight[user_tropes_idx[:10]] = trope_weights
            new_trope_table = new_trope_table + extra_weight        
            CosineSimilarityNew = Similarity(new_trope_table)
            user_movies_tropes = new_trope_table[user_movies_idx,:].sum(axis=0)
        scores = user_movies_tropes[user_tropes_idx]
        trope_scores = scores / np.linalg.norm(scores)
        
        for i,idx in enumerate(user_tropes_idx[:10]):
            temp = {}
            temp['trope'] = self.trope_idx_list[idx]
            temp['weight'] = str(trope_scores[i])
            trope_weight_dict[str(idx)] = temp
            
        
        #print(CosineSimilarityNew)
        
        user_interest = CosineSimilarityNew[user_movies_idx,:].sum(axis = 0)
        similar_movies_idx = user_interest.argsort()[::-1]
        final_results = similar_movies_idx[~np.in1d(similar_movies_idx,user_movies_idx)]
        
        vote_avg_list = []
        pop_list = []
        count = 0
        fail_idx = []
        for i,idx in enumerate(final_results[:30]):
            M = Movie_Class.Movie(self.movie_idx_list[idx])
            vote_avg,popularity,result = M.get_result()
            if result:
                count = count + 1
            else:
                fail_idx.append(i)
            vote_avg_list.append(vote_avg)
            pop_list.append(popularity)
            
        avg_vote_avg = sum(vote_avg_list)/count
        avg_pop = sum(pop_list)/count
        
        for idx in fail_idx:
            vote_avg_list[idx] = avg_vote_avg
            pop_list[idx] = avg_pop
        
        vote_avg_list = np.array(vote_avg_list)
        pop_list = np.array(pop_list)
        scores = user_interest[final_results[:30]]
        new_scors = translate(scores,scores.min(),scores.max(),0,1)
        new_vote_avg = translate(vote_avg_list,vote_avg_list.min(),vote_avg_list.max(),0,1)
        new_pop_list = translate(pop_list,pop_list.min(),pop_list.max(),0,1)
        
        scores = new_scors + new_vote_avg + new_pop_list
        
        new_scors = translate(scores,scores.min(),scores.max(),0,1)
        #final_results = np.setdiff1d(similar_movies_idx,user_movies_idx)[:10]
        
        idx_idx = new_scors.argsort()[::-1]
        """
        for idx in user_movies_idx:
            print(self.movie_idx_list[idx])
        print("similar movies")
        for i,temp_idx in enumerate(idx_idx[:10]):
            idx = final_results[temp_idx]
            print(self.movie_idx_list[idx],new_scors[temp_idx])
        """
        for idx in user_movies_idx:
            temp = {}
            a = self.trope_table[idx,user_tropes_idx[:10]]
            a[a !=0] = 1
            temp['movie'] = self.movie_idx_list[idx]
            temp['tropes'] = pd.Series(a.astype(int)).to_json(orient='values')
            user_req_movies[str(idx)] = temp
            # user_req_movies['movie'] = movie_idx_list[idx]
        
        for i,temp_idx in enumerate(idx_idx[:10]):
            temp = {}
            idx = final_results[temp_idx]
            temp['movie'] = self.movie_idx_list[idx]
            temp['similarityScore'] = str(new_scors[temp_idx])
            #find tropes in this
            a = self.trope_table[idx,user_tropes_idx[:10]]
            a[a !=0] = 1
            temp['tropes'] = pd.Series(a.astype(int)).to_json(orient='values')
            similar_movies_dict[str(idx)] = temp
            # print(movie_idx_list[idx], new_scors[i])
    
        jsonresult['requestedMovies'] = user_req_movies
        jsonresult['similarMovies'] = similar_movies_dict
        jsonresult['tropeWeights'] = trope_weight_dict
        return json.dumps(jsonresult)
    
if __name__ == '__main__':
    user_movies_idx = np.array([140,345,862])
    database = MovieData();
    print(database.getSimilarMovies(user_movies_idx,None))