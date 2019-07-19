import sys

get_defs = 'wor'
### paths for custom defintion files and scans ### change according to the operating system environment
if get_defs == 'work':
    custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\testing\twalker_defs'
    scan_path = r'C:\Users\Trumann\Desktop\work_data\NBL3\H5 data'
else:
    custom_def_path = '/home/kineticcross/Desktop/xrays/python/testing/twalker_defs' 
    scan_path = '/home/kineticcross/Desktop/data'

sys.path.append(custom_def_path)

import defs_electrical_investigation as eiDefs
import rummage_thru_H5 as rumH

NBL3_2 = {'Name': 'NBL3-2', 'areas':['1','2','3'], 'XBIC_scans': [422,423,424, 550], 'XBIV_scans': [419,420,421, 551], 
          'beam_conv': [2E5,2E5,2E5, 2E5], 
          'c_stanford': [5000,5000,5000, 50000], 
          'c_lockin':[500,500,500, 100], 
          'v_lockin': [1E3,1E3,1E3, 10000]}
NBL3_3 = {'Name': 'NBL3-3', 'areas':['1','2','3'], 'XBIC_scans': [264, 265, 266, 475], 'XBIV_scans': [261,262,263, 472], 
          'beam_conv': [2E5, 2E5, 2E5, 1E5], 
          'c_stanford': [5000,5000,5000, 200], 
          'c_lockin':[500,500,500, 20], 
          'v_lockin': [1E4,1E4,1E4, 100000]}
TS58A = {'Name': 'TS58A', 'areas':['1','2','3'], 'XBIC_scans': [385, 386, 387, 439], 'XBIV_scans': [382,383,384, 440], 
         'beam_conv': [2E5, 2E5, 2E5, 1E5], 
         'c_stanford': [5000,5000,5000, 200], 
         'c_lockin':[10000,10000,10000, 20], 
         'v_lockin': [1000,1000,1000, 100000]}

samples = [TS58A]#, NBL3_3, TS58A]

### these functions import the H5s, build the dictionaries above, and converts XBIC cts to amps
eiDefs.get_add_h5s(samples, scan_path)
eiDefs.get_scan_scalers(samples)
eiDefs.get_and_add_DSIC_channels(samples)
eiDefs.cts_to_elect(samples)

elements = ['Cu']
# changing defs_Cu_clustering.py --> psuedo.py for use as a test file when variables are loaded
# left off in def: find_ele_in_h5s() in rummage_thru_H5.py
    # see comments in that defintion, notably, put element indices where...?
    # don't forget to test the newer defs find_ele_in_h5s() and get_elem_indices()
        # didn't get the chance because h5 386 and 387 on home laptop were overwritten (didn't include 'r' in h5 import call)

# GOAL: find element channels of interest in all scans

### old notes ###

# note after these commands run, the above dictionaries will be much larger than shown, and will contain the electrical maps of interest
    # use 'sample.keys()' to view all the dictionary keys and access the groups of interest
import matplotlib.pyplot as plt
import seaborn as sns
# =============================================================================
# h5_filename = r'C:\Users\Trumann\Desktop\2017_12_2018_07_NBL3_bacth_refit\img.dat\2idd_0440.h5'
# 
# H5 = h5.File(h5_filename, 'r') #make sure this has 'r', otherwise py modulse will erae contents of file!
# 
# XBIC_name = H5['/MAPS/scaler_names'][2] #index of this identifier will be the same as the index of the desired map
# XBIC_cts = H5['/MAPS/scalers'][2] #actual XBIC map
# =============================================================================

# =============================================================================
# XBIC_scans = [416,417,418,  258,259,260,  378,379,380] #+ [550,549, 475,474, 439,438]
# XBIV_scans = [419,420,421,  261,262,263,  382,383,384] #+ [551,555, 472,473, 440,441]
# =============================================================================
