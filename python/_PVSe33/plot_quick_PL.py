"""
coding: utf-8

tzwalker
Fri Jan 29 19:11:30 2021

this program is meant to process the .txt PL and Raman data 
    from the Renishaw software
    
"""

'''for spectra of different pixels of PL map'''
import pandas as pd


IN_PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\PL'
FNAME = r'\20210119 PVSe33.4_3SLAC PL MAP - Au side test2.txt'

data = pd.read_csv(IN_PATH+FNAME, sep='\t', skiprows=1)
data.columns = ["X", "Y", "Wave #", "Intensity"]

map_dict = data.set_index(['X', 'Y']).agg(list, 1).groupby(level=(0,1)).agg(list).to_dict()

# =============================================================================
# data_arr = data.to_numpy()
# 
# i = 1
# 
# while data_arr[i,0] == data_arr[i-1,0]:
#     i = i+1
# 
# # isolate data of pixxel nca
#     # i looked in the txt file and saw where X (mm) changed
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