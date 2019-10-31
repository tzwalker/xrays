# -*- coding: utf-8 -*-
"""
Trumann
Mon Oct 21 14:04:15 2019
"""
import home_dataTransforms as dtransform
CV_switch = 'V'
# area density maps to area density arrays 
dtransform.stat_arrs(samples, 'XBI'+CV_switch+'_corr', 'XBI'+CV_switch+'_stat')
# area density arrays to area density standardized
dtransform.stand_arrs(samples, 'XBI'+CV_switch+'_stat', 'XBI'+CV_switch+'_stand')

### area density maps to mol maps ### 
# NOTE THERE IS A DEPENDENCEY HERE ON HOW MANY ELEMENTS WERE INCLUDED IN THE ABSORPTION CORRECTION!!
dtransform.make_mol_maps(samples, elements, 'XBI'+CV_switch+'_corr', 'XBI'+CV_switch+'_mol')

# mol maps to mol arrays
dtransform.stat_arrs(samples, 'XBI'+CV_switch+'_mol', 'XBI'+CV_switch+'_molStat')
# mol arrays to mol standardized
dtransform.stand_arrs(samples, 'XBI'+CV_switch+'_molStat', 'XBI'+CV_switch+'_molstand')


# 1=Cu 2=Cd 3=Te 4=Mo 5=Zn 6=ratio
element0_idx=1 # Cu
element1_idx=3 # Te
# this function adds molar ratio of two elements 
    # as defined by their indices in 'elements'
    # to add 2d ratio maps, simply replace '_molStat' with '_mol'
    # this function can divide the normal area density data ('_stat' and '_corr')
        # but there is little physical justification for this (better to use stoichiometry)
#dtransform.add_ratio_array(samples, 'XBI'+CV_switch+'_molStat', element0_idx, element1_idx)



#%%
### remove outliers, only use on Stat arrays ###
import home_clustering
DATA_KEY = 'XBI'+CV_switch+'_molStat'
BAD_CHANNEL_idx = 1; SIGMA = 3
NEW_DATA_KEY = 'XBI'+CV_switch+'_slim'
dtransform.remove_outliers(samples, DATA_KEY, BAD_CHANNEL_idx, SIGMA, NEW_DATA_KEY)

## kmeans clustering trials ##
# change this to _molStat if you want to plot clusters; otherwise use _slim
DATA_KEY = 'XBI'+CV_switch+'_slim' 
MASK_FEATURE = 0 # column index of channel within stat array
CLUSTERS = 3; KTRIALS = 5
# stores numpy array of 'n' kmeans clustering trials for each scan for each sample
home_clustering.kmeans_trials(samples, DATA_KEY, MASK_FEATURE, 
                           CLUSTERS, KTRIALS, 'XBI'+CV_switch+'kmeans_trials')
#print(samples[0].keys())
#%%
import home_clustering
import plot_correlation_matrices
import matplotlib.pyplot as plt
import numpy as np
CV_switch = 'C'
SAMPLE = NBL3_3
SCANS = [3,4]
DATA_KEY = 'XBI'+CV_switch+'_slim';     CLUSTERS_KEY = 'XBI'+CV_switch+'kmeans_trials'
FOCUS_FEATURE = 0;          FOCUS_CLUSTER = 'low'; CLUSTERS = 3
NEW_KEYS = ['spear_stats', 'pval_stats']
home_clustering.correlation_stats(SAMPLE, SCANS, DATA_KEY, CLUSTERS_KEY, 
                               CLUSTERS, FOCUS_CLUSTER, FOCUS_FEATURE, NEW_KEYS)
noXRF_line_elements = [e[0:2] for e in elements]
CHANNELS = [FOCUS_CLUSTER+' XBI'+CV_switch] + noXRF_line_elements
SPEAR_FORMAT = {'color': 'coolwarm', 
                      'cbar_format': {'ticks': list(list(np.linspace(-1,1,5))), 
                                      'label': 'Spearman Coefficient'},
                      'plt_title': 'Average Monotonicity',
                      'v_range': [-1,1],
                      'labs': 14}
STDEV_FORMAT = {'color': 'Greys', 
                      'cbar_format': {'ticks': list(list(np.linspace(-1,1,5))), 
                                      'label': 'Standard Error'},
                      'plt_title': 'Average Error',
                      'v_range': [0,1],
                      'labs': 8}

fig, (ax0,ax1) = plt.subplots(2,1)
plt.tight_layout()
# include True or None to turn numbers in cells on or off :)
plot_correlation_matrices.get_corrmtx_plot(SAMPLE['spear_stats'][0], CHANNELS, SPEAR_FORMAT, ax0, None)
plot_correlation_matrices.get_corrmtx_plot(SAMPLE['spear_stats'][1], CHANNELS, STDEV_FORMAT, ax1, None)

