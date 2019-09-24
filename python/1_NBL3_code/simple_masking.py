# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
import numpy as np
#do not average over the data between scans before performing correlation!
#want to capture relative relationships WITHIN each map; also arrays are not 
    #of same length



def get_focus_cluster(cluster_data, cluster_row, cluster_column):
    # compress clusters to their medians
    medians_of_clusters = np.array([np.median(cluster, axis=0) for cluster in cluster_data])
    # identify median of desired channel
    medians_of_focus_channel = medians_of_clusters[:,cluster_column] # if chan_column_index = 0 --> gets xbic medians; they are first column in medians_of_each_cluster
    if cluster_row == 'high':
        cluster_index = np.argmax(medians_of_focus_channel)# returns index of largest median cluster
    elif cluster_row == 'low':
        cluster_index = np.argmin(medians_of_focus_channel)  # returns index of smallest median cluster
    # extract channels of focus cluster; transpose to prep for correlation
    data_of_focus_cluster = cluster_data[cluster_index].T 
    return data_of_focus_cluster

def correlations_of_kmeans_trials(real_data, kmeans_trials, number_of_clusters, focus_cluster_row, focus_channel_col):
    corrs_of_kmeans_trials = []
    for trial in kmeans_trials:
        cluster_data = [real_data[np.where(trial==clust)[0]] for clust in number_of_clusters]
        focus_cluster = get_focus_cluster(cluster_data, focus_cluster_row, focus_channel_col)
        focus_clust_corrs = np.corrcoef(focus_cluster)
        corrs_of_kmeans_trials.append(focus_clust_corrs)
    corrs_of_kmeans_trials = np.array(corrs_of_kmeans_trials)
    # stats
    avg_corr_of_kmeans_trials = np.mean(corrs_of_kmeans_trials, axis=0)
    std_corr_of_kmeans_trials = np.std(corrs_of_kmeans_trials, axis=0)
    return corrs_of_kmeans_trials

