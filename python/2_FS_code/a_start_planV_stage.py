get_defs = 'work'
### paths for custom defintion files and scans ### change according to the operating system environment
if get_defs == 'work':
    scan_path = r'C:\Users\Trumann\Desktop\FS_data\FS3_2019_06_2IDD_stage'
    def_path = r'C:\Users\Trumann\Desktop\xrays\python'
else:
    scan_path = '/home/kineticcross/Desktop/data'
    def_path = '/home/kineticcross/Desktop/xrays/python'


import sys
sys.path.append(def_path)
import b_h5_in_elect_scale as eiDefs
import c_rummage_thru_H5 as rumH
#import d_clustering
#import e_statistics

FS3 = {'Name': 'Plan View FS3', 'XBIC_scans': [323,327,332,339,340,344], 'XBIV_scans': [321,325], 
          'beam_conv':  [2E5,2E5,2E5,2E5,2E5,2E5], 
          'c_stanford': [1E4,1E4,1E4,1E4,1E4,1E4], 
          'c_lockin':   [500,500,500,500,500,500], 
          'v_lockin':   [100,100],
          'ele_iios': []}

samples = [FS3]

eiDefs.get_add_h5s(samples, scan_path)
eiDefs.get_scan_scalers(samples)
eiDefs.get_add_elect_channel(samples, 1) # us_ic: 1, ds_ic: 2
eiDefs.cts_to_elect(samples)

elements_in = ['Se', 'Cd_L', 'Te_L']       # USER input: strings must include element lines, 
                                    # index of the element strings here dictate their positions in all future structures
rumH.find_ele_in_h5s(samples, elements_in)
rumH.extract_norm_ele_maps(samples, 'us_ic', 'roi') # 'roi' --> 'fit' if trouble w/MAPS fit

# =============================================================================
# # now apply XRF correction
# # ATTENTION: see ReadME.txt for proper use of apply_ele_iios() below
# rumH.apply_ele_iios(samples)
# 
# e_statistics.make_stat_arrays(samples)
# e_statistics.standardize_channels(samples, ['c_stat_arrs', 'v_stat_arrs'], ['c_stand_arrs', 'v_stand_arrs'])
# # use this funciton if you want to remove the pixels of all loaded
#     # maps according to bad data in one of the XRF channels
#     # not configured for using electrical channels as the bad channel
#     # see ReadMe.txt for details
# e_statistics.reduce_arrs(samples, 'Cu', elements_in, 3, ['c_stat_arrs', 'v_stat_arrs'])
# e_statistics.standardize_channels(samples, ['c_reduced_arrs', 'v_reduced_arrs'], ['c_redStand_arrs', 'v_redStand_arrs'])
# 
# # 'perf' is electrical: will be performed for both XBIC and XBIV if entered
#     # type 'all' to include all features, that is, the electrical channels and 
# cluster_channels = ['perf', 'Cu'] 
# cluster_number = 3
# # the integer argument in this function is a switch that deetermiens which data to cluster
# # 0 --> original data (no NaN), 1 --> standardized data, 
# # 2 --> reduced original data, 3 --> reduced standardized data
# # switches 1 and 3 are reccomended as they use the standardized data
# d_clustering.kclustering(samples, cluster_number, cluster_channels, elements_in, 3)
# 
# # use separate programs for plotting
# =============================================================================




