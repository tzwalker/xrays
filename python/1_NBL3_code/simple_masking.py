# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
from scipy.ndimage.filters import gaussian_filter
from samp_dict_grow import build_dict
import numpy as np
import matplotlib.pyplot as plt

# cannot be used when kclustering is called on reduced arrays
def quick_label_check(original_map, model):
    clust_map = model.labels_.reshape(np.shape(original_map))
    plt.imshow(clust_map, origin='lower')
    return

M = NBL3_2['elXBIC'][0][0][:,:-2]
model = NBL3_2['c_kmodels'][0]

quick_label_check(M, model)

# =============================================================================
# cu_arr = cu_map.ravel()
# 
# # check maps
# fig, axs = plt.subplots(1,2)
# axs[0].imshow(ele_map)
# 
# # ravel filtered map
# filt_arr = filt_map.ravel()
# filt_arr = filt_arr.reshape(-1,1)
# 
# # cluster filtered map
# model = KMeans(init='k-means++', n_clusters=3, n_init=10) 
# filt_clust = model.fit(filt_arr)
# 
# # check clusters
# filt_clust_map = filt_clust.labels_.reshape(np.shape(ele_map))
# axs[1].imshow(filt_clust_map, cmap='Greys')
# 
# plt.figure()
# sns.distplot(ele_arr, bins=50)
# =============================================================================

# apply to other maps/correlate

# =============================================================================
# 
# samp = NBL3_2
# c_scan = samp['XBIC_h5s'][scan]  # h5 always has coordinates
# x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
# y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
# x_real = plt_supp.get_real_coordinates(x_axis)
# y_real = plt_supp.get_real_coordinates(y_axis)
# 
# xbic_arr =  samp['c_stand_arrs'][scan][:,0]
# cu_arr = samp['c_stand_arrs'][scan][:,1]
# 
# fig, axs = plt.subplots(1,3)
# plt.tight_layout()
# cu_standmap = cu_arr.reshape(len(x_real), len(y_real)-2)
# axs[0].imshow(cu_standmap, origin='lower')
# 
# cu_gaussmap = 
# axs[1].imshow(cu_gaussmap, origin='lower')
# 
# xbic_standmap = xbic_arr.reshape(len(x_real), len(y_real)-2)
# axs[2].imshow(xbic_standmap, origin= 'lower')
# 
# cu_gaussravel = cu_gaussmap.ravel()
# 
# lin_model = stats.linregress(cu_gaussravel, xbic_arr)
# lin_fit = lin_model.slope * cu_gaussravel + lin_model.intercept
# 
# plt.figure()
# plt.scatter(cu_arr, xbic_arr, s=4)
# plt.figure()
# plt.scatter(cu_gaussravel, xbic_arr, s=4)
# plt.plot(cu_gaussravel, lin_fit)
# plt.text(max(cu_gaussravel)*0.75, max(xbic_arr)*0.50, "$R^2$ = {s}".format(s=str(round(lin_model.rvalue,3))))
# 
# =============================================================================
