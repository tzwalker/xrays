# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy import stats
from put_nans_back_on import put_nans_back_on
import z_plot_supplement as plt_supp

c_scan = NBL3_2['XBIC_h5s'][3]  # h5 always has coordinates
x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
x_real = plt_supp.get_real_coordinates(x_axis)
y_real = plt_supp.get_real_coordinates(y_axis)

xbic_arr =  NBL3_2['c_stand_arrs'][3][:,0]
cu_arr = NBL3_2['c_stand_arrs'][3][:,1]

cu_standmap = cu_arr.reshape(len(x_real), len(y_real)-2)
plt.figure()
plt.imshow(cu_standmap, origin='lower')

cu_gaussmap = gaussian_filter(cu_standmap, sigma=1)
plt.figure()
plt.imshow(cu_gaussmap, origin='lower')

cu_gaussravel = cu_gaussmap.ravel()

lin_model = stats.linregress(cu_gaussravel, xbic_arr)
lin_fit = lin_model.slope * cu_gaussravel + lin_model.intercept

plt.figure()
plt.scatter(cu_gaussravel, xbic_arr, s=4)
plt.plot(cu_gaussravel, lin_fit)
plt.text(max(cu_gaussravel)*0.75, max(xbic_arr)*0.50, "$R^2$ = {s}".format(s=str(round(lin_model.rvalue,3))))

# =============================================================================
# cu_arr_gauss = gaussian_filter(cu_arr, sigma=1)
# cu_standmap_gauss =  gaussian_filter(cu_stand_map, sigma=1)
# cu_trim_standmap_gauss = cu_standmap_gauss[:,:-6]
# cu_standarr_ravel = cu_trim_standmap_gauss.ravel()
# 
# xbic_stand_map = put_nans_back_on(xbic_arr, x_real, y_real)
# xbic_trim_standmap = xbic_stand_map[:,:-4]
# xbic_standarr_ravel = cu_trim_standmap_gauss.ravel()
# 
# #cu_standarr_ravel.reshape(-1,1)
# #xbic_standarr_ravel.reshape(-1,1)
# 
# 
# def plot_correlation(channel, xbic):
#     slope, intercept, r_squared, p_value, std_err = stats.linregress(channel, xbic_arr)
#     fit_line = slope*channel + intercept
#     
#     #wanted_indices = np.where(xbic_arr > 2)
#     #thres_cu_map = cu_arr[wanted_indices]
#     #thres_xbic_map = xbic_arr[wanted_indices]
#     
#     plt.figure()
#     #data = [thres_cu_map, thres_xbic_map]
#     #plt.boxplot(data)
#     plt.scatter(channel, xbic, s=4)
#     plt.plot(channel, fit_line)
#     plt.text(max(channel)*0.75, max(xbic_arr)*0.50, "$R^2$ = {s}".format(s=str(round(r_squared,3))))
#     return
# 
# #a = np.concatenate((cu_standarr_ravel, xbic_standarr_ravel), axis=2)
# 
# #plot_correlation(cu_standarr_ravel, xbic_standarr_ravel)
# plt.figure()
# plt.imshow(cu_stand_map)
# 
# plt.figure()
# plt.imshow(cu_trim_standmap_gauss)
# plt.figure()
# plt.imshow(xbic_trim_standmap)
# =============================================================================
