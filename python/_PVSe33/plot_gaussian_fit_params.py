"""
coding: utf-8

tzwalker
Tue Mar 23 17:08:43 2021

this program is meant to be run after map_analysis_PL

it assumes a set of gaussian fit parameters have been obtained for
each pixel in a PL map, and these parameters have been saved to a csv file

it allows the user to specify a gaussian fit parameter and plot it as
a function of x and y coordinate
"""

import pandas as pd
import matplotlib.pyplot as plt

# specify import file
IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\PL'
FILE = r'\gaussian fit params - 20210304 PVSe33.3_2 Au Side_PL_map0.csv'
F = IN_PATH + FILE
 
# import file array
    # 2D array, rows --> number of pixels, cols --> gaussian fit parameter
fit_params = pd.read_csv(F, delimiter=',', header=None)
fit_params = fit_params.to_numpy()

# specify parameter 
    #0: offset, 1: amplitude, 2: energy position, 3: width
fit_param = 1

# extract parameter for each pixel
relevant_data = fit_params[:,fit_param]

# reshape into map shape
    # note this shape must be known a priori
    # it can be found by viewing the shape of 'reader.spectra' of wdf file
        # x --> number of columns in wdf file
        # y --> number of rows in wdf file

# specify the number of rows and columns
x = 31
y = 31
param_map = relevant_data.reshape(y,x)

# plot parameter map
plt.imshow(param_map)

