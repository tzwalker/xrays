import sys
import home_defs

# 0=Dell work, 1=ASUS windows, 2=ASUS ubuntu
scan_path, def_path = home_defs.get_directory(1)
sys.path.append(def_path)

NBL3_2 = {'Name': 'NBL3-2', 'XBIC_scans': [422,423,424, 550,538,575], 'XBIV_scans': [419,420,421, 551], # good geom XBIC
          'beam_conv':      [2E5,2E5,2E5, 2E5,2E5,2E5], 
          'c_stanford':     [5000,5000,5000, 50000,50000,50000], 
          'c_lockin':       [500,500,500, 100,100,100], 
          'v_lockin':       [1E3,1E3,1E3, 10000],
          'STACK': {'Mo':[10.2, 500E-7], 'ZnTe':[6.34, 375E-7], 'CdTe':[5.85, 8.52E-4], 'CdS':[4.82, 80E-7], 'SnO2':[100E-7]},
          # wrong key decriptor 2017_12_2IDD, but geometry same between the two beamtimes
          '2017_12_ele_iios': [0.275, 0.0446, 0.0550], 
          '2019_03_ele_iios': [0.104, 0.00131, 0.00418]}
NBL3_3 = {'Name': 'NBL3_3', 'XBIC_scans': [264,265,266, 475,491], 'XBIV_scans': [261,262,263, 472], 
          'beam_conv':      [2E5, 2E5, 2E5, 1E5,1E5], 
          'c_stanford':     [5000,5000,5000, 200,200], 
          'c_lockin':       [500,500,500, 20,20], 
          'STACK': {'Mo':[10.2, 500E-7], 'ZnTe':[6.34, 375E-7], 'CdTe':[5.85, 10.85E-4], 'CdS':[4.82, 80E-7], 'SnO2':[100E-7]},
          'v_lockin':       [1E4,1E4,1E4, 100000],
          '2017_12_ele_iios': [0.296, 0.0488, 0.0604],
          '2019_03_ele_iios': [0.114, 0.00144, 0.00459]}
TS58A = {'Name': 'TS58A', 'XBIC_scans': [385,386,387, 439,427,404], 'XBIV_scans': [382,383,384, 440], 
         'beam_conv':       [2E5, 2E5, 2E5, 1E5,1E5,1E5], #(cts/s /V)
         'c_stanford':      [5000,5000,5000, 200,200,200], #(nA/V)
         'c_lockin':        [10000,10000,10000, 20,20,20], #(V/V)
         # first number=compound density g/cm3, second number=layer thickness (cm)
         'STACK': {'Mo':[10.2, 500E-7], 'ZnTe':[6.34, 375E-7], 'CdTe':[5.35, 10.85E-4], 'CdS':[4.82, 80E-7], 'SnO2':[100E-7]},
         # lockin amp almost certainly 10000 for 2019_03_2idd scans 385-387;
         # cross-sample comparison can be made with 500, but this is not how science is done
         'v_lockin':        [1000,1000,1000, 100000],
         '2017_12_ele_iios': [0.381, 0.0682, 0.0867],
         '2019_03_ele_iios': [0.162, 0.00209, 0.00669]}

samples = [NBL3_2, NBL3_3, TS58A]

home_defs.import_h5s(samples, scan_path)
elements = ['Cu', 'Cd_L', 'Te_L', 'Mo_L']
# sample_list, scans_to_import, electrical_channel, element_list, XRF_normalization, XRF_quantification
    # electrical_channel: 1=ds_ic, 2=us_ic, 3=SRCurrent
    # XRF_normalization: us_ic or ds_ic
    # XRF_quantification: fit or roi
home_defs.import_maps(samples, 'XBIC', 2, elements, 'us_ic', 'fit')
#%%
import numpy as np
import xraylib as xl
beam_settings = {'beam_energy': 12.7, 'beam_theta': 90, 'detector_theta': 43}

def get_prefactor(idx, compound):
	if idx == 0:
	    iio_in = 1
	else:
		before_layers = 
	    iio_in = before_layers_iio...
	return iio_in

def calc_iio(sample, element, beam_settings):
    # convert geometries to radians
    beam_theta = np.sin(beam_settings['beam_theta']*np.pi/180) 
    detector_theta = np.sin(beam_settings['detector_theta']*np.pi/180)
    step_size = 1*10**-7  # 1nm steps
    STACK = sample['STACK']
    # there needs to be some mechanism that recognizes the layer we are on, what elements come before it, and what elements are inside of it...
	# build previous layers object...?
    for layer_idx, layer in enumerate(STACK.items()):
        compound, layer_info = layer[0], layer[1]
        # percent incoming beam transmitted to layer...
        iio_in = get_prefactor(layer_idx, compound) #analogous to iio_in in iio_v_thick_sim.py/iio_vs_depth
		#...
        # percent outgoing transmitted by external layers
        
        # percent outgoing Cd_L transmitted by CdTe itself
    return

def get_iios(samples, elements, beam_settings):
    elements = [element[0:2] for element in elements]
    for sample in samples:
        element_iios = [calc_iio(sample, element, beam_settings) for element in elements]
        # remember to save the iios
    return 

ele_iios = get_iios(samples, elements, beam_settings)




#%%
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


