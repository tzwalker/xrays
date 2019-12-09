'''
created: Fri Aug 16 14:49:13 2019
author: Trumann
'''
import plot_defs as PLT
sample = TS58A
data_key = 'XBIC_corr'
scan_idx = 3; feature_idx = 3
label_list = [16,14, 
              20,20]

# use this function to plot area-density, corrected elemental maps
    # feature integer equals the index of the elmenent as seen in 'elements'
PLT.plot_nice_2Dmap(sample, data_key, scan_idx, feature_idx, label_list) 

#%%
sample = NBL3_3
data_key = 'XBIC_stand'
scan_idx = 0; feature_idx = 2
# use this function to plot standardized maps for cross-sample comparison
    # (adds nan columns)
    # feature_idx
PLT.from_stand_to_stand_map(sample, scan_idx, data_key, feature_idx)

#PLT.map_to_hist(samp, scan, axis_label_sizes, 'elXBIC_corr', 1, 50)
#%%
samp = NBL3_3
h5_key = 'XBIC_h5s'
data_key = 'XBIC_maps'
model_key = 'XBICkmeans_trials'
scan = 0; ktrial= 0; feature = 0 
# 'feature' is to easily get shape of original map;
    # the same mask will apply to all features --> changes features should have no effect on the cluster map shown as 
h5 = samp[h5_key][scan]
original_map = samp[data_key][scan][feature,:,:-2]
model = samp[model_key][scan][ktrial,:]
# use this function to plot nice cluster maps
    # USE THIS FUNCTION ONLY IF WHOLE STAT ARRAY IS THIS INPUT TO home_clustering.kmeans_trials()
    # i.e. no XBIC_slim
import plot_defs as PLT
PLT.plot_cluster_map(h5, original_map, model, 3)

