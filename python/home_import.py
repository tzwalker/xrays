# -*- coding: utf-8 -*-
"""
created: Mon Jul 15 16:53:32 2019
author: Trumann
"""
import h5py
import numpy as np
import samp_dict_grow
# transform integers in scan list to strings
def str_list(L):
    L = [str(v) for v in L]
    return L

def import_h5s(samps, path):
    for samp in samps:
        # make list containing full path+file for each scan
        # make list containing h5 files
        # add h5s to sample dictionary
        c_filenames = [(path + '/2idd_0' + scan + '.h5') for scan in str_list(samp['XBIC_scans'])]
        xbic_h5s = [h5py.File(file, 'r') for file in c_filenames]
        samp_dict_grow.build_dict(samp, 'XBIC_h5s', xbic_h5s)
        
        v_filenames = [(path + '/2idd_0' + scan + '.h5') for scan in str_list(samp['XBIV_scans'])]
        xbiv_h5s = [h5py.File(file, 'r') for file in v_filenames]
        samp_dict_grow.build_dict(samp, 'XBIV_h5s', xbiv_h5s)
    return

def get_ele_idxs(user_channels, channels_in_scan):
    decoded_chs = [chan.decode('utf-8') for chan in channels_in_scan]
    index_list = [i for user_ch in user_channels for i,decoded_ch in enumerate(decoded_chs)  if user_ch == decoded_ch]
    return index_list

def get_normalization_keys(fluxnorm, fitnorm):
    # normalization of ds_ic
    if fluxnorm == 'ds_ic':  # scale data to ds_ic
        fluxnormindex = 0
    elif fluxnorm == 'us_ic': # scale data to us_ic
        fluxnormindex = 1  
    elif fluxnorm == 'SRcurrent':  # scale data to SRcurrent
        fluxnormindex = 2
    # quantification key for navigating h5
    if fitnorm == 'roi':
        nav_keys = ['/MAPS/XRF_roi', '/MAPS/XRF_roi_quant']
    elif fitnorm == 'fit':  
        nav_keys = ['/MAPS/XRF_fits','/MAPS/XRF_fits_quant']
    return fluxnormindex, nav_keys

def import_maps(samps, switch, scaler_ch, elements, flux_norm, fit_norm):
    for samp in samps:
        ## electrical deal
        # find electrical scaler channel; store cts/s
        if switch == 'XBIC':
            raw_maps = [h5['/MAPS/scalers'][scaler_ch] for h5 in samp['XBIC_h5s']]
            # calc scale factor for each scan (nanoamps to amps for stanford)
            scale_factors = [ (stan* 1E-9) / (V2F * lock) for stan, V2F, lock in zip(samp['c_stanford'], samp['beam_conv'], samp['c_lockin'])]
            # scale cts/s to amperes
            elect_maps = [ds_ic * scale for ds_ic, scale in zip(raw_maps, scale_factors)]
        elif switch == 'XBIV':
            raw_maps = [h5['/MAPS/scalers'][scaler_ch] for h5 in samp['XBIV_h5s']]
            scale_factors = [ 1 / (V2F * lock) for V2F, lock in zip(samp['beam_conv'], samp['v_lockin'])]
            elect_maps = [ds_ic * scale for ds_ic, scale in zip(raw_maps, scale_factors)]
        ## element deal
        # get element indices for each scan inside the scan h5
        ele_indices = [get_ele_idxs(elements, file['/MAPS/channel_names']) for file in samp['XBIC_h5s']]
        # get normalization keys inside h5
        flxnorm_idx, nav_keys = get_normalization_keys(flux_norm, fit_norm)
        # initialize map storage
        scan_maps = []
        # normalize each element map (cts/s to ug/cm2)
        for scan_h5, scan_elect, scan_eles in zip(samp['XBIC_h5s'], elect_maps, ele_indices):
            norm_ele_maps = [(scan_h5[nav_keys[0]][ele_idx, :, :] / 
                              scan_h5['/MAPS/scalers'][flxnorm_idx, :, :] / 
                              scan_h5[nav_keys[1]][flxnorm_idx, 0, ele_idx]) for ele_idx in scan_eles]
            norm_ele_maps = np.array(norm_ele_maps)
            all_scan_maps = np.insert(norm_ele_maps, 0, scan_elect, axis=0) # stack electrical on top of the element maps
            scan_maps.append(all_scan_maps)
        samp_dict_grow.build_dict(samp, switch+'_maps', scan_maps)
    return 

