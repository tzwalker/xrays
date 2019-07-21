import sys
get_defs = 'work'
### paths for custom defintion files and scans ### change according to the operating system environment
if get_defs == 'work':
    custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\testing\twalker_defs'
    scan_path = r'C:\Users\Trumann\Desktop\NBL3_data\all_H5s'
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
NBL3_3 = {'Name': 'NBL3-3', 'areas':['1','2','3'], 'XBIC_scans': [264,265,266, 475], 'XBIV_scans': [261,262,263, 472], 
          'beam_conv': [2E5, 2E5, 2E5, 1E5], 
          'c_stanford': [5000,5000,5000, 200], 
          'c_lockin':[500,500,500, 20], 
          'v_lockin': [1E4,1E4,1E4, 100000]}
TS58A = {'Name': 'TS58A', 'areas':['1','2','3'], 'XBIC_scans': [385,386,387, 439], 'XBIV_scans': [382,383,384, 440], 
         'beam_conv': [2E5, 2E5, 2E5, 1E5], 
         'c_stanford': [5000,5000,5000, 200], 
         'c_lockin':[10000,10000,10000, 20], 
         'v_lockin': [1000,1000,1000, 100000]}

samples = [NBL3_2, NBL3_3]#], TS58A]

# import the H5s, build the dictionaries above, and scale the electrical signal accordingly
eiDefs.get_add_h5s(samples, scan_path)
eiDefs.get_scan_scalers(samples)
# in get_add_elect_channel() below: 
    # enter 1 if XBIC/V collected through us_ic
    # enter 2 if XBIC/V collected through ds_ic
# otherwise: see README.txt
eiDefs.get_add_elect_channel(samples, 2)  
eiDefs.cts_to_elect(samples)

elements = ['Cu', 'Cd_L']

# makes top-level dict: keys --> sample name, values --> two lists, one for xbic and one for xbiv
    # list for either xbic or xbiv -->  contains two dictionaries, one for xbic scans, another for xbiv scans
        # bottom-level dictionary: keys --> scan number, values --> list of ele_indices for that scan
# not so sure maintaining split structures (between xbic and xbiv) is necessary, see comments below
ele_indices = rumH.find_ele_in_h5s(samples, elements)


# left off in tzwalker_defs/rummage_thru_H5.py and defs_electrical_investigation.py:
    # if i do keep split structure, leave all functions alone and move unto absorption correction
    # if i do not keep split structure:
        # modify eiDefs.cts_to_elect() to combine XBIC and XBIV maps into one key:value location in master sample dict
        # modify rumH.find_ele_inh5s() back to combining all the scan ele_indices into one list
# maintaining separation pro: plotting XBIC vs. XBIV may be easier...
# maintaining separation con: ele_indices are buried in a complicated structure 
    # that i'll need to work with when applying absorption correction code...
# DO I NEED TO SEPARATE XBIC AND XBIV...? could i use if statements in defs_electrical_investigation.py???
    


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
