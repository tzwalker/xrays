get_defs = 'work'
### paths for custom defintion files and scans ### change according to the operating system environment
if get_defs == 'work':
    scan_path = r'C:\Users\Trumann\Desktop\NBL3_data\all_H5s'
else:
    scan_path = '/home/kineticcross/Desktop/data'

import b_h5_in_elect_scale as eiDefs
import c_rummage_thru_H5 as rumH
import d_clustering
import e_statistics

NBL3_2 = {'Name': 'NBL3-2', 'XBIC_scans': [422,423,424, 550], 'XBIV_scans': [419,420,421, 551], 
          'beam_conv': [2E5,2E5,2E5, 2E5], 
          'c_stanford': [5000,5000,5000, 50000], 
          'c_lockin':[500,500,500, 100], 
          'v_lockin': [1E3,1E3,1E3, 10000],
          '2017_12_ele_iios': [0.275, 0.0446, 0.0550],
          '2019_03_ele_iios': [0.104, 0.00131, 0.00418]}
NBL3_3 = {'Name': 'NBL3-3', 'XBIC_scans': [264,265,266, 475], 'XBIV_scans': [261,262,263, 472], 
          'beam_conv': [2E5, 2E5, 2E5, 1E5], 
          'c_stanford': [5000,5000,5000, 200], 
          'c_lockin':[500,500,500, 20], 
          'v_lockin': [1E4,1E4,1E4, 100000],
          '2017_12_ele_iios': [0.296, 0.0488, 0.0604],
          '2019_03_ele_iios': [0.114, 0.00144, 0.00459]}
TS58A = {'Name': 'TS58A', 'XBIC_scans': [385,386,387, 439], 'XBIV_scans': [382,383,384, 440], 
         'beam_conv': [2E5, 2E5, 2E5, 1E5], 
         'c_stanford': [5000,5000,5000, 200], 
         'c_lockin':[10000,10000,10000, 20], 
         'v_lockin': [1000,1000,1000, 100000],
         '2017_12_ele_iios': [0.381, 0.0682, 0.0867],
         '2019_03_ele_iios': [0.162, 0.00209, 0.00669]}

samples = [NBL3_2, NBL3_3, TS58A]

eiDefs.get_add_h5s(samples, scan_path)
eiDefs.get_scan_scalers(samples)
eiDefs.get_add_elect_channel(samples, 2) # USER input: 1 --> us_ic, 2 --> ds_ic
eiDefs.cts_to_elect(samples)

elements_in = ['Cu', 'Cd_L']       # USER input: strings must include element lines, 
                                    # index of the element strings here dictate their positions in all future structures
rumH.find_ele_in_h5s(samples, elements_in)
rumH.extract_norm_ele_maps(samples, 'us_ic', 'roi') # 'roi' --> 'fit' if trouble w/MAPS fit

# now apply XRF correction
# ATTENTION: see ReadME.txt for proper use of apply_ele_iios() below
rumH.apply_ele_iios(samples)

e_statistics.make_stat_arrays(samples)
e_statistics.standardize_channels(samples, ['c_stat_arrs', 'v_stat_arrs'], ['c_stand_arrs', 'v_stand_arrs'])
# use this funciton if you want to remove the pixels of all loaded
    # maps according to bad data in one of the XRF channels
    # not configured for using electrical channels as the bad channel
    # see ReadMe.txt for details
e_statistics.reduce_arrs(samples, 'Cu', elements_in, 3, ['c_stat_arrs', 'v_stat_arrs'])
e_statistics.standardize_channels(samples, ['c_reduced_arrs', 'v_reduced_arrs'], ['c_redStand_arrs', 'v_redStand_arrs'])

# 'perf' is electrical: will be performed for both XBIC and XBIV if entered
    # type 'all' to include all features, that is, the electrical channels and 
cluster_channels = ['perf', 'Cu'] 
cluster_number = 3
# the integer argument in this function is a switch that deetermiens which data to cluster
# 0 --> original data (no NaN), 1 --> standardized data, 
# 2 --> reduced original data, 3 --> reduced standardized data
# switches 1 and 3 are reccomended as they use the standardized data
d_clustering.kclustering(samples, cluster_number, cluster_channels, elements_in, 3)

# use separate programs for plotting




