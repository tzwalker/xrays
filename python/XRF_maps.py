"""
coding: utf-8

tzwalker
Wed May 26 10:58:39 2021

this program is meant to deal with XRF data only

it shows how the MAPS software handles the h5 structure
the most useful fit units are 'raw_XRF', 'fit_XRF', and 'fit_XRF_norm_quant'
    one may want to normalize to the incident beam count rate
    to see what the incident beam count rate through the whole area:
        set the correction normalization scaler 'norm_scaler'
        (usually this is 'us_ic')
        set the fit units to '_norm'
        run 'plt.imshow(nrmlize_map[:,:-2])'

if L-lines were measured, the element in 'elements' list must include '_L'

"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

data_path = r'C:\Users\triton\NBL3_data\plan_view'
scan = 475
elements = ['Cu', 'Cd_L', 'Te_L', 'Mo_L']
# options: 'us_ic', 'ds_ic', 'SRCurrent'
norm_scaler = 'us_ic' 
# options: 'roi', 'fit'
fit_access_key = 'fit' 
# options:  'raw_XRF', 'raw_XRF_norm', 'raw_XRF_norm_quant', 
    #       'fit_XRF', 'fit_XRF_norm', 'fit_XRF_norm_quant'
fit_units = 'fit_XRF_norm' 


data_file = r'\2idd_0{s}.h5'.format(s=str(scan))
data_str = data_path+data_file

h5 = h5py.File(data_str, 'r')

# order of scaler channels in h5: '/MAPS/scalers'
scaler_chs = ['SRCurrent', 'us_ic', 'ds_ic']
# to find channel to normalize, set normalization index
norm_idx = scaler_chs.index(norm_scaler)

# set-up to find correct normalization scalers
if fit_access_key == 'roi':
    fit_keys = ['/MAPS/XRF_roi', '/MAPS/XRF_roi_quant']
    if fit_units == 'raw_XRF':
        # to find element, decode h5 element strings
        dcoded_chs = [ele_str.decode('utf-8') for ele_str in h5['/MAPS/channel_names']]
        maps_for_scan = []
        for element in elements:
            ele_idx = dcoded_chs.index(element)
            ele_map = h5[fit_keys[0]][ele_idx,:,:]
            fit_map = ele_map                                   ###
            maps_for_scan.append(fit_map)
        maps_to_array = np.array(maps_for_scan)
    elif fit_units == 'raw_XRF_norm':
        dcoded_chs = [ele_str.decode('utf-8') for ele_str in h5['/MAPS/channel_names']]
        maps_for_scan = []
        for element in elements:
            ele_idx = dcoded_chs.index(element)
            ele_map = h5[fit_keys[0]][ele_idx,:,:]
            nrmlize_map = h5['/MAPS/scalers'][norm_idx, :, :]   ###
            fit_map = ele_map / nrmlize_map                     ###
            maps_for_scan.append(fit_map)
        maps_to_array = np.array(maps_for_scan)
    elif fit_units == 'raw_XRF_norm_quant':
        dcoded_chs = [ele_str.decode('utf-8') for ele_str in h5['/MAPS/channel_names']]
        maps_for_scan = []
        for element in elements:
            ele_idx = dcoded_chs.index(element)
            ele_map = h5[fit_keys[0]][ele_idx,:,:]
            nrmlize_map = h5['/MAPS/scalers'][norm_idx, :, :] 
            quant_map = h5[fit_keys[1]][norm_idx, 0, ele_idx]   ####
            fit_map = ele_map / nrmlize_map / quant_map         ####
            maps_for_scan.append(fit_map)
        maps_to_array = np.array(maps_for_scan)
    else: print("you have entered incompatible fit_units and fit_access_key. make sure to use 'roi' for raw_XRF units and 'fit' for fit_XRF units")

elif fit_access_key == 'fit':  
    fit_keys = ['/MAPS/XRF_fits','/MAPS/XRF_fits_quant']
    if fit_units == 'fit_XRF':
        # to find element, decode h5 element strings
        dcoded_chs = [ele_str.decode('utf-8') for ele_str in h5['/MAPS/channel_names']]
        maps_for_scan = []
        for element in elements:
            ele_idx = dcoded_chs.index(element)
            ele_map = h5[fit_keys[0]][ele_idx,:,:]
            fit_map = ele_map                                   ###
            maps_for_scan.append(fit_map)
        maps_to_array = np.array(maps_for_scan)
    elif fit_units == 'fit_XRF_norm':
        dcoded_chs = [ele_str.decode('utf-8') for ele_str in h5['/MAPS/channel_names']]
        maps_for_scan = []
        for element in elements:
            ele_idx = dcoded_chs.index(element)
            ele_map = h5[fit_keys[0]][ele_idx,:,:]
            nrmlize_map = h5['/MAPS/scalers'][norm_idx, :, :]   ###
            fit_map = ele_map / nrmlize_map                     ###
            maps_for_scan.append(fit_map)
        maps_to_array = np.array(maps_for_scan)
    elif fit_units == 'fit_XRF_norm_quant':
        dcoded_chs = [ele_str.decode('utf-8') for ele_str in h5['/MAPS/channel_names']]
        maps_for_scan = []
        for element in elements:
            ele_idx = dcoded_chs.index(element)
            ele_map = h5[fit_keys[0]][ele_idx,:,:]
            nrmlize_map = h5['/MAPS/scalers'][norm_idx, :, :] 
            quant_map = h5[fit_keys[1]][norm_idx, 0, ele_idx]   ####
            fit_map = ele_map / nrmlize_map / quant_map         ####
            maps_for_scan.append(fit_map)
        maps_to_array = np.array(maps_for_scan)
    else: print("you have entered incompatible fit_units and fit_access_key. make sure to use 'roi' for raw_XRF units and 'fit' for fit_XRF units")
    
check = maps_to_array[0,:,:-2]
fig, ax = plt.subplots()
im = ax.imshow(check, origin='lower', cmap='Oranges_r')
fig.colorbar(im)#,format='.1f')



