get_defs = 'wor'

### paths for custom defintions ###
import sys
if get_defs == 'work':
    custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\personal-programs\twalker_defs'
else:
    custom_def_path = '/home/kineticcross/Desktop/xrays/python/personal-programs/twalker_defs'

sys.path.append(custom_def_path)

### paths for files and scans ### change according to the operating system environment
import import_maps_H5
if get_defs == 'work':
    scan_path = r'C:\Users\Trumann\Desktop\2019_03_2IDD_NBL3\img.dat'
else:
    scan_path = '/home/kineticcross/Desktop/data'

import matplotlib.pyplot as plt


XBIC_scans = [416,417,418,258,259,260,378,379,380] #+ [550,549, 475,474,439,438]
XBIV_scans = [419,420,421,261,262,263,382,383,384] #+ [551,555, 472,473,440,441]

### transform integers in scan list to strings; prep for use in filename strings ###
def str_list(L):
    L = [str(v) for v in L]
    return L
XBIC_scans = str_list(XBIC_scans)
XBIV_scans = str_list(XBIV_scans)

### import h5 files ###
XBIC_h5s = import_maps_H5.import_h5s(XBIC_scans, scan_path)
XBIV_h5s = import_maps_H5.import_h5s(XBIV_scans, scan_path)

for i_file, v_file in zip(XBIC_h5s, XBIV_h5s):
    XBIC_map = i_file['/MAPS/scalers'][2]
    XBIV_map = v_file['/MAPS/scalers'][2]
    plt.hexbin(XBIC_map, XBIV_map)
    plt.show()
# In [12]: XBIV_h5s[0]['/MAPS/scaler_names'][2] #syntx for access to the files...
# Out[12]: b'ds_ic'
    
# example text from command line to plot hexbins; need 1d arrays; ravel() 'unravels' 2d array to 1d just like MAPS would export ASCII
    # image process to align pixels
    # plot log scale
    # 
# =============================================================================
# type(XBIV_h5s[0]['/MAPS/scalers'][2])
# Out[17]: numpy.ndarray
# 
# test_2d_array = XBIV_h5s[0]['/MAPS/scalers'][2]
# 
# test_1d_array = test_2d_array.ravel()
# 
# test_2d_array1 = XBIC_h5s[0]['/MAPS/scalers'][2]
# 
# test_1d_array1 = test_2d_array1.ravel()
# 
# import matplotlib.pyplot as plt
# 
# plt.hexbin(test_1d_array1, test_1d_array)
# Out[23]: <matplotlib.collections.PolyCollection at 0x7fbed04555f8>
# =============================================================================

# =============================================================================
# h5_filename = r'C:\Users\Trumann\Desktop\2017_12_2018_07_NBL3_bacth_refit\img.dat\2idd_0440.h5'
# 
# H5 = h5.File(h5_filename, 'r') #make sure this has 'r', otherwise py modulse will erae contents of file!
# 
# XBIC_name = H5['/MAPS/scaler_names'][2] #index of this identifier will be the same as the index of the desired map
# XBIC_cts = H5['/MAPS/scalers'][2] #actual XBIC map
# =============================================================================
