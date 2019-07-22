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

def extract_norm_ele_maps(sample_dicts, fluxnorm):
    if fluxnorm == 'ds_ic':  # scale data to ds_ic
        fluxnormindex = 0
    elif fluxnorm == 'us_ic': # scale data to us_ic
        fluxnormindex = 1;  
    elif fluxnorm == 'SRcurrent':  # scale data to SRcurrent
        fluxnormindex = 2
    
    for samp in sample_dicts:
        c_ele_maps = []

        for h5, ch_inds in zip(samp['XBIC_h5s'], samp['XBIC_eles_i']):
            scalers = h5['/MAPS/scalers']  # Scaler values for [scaler, x, y] 
            """Select to which flux measurement shall be scaled to"""
            fluxnormmatrix = scalers[1, :, :];  fluxnormmatrix[:, :] = 1  # Matrix of scalers size but all 1 for no normalization
            fluxnormmatrix = scalers[fluxnormindex, :, :]
            
            
            
            maps_of_eles_in_scan = [h5['/MAPS/XRF_fits'][ind,:,:]  for ind in ch_inds]
            c_ele_maps.append(maps_of_eles_in_scan)
        key = 'XBIC_ele_maps'
        samp.setdefault(key, c_ele_maps)
        
        v_ele_maps = []
        for h5, ch_inds in zip(samp['XBIV_h5s'], samp['XBIV_eles_i']):
            maps_of_eles_in_scan = [h5['/MAPS/XRF_fits'][ind,:,:]  for ind in ch_inds]
            v_ele_maps.append(maps_of_eles_in_scan)
        key = 'XBIV_ele_maps'
        samp.setdefault(key, v_ele_maps)
    return 


def apply_ele_iios(sample_dicts):
    for samp in sample_dicts:
        c = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'],ele_set)] for ele_set in samp['XBIC_ele_maps'][0:3]]
        # see list structure comments in psuedo.py to determine how and whether to change line 38
        c2 = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'], samp['XBIC_ele_maps'][3])]]
        scans2 = c+c2
        key = 'XBIC_ele_maps_corr'
        samp.setdefault(key, scans2)
        
        v = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'],ele_set)] for ele_set in samp['XBIV_ele_maps'][0:3]]
        # see list structure comments in psuedo.py to determine how and whether to change line 38
        v2 = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'], samp['XBIV_ele_maps'][3])]]
        scans3 = v+v2
        key = 'XBIV_ele_maps_corr'
        samp.setdefault(key, scans3)

    return


    """Load file and relevant h5 groups"""
    f = h5py.File(fullpath, 'r')
    # f = h5py.File(r"C:\MSdata\postdoc\studies\beamtimes\2017-03 APS 2-ID-D\img.datfit\2idd_0256.h5", 'r')
    # print_MAPS_H5_file_content(f)
    channel_names = f['/MAPS/channel_names']  # Names of fitted channels such as 'Cu', 'TFY', 'La_L'
    scaler_names = f['/MAPS/scaler_names']  # Names of scalers such as 'SRcurrent', 'us_ic', 'ds_ic', 'deadT', 'x_coord'
    scalers = f['/MAPS/scalers']  # Scaler values for [scaler, x, y]
    XRF_fits = f['/MAPS/XRF_fits']  # Quantified channel [channel, x, y]
    XRF_fits_quant = f['/MAPS/XRF_fits_quant']  # Number of cts per ug/cm2 [???, ???, channel]
    XRF_roi = f['/MAPS/XRF_roi']  # Quantified channel [channel, x, y]
    XRF_roi_quant = f['/MAPS/XRF_roi_quant']  # Number of cts per ug/cm2 [???, ???, channel], to be used as sum ROI in maps instead of XRF_fits_quant
    x_axis = f['/MAPS/x_axis']  # x position of pixels  [position in um]
    y_axis = f['/MAPS/y_axis']  # y position of pixels  [position in um]

    """Select to which flux measurement shall be scaled to"""
    fluxnormmatrix = scalers[1, :, :];  fluxnormmatrix[:, :] = 1  # Matrix of scalers size but all 1 for no normalization
    if fluxnorm == 'ds_ic':  # scale data to ds_ic
        fluxnormindex = 0; fluxnormmatrix = scalers[fluxnormindex, :, :]
    elif fluxnorm == 'us_ic':  # scale data to us_ic
        fluxnormindex = 1; fluxnormmatrix = scalers[fluxnormindex, :, :]
    elif fluxmeas == 'SRcurrent':  # scale data to SRcurrent
        fluxnormindex = 2; fluxnormmatrix = scalers[fluxnormindex, :, :]

    """Select XRF element of interest"""
    elementindex = e2i(channel_names, element)

    """Select which fitting to be used for quantification"""
    if fitnorm == 'roi':  # Normalization with fitted data --> is default if fit works fine
        fitnormvalue = XRF_roi_quant[fluxnormindex, 0, elementindex]
        rawmatrix = XRF_roi[elementindex, :, :]
    elif fitnorm == 'fit':  # Normalization with ROI fitted --> To be used when maps creates a problem with the quantification
        fitnormvalue = XRF_fits_quant[fluxnormindex, 0, elementindex]
        rawmatrix = XRF_fits[elementindex, :, :]

    """Calculate quantified element matrix in ug/cm2"""
    m = rawmatrix / fluxnormmatrix / fitnormvalue
    # # t = ds / us  # Transmittance: ds_ic normalized to us_ic