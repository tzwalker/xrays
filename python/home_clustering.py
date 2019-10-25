# -*- coding: utf-8 -*-
"""
Trumann
Mon Oct 21 14:01:31 2019
"""

from sklearn.cluster import KMeans
import samp_dict_grow
import numpy as np

def kmeans_trials(samps, data_key, mask_chan, clust_num, iter_num, new_data_key):
    for samp in samps:
        scans_models = []
        for i, scan_arr in enumerate(samp[data_key]):
            model_data = scan_arr[:,mask_chan]
            model_data = model_data.reshape(-1,1)
            model =  KMeans(init='k-means++', n_clusters=clust_num, n_init=10)
            models_labels = []
            count = 0
            while count < iter_num:
                model_fit = model.fit(model_data)
                model_labels = model_fit.labels_
                models_labels.append(model_labels)
                count = count+1
            models_labels = np.array(models_labels)
            scans_models.append(models_labels)
        samp_dict_grow.build_dict(samp, new_data_key, scans_models)
    return

#do not average over the data between scans before performing correlation!
#want to capture relative relationships WITHIN each map; also arrays are not 
    #of same length
def get_focus_cluster(cluster_data, cluster_row, cluster_column):
    # compress clusters to their medians
    medians_of_clusters = np.array([np.median(cluster, axis=0) for cluster in cluster_data])
    # identify median of desired channel
    medians_of_focus_channel = medians_of_clusters[:,cluster_column]
    # identify highest OR lowest median among clusters
    if cluster_row == 'high':
        cluster_index = np.argmax(medians_of_focus_channel)
    elif cluster_row == 'low':
        cluster_index = np.argmin(medians_of_focus_channel)
    # extract channels of focus cluster; transpose in prep for correlation
    data_of_focus_cluster = cluster_data[cluster_index].T
    return data_of_focus_cluster

from scipy.stats import spearmanr
def correlations_of_kmeans_trials(real_data, kmeans_trials, number_of_clusters, 
                                  focus_cluster_row, focus_channel_col):
    trials_all_corr = []
    trials_all_ps = []
    for trial in kmeans_trials:
        # separate data into clusters
        cluster_data = [real_data[np.where(trial==clust)[0]] for clust in list(range(number_of_clusters))]
        # get cluster of interest
        focus_cluster = get_focus_cluster(cluster_data, focus_cluster_row, focus_channel_col)
        # correlate cluster of interest
        trial_corr = spearmanr(focus_cluster.T) # spearman needs transpose, np.corrcoef does not
        trials_all_corr.append(trial_corr[0])
        trials_all_ps.append(trial_corr[1])
    corrs = np.array(trials_all_corr); pvals = np.array(trials_all_ps) # stack the corr matrices
    # average correlation matrices of all ktrials
    corrs_avg = np.mean(corrs, axis=0); pvals_avg = np.mean(pvals, axis=0)
    # std dev of average of correlation matrices of all ktrials
    corrs_std = np.std(corrs, axis=0); pvals_std = np.std(pvals, axis=0)
    ### include 'corrs' and 'pvals' if you want to extract the individual trials (1)
    trials_list = [corrs_avg, corrs_std, pvals_avg, pvals_std] 
    return trials_list

def correlation_stats(samp, scans, data_key, trials_key, 
                      number_of_clusters, focus_cluster_row, focus_channel_col,
                      new_data_keys):
    # rethink storage structure...
    sCorrs = []; sPvals = [] ### include 'kcorrs = []' and 'kpvals = []' if you want to store the individual trials (2)
    for scan in scans:
        real_data = samp[data_key][scan]
        kmeans_trials = samp[trials_key][scan]
        # returns list of properties from ktrials
        trials_list = correlations_of_kmeans_trials(real_data, 
                                                     kmeans_trials, 
                                                     number_of_clusters, 
                                                     focus_cluster_row, 
                                                     focus_channel_col)
        ### change these indices if you included individual ktrials (kcorrs, and kpvals) (3)
        corrs_stats = trials_list[0:2]; corrs_stats=np.array(corrs_stats) #the average and std of correlations
        pvals_stats = trials_list[2:4]; pvals_stats=np.array(pvals_stats) #the average and std of pvalues
        sCorrs.append(corrs_stats); sPvals.append(pvals_stats)
    sCorrs = np.array(sCorrs); sPvals = np.array(sPvals)
    CORRS = np.mean(sCorrs[:,0,:,:], axis=0); PVALS = np.mean(sPvals[:,0,:,:], axis=0) # global average between scans
    CORRS_std=np.std(sCorrs[:,0,:,:], axis=0); PVALS_std=np.std(sPvals[:,0,:,:], axis=0) # std dev of global average between scans
    samp_dict_grow.build_dict(samp, new_data_keys[0], [CORRS, CORRS_std])
    samp_dict_grow.build_dict(samp, new_data_keys[1], [PVALS, PVALS_std])
    return

if '__main__' ==__name__:
    SAMPLE = NBL3_2
    SCANS = [0,1,2]
    DATA_KEY = 'XBIC_slim'; CLUSTERS_KEY = 'XBICkmeans_trials'
    FOCUS_FEATURE = 0; FOCUS_CLUSTER = 'high'; CLUSTERS = 3
    NEW_KEYS = ['spear_stats', 'pval_stats']
    correlation_stats(SAMPLE, SCANS, DATA_KEY, CLUSTERS_KEY, 
                                   CLUSTERS, FOCUS_CLUSTER, FOCUS_FEATURE, NEW_KEYS)
    print(SAMPLE.keys())