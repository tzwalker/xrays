# -*- coding: utf-8 -*-
"""
created: Mon Jul 15 16:53:32 2019
author: Trumann
"""
import samp_dict_grow
import numpy as np

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

def import_maps(samps, scaler_ch, elements, flux_norm, fit_norm):
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
            all_scan_maps = np.insert(norm_ele_maps, 0, scan_xbic, axis=0)
            scan_maps.append(all_scan_maps)
        samp_dict_grow.build_dict(samp, 'maps', scan_maps)
        print('dummy line')
    return 

NBL3_2 = {'Name': 'NBL3-2', 'XBIC_scans': [422,423,424, 550,538,575], 'XBIV_scans': [419,420,421, 551], # good geom XBIC
          'beam_conv':      [2E5,2E5,2E5, 2E5,2E5,2E5], 
          'c_stanford':     [5000,5000,5000, 50000,50000,50000], 
          'c_lockin':       [500,500,500, 100,100,100], 
          'v_lockin':       [1E3,1E3,1E3, 10000],
          # wrong key decriptor 2017_12_2IDD, but geometry same between the two beamtimes
          '2017_12_ele_iios': [0.275, 0.0446, 0.0550], 
          '2019_03_ele_iios': [0.104, 0.00131, 0.00418]}
NBL3_3 = {'Name': 'NBL3_3', 'XBIC_scans': [264,265,266, 475,491], 'XBIV_scans': [261,262,263, 472], 
          'beam_conv':      [2E5, 2E5, 2E5, 1E5,1E5], 
          'c_stanford':     [5000,5000,5000, 200,200], 
          'c_lockin':       [500,500,500, 20,20], 
          'v_lockin':       [1E4,1E4,1E4, 100000],
          '2017_12_ele_iios': [0.296, 0.0488, 0.0604],
          '2019_03_ele_iios': [0.114, 0.00144, 0.00459]}
TS58A = {'Name': 'TS58A', 'XBIC_scans': [385,386,387, 439,427,404], 'XBIV_scans': [382,383,384, 440], #
         'beam_conv':       [2E5, 2E5, 2E5, 1E5,1E5,1E5], 
         'c_stanford':      [5000,5000,5000, 200,200,200], 
         'c_lockin':        [10000,10000,10000, 20,20,20], 
         # lockin amp almost certainly 10000 for 2019_03_2idd scans 385-387;
         # cross-sample comparison can be made with 500, but this is not how science is done
         'v_lockin':        [1000,1000,1000, 100000],
         '2017_12_ele_iios': [0.381, 0.0682, 0.0867],
         '2019_03_ele_iios': [0.162, 0.00209, 0.00669]}

samples = [NBL3_2, NBL3_3, TS58A]

from b_import_h5 import import_h5s
scan_path = r'C:\Users\triton\Desktop\NBL3_data'
import_h5s(samples, scan_path)
elements = ['Cu', 'Cd_L', 'Te_L', 'Mo_L']
# 1: us_ic, 2: ds_ic ; 
import_maps(samples, 2, elements, 'us_ic', 'fit') 