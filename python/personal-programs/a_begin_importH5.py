import matplotlib.pyplot as plt

import sys
custom_def_path = '/home/kineticcross/Desktop/xrays/python/personal-programs/twalker_defs'
sys.path.append(custom_def_path)

import import_maps_H5
import a_begin_absorb

scan_path = '/home/kineticcross/Desktop/xrays/python/personal-programs'

scans = ['264', '422', '385']

files = import_maps_H5.import_h5s(scans, scan_path)

#ChOIs = channels_of_interest
ChOIs = ['Cd_L', 'Te_L', 'Cu']

master_index_list = import_maps_H5.get_ChOIs_for_all_scans(files, ChOIs)

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
beam_theta = np.sin(90*np.pi/180)                                                     #angle between beam and sample normal
detect_theta = np.sin(47*np.pi/180)                                                   #angle between detector and sample normal

### stack structure (UPTREAM LAYER FIRST, DOWNSTREAM LAYER LAST) ###
STACK = ['Mo', 'ZnTe', 'CdTe', 'CdS', 'SnO2']
layer_density = [10.2, 6.34, 5.85, 4.82, 6.85]
#layer_thick = []

stack_info = a_begin_absorb.get_stack_info(STACK, layer_density, beam_energy)

Zs = a_begin_absorb.channel_to_atomic_num(ChOIs)

matched_eles = a_begin_absorb.is_ele_in_layer(stack_info, Zs)



