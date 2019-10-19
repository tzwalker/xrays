import numpy as np
import sklearn.preprocessing as skpp
import samp_dict_grow

# the dimensions of 3d axis can be combine with reshape
y=z.T.reshape(np.shape(z)[1]*np.shape(z)[2], np.shape(z)[0]) #--> stacked maps to psuedo-ASCII column format
def make_stat_arrays(samples, dict_data, new_keys):
    for sample in samples:
        c_stats_of_scans = []
        for scan_i, eles in enumerate(samp[dict_data[0]]):     
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

def get_channel_column_index(bad_XRF, loaded_XRF):
    for i, e in enumerate(loaded_XRF):
        if e[0:2] == bad_XRF:
            index = i
    return index

def reduce_arrs_actual(samps, bad_XRF, loaded_XRF, sigma_control, original_data, new_data):
    for samp in samps:
        c_reduced_arrs = []
        for full_data_array in samp[original_data[0]]:
            bad_channel_column_index = get_channel_column_index(bad_XRF, loaded_XRF) # find bad column
            bad_channel_column_index = bad_channel_column_index + 1 # add 1; xbic in position 0
            bad_chan_column = full_data_array[:, bad_channel_column_index] # isolate bad XRF column
            lwr_lim = np.mean(bad_chan_column) - sigma_control * np.std(bad_chan_column) # determine bounds
            upr_lim = np.mean(bad_chan_column) + sigma_control * np.std(bad_chan_column)
            good_indices = np.where(np.logical_and(bad_chan_column >= lwr_lim , bad_chan_column <= upr_lim)) # get indices within these bounds
            reduced_data_array = full_data_array[good_indices] # take good indices from whole array
            c_reduced_arrs.append(reduced_data_array) # store data
        samp_dict_grow.build_dict(samp, new_data[0], c_reduced_arrs)
        v_reduced_arrs = []
        for full_data_array in samp[original_data[1]]:
            bad_channel_column_index = get_channel_column_index(bad_XRF, loaded_XRF) # find bad column
            bad_channel_column_index = bad_channel_column_index + 1 # add 1; xbic in position 0
            bad_chan_column = full_data_array[:, bad_channel_column_index] # isolate bad XRF column
            lwr_lim = np.mean(bad_chan_column) - sigma_control * np.std(bad_chan_column) # determine bounds
            upr_lim = np.mean(bad_chan_column) + sigma_control * np.std(bad_chan_column)
            good_indices = np.where(np.logical_and(bad_chan_column >= lwr_lim , bad_chan_column <= upr_lim)) # get indices within these bounds
            reduced_data_array = full_data_array[good_indices] # take good indices from whole array
            v_reduced_arrs.append(reduced_data_array) # store data
        samp_dict_grow.build_dict(samp, new_data[1], v_reduced_arrs)
    return




