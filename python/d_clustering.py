from sklearn.cluster import KMeans
import samp_dict_grow

def get_column_indices(clust_chans, available_chans): # this is finding the column in the stat arrays that corresponds to the channels you want to cluster
    if 'all' in clust_chans:
        indices = list(range(len(available_chans) + 1)) # add one to include XBIC array
        return indices
    else:
        indices = []
        for index, channel in enumerate(available_chans):
            if channel[0:2] in clust_chans:
                index = index + 1 # XBIC is always @ index 0
                indices.append(index)
        if 'perf' in clust_chans:
            indices.insert(0,0)
        # do not need to sort indices because i'm iterating over the available channels,
            # the indices of which, by earlier design in e_statistics.py,
            # correspond directly to those in the stat arrays
        return indices

def find_clusters(samps, num_of_clusters, clust_channels, loaded_XRF, dict_data):
    column_indices = get_column_indices(clust_channels, loaded_XRF) # returns indices of columns of stat/standardized array for scan; used to cluster only channels of interest
    for samp in samps:
        c_scan_models = []
        for preclust_arr in samp[dict_data[0]]:
            trimmed_pre_clust_arrs = preclust_arr[:, column_indices] # use only array columns of interest
            model = KMeans(init='k-means++', n_clusters=num_of_clusters, n_init=10) # define model (must be included in this loop to reset for each scan/pre_clust_arrs)
            clust_arrs = model.fit(trimmed_pre_clust_arrs) # perform clustering
            c_scan_models.append(clust_arrs) # save model
        samp_dict_grow.build_dict(samp, 'c_kmodels', c_scan_models) # store models
        v_scan_models = []
        for preclust_arr in samp[dict_data[1]]:
            trimmed_pre_clust_arrs = preclust_arr[:, column_indices] # use only array columns of interest
            model = KMeans(init='k-means++', n_clusters=num_of_clusters, n_init=10) # define model (must be included in this loop to reset for each scan/pre_clust_arrs)
            clust_arrs = model.fit(trimmed_pre_clust_arrs) # perform clustering
            v_scan_models.append(clust_arrs) # save model
        samp_dict_grow.build_dict(samp, 'v_kmodels', v_scan_models) # store models
    return

def kclustering(samps, N, clust_channels, available_channels, outlier_switch):
    if outlier_switch == 0: # use this switch for original data without two nan columns on the end (removed in )
        samp_dict_data = ['c_stat_arrs', 'v_stat_arrs'] 
        find_clusters(samps, N, clust_channels, available_channels, samp_dict_data) 
    elif outlier_switch == 1: # use this switch for whole standardized original data
        samp_dict_data = ['c_stand_arrs', 'v_stand_arrs'] 
        find_clusters(samps, N, clust_channels, available_channels, samp_dict_data)
    elif outlier_switch == 2: # use this switch for reduced data of the original data
        samp_dict_data = ['c_reduced_arrs', 'v_reduced_arrs'] 
        find_clusters(samps, N, clust_channels, available_channels, samp_dict_data)
    elif outlier_switch == 3: # use this switch for reduced data of the original data
        samp_dict_data = ['c_redStand_arrs', 'v_redStand_arrs'] 
        find_clusters(samps, N, clust_channels, available_channels, samp_dict_data)
    return

import numpy as np

def get_focus_cluster_index(medians, chan_column_index, focus_cluster):
    medians_of_focus_channel = medians[:,chan_column_index] # if chan_column_index = 0 --> gets xbic medians; they are first column in medians_of_each_cluster
    if focus_cluster == 'high':
        cluster_index = np.argmax(medians_of_focus_channel)# returns index of largest median cluster
    elif focus_cluster == 'low':
        cluster_index = np.argmin(medians_of_focus_channel)  # returns index of smallest median cluster
    return cluster_index

def get_focus_cluster_data(real_data,clust_labs,clust_nums,focus_channel, focus_cluster):
    # separate data into clusters
    cluster_data = [real_data[np.where(clust_labs == clust)[0]] for clust in clust_nums]
    # array of median values of the data in each cluster 
        # row --> cluster; column --> median of feature (xbic,cu,cd,...)
    medians_of_clusters = np.array([np.median(cluster, axis=0) for cluster in cluster_data]) 
    focus_cluster_row_index = get_focus_cluster_index(medians_of_clusters, focus_channel, focus_cluster)
    # extract channels of focus cluster; transpose to prep for correlation
    data_of_focus_cluster = cluster_data[focus_cluster_row_index].T 
    return data_of_focus_cluster

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def plot_pearson_matrix(corr1, corr2, eles):
    cols = ['XBIC'] + eles
    corr1 = pd.DataFrame(corr1, columns=cols, index=cols)
    corr2 = pd.DataFrame(corr2, columns=cols, index=cols)
    # plot
    sns.set(style="white")
    # generate a mask for the upper triangle
    mask = np.zeros_like(corr1, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    # make cbar ticks
    cbar_tick={'ticks': list(list(np.linspace(-1,1,5))), 'label': 'Pearson Correlation Coeff.'}
    cbar_tick1={'ticks': list(list(np.linspace(-1,1,5))), 'label': 'Standard Deviation'}
    fig, (ax0, ax1) = plt.subplots(2,1)
    plt.tight_layout()
    sns.heatmap(corr1, mask=mask, cbar_kws=cbar_tick, ax=ax0,
                 cmap='coolwarm',annot=True, vmin=-1, vmax=1)
    ax0.title.set_text('Average Linearity Between Scans')
    sns.heatmap(corr2, mask=mask, cbar_kws=cbar_tick1, ax=ax1,
                 cmap='Greys',annot=True, vmin=0, vmax=1)
    ax1.title.set_text('Standard Devation')
    return

def stats_after_many_kmeans_trials(samp, scans, data_key, model_key, cluster_number, 
                           focus_channel, focus_cluster, iterations, eles):
    correlation_of_all_scans = []
    deviation_of_all_scans = []
    for scan in scans:
        real_data = samp[data_key][scan]
        model_xbic_data = samp[model_key][scan][:,focus_channel]
        model_xbic_data = model_xbic_data.reshape(-1,1)
        model =  KMeans(init='k-means++', n_clusters=cluster_number, n_init=10)
        
        correlations_of_all_clusterings = []
        count = 0
        while count < iterations:
            clust_xbic = model.fit(model_xbic_data)
            clust_labs = clust_xbic.labels_
            clust_nums = list(range(cluster_number))
            data_of_focus_cluster = get_focus_cluster_data(real_data,
                                                           clust_labs,
                                                           clust_nums,
                                                           focus_channel,
                                                           focus_cluster)
            # pearson correlation matrix of focus cluster
            clust_corrcoeffs = np.corrcoef(data_of_focus_cluster)
            # store coefficient matrix of this clustering
            correlations_of_all_clusterings.append(clust_corrcoeffs)
            count = count+1
        correlations_of_all_clusterings = np.array(correlations_of_all_clusterings)
        # calculate average of coeff matrices for all clusterings performed
        avg_corr_kmeans = np.mean(correlations_of_all_clusterings, axis=0)
        std_corr_kmeans = np.std(correlations_of_all_clusterings, axis=0)
        #plot_pearson_matrix(avg_corr_kmeans, std_corr_kmeans, elements)
        # store average coeff matrix of this scan
        correlation_of_all_scans.append(avg_corr_kmeans)
        deviation_of_all_scans.append(std_corr_kmeans)
        
    correlation_of_all_scans = np.array(correlation_of_all_scans)
    deviation_of_all_scans = np.array(deviation_of_all_scans)
    # calculate the average of coeff matrices for all scans looked at
    avg_corr_scans = np.mean(correlation_of_all_scans, axis=0)
    std_corr_scans = np.std(correlation_of_all_scans, axis=0)
    plot_pearson_matrix(avg_corr_scans, std_corr_scans, eles)
    return avg_corr_scans, std_corr_scans

# =============================================================================
# samp = NBL3_2
# scans = [0,1,2]
# data_key = 'c_reduced_arrs'
# model_key = 'c_redStand_arrs'
# cluster_number = 3
# focus_channel = 0
# focus_cluster = 'high'
# iterations = 10
# stats_after_many_kmeans_trials(samp, scans, data_key, model_key, cluster_number, 
#                            focus_channel, focus_cluster, iterations)
# =============================================================================

def kmeans_trials(samps, model_key, mask_chan, clust_num, iter_num):
    for samp in samps:
        scans_models = []
        for i, scan_arr in enumerate(samp[model_key]):
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
        samp_dict_grow.build_dict(samp, model_key[0:2]+ 'kmeans_trials', scans_models)
    return

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
        cluster_data = [real_data[np.where(trial==clust)[0]] for clust in list(range(number_of_clusters))]
        focus_cluster = get_focus_cluster(cluster_data, focus_cluster_row, focus_channel_col)
        focus_clust_corrs = np.corrcoef(focus_cluster)
        corrs_of_kmeans_trials.append(focus_clust_corrs)
    corrs_of_kmeans_trials = np.array(corrs_of_kmeans_trials)
    # stats
    avg_corr_of_kmeans_trials = np.mean(corrs_of_kmeans_trials, axis=0)
    std_corr_of_kmeans_trials = np.std(corrs_of_kmeans_trials, axis=0)
    return corrs_of_kmeans_trials
