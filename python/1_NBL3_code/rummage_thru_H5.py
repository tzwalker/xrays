def get_elem_indices(wanted_channels, channels_in_scan):
    chan = [c.decode('utf-8') for c in channels_in_scan]
    index_list = [i for i,ele in enumerate(chan) for e in wanted_channels if e == ele]
    return index_list

def find_ele_in_h5s(sample_dicts, ChOIs):
    for samp in sample_dicts:
        c_indices = [get_elem_indices(ChOIs, file['/MAPS/channel_names']) for file in samp['XBIC_h5s']]
        c_ele_indices_key = 'XBIC_eles_i'
        samp.setdefault(c_ele_indices_key, c_indices)
        
        v_indices = [get_elem_indices(ChOIs, file['/MAPS/channel_names']) for file in samp['XBIV_h5s']]
        v_ele_indices_key = 'XBIV_eles_i'
        samp.setdefault(v_ele_indices_key, v_indices)
    return

def extract_norm_ele_maps(sample_dicts, fluxnorm, fitnorm):    
    """Select to which flux measurement shall be scaled to"""
    if fluxnorm == 'ds_ic':  # scale data to ds_ic
        fluxnormindex = 0
    elif fluxnorm == 'us_ic': # scale data to us_ic
        fluxnormindex = 1;  
    elif fluxnorm == 'SRcurrent':  # scale data to SRcurrent
        fluxnormindex = 2
        
    """Select which fitting to be used for quantification"""
    if fitnorm == 'roi':  # Normalization with fitted data --> is default if fit works fine
        fitnormvalue_nav_str = '/MAPS/XRF_roi_quant'
    elif fitnorm == 'fit':  # Normalization with ROI fitted --> To be used when maps creates a problem with the quantification
        fitnormvalue_nav_str = '/MAPS/XRF_fits_quant'
    
    """Begin normalization"""
    for samp in sample_dicts:
        c_ele_maps = []
        for h5, ch_inds in zip(samp['XBIC_h5s'], samp['XBIC_eles_i']):            
            """Calculate quantified element matrix in ug/cm2"""
            maps_of_eles_in_scan = [(h5['/MAPS/XRF_roi'][elementindex, :, :] / h5['/MAPS/scalers'][fluxnormindex, :, :] / h5[fitnormvalue_nav_str][fluxnormindex, 0, elementindex]) for elementindex in ch_inds]
            
            c_ele_maps.append(maps_of_eles_in_scan)
        key = 'eXBIC'
        samp.setdefault(key, c_ele_maps)
                
        v_ele_maps = []
        for h5, ch_inds in zip(samp['XBIV_h5s'], samp['XBIV_eles_i']):
            maps_of_eles_in_scan = [(h5['/MAPS/XRF_roi'][elementindex, :, :] / h5['/MAPS/scalers'][fluxnormindex, :, :] / h5[fitnormvalue_nav_str][fluxnormindex, 0, elementindex]) for elementindex in ch_inds]
            v_ele_maps.append(maps_of_eles_in_scan)
        key = 'eXBIV'
        samp.setdefault(key, v_ele_maps)
    return 


def apply_ele_iios(sample_dicts):
    for samp in sample_dicts:
        c = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'],ele_set)] for ele_set in samp['eXBIC'][0:3]]
        # see list structure comments in psuedo.py to determine how and whether to change line 38
        c2 = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'], samp['eXBIC'][3])]]
        scans2 = c+c2
        key = 'eXBIC_corr'
        samp.setdefault(key, scans2)
        
        v = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'],ele_set)] for ele_set in samp['eXBIV'][0:3]]
        # see list structure comments in psuedo.py to determine how and whether to change line 38
        v2 = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'], samp['eXBIV'][3])]]
        scans3 = v+v2
        key = 'eXBIV_corr'
        samp.setdefault(key, scans3)

    return

