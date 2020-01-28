# -*- coding: utf-8 -*-
"""
Trumann
Mon Oct 21 14:04:15 2019
"""
import home_dataTransforms as dtransform
CV_SWITCH = 'C'
# area density maps to area density arrays 
dtransform.stat_arrs(samples, 'XBI'+CV_SWITCH+'_corr', 'XBI'+CV_SWITCH+'_stat')
# area density arrays to area density standardized
dtransform.stand_arrs(samples, 'XBI'+CV_SWITCH+'_stat', 'XBI'+CV_SWITCH+'_stand')

### area density maps to mol maps ### 
eles = ['Cu', 'Cd_L', "Te_L"] # -> if scans to plot are bulk (good geom.), then Zn channel is not present
    # change line 62
dtransform.make_mol_maps(samples, eles, 'XBI'+CV_SWITCH+'_corr', 'XBI'+CV_SWITCH+'_mol')

# mol maps to mol arrays
dtransform.stat_arrs(samples, 'XBI'+CV_SWITCH+'_mol', 'XBI'+CV_SWITCH+'_molStat')
# mol arrays to mol standardized
dtransform.stand_arrs(samples, 'XBI'+CV_SWITCH+'_molStat', 'XBI'+CV_SWITCH+'_molstand')


# 1=Cu 2=Cd 3=Te 4=Mo 5=Zn 6=ratio
#element0_idx=1 # Cu
#element1_idx=3 # Te
# this function adds molar ratio of two elements 
    # as defined by their indices in 'elements'
    # to add 2d ratio maps, simply replace '_molStat' with '_mol'
    # this function can divide the normal area density data ('_stat' and '_corr')
        # but there is little physical justification for this (better to use stoichiometry)
#dtransform.add_ratio_array(samples, 'XBI'+CV_switch+'_molStat', element0_idx, element1_idx)

### remove outliers, only use on Stat arrays ###
DATA_KEY = 'XBI'+CV_SWITCH+'_molStat'
BAD_CHANNEL_IDX = 1; SIGMA = 3
NEW_DATA_KEY = 'XBI'+CV_SWITCH+'_slim'
dtransform.remove_outliers(samples, DATA_KEY, BAD_CHANNEL_IDX, SIGMA, NEW_DATA_KEY)

#%%
import home_clustering
## kmeans clustering trials ##
# change this to _molStat if you want to plot clusters; otherwise use _slim
DATA_KEY = 'XBI'+CV_SWITCH+'_slim' 
MASK_FEATURE = 0 # column index of channel within stat array
CLUSTERS = 3; KTRIALS = 5
# stores numpy array of 'n' kmeans clustering trials for each scan for each sample
home_clustering.kmeans_trials(samples, DATA_KEY, MASK_FEATURE, 
                           CLUSTERS, KTRIALS, 'XBI'+CV_SWITCH+'kmeans_trials')
#print(samples[0].keys())
#%%
# plot correlation matrices from kmeans trials #
import home_clustering; import plot_defs
import matplotlib.pyplot as plt
import numpy as np
CV_SWITCH = 'C'
SAMPLE = NBL3_3; SCANS = [0,1,2]
DATA_KEY = 'XBI'+CV_SWITCH+'_slim';     CLUSTERS_KEY = 'XBI'+CV_SWITCH+'kmeans_trials'
FOCUS_FEATURE = 0;          FOCUS_CLUSTER = 'low'; CLUSTERS = 3
NEW_KEYS = ['spear_stats', 'pval_stats']
home_clustering.correlation_stats(SAMPLE, SCANS, DATA_KEY, CLUSTERS_KEY, 
                               CLUSTERS, FOCUS_CLUSTER, FOCUS_FEATURE, NEW_KEYS)
ELE_NAMES = [e[0:2] for e in elements] # -> change this from 'elements' to 'eles' if doing bulk scans (idx -->3,4,5)
CHANNELS = [FOCUS_CLUSTER+' XBI'+CV_SWITCH] + ELE_NAMES
SPEAR_FORMAT = {'color': 'coolwarm', 
                      'cbar_format': {'ticks': list(list(np.linspace(-1,1,5))), 
                                      'label': 'Spearman Coeff.'},
                      'plt_title': None,
                      'v_range': [-1,1],
                      'labs': 14}
STDEV_FORMAT = {'color': 'Greys', 
                      'cbar_format': {'ticks': list(list(np.linspace(-1,1,5))), 
                                      'label': 'Standard Error'},
                      'plt_title': None,
                      'v_range': [0,1],
                      'labs': 8}

fig, (ax0,ax1) = plt.subplots(2,1)
plt.tight_layout()
# include True or None to turn numbers in cells on or off :)
plot_defs.get_corrmtx_plot(SAMPLE['spear_stats'][0], CHANNELS, SPEAR_FORMAT, ax0, True)
plot_defs.get_corrmtx_plot(SAMPLE['spear_stats'][1], CHANNELS, STDEV_FORMAT, ax1, None)

