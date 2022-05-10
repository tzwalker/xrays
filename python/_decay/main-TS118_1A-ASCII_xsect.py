# -*- coding: utf-8 -*-
"""

Trumann
Mon May  9 11:09:53 2022

this program imports the overview map scan275 used for the cross-section XBIC
degradation scans276-309


"""
import pandas as pd
import numpy as np

#ASCII_PATH =  r'C:\Users\triton\XBIC_decay\TS118A_1A_2018_11_26IDC' 
ASCII_PATH = r"C:\Users\Trumann\Desktop\2018_11_26IDC\output\combined_ASCII_26idbSOFT_0275.mda.csv"
PATH_LOCKIN = r'C:\Users\Trumann\Dropbox (ASU)\1_XBIC_decay\decay_electrical.csv'

data = pd.read_csv(ASCII_PATH, skiprows=1)
old_colnames = data.columns.values
new_colnames = []
for name in old_colnames:
    new_colnames.append(name.strip())
data.rename(columns = {i:j for i,j in zip(old_colnames,new_colnames)}, inplace=True)

i = 'y pixel no'; j='x pixel no'; c = "26idc:3820:scaler1_cts2.B"

data_shape = data.pivot(index=i, columns=j, values=c)
data_shape = data_shape.to_numpy()

# convert to pA
stanford = 20 #nA
V2F = 100000
lockin = 1000
scaler_factor = (stanford*1E-9) / (V2F*lockin)
data_shape = data_shape * scaler_factor * 1e12 # A to pA

#%%
'''this cell imports XRF-related scan0051

i refit this scan the proper way following the procedure in tutorial videos;
all four detectors were fit independently

the csv was exported with fitted option and us_ic normalization
'''

import pandas as pd

#ASCII_PATH =  r'C:\Users\triton\XBIC_decay\TS118A_1A_2018_11_26IDC' 
ASCII_PATH = r"C:\Users\Trumann\Desktop\2018_11_26IDC\output\combined_ASCII_26idbSOFT_0051.h5.csv"

data = pd.read_csv(ASCII_PATH,skiprows=1)

channels = [" us_ic", " ds_ic", " Cu", " Cd_L", " Au_M"]
i = ' y pixel no'; j='x pixel no';# c = " us_ic" # 26idc:3820:scaler1_cts2.B"

data_shape = [data.pivot(index=i, columns=j, values=c) for c in channels]
data_shape = [d.to_numpy() for d in data_shape]
