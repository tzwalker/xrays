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

def get_clust_of_interest(medians_array, chan_of_interest, clust_of_interest):
    one_channel_medians = medians_array[:,chan_of_interest] # if channel_of_interest = 0 --> gets xbic medians; they are first column in medians_of_each_cluster
    if clust_of_interest == 'high':
        cluster_index = np.argmax(one_channel_medians)
    elif clust_of_interest == 'low':
        cluster_index = np.argmin(one_channel_medians)  # returns index (i.e. cluster) of desired cluster
    return cluster_index

def cluster_correlations(samp, scans, model, data_key, cluster_number, chan_of_interest, clusts_of_interest):
    correlations_of_each_scan = []
    for scan in scans:
        cluster_data = get_cluster_data(samp, scan, model, data_key, cluster_number)
        all_channel_medians = [np.median(cluster, axis=0) for cluster in cluster_data] # returns median array of each feature for each cluster
        all_channel_medians = np.array(all_channel_medians) # arrays the above data for convenience
        cluster_of_interest = get_clust_of_interest(all_channel_medians, chan_of_interest, clusts_of_interest)
        clust_corrcoeffs = np.corrcoef(cluster_data[cluster_of_interest].T) # generate the correlation matrix for desired cluster
        correlations_of_each_scan.append(clust_corrcoeffs)
    correlations_of_each_scan = np.array(correlations_of_each_scan)
    return correlations_of_each_scan

samp = TS58A
scans = [3]
model = 'c_kmodels'
data_key = 'c_reduced_arrs'
# column index of channel in which you wish to search for max or min medians
channel_of_interest = 0 
# input 'high' or 'low' to get cluster with highest or lowest values among the clusters
    # not configured to find relative performance of 'medium' clusters
clusters_of_interest = 'low'
# returns 3D pearson correlation coeff matrix for each scan
    # based off the highest or lowest feature
    # example of process:
        # find cluster with highest xbic value for a given scan (channel_of_interest = 0)
        # calculate correlation matrix between the elements and xbic in that cluster
        # repeat for the length of 'scans'
pearson_corr_coeffs = cluster_correlations(samp, scans, model, data_key, 
                                           cluster_number, channel_of_interest, clusters_of_interest)
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