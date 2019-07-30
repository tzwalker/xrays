import numpy as np

def ClusterIndicesNumpy(clustNum, labels_array): 
    return np.where(labels_array == clustNum)[0] # this will be for scatter plotting EACH cluster

def get_index_in_user_ele_list(s, E):               # copied from d_clustering.py
    for i, e in enumerate(E):                       
        if s == e[0:2]:                             # test first two characters of ele
            ele_i = i                               # use index of matched ele in 'elements' list
    return ele_i

def get_ele_maps(samp_dict, scan_i, corr_channels, user_channels):
    ele_maps = []
    for ch in corr_channels:
        ele_i = get_index_in_user_ele_list(ch, user_channels)# this index should match the index of the given element in the list 'elements'
        #print(ele_i) # good, 'Cd_L' was the element selected for correlation, and index '1' is printed (matches index in 'elements_in')
        e_map = samp_dict['elXBIC_corr'][scan_i][ele_i][:,:-2] # remove nan columns to match shape of kclust_arrs
        ele_maps.append(e_map)
    return ele_maps

def apply_mask(samps, channels_to_correlate, channels_inputed_by_user):
    for samp in samps:
        correlated_channels_in_ea_scan = []
        for scan_i, (c_model, v_model) in enumerate(zip(samp['c_kclust_arrs'], samp['v_kclust_arrs'])):
            stat_XBIC_map = samp['XBIC_maps'][scan_i][:,:-2] # assign matching elect map, remove nan columns
            to_be_stat_maps = get_ele_maps(samp, scan_i, channels_to_correlate, channels_inputed_by_user)
            # print(np.shape(stat_XBIC_map))
            # print(np.shape(to_be_stat_maps[0])) # good, shapes of these arrays match eachother
            # combine ele and elect lists
            to_be_stat_maps.insert(0, stat_XBIC_map) # maintain XBIC map in correct index position (0)
            # list comp for loop to reshape each array into one column
            stat_arrs = [m.reshape(-1,1) for m in to_be_stat_maps] # these arrays are of appropriate len
            # build clust dicts from model
            C_dict_clust_indices_of_clust_ele = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
            # np.take application, (n clusters) * (n_correlate_ele + 1) = length of this list
            other_map_clusters = [[np.take(other_map, index_list) for index_list in C_dict_clust_indices_of_clust_ele.values()] for other_map in stat_arrs]
            # structure of above list follows [['XBIC for each cluster'], ['ele1 for each cluster'], ...]
            correlated_channels_in_ea_scan.append(other_map_clusters)
        key = 'C_kclust_masked' 
        samp.setdefault(key, correlated_channels_in_ea_scan)        # make samp dict entry
        samp['C_kclust_masked'] = correlated_channels_in_ea_scan    # update entry if needed
    return other_map_clusters