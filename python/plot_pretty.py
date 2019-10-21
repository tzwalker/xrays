'''
created: Fri Aug 16 14:49:13 2019
author: Trumann
'''
import plot_supplements as PLT

sample = sample_dict0
data_key = 'XBIC_corr'
scan_idx = 0; feature_idx = 1
label_list = [16,14, 
              20,20]

# use this function to plot area-density, corrected elemental maps
    # feature integer equals the index of the elmenent as seen in 'elements'
PLT.plot_nice_2Dmap(sample, data_key, scan, feature, label_list) 


sample = sample_dict0
data_key = 'XBIC_stand'
scan_idx = 2; feature_idx = 2
# use this function to plot standardized maps for cross-sample comparison
    # (adds nan columns)
    # feature_idx
PLT.from_stand_to_stand_map(sample, scan_idx, data_key, feature_idx)

# =============================================================================
# #PLT.map_to_hist(samp, scan, axis_label_sizes, 'elXBIC_corr', 1, 50)
# samp = NBL3_3
# h5_key = 'XBIC_h5s'
# data_key = 'XBIC_maps'
# model_key = 'c_kmodels'
# scan = 0
# 
# h5 = samp[h5_key][scan]
# map_to_cluster = samp[data_key][scan][:,:-2]
# kmodel = samp[model_key][scan]
# # use this function to plot nice cluster maps
#     # only configured for not reduced arrays
#     # i.e. kclustering with switch 0 or 1 must be used
# #PLT.plot_cluster_map(h5, map_to_cluster, kmodel, cluster_number)
# =============================================================================
