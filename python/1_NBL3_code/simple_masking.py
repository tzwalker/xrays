# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

samp = NBL3_2
scan = 0
element = 0
# get Cu map
ele_map = samp['elXBIC'][scan][element][:,:-2] # --> remove nans as they mess with filter application

# apply filter to map
filt_map = gaussian_filter(ele_map, sigma=1)

# check maps
fig, axs = plt.subplots(1,2)
axs[0].imshow(ele_map)
axs[1].imshow(filt_map)

# ravel filtered map
filt_arr = filt_map.ravel()

# cluster filtered map


# indices of labels in filtered map


# apply to other maps/correlate


samp = NBL3_2
c_scan = samp['XBIC_h5s'][scan]  # h5 always has coordinates
x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
x_real = plt_supp.get_real_coordinates(x_axis)
y_real = plt_supp.get_real_coordinates(y_axis)

xbic_arr =  samp['c_stand_arrs'][scan][:,0]
cu_arr = samp['c_stand_arrs'][scan][:,1]

fig, axs = plt.subplots(1,3)
plt.tight_layout()
cu_standmap = cu_arr.reshape(len(x_real), len(y_real)-2)
axs[0].imshow(cu_standmap, origin='lower')

cu_gaussmap = 
axs[1].imshow(cu_gaussmap, origin='lower')

xbic_standmap = xbic_arr.reshape(len(x_real), len(y_real)-2)
axs[2].imshow(xbic_standmap, origin= 'lower')

cu_gaussravel = cu_gaussmap.ravel()

lin_model = stats.linregress(cu_gaussravel, xbic_arr)
lin_fit = lin_model.slope * cu_gaussravel + lin_model.intercept

plt.figure()
plt.scatter(cu_arr, xbic_arr, s=4)
plt.figure()
plt.scatter(cu_gaussravel, xbic_arr, s=4)
plt.plot(cu_gaussravel, lin_fit)
plt.text(max(cu_gaussravel)*0.75, max(xbic_arr)*0.50, "$R^2$ = {s}".format(s=str(round(lin_model.rvalue,3))))
