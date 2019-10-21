# enter the path to the folder where the H5 files are stored
scan_path = r'C:\Users\Trumann\Desktop\NBL3_data\all_H5s'
# enter the path to the folder containing custom definitions a-c,e
custom_definition_path = r'C:\Users\Trumann\Desktop\xrays\python'

import sys
sys.path.append(custom_definition_path) # get custom definitons
# standard preamble
from b_import_h5 import get_add_h5s
from b_scale_elect import get_add_electrical
import c_rummage_thru_H5
import e_statistics

# sample dictionary (REVIEW: https://www.tutorialspoint.com/python/python_dictionary.htm)
  # these electrical settings would be taken from the runnnotes
  # the setting for a given scan should match the position of the scan
      # example XBIC scan 422 electrical settings: 
        # beam_conv (V2F converter) =       2E5 cts/V
        # stanford pre-amplifier (nA) =     5000 nA/V
        # lock-in scale =                   500 V/V
      # example XBIV scan 419 electrical settings:
        # beam_conv (V2F converter) =       2E5 cts/V
        # lock-in scale =                   1E3 V/V
    
NBL3_2 = {'Name': 'NBL3-2', 
'XBIC_scans': [422, 538, 550], 
'XBIV_scans': [419, 551],
'beam_conv':      [2E5, 2E5, 2E5],      # equal to XBIC scan length
'c_stanford':     [5000, 5E4, 5E4],     # equal to XBIC scan length
'c_lockin':       [500, 100, 100],      # equal to XBIC scan length
'v_lockin':       [1000, 10000]}        # equal to XBIV scan length

# list of sample dictionaries (usually there would be more than one here)
samples = [NBL3_2]

# all of the following functions
# adds entries (i.e. 'keys') to the sample dictionaries in 'samples'
# these keys contain the data structures that are used in subsequent processing
# more than one sample_dict can be included in the list 'samples'
    # but is must match the same structure as the example NBL3_2 dict above
# an example of how to access specific data will be given at the end of the file

# imports h5 files
get_add_h5s(samples, scan_path)
# h5 files accessed through dict keys: 'XBIC_h5s', 'XBIV_h5s'

# extracts and converts electrical channel from the scaler used at the beam: 
  #1: us_ic, 2: ds_ic
  # do not change for now; it would change depending on how h5 was fit
get_add_electrical(samples, 2) 
# electrical data accessed through dict keys: 'XBIC_maps', 'XBIV_maps'

# enter elements you want to work with (must include the XRF lines)
elements = ['Cu', 'Cd_L', 'Te_L', 'Mo_L']

# extract fitted XRF channels of interest
c_rummage_thru_H5.find_ele_in_h5s(samples, elements)
c_rummage_thru_H5.extract_norm_ele_maps(samples, 'us_ic', 'fit')
# electrical data accessed through dict keys: 'elXBIC', 'elXBIV'
# Note: for your practice, no re-absorption correction is applied
    # i'm still working out the bugs here
    
# If "IndexError: out of range" is thrown, 
    # make sure length of electrical settings match length of scans
    
# reshape data for use in statistics
    # converts from 2D form to NxM form:
        # N --> number of pixels in the map
        # M --> number of elements extracted + 1 (electrical channel)
# reshaped original data
e_statistics.make_stat_arrays(samples, 
                              ['elXBIC', 'elXBIV'],                     # reference data keys
                              ['c_stat_arrs', 'v_stat_arrs'])           # new data keys
# stat data accessed through dict keys: 'c_stat_arrs', 'v_stat_arrs'

# reshaped standardized data
e_statistics.standardize_channels(samples, 
                                  ['c_stat_arrs', 'v_stat_arrs'],       # reference data keys
                                  ['c_stand_arrs', 'v_stand_arrs'])     # new data keys

# stat data accessed through dict keys: 'c_stand_arrs', 'v_stand_arrs'

### all data at this point is stored in the sample dictionary
# a structure within the dictionary is first accessed by key, 
# then by index
# data indices are determined by the order in which
    # the user inputs scans and elements

# general list syntax: sample_dict[map_key][scan_index][element_index] 

# it might be useful to see the structure shape evolve as you go deeper into
# the sample dict:
xbic_maps_of_all_scans_of_NBL3_2 = NBL3_2['XBIC_maps']
xbic_map_of_1st_scan_of_NBL3_2 = NBL3_2['XBIC_maps'][0]
xbic_map_of_2nd_scan_of_NBL3_2 = NBL3_2['XBIC_maps'][1]
Cu_map_of_2nd_scan_of_NBL3_2 = NBL3_2['elXBIC'][1][0]
Cd_L_map_of_2nd_scan_of_NBL3_2 = NBL3_2['elXBIC'][1][1]
# note to access the element maps, a different key is required,
    # and an additional index is required
    # the first index is the scan index
    # the second index is the element index

# each of the above data structures has an analog in the arrayed format
    # e.g. the statistical arrays 
# these array use Numpy for efficiency, which makes their syntax a bit different
    # REVIEW: https://docs.scipy.org/doc/numpy/user/basics.indexing.html

# general stat_array syntax: sample_dict[stat_array_key][scan_index][array_ROWS, array_COLUMNS]
    
# rows --> number of pixels in the map
# columns --> number of elements extracted + 1 (electrical channel)
# column 0 is always the electrical channel

all_data_from_1st_scan_of_NBL3_2 = NBL3_2['c_stat_arrs'][0]
xbic_arr_of_1st_scan_of_NBL3_2 = NBL3_2['c_stat_arrs'][0][:,0]
xbic_arr_of_2nd_scan_of_NBL3_2 = NBL3_2['c_stat_arrs'][1][:,0]
Cu_arr_of_2nd_scan_of_NBL3_2 = NBL3_2['c_stat_arrs'][1][:,1]
Cd_L_arr_of_2nd_scan_of_NBL3_2 = NBL3_2['c_stat_arrs'][1][:,2]


