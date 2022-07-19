# -*- coding: utf-8 -*-
"""

Trumann
Thu Apr 28 10:52:12 2022

run main-inSitu.py before this file

this file integrates XBIC maps from the in-situ sputtered Cu study (2021_11_2IDD)

imports ASCII from MAPS
shapes the data of a channel (e.g. Te_L XRF)
rotates the map (if desired)
sums along a given axis (e.g. the y-axis)

the scans had different spatial extents and resolutions, so they were trimmed accordingly

"""

import numpy as np
from skimage.transform import rotate
import matplotlib.pyplot as plt

ASCII_PATH =  r'C:\Users\Trumann\Dropbox (ASU)\2_insitu_Cu_cross_section\output' 

# create sample objects
Cu1b4c = Sample()

# define stack and scans of each sample, upstream layer first
Cu1b4c.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se': [4.82, 100E-7],
                 'SnO2': [100E-7]}

Cu1b4c.scans = [238,254,271,285,298,317,341,353,366,524]

# channels to import from ASCII
channels = [' us_ic', ' ds_ic', ' Cu', ' Se_L', ' Cd_L', ' Te_L', ' Au_M']

# uncomment this line to import maps with XBIC converted to ampere
# this requires XBIC channel ('us_ic') to be in first position of 'channels' list
#Cu1b4c.import_maps(ASCII_PATH, PATH_LOCKIN, channels)

# uncomment this line to import maps without XBIC converted to ampere
Cu1b4c.import_maps_no_XBIC_conversion(ASCII_PATH, channels)

color = 'magma'
df_map = Cu1b4c.scan524[1,:,:-2]

# =============================================================================
# # rotate dataframe, second argument is rotation in degrees
# df_rot = rotate(df_map, -8)
# 
# # integrate along y-axis
# df_sum = df_rot.sum(axis = 0)
# 
# # check original map
# plt.figure()
# plt.imshow(df_map,cmap=color)
# # check rotated map
# plt.figure()
# plt.imshow(df_rot,cmap=color)
# # check integration (e.g. of rotated map)
# plt.figure()
# plt.plot(df_sum)
# =============================================================================

num_of_scans = len(Cu1b4c.maps)
x_points = 39


# get rotated, integrated profile for scans with x points = 41, y points = 31
# trim 10 y points and NaN values in x
xbic = Cu1b4c.scan238[1,10:,:-2]
plt.figure()
plt.imshow(xbic)
#print(np.shape(xbic))
xbic_rot = rotate(xbic, -8)
plt.figure()
plt.imshow(xbic_rot)
xbic_sum0 = xbic_rot.sum(axis=0).reshape(-1,1)
plt.figure()
plt.plot(xbic_sum0)

# get rotated, integrated profiles for scans with x points = 41
xbic_lines = []
for im in Cu1b4c.maps[1:-3]:
    xbic = im[1,:,:-2]
    #print(np.shape(xbic))
    xbic_rot = rotate(xbic, -8)
    xbic_sum = xbic_rot.sum(axis=0)
    xbic_lines.append(xbic_sum)
xbic_arr1 = np.array(xbic_lines).T

# get rotated, integrated profiles for scans with x points = 51
xbic_lines = []
for im in Cu1b4c.maps[-3:]:
    # trim 10 x points, 5 in +x and 5 in -x
    xbic = im[1,:,5:-7]
    #print(np.shape(xbic))
    xbic_rot = rotate(xbic, -8)
    xbic_sum = xbic_rot.sum(axis=0)
    xbic_lines.append(xbic_sum)
xbic_arr2 = np.array(xbic_lines).T

array_to_origin = np.concatenate((xbic_sum0,xbic_arr1,xbic_arr2),axis=1)

#%%
'''this cell is for Cu XRF integrations'''

import numpy as np
from skimage.transform import rotate
import matplotlib.pyplot as plt

num_of_scans = len(Cu1b4c.maps)
x_points = 39


# get rotated, integrated profile for scans with x points = 41, y points = 31
# trim 10 y points and NaN values in x
xbic = Cu1b4c.scan238[2,10:,:-2]
plt.figure()
plt.imshow(xbic)
#print(np.shape(xbic))
xbic_rot = rotate(xbic, -8)
plt.figure()
plt.imshow(xbic_rot)
xbic_sum0 = xbic_rot.sum(axis=0).reshape(-1,1)
plt.figure()
plt.plot(xbic_sum0)

# get rotated, integrated profiles for scans with x points = 41
xbic_lines = []
for im in Cu1b4c.maps[1:-3]:
    xbic = im[2,:,:-2]
    #print(np.shape(xbic))
    xbic_rot = rotate(xbic, -8)
    xbic_sum = xbic_rot.sum(axis=0)
    xbic_lines.append(xbic_sum)
xbic_arr1 = np.array(xbic_lines).T

# get rotated, integrated profiles for scans with x points = 51
xbic_lines = []
for im in Cu1b4c.maps[-3:]:
    # trim 10 x points, 5 in +x and 5 in -x
    xbic = im[2,:,5:-7]
    #print(np.shape(xbic))
    xbic_rot = rotate(xbic, -8)
    xbic_sum = xbic_rot.sum(axis=0)
    xbic_lines.append(xbic_sum)
xbic_arr2 = np.array(xbic_lines).T

array_to_origin = np.concatenate((xbic_sum0,xbic_arr1,xbic_arr2),axis=1)
#%%
# get average for each integrated profile over time
for integrated_profile in array_to_origin.T:
    print(np.mean(integrated_profile))

# get XBIC max for each integrated profile over time
for integrated_profile in array_to_origin.T:
    print(np.max(integrated_profile))
    
#%%
'''quick plotting'''
num_plots = 10

# Have a look at the colormaps here and decide which one you'd like:
# http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
colormap = plt.cm.gist_ncar
plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.magma(np.linspace(0, 1, num_plots))))

# time labels
labels = [0,1.04,2.33,4.11,5.24,7.18,9.9,10.98,12.37,24.34]

for i,line in enumerate(array_to_origin.T):
    plt.plot(line)
    labels.append(str(labels[i]))

# I'm basically just demonstrating several different legend options here...
plt.legend(labels, ncol=4, loc='upper center', 
           bbox_to_anchor=[0.5, 1.1], 
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)
