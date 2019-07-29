import numpy as np

def ClusterIndicesNumpy(clustNum, labels_array): 
    return np.where(labels_array == clustNum)[0]

def get_ele_maps(samp_dict, scan_i, chans):
    ele_maps = []
    for ele_i, ch in enumerate(chans):
        e_map = samp_dict['elXBIC_corr'][scan_i][ele_i]
        ele_maps.append(e_map)
    return ele_maps

def apply_mask(samps, channels):
    for samp in samps:
        for scan_i, (c_model, v_model) in enumerate(zip(samp['c_kclust_arrs'], samp['v_kclust_arrs'])):
            stat_XBIC_map = samp['XBIC_maps'][scan_i][:,:,-2] # assign matching elect map and remove nan columns
            list_of_ele_maps = get_ele_maps(samp, scan_i, channels)
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