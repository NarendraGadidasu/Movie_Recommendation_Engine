# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 08:16:02 2018

@author: A103932
"""

import pandas as pd

import numpy as np

all_movies = pd.read_csv('all_movies.csv')

all_movies = all_movies.head(5000)

trope_weight = all_movies.groupby(['Trope'], as_index = False)['Movie'].agg('count')

trope_weight.columns = ['Trope', 'Weight']

trope_weight['Weight'] = np.where(trope_weight['Weight'] == 0,0,1./trope_weight['Weight'])

unique_movies = pd.DataFrame(all_movies['Movie'].unique())

unique_movies['key'] = 1

unique_movies.columns = ['Movie', 'key']

unique_tropes = pd.DataFrame(trope_weight['Trope'].unique())

unique_tropes['key'] = 1

unique_tropes.columns  = ['Trope', 'key']

movie_trope_combinations = pd.merge(unique_movies, unique_tropes, on = ['key'], how = 'inner')

movie_trope_combinations = movie_trope_combinations.drop(columns = 'key')

all_movies_with_weights = pd.merge(all_movies, trope_weight, on = ['Trope'], how = 'left')

all_movies_with_weights = pd.merge(movie_trope_combinations, all_movies_with_weights, on = ['Movie','Trope'], how = 'left')

all_movies_with_weights = all_movies_with_weights.fillna(0)

#all_movies_with_weights = pd.read_csv('Dummmy.csv')

Similarity_Input = pd.merge(all_movies_with_weights, all_movies_with_weights, on = ['Trope'], how = 'inner')

Similarity_Input['Numerator'] = Similarity_Input['Weight_x']*Similarity_Input['Weight_y']*1.0

Similarity_Input['Denominator_1'] = Similarity_Input['Weight_x']*Similarity_Input['Weight_x']*1.0

Similarity_Input['Denominator_2'] = Similarity_Input['Weight_y']*Similarity_Input['Weight_y']*1.0

Similarity = Similarity_Input.groupby(['Movie_x', 'Movie_y'], as_index=False)['Numerator', 'Denominator_1', 'Denominator_2'].agg(np.sum)

Similarity['Similarity_Score'] = 1.0*Similarity['Numerator']/((Similarity['Denominator_1']*Similarity['Denominator_2'])**0.5)

Similarity_Matrix = Similarity.pivot_table(index = 'Movie_x', columns = 'Movie_y', values = 'Similarity_Score', aggfunc = 'sum')

Similarity_Matrix.to_csv('Similarity_Matrix.csv')

#matrix = all_movies_with_weights.pivot_table(index = 'Movie', columns = 'Trope', values = 'Weight', aggfunc = 'sum')
#
#matrix = matrix.fillna(0)
#
#matrix['Movie'] = matrix.index
#matrix.to_csv("final.csv")

