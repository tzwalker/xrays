import sys
import matplotlib.pyplot as plt
import seaborn as sns

get_defs = 'work'
### paths for custom defintion files and scans ### change according to the operating system environment
if get_defs == 'work':
    custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\personal-programs\twalker_defs'
    scan_path = r'C:\Users\Trumann\Desktop\2019_03_2IDD_NBL3\img.dat'
else:
    custom_def_path = '/home/kineticcross/Desktop/xrays/python/personal-programs/twalker_defs' 
    scan_path = '/home/kineticcross/Desktop/data'

sys.path.append(custom_def_path)
import import_maps_H5

def str_list(L):
    ### transform integers in scan list to strings; prep for use in filename strings ###
    L = [str(v) for v in L]
    return L

def get_add_h5s(samps):
    for s in samps:
        ### change scan integers to strings ###
        s['XBIC_scans'] = str_list(s['XBIC_scans'])
        s['XBIV_scans'] = str_list(s['XBIV_scans'])
        ### import h5 files ###
        XBIC_h5s = import_maps_H5.import_h5s(s['XBIC_scans'], scan_path)
        XBIV_h5s = import_maps_H5.import_h5s(s['XBIV_scans'], scan_path)
        key = 'XBIC_h5s'
        s.setdefault(key, XBIC_h5s)
        key = 'XBIV_h5s'
        s.setdefault(key, XBIV_h5s)
    return

def get_scan_scalers(samps):
    for s in samps:
        C_scale = [stan / (bc * lock) for stan,bc,lock in zip(s['c_stanford'], s['beam_conv'], s['c_lockin'])]
        key = 'c_scaler'
        s.setdefault(key, C_scale)
        V_scale = [1 / (bc * lock) for bc,lock in zip(s['beam_conv'], s['c_lockin'])]
        key = 'v_scaler'
        s.setdefault(key, V_scale)
    return

NBL3_2 = {'Name': 'NBL3-2', 'XBIC_scans': [416, 417, 418], 'XBIV_scans': [419,420,421], 
          'beam_conv': [2E5,2E5,2E5], 'c_stanford': [5E4,5E4,5E4], 'c_lockin':[500,500,500], 'v_lockin': [1E3,1E3,1E3]}
NBL3_3 = {'Name': 'NBL3-3', 'XBIC_scans': [258, 259, 260], 'XBIV_scans': [261,262,263], 
          'beam_conv': [2E5, 2E5, 2E5], 'c_stanford': [5E3,5E3,5E3], 'c_lockin':[500,500,500], 'v_lockin': [1E4,1E4,1E4]}
TS58A = {'Name': 'TS58A', 'XBIC_scans': [378, 379, 380], 'XBIV_scans': [382,383,384], 
         'beam_conv': [2E5, 2E5, 2E5], 'c_stanford': [50,50,50], 'c_lockin':[1E4,1E4,1E4], 'v_lockin': [1E4,1E4,1E4]}

samples = [NBL3_2, NBL3_3, TS58A]

get_add_h5s(samples)

get_scan_scalers(samples)


# =============================================================================
# joint_plots = []
# for i_file, v_file in zip(XBIC_h5s, XBIV_h5s):
#     XBIC_map = i_file['/MAPS/scalers'][2]
#     XBIV_map = v_file['/MAPS/scalers'][2]
#     XBIC_arr = XBIC_map.ravel()
#     XBIV_arr = XBIV_map.ravel()
#     g = sns.jointplot(XBIC_arr, XBIV_arr, kind="reg", color="#5d5d60", scatter_kws={'s':2}, joint_kws={'line_kws':{'color':'red'}})
#     #plt.hexbin(XBIC_map, XBIV_map)
#     #plt.show()
# 
# 
# 
# XBIV_2D = XBIV_h5s[0]['/MAPS/scalers'][2]
# XBIC_2D = XBIC_h5s[0]['/MAPS/scalers'][2]
# 
# XBIV_1D = XBIV_2D.ravel()
# XBIC_1D = XBIC_2D.ravel()
# 
# g = sns.jointplot(XBIC_1D, XBIV_1D, kind="reg", color="#5d5d60", scatter_kws={'s':2}, joint_kws={'line_kws':{'color':'red'}})
# #sns.regplot(XBIC_1D, XBIV_1D, ax=g.ax_joint, scatter=False)
# #sns.despine(right = True)
# =============================================================================


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

# =============================================================================
# XBIC_scans = [416,417,418,  258,259,260,  378,379,380] #+ [550,549, 475,474,439,438]
# XBIV_scans = [419,420,421,  261,262,263,  382,383,384] #+ [551,555, 472,473,440,441]
# =============================================================================
