from sklearn.cluster import KMeans
import samp_dict_grow
import numpy as np

def kmeans_trials(samps, model_key, mask_chan, clust_num, iter_num, new_data_key):
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
        samp_dict_grow.build_dict(samp, model_key[0:2]+ new_data_key, scans_models)
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

def correlations_of_kmeans_trials(real_data, kmeans_trials, number_of_clusters, 
                                  focus_cluster_row, focus_channel_col):
    corrs_of_kmeans_trials = []
    for trial in kmeans_trials:
        # separate data into clusters
        cluster_data = [real_data[np.where(trial==clust)[0]] 
        for clust in list(range(number_of_clusters))]
        # get cluster of interest
        focus_cluster = get_focus_cluster(cluster_data, focus_cluster_row, focus_channel_col)
        # correlate cluster of interest
        focus_clust_corrs = np.corrcoef(focus_cluster)
        corrs_of_kmeans_trials.append(focus_clust_corrs)
    # correlations of cluster of interest in all kmeans trials
    corrs_of_kmeans_trials = np.array(corrs_of_kmeans_trials)
    # average between correlations of all kmeans trials
    avg_corr_of_kmeans_trials = np.mean(corrs_of_kmeans_trials, axis=0)
    # std dev of correlations of all kmeans trials
    std_corr_of_kmeans_trials = np.std(corrs_of_kmeans_trials, axis=0)
    return avg_corr_of_kmeans_trials, std_corr_of_kmeans_trials

def correlation_stats(samp, scans, data_key, trials_key, 
                      number_of_clusters, focus_cluster_row, focus_channel_col):
    corrs_of_scans_kavg_matrices = []
    corrs_of_scans_kstd_dev_matrices = []
    for scan in scans:
        real_data = samp[data_key][scan]
        kmeans_trials = samp[trials_key][scan]
        # average between correlations of all kmeans trials
        # std dev of correlations of all kmeans trials
            # this fxn is a dobule inner for loop
        avg, std_dev = correlations_of_kmeans_trials(real_data, 
                                                     kmeans_trials, 
                                                     number_of_clusters, 
                                                     focus_cluster_row, 
                                                     focus_channel_col)
        corrs_of_scans_kavg_matrices.append(avg)
        corrs_of_scans_kstd_dev_matrices.append(std_dev)
    corrs_of_scans_kavg_matrices = np.array(corrs_of_scans_kavg_matrices)
    corrs_of_scans_kstd_dev_matrices = np.array(corrs_of_scans_kstd_dev_matrices)
    # stats
    scan_avg = np.mean(corrs_of_scans_kavg_matrices, axis=0) # average over all scans
    scan_stdev = np.std(corrs_of_scans_kavg_matrices, axis=0) # std_dev from averaging over all scans
    trials_stdev_avg = np.mean(corrs_of_scans_kstd_dev_matrices, axis=0) # average over standard_deviation of all ktrials
    trials_stdev_stdev = np.std(corrs_of_scans_kstd_dev_matrices, axis=0) # std_dev from averaging over std_dev of all ktrials
    kstats_dict= dict()
    samp_dict_grow.build_dict(kstats_dict, 'all_kcorrs', corrs_of_scans_kavg_matrices)
    samp_dict_grow.build_dict(kstats_dict, 'kcorr_avg', scan_avg)
    samp_dict_grow.build_dict(kstats_dict, 'kcorr_std', scan_stdev)
    samp_dict_grow.build_dict(kstats_dict, 'ktrials_stats', [trials_stdev_avg,trials_stdev_stdev])
    samp_dict_grow.build_dict(samp, data_key[0:2]+'kstats', kstats_dict)
    return
