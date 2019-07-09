get_defs = 'work'

### paths for custom defintions ###
import sys
if get_defs == 'work':
    custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\personal-programs\twalker_defs'
else:
    custom_def_path = '/home/kineticcross/Desktop/xrays/python/personal-programs/tzwalker_defs'

sys.path.append(custom_def_path)

### paths for files and scans ### change according to the operating system environment
import import_maps_H5
if get_defs == 'work':
    scan_path = r'C:\Users\Trumann\Desktop\2019_03_2IDD_NBL3\img.dat'
else:
    scan_path = '/home/kineticcross/Desktop/xrays/python/personal-programs'



XBIC_scans = [416,417,418,258,259,260,378,379,380] + [550, 549, 475,474,439,438]
XBIV_scans = []




XBIC_h5s = import_maps_H5.import_h5s(XBIC_scans, scan_path)

h5_filename = r'C:\Users\Trumann\Desktop\2017_12_2018_07_NBL3_bacth_refit\img.dat\2idd_0440.h5'

H5 = h5.File(h5_filename, 'r') #make sure this has 'r', otherwise py modulse will erae contents of file!

XBIC_name = H5['/MAPS/scaler_names'][2] #index of this identifier will be the same as the index of the desired map
XBIC_cts = H5['/MAPS/scalers'][2] #actual XBIC map