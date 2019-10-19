import sys

def get_directory(machine_index):
    if machine_index==0: #--> Dell work
        scan_path = r'C:\Users\Trumann\Desktop\NBL3_data\all_H5s'
        def_path = r'C:\Users\Trumann\Desktop\xrays\python'
    elif machine_index==1: #-->ASUS windows
        scan_path = r'C:\Users\triton\Desktop\NBL3_data'
        def_path = r'C:\Users\triton\xrays\python'
    elif machine_index==2: #-->ASUS ubuntu
        scan_path = '/home/kineticcross/Desktop/data'
        def_path = '/home/kineticcross/Desktop/xrays/python'
    return scan_path, def_path

# 0=Dell work, 1=ASUS windows, 2=ASUS ubuntu
scan_path, def_path = get_directory(2)
sys.path.append(def_path)
import home_defs

NBL3_2 = {'Name': 'NBL3_2', 
          'XBIC_scans':     [422,423,424,  # 2019_03
                             550,538,575], # 2019_12
          'beam_conv':      [2E5,2E5,2E5, 
                             2E5,2E5,2E5], 
          'c_stanford':     [5000,5000,5000, 
                             50000,50000,50000], 
          'c_lockin':       [500,500,500, 
                             100,100,100], 
          'XBIV_scans':     [419,420,421,   # 2019_03
                             551],          # 2017_12 
          'v_lockin':       [1E3,1E3,1E3, 
                             10000],
         # in 'STACK': 
             # first number=compound density (g/cm3), 
             # second number=layer thickness (cm)
          'STACK': {'Mo':[10.2, 500E-7], 'ZnTe':[6.34, 375E-7], 'Cu':[8.96, 2.5E-7], 'CdTe':[5.85, 8.52E-4], 'CdS':[4.82, 80E-7], 'SnO2':[100E-7]}
          }
NBL3_3 = {'Name': 'NBL3_3', 
          'XBIC_scans':     [264,265,266, 
                             475,491],  
          'beam_conv':      [2E5, 2E5, 2E5, 
                             1E5,1E5], 
          'c_stanford':     [5000,5000,5000, 
                             200,200], 
          'c_lockin':       [500,500,500, 
                             20,20], 
          'XBIV_scans':     [261,262,263, 
                             472],
          'v_lockin':       [1E4,1E4,1E4, 
                             100000],
          'STACK': {'Mo':[10.2, 500E-7], 'ZnTe':[6.34, 375E-7],'Cu':[8.96, 10E-7], 'CdTe':[5.85, 10.85E-4], 'CdS':[4.82, 80E-7], 'SnO2':[100E-7]}
          }
TS58A = {'Name': 'TS58A', 
         'XBIC_scans':     [385,386,387, 
                            439,427,404],  
         'beam_conv':       [2E5, 2E5, 2E5, 
                             1E5,1E5,1E5], #(cts/s /V)
         'c_stanford':      [5000,5000,5000, 
                             200,200,200], #(nA/V)
         'c_lockin':        [10000,10000,10000, 
                             20,20,20], #(V/V)
         # lockin scale almost certainly 10000 for 2019_03_2idd scans 385-387;
         'XBIV_scans':      [382,383,384, 
                             440],
         'v_lockin':        [1000,1000,1000, 
                             100000],
         'STACK': {'Mo':[10.2, 500E-7], 'ZnTe':[6.34, 375E-7], 'Cu':[8.96, 2.5E-7], 'CdTe':[5.85, 5.35E-4], 'CdS':[4.82, 80E-7], 'SnO2':[100E-7]}
         }

samples = [NBL3_2, NBL3_3, TS58A]

home_defs.import_h5s(samples, scan_path)
elements = ['Cu', 'Cd_L', 'Te_L', 'Mo_L']
# sample_list, scans_to_import, electrical_channel, element_list, XRF_normalization, XRF_quantification
    # electrical_channel: 1=ds_ic, 2=us_ic, 3=SRCurrent
    # XRF_normalization: us_ic or ds_ic
    # XRF_quantification: fit or roi
home_defs.import_maps(samples, 'XBIC', 2, elements, 'us_ic', 'fit')
home_defs.import_maps(samples, 'XBIV', 2, elements, 'us_ic', 'fit')

import home_abs
iio_layer = 'CdTe'
iio_elements = ['Cu', 'Cd', 'Te'] # enter in same order as seen in 'elements'
# in case you typed in the elements out of position
ele_map_idxs = [1,2,3] #--> index of element in 'elements'
ele_iio_idxs = [0,1,2] #--> index of element in 'iio_elements'

### 2019_03 beamtime
beam_settings0 = {'beamtime': '2019_03','beam_energy': 12.7, 'beam_theta':75, 'detect_theta':15}
home_abs.get_layer_iios(samples, iio_elements, beam_settings0, iio_layer) 
# enter index of scans you want to correct for each sample
sample_scan_idxs=[[0,1,2], [0,1,2], [0,1,2]] 
home_abs.apply_iios(samples, 'XBIC', sample_scan_idxs, '2019_03_iios', ele_map_idxs, ele_iio_idxs) #--> correct current scans from 2019_03
sample_scan_idxs=[[0,1,2], [0,1,2], [0,1,2]] 
home_abs.apply_iios(samples, 'XBIV', sample_scan_idxs, '2019_03_iios', ele_map_idxs, ele_iio_idxs) #--> correct voltage scans from 2019_03

### 2017_12 beamtime
beam_settings1 = {'beamtime': '2017_12','beam_energy': 8.99, 'beam_theta':90, 'detect_theta':43}
home_abs.get_layer_iios(samples, iio_elements, beam_settings1, iio_layer)
# enter index of scans you want to correct for each sample
sample_scan_idxs=[[3,4,5], [3,4], [3,4,5]] 
home_abs.apply_iios(samples, 'XBIC', sample_scan_idxs, '2017_12_iios', ele_map_idxs, ele_iio_idxs) #--> correct current scans from 2017_12
sample_scan_idxs=[[3], [3], [3]]
home_abs.apply_iios(samples, 'XBIV', sample_scan_idxs, '2017_12_iios', ele_map_idxs, ele_iio_idxs) #--> correct voltage scans from 2017_12

# see dictionary growth; clean workspace
del(sample_scan_idxs, ele_map_idxs, ele_iio_idxs)

# combine corrected maps
home_abs.join_corrected_beamtimes(samples, ['XBIC2019_03_corr', 'XBIC2017_12_corr'], ['XBIV2019_03_corr', 'XBIV2017_12_corr'])
#print(samples[0].keys())

# clean dictionaries (optional)
home_abs.clean_dictionaries(samples, '2019_03_corr')
home_abs.clean_dictionaries(samples, '2017_12_corr')
print(samples[0].keys())

#%%
import e_statistics

e_statistics.make_stat_arrays(samples, 
                              ['elXBIC', 'elXBIV'],                     # reference data
                              ['c_stat_arrs', 'v_stat_arrs'])           # new data
e_statistics.standardize_channels(samples, 
                                  ['c_stat_arrs', 'v_stat_arrs'],       # reference data
                                  ['c_stand_arrs', 'v_stand_arrs'])     # new data


## preparation for clustering ###
# use this funciton if you want to remove the pixels of all loaded
    # maps according to bad data in one of the XRF channels
    # not configured for using electrical channels as the bad channel
    # see ReadMe.txt for details
e_statistics.reduce_arrs_actual(samples, 'Cu', elements, 3,             # int = # of std
                         ['c_stat_arrs', 'v_stat_arrs'],                # reference data
                         ['c_reduced_arrs', 'v_reduced_arrs'])          # new data


e_statistics.standardize_channels(samples, 
                                  ['c_reduced_arrs', 'v_reduced_arrs'], 
                                  ['c_redStand_arrs', 'v_redStand_arrs'])
#%%
import d_clustering
## clustering trials ##
data_key = 'c_reduced_arrs'
channel_for_mask = 0 # column index of channel within stat array of choice (the key used in kmeans_trials())
number_of_clusters = 3
number_of_kmeans_trials = 5
# stores numpy array of 'n' kmeans clustering trials for each scan for each sample
    # for a given scan, array will be 'n'x'len(redStand_arr)'
    # example navigation use: sample_dict['c_kmeans_trials'][scan_num]
d_clustering.kmeans_trials(samples, data_key, channel_for_mask, 
                           number_of_clusters, number_of_kmeans_trials, 'kmeans_trials')


