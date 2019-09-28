import samp_dict_grow

def get_ele_idxs(user_channels, channels_in_scan):
    decoded_chs = [chan.decode('utf-8') for chan in channels_in_scan]
    index_list = [i for user_ch in user_channels for i,decoded_ch in enumerate(decoded_chs)  if user_ch == decoded_ch]
    return index_list

def find_ele_in_h5s(sample_dicts, ChOIs):
    for samp in sample_dicts:
        c_indices = [get_ele_idxs(ChOIs, file['/MAPS/channel_names']) for file in samp['XBIC_h5s']]
        c_ele_indices_key = 'XBIC_eles_i'
        samp.setdefault(c_ele_indices_key, c_indices)
        
        v_indices = [get_ele_idxs(ChOIs, file['/MAPS/channel_names']) for file in samp['XBIV_h5s']]
        v_ele_indices_key = 'XBIV_eles_i'
        samp.setdefault(v_ele_indices_key, v_indices)
    return

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


def extract_norm_ele_maps(sample_dicts, fluxnorm, fitnorm):
    flxnorm_idx, nav_keys = get_normalization_keys(fluxnorm, fitnorm)
    for samp in sample_dicts:
        c_ele_maps = []
        for h5, ch_inds in zip(samp['XBIC_h5s'], samp['XBIC_eles_i']):            
            """Calculate quantified element matrix in ug/cm2"""
            maps_of_eles_in_scan = [(h5[nav_keys[0]][elementindex, :, :] / h5['/MAPS/scalers'][flxnorm_idx, :, :] / 
                                     h5[nav_keys[1]][flxnorm_idx, 0, elementindex]) for elementindex in ch_inds]
            c_ele_maps.append(maps_of_eles_in_scan)
        samp_dict_grow.build_dict(samp, 'elXBIC', c_ele_maps)
        v_ele_maps = []
        for h5, ch_inds in zip(samp['XBIV_h5s'], samp['XBIV_eles_i']):
            maps_of_eles_in_scan = [(h5[nav_keys[0]][elementindex, :, :] / h5['/MAPS/scalers'][flxnorm_idx, :, :] / 
                                     h5[nav_keys[1]][flxnorm_idx, 0, elementindex]) for elementindex in ch_inds]
            v_ele_maps.append(maps_of_eles_in_scan)
        samp_dict_grow.build_dict(samp, 'elXBIV', v_ele_maps)
    return 

def apply_ele_iios(sample_dicts):
    for samp in sample_dicts:
        c = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'],ele_set)] for ele_set in samp['elXBIC'][0:3]]
        # see list structure comments in psuedo.py to determine how and whether to change line 38
        c2 = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'], samp['elXBIC'][3])]]
        scans2 = c+c2
        key = 'elXBIC_corr'
        samp.setdefault(key, scans2)
        
        v = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'],ele_set)] for ele_set in samp['elXBIV'][0:3]]
        # see list structure comments in psuedo.py to determine how and whether to change line 38
        v2 = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'], samp['elXBIV'][3])]]
        scans3 = v+v2
        key = 'elXBIV_corr'
        samp.setdefault(key, scans3)

    return

