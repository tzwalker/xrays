# -*- coding: utf-8 -*-
"""
Trumann
Tue Feb  4 11:26:59 2020

want to get at data taken at two different angles
2016_07_2IDD - miasole 'large grain' sample 5
Area 1 0  deg - scan130
Area 1 15 deg - scan122

Area 2 0  deg - scan127
Area 2 15 deg - scan119
"""
import sys
sys.path.append(r'C:\Users\Trumann\xrays\python\2_FS_code')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plot_FS_defs as fsdef


def import_scan(path, scan, channels):
    file = r'\combined_ASCII_2idd_0{s}.h5.csv'.format(s=str(scan)) #filename
    csv = pd.read_csv(path+file, skiprows=1) #import data
    fsdef.noColNameSpaces(csv) #remove white spaces in ascii headers
    maps_df = [csv.pivot(index='y pixel no', columns='x pixel no', values=chan) for chan in CHANNELS]
    maps_arr = [np.array(df) for df in maps_df] #convert ascii into 2d arrays
    map_stack = np.array(maps_arr) #stack 2d arrays into 3d structure
    return map_stack

path = r'C:\Users\Trumann\Desktop\angle_data\output'
CHANNELS = ['ds_ic', 'Cu', 'In_L', 'Ga', 'Se', 'Zn', 'Ca']

deg15 = import_scan(path,119,CHANNELS)
deg0 = import_scan(path,127, CHANNELS)
# if "dx" is (-) --> index like "dx:" ; # if "dx" is (+) --> index like ":dx"
# for high res scans 130 and 122, dx,dy = -10,10
# for low res scans 127 and 119, need to zoom in on one region for both... 
dx,dy = -10,10
deg15 = np.roll(deg15,dx,axis=1); deg15[:,dx:,:] = np.nan
deg15 = np.roll(deg15,dy, axis=2); deg15[:,:,:dy]= np.nan
deg15_roi = deg15[:,:dx,dy:] #get only the shifted area

dx,dy = 20,-15
deg0 = np.roll(deg0,dx,axis=1); deg0[:,:dx,:] = np.nan
deg0 = np.roll(deg0,dy, axis=2); deg0[:,:,dy:]= np.nan
deg0_roi = deg0[:,dx:,:dy] #get only the shifted area

deg15_roi_test = deg15_roi[:,:,:] # chop off low vals of rolled image
deg0_roi_test = deg0_roi[:,:,:-5] # chop off low vals of rolled image

#delta maps
#delta_map = deg15/deg0_roi
fig, (ax0,ax1) = plt.subplots(1,2)
ax0.imshow(deg15_roi_test[5,:,:])
ax1.imshow(deg0_roi_test[5,:,:])
#ax2.imshow(delta_map[5,:,:])
#%%
#check correlations between two geometries (of same area)
from scipy.stats import spearmanr
import custom_heatmap_defs
data = deg15_roi_test[[1,3,4,5],:,:]
data_prep = data.reshape(np.shape(data)[0], (np.shape(data)[1]*np.shape(data)[2]))
spear = spearmanr(data_prep.T)
AXIS_NAMES = ['Cu', 'Ga', 'Se', 'Zn']
fig, ax0 = plt.subplots()
plt.tight_layout()
IM, CBAR = custom_heatmap_defs.heatmap(spear[0], AXIS_NAMES, AXIS_NAMES, mask=True,
                   cmap="coolwarm", xylabelsizes=[16,16],
                   cbarlabel="Monotonicity", 
                   cbarpad=20, cbar_labsize=16, cbar_ticksize=16,
                   ax=ax0, vmin=-1, vmax=1)
TEXTS = custom_heatmap_defs.annotate_heatmap(IM, valfmt="{x:.2g}", fontsize=10, 
                                             threshold=[-0.5,0.5])


