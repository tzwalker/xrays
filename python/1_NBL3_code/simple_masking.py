# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
import numpy as np
import matplotlib.pyplot as plt

scan = 2

cu_maps = [samp['elXBIC_corr'][scan][0][:,:-2] for samp in samples]
xbic_maps = [samp['XBIC_maps'][scan][:,:-2] for samp in samples]

cu_data = [samp['elXBIC_corr'][scan][0][:,:-2].ravel() for samp in samples]
xbic_data = [samp['XBIC_maps'][scan][:,:-2].ravel() for samp in samples]
    
x_boxlabs = [samp['Name'] for samp in samples]

fig, axs = plt.subplots(1,2)
plt.tight_layout()
axs[0].imshow(cu_maps[2], origin='lower')
axs[1].imshow(xbic_maps[2], origin='lower')

plt.figure()
plt.boxplot(cu_data)
plt.xticks([1, 2, 3], x_boxlabs)
plt.suptitle('Thickness corrected Cu')
plt.figure()
plt.boxplot(xbic_data)
plt.xticks([1, 2, 3], x_boxlabs)
plt.suptitle('XBIC')

### plotting and correlating (via scatter) gaussian filtered standardized arrays
# =============================================================================
# from scipy.ndimage import gaussian_filter
# from scipy import stats
# from put_nans_back_on import put_nans_back_on
# import z_plot_supplement as plt_supp
# samp = TS58A
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
# cu_gaussmap = gaussian_filter(cu_standmap, sigma=1)
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
# =============================================================================