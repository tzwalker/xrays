# -*- coding: utf-8 -*-
"""
Trumann
Fri Oct 11 17:05:06 2019
"""
import scipy.io
import numpy as np
import h5py
# transform integers in scan list to strings
def str_list(L):
    L = [str(v) for v in L]
    return L

def h5_to_matlab(scan_list, import_path, exprot_path, elect_chan, XRF_norm):
    filenames = [(import_path + '/2idd_0' + scan + '.h5') for scan in str_list(scan_list)]
    nav_keys = ['/MAPS/XRF_fits','/MAPS/XRF_fits_quant']
    files = [h5py.File(file, 'r') for file in filenames]

    matlab_dicts = []
    for scan_h5 in files:
        electrical = scan_h5['/MAPS/scalers'][elect_chan] # cts/s
        number_of_elements = np.shape(scan_h5[nav_keys[0]])[0]
        ele_idxs = list(range(number_of_elements))
        
        for ele_idx in ele_idxs:
            norm_ele_maps = [scan_h5[nav_keys[0]][ele_idx,:,:] / 
                             scan_h5['/MAPS/scalers'][XRF_norm,:,:] / 
                             scan_h5[nav_keys[1]][XRF_norm, 0, ele_idx] for ele_idx in ele_idxs]
        encoded_element_names = scan_h5['MAPS/channel_names']
        decoded_element_names = [chan.decode('utf-8') for chan in encoded_element_names]
        # add electrical channel
        norm_ele_maps.insert(0, electrical); decoded_element_names.insert(0, 'ds_ic')
        mat_dict_of_h5s = {name: Map for name, Map in zip(decoded_element_names, norm_ele_maps)}
        matlab_dicts.append(mat_dict_of_h5s)
    export_filenames = [(export_path + r'\h5scan_' + name[-7:-3] + '.mat') for name in filenames]
    for mat_dict, fname in zip(matlab_dicts, export_filenames):
        scipy.io.savemat(fname, mat_dict)
    return

XRF_norm = 1 #us_ic
elect_chan = 2 #ds_ic

import_path = r'C:\Users\triton\Desktop\NBL3_data' 
export_path = r'C:\Users\triton\Dropbox (ASU)\Internal Reports\Data sharing with Math\Trumann\mat_files_shaped\TS58A'

XBIC = [408]#, , , ]

h5_to_matlab(XBIC, import_path, export_path, elect_chan, XRF_norm)

#%%
path = r'C:\Users\triton\Dropbox (ASU)\Internal Reports\Data sharing with Math\Trumann\mat_files_shaped\TS58A'
file = r'\h5scan_0408.mat'

f = path + file

from scipy.io import loadmat, whosmat

z = loadmat(f)
