import numpy as np
import sklearn.preprocessing as skpp
import samp_dict_grow

def make_stat_arrays(samps):
    for samp in samps:
        # array XBIC scans first
        c_stats_of_scans = []
        for scan_i, eles in enumerate(samp['elXBIC_corr']):     # samp['elXBIC_corr'][scan][element]
            stat_XBIC_map = samp['XBIC_maps'][scan_i][:,:-2]                # get XBIC and chop off nans
            held_maps = [ele[:,:-2] for ele in eles]                        # get element maps and chop off nans
            held_maps.insert(0, stat_XBIC_map)                              # combine maps into list with XBIC @ index 0
            stats_of_scan = [m.reshape(-1,1) for m in held_maps]            # array each map
            combine_stats_of_scan = np.concatenate(stats_of_scan, axis = 1) # combine the arrays
            c_stats_of_scans.append(combine_stats_of_scan)                  # add these arrays to sample dictionary
        samp_dict_grow.build_dict(samp, 'c_stat_arrs', c_stats_of_scans)  # add comb arrs to dict
        v_stats_of_scans = []
        for scan_i, eles in enumerate(samp['elXBIV_corr']):     # samp['elXBIC_corr'][scan][element]
            stat_XBIC_map = samp['XBIV_maps'][scan_i][:,:-2]                # get XBIV and chop off nans
            held_maps = [ele[:,:-2] for ele in eles]                        # get element maps and chop off nans
            held_maps.insert(0, stat_XBIC_map)                              # combine maps into list with XBIC @ index 0
            stats_of_scan = [m.reshape(-1,1) for m in held_maps]            # array each map
            combine_stats_of_scan = np.concatenate(stats_of_scan, axis = 1) # combine the arrays
            v_stats_of_scans.append(combine_stats_of_scan)                  # add these arrays to sample dictionary
        samp_dict_grow.build_dict(samp, 'v_stat_arrs', v_stats_of_scans)  # add comb arrs to dict
    return

def standardize_channels(samps, dict_data, new_keys):
    scaler = skpp.StandardScaler()
    for samp in samps:
        c_standardized_stats = []
        for scan_arrays in samp[dict_data[0]]:
            c_stand_arrs = [scaler.fit_transform(column.reshape(-1,1)) for column in scan_arrays.T]
            combine_stand_arrs_of_scan = np.concatenate(c_stand_arrs, axis = 1)
            c_standardized_stats.append(combine_stand_arrs_of_scan)
        samp_dict_grow.build_dict(samp, new_keys[0], c_standardized_stats)
        v_standardized_stats = []
        for scan_arrays in samp[dict_data[1]]:
            c_stand_arrs = [scaler.fit_transform(column.reshape(-1,1)) for column in scan_arrays.T]
            combine_stand_arrs_of_scan = np.concatenate(c_stand_arrs, axis = 1)
            v_standardized_stats.append(combine_stand_arrs_of_scan)
        samp_dict_grow.build_dict(samp, new_keys[1], v_standardized_stats)
    return

def get_channel_column_index_in_scan_chan_arrs(ch, available_chans):
    for index, channel in enumerate(available_chans):
        if ch[0:2] in available_chans:
            index = index # do not add 1 to index here because XBIC is not in list 'available_chans'
    return index

def get_bad_chan_limits(scan_channel_arrs, control, ch_i):
    bad_chan = scan_channel_arrs[:,ch_i]
    bad_chan_mean = np.mean(bad_chan)
    bad_chan_sig = np.std(bad_chan)
    upr_lim = bad_chan_mean + control * bad_chan_sig
    lwr_lim = bad_chan_mean - control * bad_chan_sig
    return bad_chan, lwr_lim, upr_lim

def reduce_arrs(samples, channel, ch_in, threshold_control, data_to_reduce): # where data_to_reduce is the dict key of interest
    ch_i = get_channel_column_index_in_scan_chan_arrs(channel, ch_in)
    for samp in samples:
        reduced_scan_arrs = []
        for scan_channel_arrs in samp[data_to_reduce[0]]:
            bad_chan, lwr_lim, upr_lim = get_bad_chan_limits(scan_channel_arrs, threshold_control, ch_i)
            indices_to_keep = [i for i,x in enumerate(bad_chan) if (lwr_lim < x < upr_lim)]
            indices_to_keep = np.array(indices_to_keep)
            red_arrs = scan_channel_arrs[indices_to_keep, :]
            reduced_scan_arrs.append(red_arrs)
        samp_dict_grow.build_dict(samp, 'c_reduced_arrs', reduced_scan_arrs)
        # do same for voltage scans
        reduced_scan_arrs = []
        for scan_channel_arrs in samp[data_to_reduce[1]]:
            bad_chan, lwr_lim, upr_lim = get_bad_chan_limits(scan_channel_arrs, threshold_control, ch_i)
            indices_to_keep = [i for i,x in enumerate(bad_chan) if (lwr_lim < x < upr_lim)]
            indices_to_keep = np.array(indices_to_keep)
            red_arrs = scan_channel_arrs[indices_to_keep, :]
            reduced_scan_arrs.append(red_arrs)
        samp_dict_grow.build_dict(samp, 'v_reduced_arrs', reduced_scan_arrs)
    return

#reduce_arrs(samples, 'Cu', elements_in, 2, ['c_stat_arrs', 'v_stat_arrs']) 
# --> left off: revised boundaries with which to remove data samples before tranformation
    # whole standardized arrays exist in samp dictionary along with whole original data
    # check if the function above will make reduced scan_channel_arrays for either the original data
        # and the standardized data
# =============================================================================
# def standardize_channels(samps):
#     scaler = skpp.Stahttps://docs.scipy.org/doc/numpy/reference/generated/numpy.delete.htmlndardScaler()
#     for samp in samps:
#         # apply_mask() also saves an arrayed version of every map; this is a requirement for proper statistics and standardization
#         c_stand_arrs = [[scaler.fit_transform(channel) for channel in stat_arr] for stat_arr in samp['c_stat_arrs']]
#         # essentially the clustered arrays are just one level deeper, i.e. each channel has n clusters
#         c_stand_clust_arrs = [[[scaler.fit_transform(clust.reshape(-1,1)) for clust in channel] for channel in stat_arr] for stat_arr in samp['C_kclust_masked']]
#         # do the same with XBIV maps
#         v_stand_arrs = [[scaler.fit_transform(channel) for channel in stat_arr] for stat_arr in samp['v_stat_arrs']]
#         v_stand_clust_arrs = [[[scaler.fit_transform(clust.reshape(-1,1)) for clust in channel] for channel in stat_arr] for stat_arr in samp['V_kclust_masked']]
#         
#         c_key = 'c_stat_arrs_stand'
#         v_key = 'v_stat_arrs_stand'
#         samp.setdefault(c_key, c_stand_arrs)
#         samp.setdefault(v_key, v_stand_arrs)
#         samp['c_stat_arrs_stand'] = c_stand_arrs
#         samp['v_stat_arrs_stand'] = v_stand_arrs
#         
#         c_key = 'c_kclust_arrs_stand'
#         v_key = 'v_kclust_arrs_stand'
#         samp.setdefault(c_key, c_stand_clust_arrs)
#         samp.setdefault(v_key, v_stand_clust_arrs)
#         samp['c_kclust_arrs_stand'] = c_stand_clust_arrs
#         samp['v_kclust_arrs_stand'] = v_stand_clust_arrs
#     return
# =============================================================================

# =============================================================================
# # use with apply_mask() maybe...
# def get_index_in_user_ele_list(s, E):               # copied from d_clustering.py
#     for i, e in enumerate(E):                       
#         if s == e[0:2]:                             # test first two characters of ele
#             ele_i = i                               # use index of matched ele in 'elements' list
#     return ele_i
# 
# def get_ele_maps(samp_dict, scan_i, corr_channels, user_channels):
#     ele_maps = []
#     for ch in corr_channels:
#         ele_i = get_index_in_user_ele_list(ch, user_channels) 
#         e_map = samp_dict['elXBIC_corr'][scan_i][ele_i][:,:-2]
#         ele_maps.append(e_map)
#     return ele_maps
# 
# def apply_mask(samps, channels_to_correlate, channels_inputed_by_user):
#     for samp in samps:
#         # apply mask to channels in XBIC scans first
#         c_correlated_channels_in_ea_scan = []
#         for scan_i, c_model in enumerate(samp['c_kclust_arrs']):
#             clust_ele_mask_dict = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
#             other_map_clusters = [[np.take(other_map, mask_indices) for mask_indices in clust_ele_mask_dict.values()] for other_map in stat_arrs]
#             c_correlated_channels_in_ea_scan.append(other_map_clusters) # save masked arrays 
#         key = 'C_kclust_masked' 
#         samp.setdefault(key, c_correlated_channels_in_ea_scan)        # store masked arrays
#         samp['C_kclust_masked'] = c_correlated_channels_in_ea_scan    # update entry if needed
# 
#         # apply mask to channels in XBIV scans
#         v_correlated_channels_in_ea_scan = []
#         for scan_i, c_model in enumerate(samp['c_kclust_arrs']):
#             clust_ele_mask_dict = {str(clust_num): np.where(c_model.labels_ == clust_num)[0] for clust_num in range(c_model.n_clusters)}
#             other_map_clusters = [[np.take(other_map, mask_indices) for mask_indices in clust_ele_mask_dict.values()] for other_map in stat_arrs]
#             v_correlated_channels_in_ea_scan.append(other_map_clusters)
#         key = 'V_kclust_masked' 
#         samp.setdefault(key, v_correlated_channels_in_ea_scan)        # make samp dict entry
#         samp['V_kclust_masked'] = v_correlated_channels_in_ea_scan    # update entry if needed
#     return
# =============================================================================
