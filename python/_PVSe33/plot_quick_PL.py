"""
coding: utf-8

tzwalker
Fri Jan 29 19:11:30 2021

this program is meant to process the .txt PL and Raman data 
    from the Renishaw software
    
"""


import pandas as pd
import numpy as np


IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\PL'
FNAME = r'\20210119 PVSe33.4_3SLAC PL MAP - Au side test2.txt'

data = pd.read_csv(IN_PATH+FNAME, sep='\t', skiprows=1)
data.columns = ["X", "Y", "Wave #", "Intensity"]

# create dictionary where each pixel is an entry
# from StackOverflow solution:
    # https://stackoverflow.com/questions/65969561/how-do-i-convert-mapped-data-to-dictionary-where-each-xy-coordinate-contains-a/65969669#65969669
map_dict = data.set_index(['X', 'Y']).agg(list, 1).groupby(level=(0,1)).agg(list).to_dict()

vals = np.fromiter(map_dict.values(), dtype=float)

#for pixel in map_dict:
pixel_spectrum = map_dict[pixel]
pixel_spectrum_arr = np.array(pixel_spectrum)
# fit spectrum to a Gaussian distribution
# get max amplitude of Gaussian fit
# copy dictionary key
# set value of copy dictionary key to max amplitude
# store this key-value pair in new dictionary

print(np.shape(pixel_spectrum))
    

# =============================================================================
# '''for spectra of different pixels of PL map'''
# # isolate data of pixel with index, 'n'
#     # i looked in the txt file and found the index where X changed
# n = 20
# row_idxLo = 511*n+n
# row_idxHi = 511*(n+1)+n
# data_pixel01 = data.iloc[row_idxLo:row_idxHi]
# 
# # extract spectrum
# data_pixel01_spectrum = data_pixel01[data_pixel01.columns[-2:]]
# 
# import matplotlib.pyplot as plt
# plt.plot(data_pixel01_spectrum["Wave #"], data_pixel01_spectrum["Intensity"])
# 
# =============================================================================
#%%
'''for single spectrum'''
import pandas as pd
import matplotlib.pyplot as plt

IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\PL'
FNAME = r'\20210119 PVSe33.4_3SLAC PL - glass side test1.txt'

data = pd.read_csv(IN_PATH+FNAME, sep='\t', skiprows=1)
data.columns = ["Wave #", "Intensity"]

plt.plot(data["Wave #"], data["Intensity"])