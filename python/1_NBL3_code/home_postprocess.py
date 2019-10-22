# -*- coding: utf-8 -*-
"""
Trumann
Mon Oct 21 14:04:15 2019
"""
### begin post processing ###
import home_dataTransforms as dtransform
dtransform.make_mol_maps(samples, elements, 'XBIC_corr', 'XBIC_mol')
#dtransform.make_mol_maps(samples, elements, 'XBIV_corr', 'XBIV_mol')

#dtransform.stat_arrs(samples, 'XBIC_corr', 'XBIC_stat')
dtransform.stat_arrs(samples, 'XBIC_mol', 'XBIC_molStat')
#dtransform.stat_arrs(samples, 'XBIV_corr', 'XBIV_stat')
#dtransform.stat_arrs(samples, 'XBIV_mol', 'XBIV_molStat')

element0_idx=1 # Cu
element1_idx=3 # Te
# this function adds molar ratio of two elements 
    # as defined by their indices in 'elements'
    # to add 2d ratio maps, simply replace '_molStat' with '_mol'
    # this function can divide the normal area density data ('_stat' and '_corr')
        # but there is little physical justification for this (better to use stoichiometry)
dtransform.add_ratio_array(samples, 'XBIC_molStat', element0_idx, element1_idx)


#dtransform.stand_arrs(samples, 'XBIC_stat', 'XBIC_stand')
#dtransform.stand_arrs(samples, 'XBIV_stat', 'XBIV_stand')
#%%
import home_clustering
DATA_KEY = 'XBIC_molStat'
BAD_CHANNEL_idx = 1; SIGMA = 3
NEW_DATA_KEY = 'XBIC_slim'
dtransform.remove_outliers(samples, DATA_KEY, BAD_CHANNEL_idx, SIGMA, NEW_DATA_KEY)

## clustering trials ##
DATA_KEY = 'XBIC_slim'
MASK_FEATURE = 0 # column index of channel within stat array
CLUSTERS = 3; KTRIALS = 5
# stores numpy array of 'n' kmeans clustering trials for each scan for each sample
home_clustering.kmeans_trials(samples, DATA_KEY, MASK_FEATURE, 
                           CLUSTERS, KTRIALS, 'XBICkmeans_trials')
#print(samples[0].keys())
#%%
import home_clustering
import plot_correlation_matrices
import matplotlib.pyplot as plt
import numpy as np
SAMPLE = NBL3_2
SCANS = [0,1,2]
DATA_KEY = 'XBIC_slim';     CLUSTERS_KEY = 'XBICkmeans_trials'
FOCUS_FEATURE = 0;          FOCUS_CLUSTER = 'high'; CLUSTERS = 3
NEW_KEYS = ['spear_stats', 'pval_stats']
home_clustering.correlation_stats(SAMPLE, SCANS, DATA_KEY, CLUSTERS_KEY, 
                               CLUSTERS, FOCUS_CLUSTER, FOCUS_FEATURE, NEW_KEYS)
#print(SAMPLE.keys())
CHANNELS = ['XBIC'] + elements + ['Cu/Te']
SPEAR_FORMAT = {'color': 'coolwarm', 
                      'cbar_format': {'ticks': list(list(np.linspace(-1,1,5))), 
                                      'label': 'Spearman Coefficient'},
                      'plt_title': 'Average Monotonicity',
                      'v_range': [-1,1]}
STDEV_FORMAT = {'color': 'Greys', 
                      'cbar_format': {'ticks': list(list(np.linspace(-1,1,5))), 
                                      'label': 'Standard Error'},
                      'plt_title': 'Average Error',
                      'v_range': [0,1]}

fig, (ax0, ax1) = plt.subplots(2,1)
plt.tight_layout()
plot_correlation_matrices.get_corrmtx_plot(SAMPLE['spear_stats'][0], CHANNELS, SPEAR_FORMAT, ax0)
plot_correlation_matrices.get_corrmtx_plot(SAMPLE['spear_stats'][1], CHANNELS, STDEV_FORMAT, ax1)