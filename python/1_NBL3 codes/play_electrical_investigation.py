import sys
import matplotlib.pyplot as plt
import seaborn as sns

get_defs = 'work'
### paths for custom defintion files and scans ### change according to the operating system environment
if get_defs == 'work':
    custom_def_path = r'C:\Users\Trumann\Desktop\xrays\python\personal-programs\twalker_defs'
    scan_path = r'C:\Users\Trumann\Desktop\work_data\NBL3\H5 data'
else:
    custom_def_path = '/home/kineticcross/Desktop/xrays/python/personal-programs/twalker_defs' 
    scan_path = '/home/kineticcross/Desktop/data'

sys.path.append(custom_def_path)

import electrical_investigation_defs as eiDefs

NBL3_2 = {'Name': 'NBL3-2', 'areas':['1','2','3'], 'XBIC_scans': [416, 417, 418], 'XBIV_scans': [419,420,421], 
          'beam_conv': [2E5,2E5,2E5], 
          'c_stanford': [5000,5000,5000], 
          'c_lockin':[500,500,500], 
          'v_lockin': [1E3,1E3,1E3]}
NBL3_3 = {'Name': 'NBL3-3', 'areas':['1','2','3'], 'XBIC_scans': [258, 259, 260], 'XBIV_scans': [261,262,263], 
          'beam_conv': [2E5, 2E5, 2E5], 
          'c_stanford': [5000,5000,5000], 
          'c_lockin':[500,500,500], 
          'v_lockin': [1E4,1E4,1E4]}
TS58A = {'Name': 'TS58A', 'areas':['1','2','3'], 'XBIC_scans': [378, 379, 380], 'XBIV_scans': [382,383,384], 
         'beam_conv': [2E5, 2E5, 2E5], 
         'c_stanford': [50,50,50], 
         'c_lockin':[10000,10000,10000], 
         'v_lockin': [1000,1000,1000]}

samples = [TS58A]#, NBL3_3, TS58A]

### these functions import the H5s, build the dictionaries above, and converts XBIC cts to amps
eiDefs.get_add_h5s(samples, scan_path)
eiDefs.get_scan_scalers(samples)
eiDefs.get_and_add_DSIC_channels(samples)
eiDefs.cts_to_amps(samples)
# note after these commands run, the above dictionaries will be much larger than shown, and will contain the electrical maps of interest
    # use 'sample.keys()' to view all the dictionary keys and access the groups of interest

# =============================================================================
# for s in samples:
#     XBIC_maps = s['XBIC_maps']
#     XBIV_maps = s['XBIV_maps']
#     for i, v, a in zip(XBIC_maps, XBIV_maps, s['areas']):
# # =============================================================================
# #         fig1 = plt.figure()
# #         XBIC_arr = i.ravel()
# #         XBIV_arr = v.ravel()
# #         g = sns.jointplot(XBIC_arr, XBIV_arr, kind="reg", color="#5d5d60", scatter_kws={'s':2}, joint_kws={'line_kws':{'color':'red'}})
# #         plt.title(s['Name'] + ' ' + 'joint plot' + a)
# # =============================================================================
#         
#         fig2 = plt.figure()
#         h = sns.heatmap(i, square = True)
#         h.invert_yaxis()
#         plt.title(s['Name'] + ' ' + 'Amp Area ' + a)
#         
#         fig3 = plt.figure()
#         j = sns.heatmap(v, square = True)
#         j.invert_yaxis()
#         plt.title(s['Name'] + ' ' + 'Volt Area ' + a)
#         #plt.show()
# =============================================================================

#g = sns.jointplot(XBIC_1D, XBIV_1D, kind="reg", color="#5d5d60", scatter_kws={'s':2}, joint_kws={'line_kws':{'color':'red'}})
#sns.regplot(XBIC_1D, XBIV_1D, ax=g.ax_joint, scatter=False)
#sns.despine(right = True)


# In [12]: XBIV_h5s[0]['/MAPS/scaler_names'][2] #syntx for access to the files...
# Out[12]: b'ds_ic'
    
# example text from command line to plot hexbins; need 1d arrays; ravel() 'unravels' 2d array to 1d just like MAPS would export ASCII
    # image process to align pixels
    # plot log scale

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
