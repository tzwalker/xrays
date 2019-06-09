import h5py as h5
import matplotlib.pyplot as plt
import a_begin_absorb

path = '/home/kineticcross/Desktop/xrays/python/personal-programs'

scans = ['264', '422', '385']

def import_h5s(scans):
    imported_h5s = []
    for scan in scans:
        filename = '/2idd_0' + scan + '.h5'
        f = h5.File(path + filename)
        imported_h5s.append(f)
        
    return imported_h5s

files = import_h5s(scans)

#this function performs a strign comparison within the pertinent H5 group and extracts the index of interest
def get_desired_channel_index(H5_channel_names_as_strings, e):
    s=0                                                                             #initialize index search
    for index, channel_string in enumerate(H5_channel_names_as_strings):            #search channel_names for element string
        if e == channel_string.decode():                                            #compare element string to decoded channel_name string
            s = index                                                               #get appropriate index
    return s

#ChOIs = channels_of_interest
ChOIs = ['Cd_L', 'Te_L', 'Cu']

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
    

master_index_list = get_ChOIs_for_all_scans(files, ChOIs)

#this function uses the element indices from the master_index_list to extract the 2D fitted data arrays from the H5 file
#it also build a master list that contains the 2D numpy arrays of interest, rather than just the indices
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

master_map_list = extract_maps(files, master_index_list)

import numpy as np

### beam settings ###
beam_energy = 8.99                                                  #keV
beam_theta = 90                                                     #angle between beam and sample normal
detect_theta = 47                                                   #angle between detector and sample normal
beam_geometry = np.sin(beam_theta*np.pi/180)                        #convert to radians
detect_gemoetry = np.sin(detect_theta*np.pi/180)                    #convert to radians

### stack structure (UPTREAM LAYER FIRST, DOWNSTREAM LAYER LAST) ###
STACK = ['Mo', 'ZnTe', 'CdTe', 'CdS', 'SnO2']
layer_density = [10.2, 6.34, 5.85, 4.82, 6.85]
layer_thick = []

stack_info = a_begin_absorb.get_stack_info(STACK, layer_density, beam_energy)
