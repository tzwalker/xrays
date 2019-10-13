get_defs = 'work'

### paths for custom defintions ###
import sys
if get_defs == 'work':
    custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\personal-programs\twalker_defs'
else:
    custom_def_path = '/home/kineticcross/Desktop/xrays/python/personal-programs/tzwalker_defs'

sys.path.append(custom_def_path)

### paths for files and scans ###
import rummage_thru_H5

if get_defs == 'work':
    scan_path = r'C:\Users\Trumann\Desktop\2019_03_2IDD_NBL3\img.dat'
else:
    scan_path = '/home/kineticcross/Desktop/xrays/python/personal-programs'

scans = ['264', '422', '385']
energy = [8.99, 8.99, 8.99]         #keV

### stack structure (UPTREAM LAYER FIRST, DOWNSTREAM LAYER LAST) ###
STACKS = [ ['Mo', 'ZnTe', 'CdTe', 'CdS', 'SnO2'],
         ['Mo', 'ZnTe', 'CdTe', 'CdS', 'SnO2'],
         ['Mo', 'ZnTe', 'CdTe', 'CdS', 'SnO2'] ]

lay_densities = [ [10.2, 6.34, 5.85, 4.82, 6.85],
                 [10.2, 6.34, 5.85, 4.82, 6.85],
                 [10.2, 6.34, 5.85, 4.82, 6.85] ]

### enter thickness in centimeter of each layer for the sample in each scan ###
# number of items in each of these lists needs to equal number of scans.samples being studied
lay_thicks = [ [500E-7, 375E-7, 4E-4, 80E-7, 100E-7], 
              [500E-7, 375E-7, 5E-4, 80E-7, 100E-7], 
              [500E-7, 375E-7, 6E-4, 80E-7, 100E-7] ]

### call these to import raw data ###
#files = rummage_thru_H5.import_h5s(scans, scan_path)
#master_index_list = rummage_thru_H5.get_ChOIs_for_all_scans(files, ChOIs)
#master_map_list = rummage_thru_H5.extract_maps(files, master_index_list)

import numpy as np
import absorb_defs

### beam settings ###
beam_theta = np.sin(90*np.pi/180)                                                     #angle between beam and sample normal
detect_theta = np.sin(47*np.pi/180)                                                   #angle between detector and sample normal

list_of_list_of_layer_dicts = absorb_defs.get_stack_info(STACKS, lay_densities, lay_thicks, energy)

#ChOIs = channels_of_interest
ChOIs = ['Cd_L', 'Te_L', 'Cu']

#print(play_absorb.test_fxn(ChOIs, list_of_list_of_layer_dicts))

#Zs = a_begin_absorb.channel_to_atomic_num(ChOIs)

#matched_eles = a_begin_absorb.is_ele_in_layer(stack_info, Zs)


#import matplotlib.pyplot as plt

