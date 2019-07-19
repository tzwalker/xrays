import h5py

def import_h5s(s, p):
    imported_h5s = []
    for scan in s:
        # add if statement to check between sectors
        filename = '/2idd_0' + scan + '.h5'
        f = h5py.File(p + filename, 'r') # this needs to be an 'r'!!! otherwise the h5s will be overwritten...
        imported_h5s.append(f)
    return imported_h5s

def get_elem_indices(w, chan):
    chan = [x.decode('utf-8') for x in chan]
    index_list = [i for i,ele in enumerate(chan) for e in w if e == ele]
    return index_list

def find_ele_in_h5s(sample_dicts, ChOIs):
    for samp in sample_dicts:
        for file in samp['XBIC_h5s']:
            ch_names = file['/MAPS/channel_names']
            c_indices = get_elem_indices(ChOIs, ch_names)
        # what to do with the element indices...?
            # do i store these outside of the sample dictionary...
            # or would they be more useful somehwere else...?
            # they would definitely be more accessible if they are not in the sample dictionary...
            # if i make list_of_lists as done below, i can call extract_maps()...
        for file in samp['XBIV_h5s']:
            ch_names = file['/MAPS/channel_names']
            v_indices = get_elem_indices(ChOIs, ch_names)    
    
    list_of_indices = []                                            #initialize master list
    for file in enumerate(files):
        channel_names = file['/MAPS/channel_names']                 #navigate to the structure conatining the channel names as element strings, e.g. 'Cd_L'
        decoded_ele_string_indices = []                             #initialize internal list
        for ele in ChOIs:
            s = get_desired_channel_index(channel_names, ele)       #perform string comparison between 'channels of interest' and 'channel names', and extract index of interest
            decoded_ele_string_indices.append(s)                    #build internal list
        list_of_indices.append(decoded_ele_string_indices)          #add internal list (i.e. a scan) to master list 
    return list_of_indices

### older defs; borrow ideas from here ###

# this function uses the element indices from the master_index_list to extract the 2D fitted data arrays from the H5 file
# it also build a master list that contains the 2D numpy arrays of interest, rather than just the indices
def extract_maps(H5s, list_of_lists):
    maps = []                                                       #initialize master list
    for H5, channel_indices in zip(H5s, list_of_lists):
        scan_maps = []                                              #initialize internal (single scan) list
        XRF_fits = H5['/MAPS/XRF_fits']                             #navigate to structure containing all fitted XRF data
        for element_index in channel_indices:
            map_of_interest = XRF_fits[element_index,:,:]           #use element index to extract map of interest
            scan_maps.append(map_of_interest)                       #build internal list
        maps.append(scan_maps)                                      #add internal list (i.e. a scan) to master list
    return maps


#this function performs a strign comparison within the pertinent H5 group and extracts the index of interest
def get_desired_channel_index(H5_channel_names_as_strings, e):
    s=0                                                                             #initialize index search
    for index, channel_string in enumerate(H5_channel_names_as_strings):            #search channel_names for element string
        if e == channel_string.decode():                                            #compare element string to decoded channel_name string
            s = index                                                               #get appropriate index
    return s

#returns list of lists
#each internal list represents a scan, and contains the indices of the channels of interest
#channel indices are required to navigate the H5 data structures
def get_ChOIs_for_all_scans(files, ChOIs):
    list_of_indices = []                                            #initialize master list
    for scan_index, file in enumerate(files):
        channel_names = file['/MAPS/channel_names']                 #navigate to the structure conatining the channel names as element strings, e.g. 'Cd_L'
        decoded_ele_string_indices = []                             #initialize internal list
        for ele in ChOIs:
            s = get_desired_channel_index(channel_names, ele)       #perform string comparison between 'channels of interest' and 'channel names', and extract index of interest
            decoded_ele_string_indices.append(s)                    #build internal list
        list_of_indices.append(decoded_ele_string_indices)          #add internal list (i.e. a scan) to master list
    return list_of_indices
