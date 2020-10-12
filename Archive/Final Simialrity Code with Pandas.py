# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 10:42:36 2018

@author: A103932
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 08:16:02 2018
@author: A103932
"""

import pandas as pd

import numpy as np

all_movies = pd.read_csv('all_movies.csv')

trope_weight = all_movies.groupby(['Trope'], as_index = False)['Movie'].agg('count')

trope_weight.columns = ['Trope', 'Weight']

trope_weight['Weight'] = np.where(trope_weight['Weight'] == 0,0,1./trope_weight['Weight'])

all_movies_with_weights = pd.merge(all_movies, trope_weight, on = ['Trope'], how = 'left')

matrix = all_movies_with_weights.pivot_table(index = 'Movie', columns = 'Trope', values = 'Weight', aggfunc = 'sum')

matrix = matrix.fillna(0)

movie_matrix = matrix.dot(matrix.T)

similarity_denominator = np.square(matrix)

similarity_denominator = similarity_denominator.sum(axis = 1)

similarity_denominator = 1/similarity_denominator

similarity_denominator = np.sqrt(similarity_denominator)

movie_matrix = movie_matrix*similarity_denominator

movie_matrix = (movie_matrix.T)*similarity_denominator

movie_matrix.to_csv('movie_matrix.csv')

