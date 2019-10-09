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
    trials_corrs = []
    for trial in kmeans_trials:
        # separate data into clusters
        cluster_data = [real_data[np.where(trial==clust)[0]] 
        for clust in list(range(number_of_clusters))]
        # get cluster of interest
        focus_cluster = get_focus_cluster(cluster_data, focus_cluster_row, focus_channel_col)
        # correlate cluster of interest
        trial_corr = np.corrcoef(focus_cluster)
        trials_corrs.append(trial_corr)
    trials_corrs = np.array(trials_corrs)
    # average correlation of all ktrials
    trials_avg = np.mean(trials_corrs, axis=0)
    # std dev of average correlation of all ktrials
    trials_std = np.std(trials_corrs, axis=0)
    return trials_avg, trials_std

def correlation_stats(samp, scans, data_key, trials_key, 
                      number_of_clusters, focus_cluster_row, focus_channel_col):
    scans_corrs = [] # avg correlations for each scan (after multiple clusterings)
    scans_stds = [] # std_devs from averaging over ktrials for each scan
    for scan in scans:
        real_data = samp[data_key][scan]
        kmeans_trials = samp[trials_key][scan]
        # average correlation of all ktrials ; # std dev of average correlation of all ktrials
        trials_avg, trials_std = correlations_of_kmeans_trials(real_data, 
                                                     kmeans_trials, 
                                                     number_of_clusters, 
                                                     focus_cluster_row, 
                                                     focus_channel_col)
        scans_corrs.append(trials_avg);  scans_stds.append(trials_std)
    scans_corrs = np.array(scans_corrs); scans_stds = np.array(scans_stds)
    # scan level stats
    trials_stdev_avg = np.mean(scans_stds, axis=0) # average st_dev of ktrials for each scan
    trials_stdev_stdev = np.std(scans_stds, axis=0) # std_dev of average st_dev of ktrials for each scan
    sample_avg = np.mean(scans_corrs, axis=0) # average correlation for each sample
    sample_stdev = np.std(scans_corrs, axis=0) # std_dev of average correlation for each sample
    kstats_dict= dict()
    samp_dict_grow.build_dict(kstats_dict, 'trials_avgs', scans_corrs)
    samp_dict_grow.build_dict(kstats_dict, 'samp_avg', sample_avg)
    samp_dict_grow.build_dict(kstats_dict, 'samp_std', sample_stdev)
    samp_dict_grow.build_dict(kstats_dict, 'ktrials_stats', [trials_stdev_avg,trials_stdev_stdev])
    samp_dict_grow.build_dict(samp, data_key[0:2]+'kstats', kstats_dict)
    return
