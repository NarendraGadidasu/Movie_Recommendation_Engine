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

matrix = matrix.reset_index()

matrix['key'] = 1

movie_combs = []

for i in matrix.index:
    for j in matrix.index:
        matrix_cross = pd.merge(matrix.loc[[i]][:], matrix.loc[[j]][:], how = 'inner', on = 'key')
        matrix_cross = matrix_cross.drop(columns = 'key')
        l = list(matrix.columns)
        l.remove('key')
        l.remove('Movie')
        matrix_cross['Numerator'] = 0
        matrix_cross['Denominator_1'] = 0
        matrix_cross['Denominator_2'] = 0
        for t in l:
            matrix_cross['Numerator'] += matrix_cross[t+'_x']*matrix_cross[t+'_y']
            matrix_cross['Denominator_1'] += matrix_cross[t+'_x']*matrix_cross[t+'_x']
            matrix_cross['Denominator_2'] += matrix_cross[t+'_y']*matrix_cross[t+'_y']
            matrix_cross = matrix_cross.drop(columns = t+'_x')
            matrix_cross = matrix_cross.drop(columns = t+'_y')
        matrix_cross['Similarity_Score'] = 1.0*matrix_cross['Numerator']/((matrix_cross['Denominator_1']*matrix_cross['Denominator_2'])**0.5)
        movie_combs.append(matrix_cross)
            
Similarity = pd.concat(movie_combs)

Similarity_Matrix = Similarity.pivot_table(index = 'Movie_x', columns = 'Movie_y', values = 'Similarity_Score', aggfunc = 'sum')

Similarity_Matrix.to_csv('Similarity_Matrix_final.csv')



