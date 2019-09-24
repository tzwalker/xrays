def get_directory(machine_index):
    if machine_index==0: #--> Dell work
        scan_path = r'C:\Users\Trumann\Desktop\NBL3_data\all_H5s'
        def_path = r'C:\Users\Trumann\Desktop\xrays\python'
    elif machine_index==1: #-->ASUS windows
        scan_path = r'C:\Users\triton\Desktop\NBL3_data\all_H5s'
        def_path = r'C:\Users\triton\xrays\python'
    elif machine_index==2: #-->ASUS ubuntu
        scan_path = '/home/kineticcross/Desktop/data'
        def_path = '/home/kineticcross/Desktop/xrays/python'
    return scan_path, def_path

scan_path, def_path = get_directory(0)
    
import sys
sys.path.append(def_path)
from b_import_h5 import get_add_h5s
from b_scale_elect import get_add_electrical
import c_rummage_thru_H5
import d_clustering
import e_statistics
import f_corr_pearsons

NBL3_2 = {'Name': 'NBL3-2', 'XBIC_scans': [422,423,424, 550,538,575], 'XBIV_scans': [419,420,421, 551], # good geom XBIC
          'beam_conv':      [2E5,2E5,2E5, 2E5,2E5,2E5], 
          'c_stanford':     [5000,5000,5000, 50000,50000,50000], 
          'c_lockin':       [500,500,500, 100,100,100], 
          'v_lockin':       [1E3,1E3,1E3, 10000],
          # wrong key decriptor 2017_12_2IDD, but geometry same between the two beamtimes
          '2017_12_ele_iios': [0.275, 0.0446, 0.0550], 
          '2019_03_ele_iios': [0.104, 0.00131, 0.00418]}
NBL3_3 = {'Name': 'NBL3_3', 'XBIC_scans': [264,265,266, 475,491], 'XBIV_scans': [261,262,263, 472], 
          'beam_conv':      [2E5, 2E5, 2E5, 1E5,1E5], 
          'c_stanford':     [5000,5000,5000, 200,200], 
          'c_lockin':       [500,500,500, 20,20], 
          'v_lockin':       [1E4,1E4,1E4, 100000],
          '2017_12_ele_iios': [0.296, 0.0488, 0.0604],
          '2019_03_ele_iios': [0.114, 0.00144, 0.00459]}
TS58A = {'Name': 'TS58A', 'XBIC_scans': [385,386,387, 439,427,404], 'XBIV_scans': [382,383,384, 440], #
         'beam_conv':       [2E5, 2E5, 2E5, 1E5,1E5,1E5], 
         'c_stanford':      [5000,5000,5000, 200,200,200], 
         'c_lockin':        [10000,10000,10000, 20,20,20], 
         # lockin amp almost certainly 10000 for 2019_03_2idd scans 385-387;
         # cross-sample comparison can be made with 500, but this is not how science is done
         'v_lockin':        [1000,1000,1000, 100000],
         '2017_12_ele_iios': [0.381, 0.0682, 0.0867],
         '2019_03_ele_iios': [0.162, 0.00209, 0.00669]}

samples = [NBL3_2, NBL3_3, TS58A]

get_add_h5s(samples, scan_path)
get_add_electrical(samples, 2) # 1: us_ic, 2: ds_ic

# enter elements you want to work with
# index of the element string dictates position future structures
elements = ['Cu', 'Cd_L', 'Te_L', 'Mo_L']        #remove zinc to allow beam to beam comparisons

c_rummage_thru_H5.find_ele_in_h5s(samples, elements)
c_rummage_thru_H5.extract_norm_ele_maps(samples, 'us_ic', 'fit')

# now apply XRF correction
# ATTENTION: see ReadME.txt for proper use of apply_ele_iios() below
#c_rummage_thru_H5.apply_ele_iios(samples)

# note if "IndexError: out of range" is thrown, 
    # make sure length of all the electrical setting dictionary entries match
    # the length of the scans
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

data_key = 'c_reduced_arrs'
channel_for_mask = 0 #column index of channel within stat array of choice (the key used in kmeans_trials())
number_of_clusters = 3
number_of_kmeans_trials = 5
# stores numpy array of 'n' kmeans clustering trials for each scan for each sample
    # for a given scan, array will be 'n'x'len(redStand_arr)'
    # example navigation use: sample_dict['c_kmeans_trials'][scan_num]
d_clustering.kmeans_trials(samples, data_key, channel_for_mask, 
                           number_of_clusters, number_of_kmeans_trials)
samp = NBL3_2
trials_key = 'c_kmeans_trials'
focus_cluster = 'high'
focus_channel = 0
scans = [0,1,2]

d_clustering.correlation_stats(NBL3_2, scans, data_key, trials_key, number_of_clusters, focus_cluster, focus_channel)
z = NBL3_2['c_kcorr_std']