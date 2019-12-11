'''
created: Fri Aug 16 14:49:13 2019
author: Trumann
'''
import plot_defs as PLT
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
SAMP = TS58A; SCAN = 1; CHAN = 1
DATA_KEY = 'XBIC_corr'
LABELS = [16,14, 20,20]

colors = [(0, 0, 0), (0.5, 0, 0), (1, 0, 0)]  # R -> G -> B
cmap_name = 'imgj_reds'
# Create the colormap
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=255)
# use this function to plot area-density, corrected elemental maps
    # feature integer equals the index of the elmenent as seen in 'elements'
PLT.plot_nice_2Dmap(SAMP, DATA_KEY, SCAN, CHAN, LABELS, cm) 


#%%
SAMP = TS58A; SCAN = 1; CHAN = 0
DATA_KEY = 'XBIC_maps'
# use this function to plot standardized maps for cross-sample comparison
# NOTE: run data transformation before this funciton to get the right dict keys
    # (adds nan columns)
    # feature_idx
PLT.from_stand_to_stand_map(SAMP, SCAN, DATA_KEY, CHAN)

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

