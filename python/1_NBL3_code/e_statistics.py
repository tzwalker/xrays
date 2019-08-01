import numpy as np
import sklearn.preprocessing as skpp

def get_index_in_user_ele_list(s, E):               # copied from d_clustering.py
    for i, e in enumerate(E):                       
        if s == e[0:2]:                             # test first two characters of ele
            ele_i = i                               # use index of matched ele in 'elements' list
    return ele_i

def get_ele_maps(samp_dict, scan_i, corr_channels, user_channels):
    ele_maps = []
    for ch in corr_channels:
        ele_i = get_index_in_user_ele_list(ch, user_channels) 
        e_map = samp_dict['elXBIC_corr'][scan_i][ele_i][:,:-2]
        ele_maps.append(e_map)
    return ele_maps

def apply_mask(samps, channels_to_correlate, channels_inputed_by_user):
    for samp in samps:
        # apply mask to channels in XBIC scans first
        c_correlated_channels_in_ea_scan = []
        c_stat_arrs = []
        for scan_i, c_model in enumerate(samp['c_kclust_arrs']):
            stat_XBIC_map = samp['XBIC_maps'][scan_i][:,:-2]
            to_be_stat_maps = get_ele_maps(samp, scan_i, channels_to_correlate, channels_inputed_by_user)
            to_be_stat_maps.insert(0, stat_XBIC_map) 
            stat_arrs = [m.reshape(-1,1) for m in to_be_stat_maps]
            clust_ele_mask_dict = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
            other_map_clusters = [[np.take(other_map, mask_indices) for mask_indices in clust_ele_mask_dict.values()] for other_map in stat_arrs]
            c_correlated_channels_in_ea_scan.append(other_map_clusters) # save masked arrays 
            c_stat_arrs.append(stat_arrs)                    # save stat arrays for further use
        key = 'C_kclust_masked' 
        samp.setdefault(key, c_correlated_channels_in_ea_scan)        # store masked arrays
        samp['C_kclust_masked'] = c_correlated_channels_in_ea_scan    # update entry if needed
        ky = 'c_stat_arrs'
        samp.setdefault(ky, c_stat_arrs)                     # store stat arrays
        samp['c_stat_arrs'] = c_stat_arrs         # update entry if needed
        # apply mask to channels in XBIV scans
        v_correlated_channels_in_ea_scan = []
        v_stat_arrs = []
        for scan_i, c_model in enumerate(samp['c_kclust_arrs']):
            stat_XBIC_map = samp['XBIC_maps'][scan_i][:,:-2]
            to_be_stat_maps = get_ele_maps(samp, scan_i, channels_to_correlate, channels_inputed_by_user)
            to_be_stat_maps.insert(0, stat_XBIC_map) 
            stat_arrs = [m.reshape(-1,1) for m in to_be_stat_maps] 
            clust_ele_mask_dict = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
            other_map_clusters = [[np.take(other_map, mask_indices) for mask_indices in clust_ele_mask_dict.values()] for other_map in stat_arrs]
            v_correlated_channels_in_ea_scan.append(other_map_clusters)
            v_stat_arrs.append(stat_arrs)
        key = 'V_kclust_masked' 
        samp.setdefault(key, v_correlated_channels_in_ea_scan)        # make samp dict entry
        samp['V_kclust_masked'] = v_correlated_channels_in_ea_scan    # update entry if needed
        ky = 'v_stat_arrs'
        samp.setdefault(ky, v_stat_arrs)                     # store stat arrays
        samp['v_stat_arrs'] = v_stat_arrs         # update entry if needed
    return



def standardize_channels(samps):
    scaler = skpp.StandardScaler()
    for samp in samps:
        # apply_mask() also saves an arrayed version of every map; this is a requirement for proper statistics and standardization
        c_stand_arrs = [[scaler.fit_transform(channel) for channel in stat_arr] for stat_arr in samp['c_stat_arrs']]
        # essentially the clustered arrays are just one level deeper, i.e. each channel has n clusters
        c_stand_clust_arrs = [[[scaler.fit_transform(clust.reshape(-1,1)) for clust in channel] for channel in stat_arr] for stat_arr in samp['C_kclust_masked']]
        # do the same with XBIV maps
        v_stand_arrs = [[scaler.fit_transform(channel) for channel in stat_arr] for stat_arr in samp['v_stat_arrs']]
        v_stand_clust_arrs = [[[scaler.fit_transform(clust.reshape(-1,1)) for clust in channel] for channel in stat_arr] for stat_arr in samp['V_kclust_masked']]
        
        c_key = 'c_stat_arrs_stand'
        v_key = 'v_stat_arrs_stand'
        samp.setdefault(c_key, c_stand_arrs)
        samp.setdefault(v_key, v_stand_arrs)
        samp['c_stat_arrs_stand'] = c_stand_arrs
        samp['v_stat_arrs_stand'] = v_stand_arrs
        
        c_key = 'c_kclust_arrs_stand'
        v_key = 'v_kclust_arrs_stand'
        samp.setdefault(c_key, c_stand_clust_arrs)
        samp.setdefault(v_key, v_stand_clust_arrs)
        samp['c_kclust_arrs_stand'] = c_stand_clust_arrs
        samp['v_kclust_arrs_stand'] = v_stand_clust_arrs
    return
