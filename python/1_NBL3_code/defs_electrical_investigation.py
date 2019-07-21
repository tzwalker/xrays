# -*- coding: utf-8 -*-
"""
created: Mon Jul 15 16:53:32 2019
author: Trumann
"""
import h5py

def import_h5s(s, p):
    imported_h5s = []
    for scan in s:
        # add if statement to check between sectors
        filename = '/2idd_0' + scan + '.h5'
        f = h5py.File(p + filename, 'r') # this needs to be an 'r'!!! otherwise the h5s will be overwritten...
        imported_h5s.append(f)
    return imported_h5s

### transform integers in scan list to strings; prep for use in filename strings ###
def str_list(L):
    L = [str(v) for v in L]
    return L

def get_add_h5s(samps, pth):
    for s in samps:
        ### change scan integers to strings ###
        s['XBIC_scans'] = str_list(s['XBIC_scans'])
        s['XBIV_scans'] = str_list(s['XBIV_scans'])
        ### import h5 files ###
        XBIC_h5s = import_h5s(s['XBIC_scans'], pth)
        XBIV_h5s = import_h5s(s['XBIV_scans'], pth)
        ### add files to sample dicitonaries ###
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

# added scaler_channel input to be defined by user
def get_add_elect_channel(samps, scaler_ch):
    for s in samps:
        IC_h5s = s['XBIC_h5s']
        ds_ic0 = [h5['/MAPS/scalers'][scaler_ch] for h5 in IC_h5s]  #grab xbic channels
        key = 'XBIC_ct_maps'
        s.setdefault(key, ds_ic0)
        
        IV_h5s = s['XBIV_h5s']
        ds_ic1 = [h5['/MAPS/scalers'][scaler_ch] for h5 in IV_h5s] #grab xbiv channels
        key = 'XBIV_ct_maps'
        s.setdefault(key, ds_ic1)
    return

def cts_to_elect(samps):
    for s in samps: 
        XBIC_scaled = [ds_ic * scale for ds_ic, scale in zip(s['XBIC_ct_maps'], s['c_scaler'])]  
        XBIV_scaled = [ds_ic * scale for ds_ic, scale in zip(s['XBIV_ct_maps'], s['v_scaler'])]
        c_key = 'XBIC_maps'
        v_key = 'XBIV_maps'
        s.setdefault(c_key, XBIC_scaled)
        s.setdefault(v_key, XBIV_scaled)
    return

