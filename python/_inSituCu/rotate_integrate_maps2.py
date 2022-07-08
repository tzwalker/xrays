# -*- coding: utf-8 -*-
"""

Trumann
Thu Jul  7 12:59:02 2022

this file imports the map scans, rotaes the XBIC map, constructs the XBIC profile
and 
"""


from class_ascii_Sample import Sample
import numpy as np
import pandas as pd
from skimage.transform import rotate
import matplotlib.pyplot as plt

ASCII_PATH =  r'C:\Users\Trumann\Dropbox (ASU)\2_insitu_Cu_cross_section\output' 

scan_path = r'C:\Users\Trumann\Dropbox (ASU)\2_insitu_Cu_cross_section\map_scan_numbers_times.csv'

df = pd.read_csv(scan_path,skiprows=1)
scan_nums = df['scan'].values

# create sample objects
Cu1b4c = Sample()

# define stack and scans of each sample, upstream layer first
Cu1b4c.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se': [4.82, 100E-7],
                 'SnO2': [100E-7]}

# 238 244	254	271	285	298	317	341	353	366	367	379	391	403	428	458	488	524
Cu1b4c.scans = list(scan_nums)

# channels to import from ASCII
channels = [' us_ic', ' ds_ic', ' Cu', ' Se_L', ' Cd_L', ' Te_L', ' Au_M']

# uncomment this line to import maps without XBIC converted to ampere
Cu1b4c.import_maps_no_XBIC_conversion(ASCII_PATH, channels)
#%%
'''
this cell gets the line profiles; remove scaler_factor for cts/s

different loops are needed because the maps were not collected with same number
of xy pixels

'''
# =============================================================================
# # check shape of arrays 
# for m in Cu1b4c.maps:
#     print(np.shape(m))
# =============================================================================

scaler_factor = (50000*1E-9) / (2e5*500) * 1e9 # nA

# need to remove 10 rows from first scan238
xbic = Cu1b4c.scan238[1,10:,:-2] *scaler_factor
xbic_rot = rotate(xbic, -8)
xbic_sum0 = xbic_rot.sum(axis=0).reshape(-1,1)
# for error on depth where max XBIC is
index_of_max = xbic_sum0.argmax(axis=0)
xbic_std0 = xbic_rot.std(axis=0).reshape(-1,1)
xbic_std00 = xbic_std0[index_of_max]

# get rotated, integrated profiles for scans with x points = 41 (scans244-366)
xbic_lines = []
xbic_stds = []
for im in Cu1b4c.maps[1:-10]:
    xbic = im[1,:,:-2] *scaler_factor
    #print(np.shape(xbic))
    xbic_rot = rotate(xbic, -8)
    xbic_sum = xbic_rot.sum(axis=0)
    xbic_lines.append(xbic_sum)
    
    index_of_max = xbic_sum.argmax(axis=0)
    xbic_std = xbic_rot.std(axis=0).reshape(-1,1)
    std_max = xbic_std[index_of_max]
    xbic_stds.append(std_max)
    
xbic_arr1 = np.array(xbic_lines).T
xbic_std1 = np.array(xbic_stds).T

# get rotated, integrated profiles for scans with x points = 51 (scans367-524)
xbic_lines = []
xbic_stds = []
for im in Cu1b4c.maps[-10:]:
    # trim 10 x points, 5 in +x and 5 in -x
    xbic = im[1,:,5:-7] *scaler_factor
    xbic_rot = rotate(xbic, -8)
    xbic_sum = xbic_rot.sum(axis=0)
    xbic_lines.append(xbic_sum)
    
    index_of_max = xbic_sum.argmax(axis=0)
    xbic_std = xbic_rot.std(axis=0).reshape(-1,1)
    std_max = xbic_std[index_of_max]
    xbic_stds.append(std_max)
    
xbic_arr2 = np.array(xbic_lines).T
xbic_std2 = np.array(xbic_stds).T

# copy into Origin - XBIC profiles
array_to_origin = np.concatenate((xbic_sum0,xbic_arr1,xbic_arr2),axis=1)

# copy into Origin - times, maximums, and std dev
time = df['timestamp'].values / 100 # decimal Hr
maxima = np.max(array_to_origin, axis=0) # nA
stds = np.concatenate((xbic_std00,xbic_std1,xbic_std2),axis=1).T
#%%
'''this cell normalizes to the us_ic so that scans can be compared across time'''

# array index [0,:,:] is the us_ic

# need to remove 10 rows from first scan238
xbic = Cu1b4c.scan238[1,10:,:-2] / Cu1b4c.scan238[0,10:,:-2]
xbic_rot = rotate(xbic, -8)
xbic_sum0 = xbic_rot.sum(axis=0).reshape(-1,1)
# for error on depth where max XBIC is
index_of_max = xbic_sum0.argmax(axis=0)
xbic_std0 = xbic_rot.std(axis=0).reshape(-1,1)
xbic_std00 = xbic_std0[index_of_max]

# get rotated, integrated profiles for scans with x points = 41 (scans244-366)
xbic_lines = []
xbic_stds = []
for im in Cu1b4c.maps[1:-10]:
    xbic = im[1,:,:-2] / im[0,:,:-2]
    #print(np.shape(xbic))
    xbic_rot = rotate(xbic, -8)
    xbic_sum = xbic_rot.sum(axis=0)
    xbic_lines.append(xbic_sum)
    
    index_of_max = xbic_sum.argmax(axis=0)
    xbic_std = xbic_rot.std(axis=0).reshape(-1,1)
    std_max = xbic_std[index_of_max]
    xbic_stds.append(std_max)
    
xbic_arr1 = np.array(xbic_lines).T
xbic_std1 = np.array(xbic_stds).T

# get rotated, integrated profiles for scans with x points = 51 (scans367-524)
xbic_lines = []
xbic_stds = []
for im in Cu1b4c.maps[-10:]:
    # trim 10 x points, 5 in +x and 5 in -x
    xbic = im[1,:,5:-7] / im[0,:,5:-7]
    xbic_rot = rotate(xbic, -8)
    xbic_sum = xbic_rot.sum(axis=0)
    xbic_lines.append(xbic_sum)
    
    index_of_max = xbic_sum.argmax(axis=0)
    xbic_std = xbic_rot.std(axis=0).reshape(-1,1)
    std_max = xbic_std[index_of_max]
    xbic_stds.append(std_max)
    
xbic_arr2 = np.array(xbic_lines).T
xbic_std2 = np.array(xbic_stds).T

# copy into Origin - XBIC profiles
array_to_origin = np.concatenate((xbic_sum0,xbic_arr1,xbic_arr2),axis=1)

# copy into Origin - times, maximums, and std dev
time = df['timestamp'].values / 100 # decimal Hr
maxima = np.max(array_to_origin, axis=0) # nA
stds = np.concatenate((xbic_std00,xbic_std1,xbic_std2),axis=1).T
