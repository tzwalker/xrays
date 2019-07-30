import numpy as np

def ClusterIndicesNumpy(clustNum, labels_array): 
    return np.where(labels_array == clustNum)[0]

def match_ele_index(corr_ch, ch_in):
    for index,c in enumerate(ch_in):
        if c == corr_ch:
            ele_i = index
    return ele_i

def get_ele_maps(samp_dict, scan_i, corr_channels, user_channels):
    ele_maps = []
    for ch in corr_channels:
        ele_i = match_ele_index(ch, user_channels)# this index should match the index of the given element in the list 'elements'
        print(ele_i) # good, 'Cd_L' was the element selected for correlation, and index '1' is printed (matches index in 'elements_in')
        e_map = samp_dict['elXBIC_corr'][scan_i][ele_i][:,:-2] # remove nan columns to match shape of kclust_arrs
        ele_maps.append(e_map)
    return ele_maps

def apply_mask(samps, channels_to_correlate, channels_inputed_by_user):
    for samp in samps:
        for scan_i, (c_model, v_model) in enumerate(zip(samp['c_kclust_arrs'], samp['v_kclust_arrs'])):
            stat_XBIC_map = samp['XBIC_maps'][scan_i][:,:-2] # assign matching elect map, remove nan columns
            list_of_ele_maps = get_ele_maps(samp, scan_i, channels_to_correlate, channels_inputed_by_user)
            
            # print(np.shape(stat_XBIC_map))
            # print(np.shape(list_of_ele_maps[0])) # good, shapes of these arrays match eachother
            # combine ele and elect lists
            # for loop to reshape each array into one column
            # build clust dicts from model
            # np.take application
            # what should be the output...?
# =============================================================================
#             c_clust_index_dict = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
#             
#             
#             v_clust_index_dict = {str(i): np.where(v_model.labels_ == i)[0] for i in range(v_model.n_clusters)}
# =============================================================================
            
            
    return 