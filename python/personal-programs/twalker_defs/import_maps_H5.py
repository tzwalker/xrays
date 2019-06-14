import h5py as h5

def import_h5s(s, p):
    imported_h5s = []
    for scan in s:
        # add if statement to check between sectors
        
        filename = '/2idd_0' + scan + '.h5'
        f = h5.File(p + filename)
        imported_h5s.append(f)
        
    return imported_h5s


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
