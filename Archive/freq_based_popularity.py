# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 08:55:08 2018

@author: A103932
"""

import pandas as pd

import numpy as np

all_movies = pd.read_csv('all_movies.csv')

trope_weight = all_movies.groupby(['Trope'], as_index = False)['Movie'].agg('count')

trope_weight.columns = ['Trope', 'Weight']

all_movies_with_weights = pd.merge(all_movies, trope_weight, on = ['Trope'], how = 'left')

#matrix = all_movies_with_weights.pivot_table(index = 'Movie', columns = 'Trope', values = 'Weight', aggfunc = 'sum')
#
#matrix = matrix.fillna(0)

selected_movies = pd.read_csv('Selected_movies.csv')

t1 = pd.merge(all_movies_with_weights, selected_movies, on=['Movie'], how = 'left', indicator = True)

all_excl_sel = t1[t1['_merge']=='left_only'][['Movie', 'Trope', 'Weight']]

sel = pd.merge(all_movies_with_weights, selected_movies, how = 'inner', on = ['Movie'])

all_excl_sel.columns = ['Movie', 'Trope', 'OverallPopularity']

sel.columns = ['Movie', 'Trope', 'OverallPopularity']

sel_pop = sel.groupby('Trope', as_index = False)['Movie'].agg('count')

sel_pop.columns = ['Trope', 'UserPopularity']

sugg = pd.merge(all_excl_sel, sel_pop, on = ['Trope'], how = 'inner')

sugg['CombinedPopularity'] = sugg['OverallPopularity']*sugg['UserPopularity']

sugg = sugg.groupby('Movie', as_index = False)['OverallPopularity', 'UserPopularity', 'CombinedPopularity'].agg(np.sum)

sugg = sugg.sort_values(['UserPopularity', 'OverallPopularity'], ascending = [False, False])

sugg.head().to_csv('suggestions_userpop.csv')

sugg = sugg.sort_values(['CombinedPopularity'], ascending = [False])

sugg.head().to_csv('suggestions_combpop.csv')





