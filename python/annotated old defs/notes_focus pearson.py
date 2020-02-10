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

def pearson_correlations(samp, scans, eles, model, masked_data, mask_switch, num_of_clusts):
    if mask_switch == "focus":
        corr_coeffs = focus_cluster_corr(samp, scans, model, masked_data, num_of_clusts, 
                                           'high', 0)
    elif mask_switch == "no_focus":
        corr_coeffs = unmasked_mapcorr(samp, scans, masked_data)
    
    plot_avg_pearson(corr_coeffs, eles)
    return