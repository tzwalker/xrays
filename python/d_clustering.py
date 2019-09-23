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
samp = NBL3_2
scan = 0
real_data = samp['c_reduced_arrs'][scan]
model_data = samp['c_redStand_arrs'][scan]
model_xbic_data = model_data[:,0]
model_xbic_data = model_xbic_data.reshape(-1,1)
num_of_clusts = 3
model =  KMeans(init='k-means++', n_clusters=num_of_clusts, n_init=10)

def get_focus_cluster_index(medians, chan_column_index, focus_cluster):
    medians_of_focus_channel = medians[:,chan_column_index] # if chan_column_index = 0 --> gets xbic medians; they are first column in medians_of_each_cluster
    if focus_cluster == 'high':
        cluster_index = np.argmax(medians_of_focus_channel)# returns index of largest median cluster
    elif focus_cluster == 'low':
        cluster_index = np.argmin(medians_of_focus_channel)  # returns index of smallest median cluster
    return cluster_index

count = 0
correlations_of_each_scan = []
while count < 10:
    clust_xbic = model.fit(model_xbic_data)
    clust_labs = clust_xbic.labels_
    clust_nums = list(range(num_of_clusts))
    cluster_data = [real_data[np.where(clust_labs == clust)[0]] for clust in clust_nums]
    medians_of_clusters = [np.median(cluster, axis=0) for cluster in cluster_data]
    medians_of_clusters = np.array(medians_of_clusters) # row --> cluster; column --> median of feature (xbic,cu,cd,...)
    cluster_row_index = get_focus_cluster_index(medians_of_clusters, 0, 'high')
    data_of_focus_cluster = cluster_data[cluster_row_index].T # --> extract channels of focus cluster; transpose to prep for correlation
    clust_corrcoeffs = np.corrcoef(data_of_focus_cluster)
    correlations_of_each_scan.append(clust_corrcoeffs)
    count = count+1
correlations_of_each_scan = np.array(correlations_of_each_scan)
#need some way to visualize this... ask Tara
# will adding more data to the optimization reduce the number of local minima?
    # rerun code above with full data array
    # result: still varied convergence
# using labels to index into real data is a no-go as the reustling arrays will be of different lengths
    # according to the difference in the labels (which is what i'm trying to determine)
    # for simplicity, only use xbic channel to cluster for now
# the most common sums resulting from summing along rows of clust_labels_from_each_attempt 
    # will identify a data point that was put in the same cluster between each clustering attempt
    # exception: if all cluster attempts place a data point in cluster "0",
    # then the sum of that row will equal zero (this is unlikely)
        # solution would be to first check the summed_rows array for any sums of zero
summed_rows = np.sum(clust_labels_from_each_attempt1, axis=1)
if 0 in summed_rows:
    print('cannot use bincount')
else:
    print("take indices of 'most common' sums")
try_bincount = np.bincount(summed_rows)
# find indices of "most common" sums
# note this threshold of 100 will have to scale with the number of kmeans iterations, 
    # for now the number of iterations will be 10
    # future suggestion: make threshold 10x the number of iterations
trim_bincount = np.array(np.where(try_bincount > 100))
indices_of_consistently_clustered_data = np.where(summed_rows == trim_bincount)
indices_of_consistently_clustered_data = [np.array(np.where(summed_rows==important_sum)) for important_sum in trim_bincount[0]]
# combine all these indices in preparation for indexing into actual data
indices_of_consistent_data_combined = np.vstack(indices_of_consistently_clustered_data)



