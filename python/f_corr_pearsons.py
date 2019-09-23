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

def unmasked_mapcorr(samp, scans, data_key):
    correlations_of_each_scan = []
    for scan in scans:
        data = samp[data_key][scan]
        map_corrcoeffs = np.corrcoef(data.T)
        correlations_of_each_scan.append(map_corrcoeffs)
    correlations_of_each_scan = np.array(correlations_of_each_scan)
    return correlations_of_each_scan

def plot_avg_pearson(corr_coeffs, eles):
    # data conversion
    avg_corr = np.mean(corr_coeffs, axis=0)
    std_corr = np.std(corr_coeffs, axis=0)
    # MAKE SURE THIS MATCHES NUMBER OF LOADED ELEMENTS; changes depending on how h5s were fit
    cols = ['XBIC'] + eles
    avgs = pd.DataFrame(avg_corr, columns=cols, index=cols)
    std_devs = pd.DataFrame(std_corr, columns=cols, index=cols)
    # plot
    sns.set(style="white")
    # generate a mask for the upper triangle
    mask = np.zeros_like(avgs, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    # make cbar ticks
    cbar_tick={'ticks': list(list(np.linspace(-1,1,5))), 'label': 'pearson corr coefficient'}
    cbar_tick1={'ticks': list(list(np.linspace(-1,1,5))), 'label': 'standard deviation'}
    fig, (ax0, ax1) = plt.subplots(2,1)
    plt.tight_layout()
    sns.heatmap(avgs, mask=mask, cbar_kws=cbar_tick, ax=ax0,
                     cmap='coolwarm', annot=True, vmin=-1, vmax=1)
    ax0.title.set_text('average linearity between areas')
    sns.heatmap(std_devs, mask=mask, cbar_kws=cbar_tick1, ax=ax1,
                 cmap='Greys',annot=True, vmin=0, vmax=1)
    ax1.title.set_text('standard deviations')
    return

def pearson_correlations(samp, scans, eles, model, masked_data, mask_switch, num_of_clusts):
    if mask_switch == "focus":
        corr_coeffs = focus_cluster_corr(samp, scans, model, masked_data, num_of_clusts, 
                                           'high', 0)
    elif mask_switch == "no_focus":
        corr_coeffs = unmasked_mapcorr(samp, scans, masked_data)
    
    plot_avg_pearson(corr_coeffs, eles)
    return

# =============================================================================
# scans = [0,1,2]
# mask_switch = 'focus' #or 'no_focus'
# model = 'c_kmodels'
# masked_data = 'c_stat_arrs'
# pearson_correlations(mask_switch, model, masked_data, scans)
# =============================================================================


