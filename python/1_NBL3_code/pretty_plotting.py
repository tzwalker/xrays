'''
created: Fri Aug 16 14:49:13 2019
author: Trumann
'''
import plot_supplement as PLT

samp = NBL3_3
scan = 0
axis_label_sizes = 16

# use this function to plot normal-unit, corrected elemental maps
    # -1:XBIC, 0:Cu, 1:Cd, 2:Te, etc...
PLT.plot_nice_2Dmap(samp, scan, axis_label_sizes, 'elXBIC', 0) 
PLT.map_to_hist(samp, scan, axis_label_sizes, 'elXBIC_corr', 1, 50)


sample = TS58A
scan = 0
channel = 0
data = 'c_stand_arrs'
# use this functino to plot standardized electrical maps
    # adds nan columns
    # 0:XBIC, 1:Cu, 2:Cd (match to index of 'elements' list)
#PLT.from_stand_to_stand_map(sample, scan, data, channel)

samp = NBL3_3
h5_key = 'XBIC_h5s'
data_key = 'XBIC_maps'
model_key = 'c_kmodels'
scan = 0

h5 = samp[h5_key][scan]
map_to_cluster = samp[data_key][scan][:,:-2]
kmodel = samp[model_key][scan]
# use this function to plot nice cluster maps
    # only configured for not reduced arrays
    # i.e. kclustering with switch 0 or 1 must be used
#PLT.plot_cluster_map(h5, map_to_cluster, kmodel, cluster_number)
