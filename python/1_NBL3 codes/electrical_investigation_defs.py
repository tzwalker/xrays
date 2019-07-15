# -*- coding: utf-8 -*-
"""
created: Mon Jul 15 15:43:12 2019
author: Trumann
"""

import import_maps_H5

def str_list(L):
    ### transform integers in scan list to strings; prep for use in filename strings ###
    L = [str(v) for v in L]
    return L

def get_add_h5s(samps, pth):
    for s in samps:
        ### change scan integers to strings ###
        s['XBIC_scans'] = str_list(s['XBIC_scans'])
        s['XBIV_scans'] = str_list(s['XBIV_scans'])
        ### import h5 files ###
        XBIC_h5s = import_maps_H5.import_h5s(s['XBIC_scans'], pth)
        XBIV_h5s = import_maps_H5.import_h5s(s['XBIV_scans'], pth)
        key = 'XBIC_h5s'
        s.setdefault(key, XBIC_h5s)
        key = 'XBIV_h5s'
        s.setdefault(key, XBIV_h5s)
    return

def get_scan_scalers(samps):
    for s in samps:
        C_scale = [ (stan* 1E-9) / (bc * lock) for stan,bc,lock in zip(s['c_stanford'], s['beam_conv'], s['c_lockin'])]
        key = 'c_scaler'
        s.setdefault(key, C_scale)
        V_scale = [1 / (bc * lock) for bc,lock in zip(s['beam_conv'], s['c_lockin'])]
        key = 'v_scaler'
        s.setdefault(key, V_scale)
    return

# note the scaler index in this function 
# must match the scaler index where the XBIC signal of interest is stored 
# in the H5 structure (usually ds_ic, which is index 2)
    # us_ic is index 1
    # to get the list of available scalers, load H5, and write a for loop
    # to print out the values under the scaler_names group
    # e.g. file['/MAPS/''scaler_names'], where 'file' is a loaded H5
def get_and_add_DSIC_channels(samps):
    for s in samps:
        IC_h5s = s['XBIC_h5s']
        ds_ic0 = [h5['/MAPS/scalers'][2] for h5 in IC_h5s]  #grab xbic channels
        key = 'XBIC_ct_maps'
        s.setdefault(key, ds_ic0)
        
        IV_h5s = s['XBIV_h5s']
        ds_ic1 = [h5['/MAPS/scalers'][2] for h5 in IV_h5s] #grab xbiv channels
        key = 'XBIV_ct_maps'
        s.setdefault(key, ds_ic1)
    return

def cts_to_amps(samps):
    for s in samps: 
        XBIC_scaled = [ds_ic * scale for ds_ic, scale in zip(s['XBIC_ct_maps'], s['c_scaler'])]  
        XBIV_scaled = [ds_ic * scale for ds_ic, scale in zip(s['XBIV_ct_maps'], s['v_scaler'])]
        c_key = 'XBIC_maps'
        v_key = 'XBIV_maps'
        s.setdefault(c_key, XBIC_scaled)
        s.setdefault(v_key, XBIV_scaled)
    return