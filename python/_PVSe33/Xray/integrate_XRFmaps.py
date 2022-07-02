# -*- coding: utf-8 -*-
"""

Trumann
Tue May 24 08:37:53 2022

run "main-PVSe33-ASCII-xsect" before this program

this file integrates the maps from 
2021_07_2IDD

window cross sections
0hr - scan072 
500hr - scan144

infinite cross sections
0hr - scan119
500hr - scan151

"""
import numpy as np
from skimage.transform import rotate

'''
0hr infinite integrate

this cell is for the integrated profiles of the maps used in
'plot_master_cross sections.py'
    these are the infinite cross section maps

different profiles are needed for these maps since they were cropped
from the original areas

be sure to load the correct file in 
'main-PVSe33-ASCII-xsect.py'

run 'plot_master_cross sections.py' with the correct map loaded

'''
# scan 119
df_sums = []
for df in df_maps:
    df_arr = np.array(df)
    df_sum = df_arr.sum(axis=0)
    df_sums.append(df_sum)
    
df_sums_arr = np.array(df_sums).T
#%%
'''
500hr infinite integrate

this cell is for the integrated profiles of the maps used in
'plot_master_cross sections.py'
    these are the infinite cross section maps

different profiles are needed for these maps since they were cropped
from the original areas

be sure to load the correct file in 
'main-PVSe33-ASCII-xsect.py'

run 'plot_master_cross sections.py' with the correct map loaded

'''
# scan 151
# select 11 rows from across the map
# since the original area was cropped, the last index must be less than 60
    # this guarantees the integration is within the cropped
    # map displayed in the paper
keep_pixels = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40]

df_sums = []
for df in df_maps:
    df_arr = np.array(df)
    df_match = df_arr[keep_pixels, :]
    df_sum = df_match.sum(axis=0)
    df_sums.append(df_sum)
df_sums_arr = np.array(df_sums).T

#%%
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

### i'm checking if the Se distribution looks smeared in the windows
    # like the infinite cross section - doesn't look like it, could be due to FIB cleaning
# for window scans 72 and 144, the number of y points and y length were the same
    # no need to exclude rows before integrating

# redo integrate window scan 72 (0hr), apply -2deg rotation, i want the Au channel from this scan
df_sums = []
for df in df_maps:
    df_arr = np.array(df)
    # rotate dataframe, second argument is rotation in degrees
    df_rot = rotate(df_arr, -2)
    df_sum = df_rot.sum(axis=0)
    df_sums.append(df_sum)
df_sums_arr = np.array(df_sums).T
    
# =============================================================================
# # redo integrate window scan 144 (500hr), apply -2deg rotation, i want the Au channel from this scan
# df_sums = []
# for df in df_maps:
#     df_arr = np.array(df)
#     # rotate dataframe, second argument is rotation in degrees
#     df_rot = rotate(df_arr, -2)
#     df_sum = df_rot.sum(axis=0)
#     df_sums.append(df_sum)
# df_sums_arr = np.array(df_sums).T
# =============================================================================