### NOTES: b_h5_in_elect_scale.py ###
# finding elements in h5
wanted =        ['cu', 'cd', 'te']
h5_channels =   ['cd', 'fe', 'cu', 'zn', 'se', 'te']
h5_channels = [x.encode('utf-8') for x in h5_channels]

def find_eles_in_channel_names(w, chan):
    chan = [x.decode('utf-8') for x in chan]
    index_list = [i for i,ele in enumerate(chan) for e in w if e == ele]
    return index_list

new_list = find_eles_in_channel_names(wanted, h5_channels)

# adding elements to sample dictionary
list_of_lists = NBL3_2['XBIC_eles']
h5s = NBL3_2['XBIC_h5s']

def extract_maps(H5s, list_of_lists):
    maps = []                                                       #initialize master list
    for H5, channel_indices in zip(H5s, list_of_lists):
        scan_maps = []                                              #initialize internal (single scan) list
        XRF_fits = H5['/MAPS/XRF_fits']                             #navigate to structure containing all fitted XRF data
        for element_index in channel_indices:
            map_of_interest = XRF_fits[element_index,:,:]           #use element index to extract map of interest
            scan_maps.append(map_of_interest)                       #build internal list
    maps.append(scan_maps)                                      #add internal list (i.e. a scan) to master list
    return 

list_of_maps = extract_maps(h5s, list_of_lists)

sample_dict = NBL3_2
sample_maps = []
for h5, ch_inds in zip(sample_dict['XBIC_h5s'], sample_dict['XBIC_eles_i']):
    maps_of_eles_in_scan = [h5['/MAPS/XRF_fits'][ind,:,:]  for ind in ch_inds]
    sample_maps.append(maps_of_eles_in_scan)
key = 'test_ele_maps'
sample_dict.setdefault(key, sample_maps)