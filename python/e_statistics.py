import numpy as np
import sklearn.preprocessing as skpp
import samp_dict_grow

def make_stat_arrays(samps, dict_data, new_keys):
    for samp in samps:
        # array XBIC scans first
        c_stats_of_scans = []
        for scan_i, eles in enumerate(samp[dict_data[0]]):     # samp['elXBIC_corr'][scan][element]
            stat_XBIC_map = samp['XBIC_maps'][scan_i][:,:-2]                # get XBIC and chop off nans
            held_maps = [ele[:,:-2] for ele in eles]                        # get element maps and chop off nans
            held_maps.insert(0, stat_XBIC_map)                              # combine maps into list with XBIC @ index 0
            stats_of_scan = [m.reshape(-1,1) for m in held_maps]            # array each map
            combine_stats_of_scan = np.concatenate(stats_of_scan, axis = 1) # combine the arrays
            c_stats_of_scans.append(combine_stats_of_scan)                  # add these arrays to sample dictionary
        samp_dict_grow.build_dict(samp, new_keys[0], c_stats_of_scans)  # add comb arrs to dict
        v_stats_of_scans = []
        for scan_i, eles in enumerate(samp[dict_data[1]]):     # samp['elXBIC_corr'][scan][element]
            stat_XBIC_map = samp['XBIV_maps'][scan_i][:,:-2]                # get XBIV and chop off nans
            held_maps = [ele[:,:-2] for ele in eles]                        # get element maps and chop off nans
            held_maps.insert(0, stat_XBIC_map)                              # combine maps into list with XBIC @ index 0
            stats_of_scan = [m.reshape(-1,1) for m in held_maps]            # array each map
            combine_stats_of_scan = np.concatenate(stats_of_scan, axis = 1) # combine the arrays
            v_stats_of_scans.append(combine_stats_of_scan)                  # add these arrays to sample dictionary
        samp_dict_grow.build_dict(samp, new_keys[1], v_stats_of_scans)  # add comb arrs to dict
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

def reduce_arrs(samples, channel, ch_in, threshold_control, data_to_reduce, new_keys): # where data_to_reduce is the dict key of interest
    ch_i = get_channel_column_index_in_scan_chan_arrs(channel, ch_in)
    for samp in samples:
        reduced_scan_arrs = []
        for scan_channel_arrs in samp[data_to_reduce[0]]:
            bad_chan, lwr_lim, upr_lim = get_bad_chan_limits(scan_channel_arrs, threshold_control, ch_i)
            indices_to_keep = [i for i,x in enumerate(bad_chan) if (lwr_lim < x < upr_lim)]
            indices_to_keep = np.array(indices_to_keep)
            red_arrs = scan_channel_arrs[indices_to_keep, :]
            reduced_scan_arrs.append(red_arrs)
        samp_dict_grow.build_dict(samp, new_keys[0], reduced_scan_arrs)
        # do same for voltage scans
        reduced_scan_arrs = []
        for scan_channel_arrs in samp[data_to_reduce[1]]:
            bad_chan, lwr_lim, upr_lim = get_bad_chan_limits(scan_channel_arrs, threshold_control, ch_i)
            indices_to_keep = [i for i,x in enumerate(bad_chan) if (lwr_lim < x < upr_lim)]
            indices_to_keep = np.array(indices_to_keep)
            red_arrs = scan_channel_arrs[indices_to_keep, :]
            reduced_scan_arrs.append(red_arrs)
        samp_dict_grow.build_dict(samp, new_keys[1], reduced_scan_arrs)
    return

samp = NBL3_2
scan = 0
data_key = 'c_reduced_arrs'
model_key = 'c_kmodels'
data = samp[data_key][scan]
clust_label = samp[model_key][scan].labels_
clust_numbers = list(range(cluster_number))

data_channels_as_list_items = [data[:,i] for i, ele in enumerate(data.T)] # make list out of each column/channel of numpy array
medians = []
for channel in data_channels_as_list_items:
    clusters_for_each_channel = [ channel[np.where(clust_label == cluster_number)[0]] for cluster_number in clust_numbers ] # find where indices match for each cluster in the column/channel 
    cluster_medians = [np.median(cluster) for cluster in clusters_for_each_channel] # find the median of each cluster array of the column/channel
    medians.append(cluster_medians)

indices_of_median_maxes = []
indices_of_median_mins = []
for channel in medians:
    index_of_median_maxes = channel.index(max(channel)) #--> really "cluster containing median max"
    index_of_median_mins = channel.index(min(channel))  #--> really "cluster containing median min"
    indices_of_median_maxes.append(index_of_median_maxes)
    indices_of_median_mins.append(index_of_median_mins)

# these lists trade off, producing a unique identifier for a given combo in the max XBIC cluster
indices_test_cluster0 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 0]
indices_test_cluster1 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 1]
indices_test_cluster2 = [i for i, cluster in enumerate(indices_of_median_maxes) if cluster == 2]

test_combo_labels = ['A', 'B', 'C', 'D'] #--> change these to the indices 0,1,2,3 ; or however many channels you have

# use this to generate the possible combinations
from itertools import chain, combinations

def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1)))

for subset in all_subsets(test_combo_labels):
    print(subset)

# match/count the tuples of 'print(subset)' to the identifiers outputted by 'indices_test_cluster0' lines
    




