

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
#%%
import numpy as np
import sklearn.preprocessing as skpp
import samp_dict_grow

# the dimensions of 3d axis can be combine with reshape
#y=z.T.reshape(np.shape(z)[1]*np.shape(z)[2], np.shape(z)[0]) #--> stacked maps to psuedo-ASCII column format

def stat_arrs(samples, dict_data, new_dict_data):
    for sample in samples:
        stat_scans = []
        for maps in sample[dict_data]:
            no_nan_maps = maps[:,:,:-2]
            z3Dto2D_rows = np.shape(no_nan_maps)[1]*np.shape(no_nan_maps)[2]
            z3Dto2D_cols = np.shape(no_nan_maps)[0]
            stat_arrs = no_nan_maps.T.reshape(z3Dto2D_rows, z3Dto2D_cols)
            stat_scans.append(stat_arrs)
        samp_dict_grow.build_dict(sample, new_dict_data, stat_scans)
    return

def stand_arrs(samples, dict_data, new_dict_data):
    scaler = skpp.StandardScaler()
    for sample in samples:
        stand_scans = []
        for stat_arrs in sample[dict_data]:
            stand_arrs_sep = [scaler.fit_transform(column.reshape(-1,1)) for column in stat_arrs.T] # is this necessary...? can i apply standardization on whole matrix...
            stand_arrs_comb = np.concatenate(stand_arrs_sep, axis = 1)
            stand_scans.append(stand_arrs_comb)
        samp_dict_grow.build_dict(sample, new_dict_data, stand_scans)
    return

def get_limits(bad_arr, sigma):
    lwr_lim = np.mean(bad_arr) - sigma*np.std(bad_arr)
    upr_lim = np.mean(bad_arr) + sigma*np.std(bad_arr)
    good_logic_arr = np.logical_and(bad_arr >= lwr_lim , bad_arr <= upr_lim)
    good_indices = np.where(good_logic_arr) # get indices within these bounds
    return good_indices

def remove_outliers(samples, dict_data, bad_idx, sigma, new_dict_data):
    for sample in samples:
        no_outliers = []
        for scan_arr in sample[dict_data]:
            bad_arr = scan_arr[:,bad_idx]
            good_indices = get_limits(bad_arr, sigma)
            no_outlier = scan_arr[good_indices]
            no_outliers.append(no_outlier)
        samp_dict_grow.build_dict(sample, new_dict_data, no_outliers)
        print('dummy_line')
    return

if '__main__' == __name__:
    remove_outliers(samples, 'XBIC_stat', 1, sigma=3, 'XBIC_slim')
    print('success')


