# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
import numpy as np
import matplotlib.pyplot as plt

#samp = TS58A
scans = [0,1,2,3]
model = 'c_kmodels'
data = 'c_reduced_arrs'
clusts = [0,1,2]

def plot_clust_boxes(clust_nums, clust_labs, x, y, z, scan, sam):
    fig, axs = plt.subplots(3,1)
    plt.tight_layout()
    x1 = [x[np.where(clust_labs == clust)[0]] for clust in clust_nums] # each item in list are the values of a cluster for x data
    y1 = [y[np.where(clust_labs == clust)[0]] for clust in clust_nums] # each item in list are the values of a cluster for y data
    z1 = [z[np.where(clust_labs == clust)[0]] for clust in clust_nums]
    
    bp_dictx = axs[0].boxplot(x1, showfliers=False) # initialize boxplot object
    for line in bp_dictx['medians']:
        med = line.get_ydata()                  # get median value array
        xpoint, ypoint = line.get_xydata()[1]   # get plot coordinates of median
        # annotate this position with median as string
        axs[0].annotate(xy=(xpoint,ypoint), 
           s=' ' + "{:.3f}".format(med[0]), 
           horizontalalignment='left') # add text with formatting
    axs[0].title.set_text('reduced copper')
    
    bp_dicty = axs[1].boxplot(y1, showfliers=False)
    for line in bp_dicty['medians']:
        med = line.get_ydata()
        xpoint, ypoint = line.get_xydata()[1] 
        axs[1].annotate(xy=(xpoint,ypoint), 
           s=' ' + "{:.2e}".format(med[0]), horizontalalignment='left')
    axs[1].title.set_text('reduced xbic')
    
    bp_dictz = axs[2].boxplot(z1, showfliers=False)
    for line in bp_dictz['medians']:
        med = line.get_ydata()
        xpoint, ypoint = line.get_xydata()[1] 
        axs[2].annotate(xy=(xpoint,ypoint), 
           s=' ' + "{:.2e}".format(med[0]), horizontalalignment='left')
    axs[2].title.set_text('reduced cd')
    plt.savefig(r'C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190904 clustering and boxplots\{sample}_area{sc}'.format(sample=sam, sc=scan))
    return

def plot_more_boxes(model, data, scans):
    for samp, samp_name in zip(samples, samp_names):
        for scan in scans:
            clust_labs = samp[model][scan].labels_
            #clust_cent  = samp[model][scan].cluster_centers_
            data_xbic = samp[data][scan][:,0]
            data_cu = samp[data][scan][:,1]
            data_cd = samp[data][scan][:,2]
            plot_clust_boxes(clusts, clust_labs, data_cu, data_xbic, data_cd, scan, samp_name)
    return
samp_names = ['NBL3_2', 'NBL3_3', 'TS58A']
plot_more_boxes(model, data, scans)

# =============================================================================
# def print_clust_means(clust_nums, x, y):
#     x1 = [x[np.where(clust_labs == clust)[0]] for clust in clust_nums]
#     y1 = [y[np.where(clust_labs == clust)[0]] for clust in clust_nums]
#     for i, (xclust, yclust) in enumerate(zip(x1,y1)):
#         print('copper clust ' + str(i) + ': ' + str(np.mean(xclust)))
#         print('xbic clust ' + str(i) + ': ' + str(np.mean(yclust)))
#     return
#     
# #print_clust_means(clust, data_cu, data_xbic)
# =============================================================================
# =============================================================================
#     for clust in clust_nums:
#         
#         indices = np.where(clust_labs == clust)[0]
#         x1 = x[indices]
#         y1 = y[indices]
# =============================================================================

### basic boxplots of raw data 
# =============================================================================
# 
# cu_maps = [samp['elXBIC_corr'][scan][0][:,:-2] for samp in samples]
# xbic_maps = [samp['XBIC_maps'][scan][:,:-2] for samp in samples]
# 
# cu_data = [samp['elXBIC_corr'][scan][0][:,:-2].ravel() for samp in samples]
# xbic_data = [samp['XBIC_maps'][scan][:,:-2].ravel() for samp in samples]
#     
# x_boxlabs = [samp['Name'] for samp in samples]
# 
# fig, axs = plt.subplots(1,2)
# plt.tight_layout()
# axs[0].imshow(cu_maps[2], origin='lower')
# axs[1].imshow(xbic_maps[2], origin='lower')
# 
# plt.figure()
# plt.boxplot(cu_data)
# plt.xticks([1, 2, 3], x_boxlabs)
# plt.suptitle('Thickness corrected Cu')
# plt.figure()
# plt.boxplot(xbic_data)
# plt.xticks([1, 2, 3], x_boxlabs)
# plt.suptitle('XBIC')
# =============================================================================

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