# -*- coding: utf-8 -*-
"""
created: Mon Jul 15 16:53:32 2019
author: Trumann
"""
from samp_dict_grow import build_dict

def get_add_electrical(samps, scaler_ch):
    for samp in samps:
        # calculate the scale factor (in amperes) according to electrical settings of scan
            # this for loop takes advantage of the order of 
            # 'c_stanford', 'beam_conv', and 'c_lockin' lists in the sample dicts
        xbic_scale_factors = [ (stan* 1E-9) / (V2F * lock) 
        for stan, V2F, lock 
        in zip(samp['c_stanford'], samp['beam_conv'], samp['c_lockin'])]
        
        # store scaler containing electrical in list
        raw_xbic = [h5['/MAPS/scalers'][scaler_ch] for h5 in samp['XBIC_h5s']]
        
        # convert scaler channel into amps
        xbic_scaled = [ds_ic * scale for ds_ic, scale in zip(raw_xbic, xbic_scale_factors)]
        
        # import XBIC_maps to sample dict
        build_dict(samp, 'XBIC_maps', xbic_scaled)
        
        xbiv_scale_factors = [ 1 / (V2F * lock) for V2F, lock 
                              in zip(samp['beam_conv'], samp['c_lockin'])]
        raw_xbiv = [h5['/MAPS/scalers'][scaler_ch] for h5 in samp['XBIV_h5s']]  #grab xbic channels
        xbiv_scaled = [ds_ic * scale for ds_ic, scale in zip(raw_xbiv, xbiv_scale_factors)]
        build_dict(samp, 'XBIV_maps', xbiv_scaled)
    return 
