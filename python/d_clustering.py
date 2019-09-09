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


# =============================================================================
# samp = NBL3_2
# scan = 0
# 
# z = samp['c_reduced_arrs'][scan]
# preclust_arr = z[:,0]
# preclust_arr = preclust_arr.reshape(-1,1)
# model =  KMeans(init='k-means++', n_clusters=3, n_init=10)
# clust_arr = model.fit(preclust_arr)
# =============================================================================

