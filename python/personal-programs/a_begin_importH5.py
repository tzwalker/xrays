import matplotlib.pyplot as plt

get_defs = 'work'

import sys
if get_defs == 'work':
    custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\personal-programs\twalker_defs'
else:
    custom_def_path = '/home/kineticcross/Desktop/xrays/python/personal-programs'

sys.path.append(custom_def_path)

import import_maps_H5
import a_begin_absorb

if get_defs == 'work':
    scan_path = r'C:\Users\Trumann\Desktop\2019_03_2IDD_NBL3\img.dat'
else:
    scan_path = '/home/kineticcross/Desktop/xrays/python/personal-programs'

scans = ['264', '422', '385']
energy = [8.99, 8.99, 8.99]         #keV

### stack structure (UPTREAM LAYER FIRST, DOWNSTREAM LAYER LAST) ###
STACKS = [ ['Mo', 'ZnTe', 'CdTe', 'CdS', 'SnO2'],
         ['Au', 'CdTe', 'CdS', 'SnO2'],
         ['Mo', 'ZnTe', 'CdTe', 'CdS', 'SnO2'] ]

lay_densities = [ [10.2, 6.34, 5.85, 4.82, 6.85],
                 [19.3, 5.85, 4.82, 6.85],
                 [10.2, 6.34, 5.85, 4.82, 6.85] ]

### enter thickness in centimeter of each layer for the sample in each scan ###
# number of items in each of these lists needs to equal number of scans.samples being studied
lay_thicks = [ [500E-7, 375E-7, 4E-4, 80E-7, 100E-7], 
              [500E-7, 375E-7,  5E-4, 80E-7, 100E-7], 
              [500E-7, 375E-7,  6E-4, 80E-7, 100E-7] ]

#files = import_maps_H5.import_h5s(scans, scan_path)


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

#master_map_list = extract_maps(files, master_index_list)

import numpy as np
import stk_info

### beam settings ###
beam_theta = np.sin(90*np.pi/180)                                                     #angle between beam and sample normal
detect_theta = np.sin(47*np.pi/180)                                                   #angle between detector and sample normal

what_will_this_be = stk_info.get_stack_info(STACKS, lay_densities, lay_thicks, energy)





#ChOIs = channels_of_interest
ChOIs = ['Cd_L', 'Te_L', 'Cu']

#master_index_list = import_maps_H5.get_ChOIs_for_all_scans(files, ChOIs)

# =============================================================================
# for scan, en, tm, tz, tcd, #tc, ts in zip(scans, energy, thk_Mok, thk_ZnTe, thk_CdTe, thk_CdS, thk_Sno2):
#     stack_info = stk_info.get_stack#_info(STACK, layer_density, energy)    
#     stack_for_each_sample_list.append(stack_info)
# =============================================================================
    

#Zs = a_begin_absorb.channel_to_atomic_num(ChOIs)

#matched_eles = a_begin_absorb.is_ele_in_layer(stack_info, Zs)



