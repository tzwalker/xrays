# -*- coding: utf-8 -*-
"""
Trumann
Fri Aug 30 12:37:17 2019

usefeul function for visualizing standardized data as a map
puts two nan columns back on standardized arrays
"""
import numpy as np

def put_nans_back_on(array, y_coord, x_coord):
    slim_map = array.reshape(len(y_coord), len(x_coord)-2)           # minus 2cols (chopped off nans in e_statistics.py)
    nans_to_attach = np.full((np.size(slim_map, axis=0),2), np.nan) # get 2cols of nan
    nan_map = np.append(slim_map, nans_to_attach, 1)                 # attach nan
    return nan_map