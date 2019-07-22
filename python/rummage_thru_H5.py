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

def extract_ele_maps(sample_dicts):
    for samp in sample_dicts:
        c_ele_maps = []
        for h5, ch_inds in zip(samp['XBIC_h5s'], samp['XBIC_eles_i']):
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
        # see list structure comments below to determine how and whether to change line 38
        c2 = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'], samp['XBIC_ele_maps'][3])]]
        scans2 = c+c2
        key = 'XBIC_ele_maps_corr'
        samp.setdefault(key, scans2)
        
        v = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'],ele_set)] for ele_set in samp['XBIV_ele_maps'][0:3]]
        # see list structure comments below to determine how and whether to change line 38
        v2 = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'], samp['XBIV_ele_maps'][3])]]
        scans3 = v+v2
        key = 'XBIV_ele_maps_corr'
        samp.setdefault(key, scans3)
## list structure comments ##
# c = [[(ele/iio) for iio,ele in zip(samp['2017_12_ele_iios'],ele_set)] for ele_set in samp['XBIC_ele_maps'][0:3]]
    # this produces list structure: [ [-,-], [-,-], [-,-] ] , len = 3
    
# c2 = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'], samp['XBIC_ele_maps'][3])]]
    # this produces list structure: [ [-,-] ] , len = 1
    # can add to [ [-,-], [-,-], [-,-] ] to make [ [-,-], [-,-], [-,-], [-,-] ]
    # len = 4
    
# c3 = [[(ele/iio) for iio,ele in zip(samp['2019_03_ele_iios'],ele_set)] for ele_set in samp['XBIC_ele_maps'][3]]
    # this produces list structure: [-,-] , len = 2 as samp['XBIC_ele_maps'][3] is only a single item
    # if added to [ [-,-], [-,-], [-,-] ] resulting structure would be [ [-,-], [-,-], [-,-], -,- ] , len = 5

# never use c3; if more than one scan from a separate beamtime is to be processed,
    # change c2 into the form of c, and be sure to slice list according to corresponding positions in sample dict
    return


