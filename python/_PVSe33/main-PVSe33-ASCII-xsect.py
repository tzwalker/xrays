"""
coding: utf-8

tzwalker
Mon Aug  2 11:07:19 2021

Se XANES
this program is meant to analyze PVSe33 cross-section data
2021_07_2IDD

Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_07_2IDD_SeXRF\output

for scans with different widths, chopping x will be done in Origin
    (the plot x axis range will be adjusted to match between scans)

the length of scan 119 is 10um (11pts) and the length of scan 151 is 12um (76pts)
    -both the physical distance and the resolution (no. of observations) 
    is different between the two scans
    -when integrating i want to be able to compare the same physical distance 
    and number of observations
    -this necessarily means i will need to get rid of most of the pts in
    before integrating scan 151
    -from scan 151, keep 10 rows spread over a 10um length
    -keep row at every 1um step
    -1um step is about 6 rows at 0.16nm per row
    -keep pixel idxs: [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60]

imports ASCII from MAPS
shapes the data of a channel (e.g. Te_L XRF)
rotates the map (if desired)
sums along a given axis (e.g. the y-axis)

lockin settings
scan72 (window), scan119 (inf) 
    stanford 50uA/V, 1000 V/V

scan144 (window), scan151 (inf)
    stanford 50uA/V, 1000 V/V
"""

import pandas as pd

def remove_column_header_spaces(dataframe):
    old_colnames = dataframe.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    header_dict = {i:j for i,j in zip(old_colnames,new_colnames)}
    dataframe.rename(columns = header_dict, inplace=True)
    return dataframe

# directory information for data file
PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_07_2IDD_SeXRF\output'

# change depending on sector
FILENAME = r'\combined_ASCII_2idd_0144.h5.csv'
DATA = PATH+FILENAME

channels = ['ds_ic', 'Cu', 'Se', 'Te_L', 'Au_L']

df_maps = []
for chan in channels:
    # import the data as a pandas dataframe ('df'); skip first row header
    df = pd.read_csv(DATA, skiprows=1)
    
    # remove column header spaces (for convenient reference to column headers)
        # this step is necessary because MAPS outputs ASCIIs with extra spaces
    df_clean = remove_column_header_spaces(df)
    
    # shape data of a given column into 2D map
    x_pix = 'x pixel no'
    y_pix = 'y pixel no'
    # specify XRF or XBIC (usually under 'ds_ic' column header)
    channel = chan
    df_map = df_clean.pivot(index = y_pix, columns = x_pix, values = channel)
    df_maps.append(df_map)

# convert XBIC
scaler_factor = (50E-6) / (2E5*1000) # ampere (A)
df_xbic = df_maps[0] * scaler_factor * 1E9 # from A to nA
df_maps[0] = df_xbic # replace imported df


### for infinite cross section integration along length
# =============================================================================
# # scan 119
# df_sums = []
# for df in df_maps:
#     df_arr = np.array(df)
#     df_sum = df_arr.sum(axis=0)
#     df_sums.append(df_sum)
#     
# df_sums_arr = np.array(df_sums).T
# =============================================================================

# =============================================================================
# # scan 151 to match scan length (10um) and resolution (11pts) of scan 119
# keep_pixels = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
# 
# df_sums = []
# for df in df_maps:
#     df_arr = np.array(df)
#     df_match = df_arr[keep_pixels, :]
#     df_sum = df_match.sum(axis=0)
#     df_sums.append(df_sum)
# df_sums_arr = np.array(df_sums).T
#     
# =============================================================================


    
        
#%%
"""
coding: utf-8

tzwalker
Tue Jan  4 11:16:23 2022

Cu XANES
this program is meant to analyze PVSe33 cross-section data
2021_11_2IDD

imports ASCII from MAPS
shapes the data of a channel (e.g. Te_L XRF)
rotates the map (if desired)
sums along a given axis (e.g. the y-axis)

scan1086 (inf)
    stanford 50uA/V, 1000 V/V
    10um x 40um
    51pt x 201pt -> 200nm x 200nm

scan1210 (inf)
    stanford 50uA/V, 1000 V/V
    14um x 20um
    71pt x 101pt -> 200nm x 200nm
"""

import pandas as pd
import numpy as np

def remove_column_header_spaces(dataframe):
    old_colnames = dataframe.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    header_dict = {i:j for i,j in zip(old_colnames,new_colnames)}
    dataframe.rename(columns = header_dict, inplace=True)
    return dataframe

# directory information for data file
PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_11_2IDD_CuXRF\output'

sample = '500hr'
SAVE = 1

if sample == '0hr':
    FILENAME = r'\combined_ASCII_2idd_1086.h5.csv' # 0hr
elif sample == "500hr":
    FILENAME = r'\combined_ASCII_2idd_1210.h5.csv' # 500hr

DATA = PATH+FILENAME

channels = ['ds_ic', 'Cu', 'Cd_L']

df_maps = []
for chan in channels:
    # import the data as a pandas dataframe ('df'); skip first row header
    df = pd.read_csv(DATA, skiprows=1)
    
    # remove column header spaces (for convenient reference to column headers)
        # this step is necessary because MAPS outputs ASCIIs with extra spaces
    df_clean = remove_column_header_spaces(df)
    
    # shape data of a given column into 2D map
    x_pix = 'x pixel no'
    y_pix = 'y pixel no'
    # specify XRF or XBIC (usually under 'ds_ic' column header)
    channel = chan
    df_map = df_clean.pivot(index = y_pix, columns = x_pix, values = channel)
    df_maps.append(df_map)

# convert XBIC
scaler_factor = (50E-6) / (2E5*1000) # ampere (A)
df_xbic = df_maps[0] * scaler_factor * 1E9 # from A to nA
df_maps[0] = df_xbic # replace imported df


### for infinite cross section integration along length
if sample == '0hr':
    # scan 1086 
    # the length of this scan was 40um
    # only want to integrate over 20um of length to be comparable to scan 1210
    # there are 200 rows in this scan, therefore remove 100 rows to get 20um
    df_sums = []
    for df in df_maps:
        df_arr = np.array(df)
        #df_sum = df_arr.sum(axis=0)
        df_match = df_arr[100:, :]
        df_sum = df_match.sum(axis=0)
        df_sums.append(df_sum)
    df_sums_arr = np.array(df_sums).T
    
elif sample == "500hr":
    # scan 1210
    df_sums = []
    for df in df_maps:
        df_arr = np.array(df)
        df_sum = df_arr.sum(axis=0)
        df_sums.append(df_sum)
    
    df_sums_arr = np.array(df_sums).T

if SAVE == 1:
    PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_11_2IDD_CuXRF"
    FNAME = r"\{s}_vert_integrated.csv".format(s=sample)
    # column 1 -> XBIC
    # column 2 -> Cu
    # column 3 -> Cd
    np.savetxt(PATH_OUT+FNAME, df_sums_arr, delimiter=",")