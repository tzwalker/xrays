# -*- coding: utf-8 -*-
"""
Trumann
Fri Mar 13 11:46:58 2020
"""

import numpy as np
import sklearn.preprocessing as sklp
scaler = sklp.StandardScaler()

def standardize_map(array):
    # maintain map dimensions
    map_dimensions = np.shape(array)
    # standardization requires one column
    array = array.reshape(-1,1) 
    # standardize
    array = scaler.fit_transform(array) 
    # shape standardized data back into map
    array = array.reshape(map_dimensions) 
    return array