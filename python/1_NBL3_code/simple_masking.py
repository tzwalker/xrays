# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_clust_boxes(clust_nums, clust_labs, data, scan, sam):
    fig, axs = plt.subplots(len(data),1)
    plt.tight_layout()
    clusters_for_each_channel = []
    for channel in data: # data is a list; each item is a column from the original numpy arr
        cluster_list = [channel[np.where(clust_labs == clust)[0]] for clust in clust_nums]
        clusters_for_each_channel.append(cluster_list)
    for i, clusters in enumerate(clusters_for_each_channel):
        bp_dict = axs[i].boxplot(clusters, showfliers=False)
        for line in bp_dict['medians']:
            med = line.get_ydata()                  # get median value array
            xpoint, ypoint = line.get_xydata()[1]   # get plot coordinates of median
            # annotate this position with median as string
            axs[i].annotate(xy=(xpoint,ypoint), 
               s=' ' + "{:.4g}".format(med[0]), 
               horizontalalignment='left') # add text with formatting
        axs[i].title.set_text(boxplot_names[i])
    plt.savefig(r'C:\Users\Trumann\Desktop\Plot Directory\NBL3\20190904 clustering and boxplots\noflier_{sample}_area{sc}'.format(sample=sam, sc=scan))
    return

def get_cluster_data(samp, scan, model_key, data_key, num_of_clust):
    data = samp[data_key][scan]
    clust_labs = samp[model_key][scan].labels_
    clust_nums = list(range(num_of_clust))
    cluster_data = [data[np.where(clust_labs == clust)[0]] for clust in clust_nums]
    return cluster_data

samp = NBL3_2
scan = 0
model = 'c_kmodels'
data_key = 'c_reduced_arrs'

z_cluster_data = get_cluster_data(samp, scan, model, data_key, cluster_number)

def clust_scatter_matrix(cluster_data, elements):
    cols = elements.insert(0, 'xbic')
    df = pd.DataFrame(cluster_data[0], columns = cols) # make for loop to go over each cluster in cluster_data
    pd.plotting.scatter_matrix(df, alpha = 0.2)
    return

z_test_corr = [np.corrcoef(cluster_data.T) for cluster_data in z_cluster_data]
z_test_medians = [np.median(cluster, axis=0) for cluster in z_cluster_data]
z_test_arr_medians = np.array(z_test_medians)
max_list = np.max(z_test_arr_medians, axis=0) # need to make tuple (index of feature, index of feature)

### ####
def plot_more_boxes(model, key, scans):
    for samp, samp_name in zip(samples, samp_names):
        for scan in scans:
            clust_labs = samp[model][scan].labels_
            data = [samp[key][scan][:,i] for i, ele in enumerate(samp[key][scan].T)] #this format is necessary for boxplots
            plot_clust_boxes(clusts, clust_labs, data, scan, samp_name)
    return
#samp_names = ['NBL3_2', 'NBL3_3', 'TS58A']
#boxplot_names = ['reduced xbic', 'reduced cu','reduced cd','reduced te']
#plot_more_boxes(model, data_key, scans)

def return_cluster_unique_lists(cluster_data):
    medians = [np.median(cluster, axis=0) for cluster in cluster_data]
    arr_medians = np.array(medians).T # for convenience of max/min identification between clusters
    
    indices_of_median_maxes = []
    indices_of_median_mins = []
    for channel in medians:
        index_of_median_maxes = channel.index(max(channel)) #--> really "cluster containing median max"
        index_of_median_mins = channel.index(min(channel))  #--> really "cluster containing median min"
        indices_of_median_maxes.append(index_of_median_maxes)
        indices_of_median_mins.append(index_of_median_mins)
    
    # these lists trade off, producing a unique identifier for a given combo in the max XBIC cluster
    indices_test_cluster0 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 0]
    indices_test_cluster1 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 1]
    indices_test_cluster2 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 2]
    return 

# =============================================================================
# test_combo_labels = list(range(len(elements)+1)) #--> change these to the indices 0,1,2,3 ; or however many channels you have
# 
# from itertools import chain, combinations # use this to generate the possible combinations
# 
# def all_subsets(ss):
#     combos = [combinations(ss, x) for x in range(0,len(ss)+1)]
#     return chain(*combos)
# 
# subsets = all_subsets(test_combo_labels)
# print(subsets)
# =============================================================================

# match/count the tuples of 'print(subset)' to the identifiers outputted by 'indices_test_cluster0' lines

### basic boxplots of raw data 
# =============================================================================
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
# 
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
