# -*- coding: utf-8 -*-
"""
Trumann
Wed Sep 11 11:47:57 2019
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def get_cluster_data(samp, scan, model_key, data_key, num_of_clust):
    data = samp[data_key][scan]
    clust_labs = samp[model_key][scan].labels_
    clust_nums = list(range(num_of_clust))
    cluster_data = [data[np.where(clust_labs == clust)[0]] for clust in clust_nums]
    return cluster_data

def get_focus_cluster_index(medians, chan_column_index, focus_cluster):
    medians_of_focus_channel = medians[:,chan_column_index] # if chan_column_index = 0 --> gets xbic medians; they are first column in medians_of_each_cluster
    if focus_cluster == 'high':
        cluster_index = np.argmax(medians_of_focus_channel)# returns index of largest median cluster
    elif focus_cluster == 'low':
        cluster_index = np.argmin(medians_of_focus_channel)  # returns index of smallest median cluster
    return cluster_index

def focus_cluster_corr(samp, scans, model, data_key, cluster_number, focus_cluster, focus_channel):
    correlations_of_each_scan = []
    for scan in scans:
        data_of_clusters = get_cluster_data(samp, scan, model, data_key, cluster_number)
        medians_of_clusters = [np.median(cluster, axis=0) for cluster in data_of_clusters] # compress features in each cluster to their median values
        medians_of_clusters = np.array(medians_of_clusters) # row --> cluster; column --> median of feature (xbic,cu,cd,...)
        cluster_row_index = get_focus_cluster_index(medians_of_clusters, focus_channel, focus_cluster)
        data_of_focus_cluster = data_of_clusters[cluster_row_index].T # --> extract channels of focus cluster; transpose to prep for correlation
        clust_corrcoeffs = np.corrcoef(data_of_focus_cluster) # generate the correlation matrix for desired cluster
        correlations_of_each_scan.append(clust_corrcoeffs)
    correlations_of_each_scan = np.array(correlations_of_each_scan)
    return correlations_of_each_scan

#samp = NBL3_2
#scans = [0,1,2]
#model = 'c_kmodels'
#data_key = 'c_reduced_arrs'
# column index of channel in which you wish to search for max or min medians
#channel_of_interest = 0 
# input 'high' or 'low' to get cluster with highest or lowest values among the clusters
    # not configured to find relative performance of 'medium' clusters
#clusters_of_interest = 'high'
# returns 3D pearson correlation coeff matrix for each scan
    # based off the highest or lowest cluster of the given feature
    # example of process:
        # find cluster with highest xbic value for a given scan (channel_of_interest = 0)
        # calculate correlation matrix between the elements and xbic in that cluster
        # repeat for the length of 'scans'
pearson_corr_coeffs = focus_cluster_corr(NBL3_2, [3,4,5], 'c_kmodels', 'c_reduced_arrs', 
                                           cluster_number, 'low', 0)

# two compenents to finding cluster data
# example: 'high' xbic cluster
    # compenent 1: the channel you want to 
# focus_channel --> 'high' xbic finds medians of feature, i.e. the column in all_channel_medians
# focus_cluster finds row of cluster...

# clustering performed with reduced stand arrays, but map retrieved from regular
    # reduced data; no error thrown because these arrays are of same length
    # but need to check if there's a difference in the mask produced
        # need to check using arrs as reduced cannot be shaped easily
    # RESULT: clustering mask seemed identical when only using a single cluster channel

# Next step: make matrices for these scans when focus channel is high copper!


def plot_avg_pearson(corr_coeffs):
    # data conversion
    avg_corr = np.mean(corr_coeffs, axis=0)
    ele_labels = [e[0:2] for e in elements]
    cols = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo'] # MAKE SURE THIS MATCHES NUMBER OF LOADED ELEMENTS; changes depending on how h5s were fit
    df = pd.DataFrame(avg_corr, columns=cols, index=cols)
    # plot
    sns.set(style="white")
    # generate a mask for the upper triangle
    mask = np.zeros_like(df, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    # make cbar ticks
    cbar_tick={'ticks': list(list(np.linspace(-1,1,5)))}
    fig, ax = plt.subplots(1)
    ax = sns.heatmap(df, mask=mask, cbar_kws=cbar_tick, 
                     cmap='coolwarm', annot=True, vmin=-1, vmax=1)
    
    return

plot_avg_pearson(pearson_corr_coeffs)