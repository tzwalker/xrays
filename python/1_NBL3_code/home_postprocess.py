# -*- coding: utf-8 -*-
"""
Trumann
Mon Oct 21 14:04:15 2019
"""
CV_switch = 'V'
### area density to molar density ###
import home_dataTransforms as dtransform
dtransform.make_mol_maps(samples, elements, 'XBI'+CV_switch+'_corr', 'XBI'+CV_switch+'_mol')
#dtransform.make_mol_maps(samples, elements, 'XBIV_corr', 'XBIV_mol')

### mol maps to mol arrays ###
#dtransform.stat_arrs(samples, 'XBIC_corr', 'XBIC_stat')
dtransform.stat_arrs(samples, 'XBI'+CV_switch+'_mol', 'XBI'+CV_switch+'_molStat')
#dtransform.stat_arrs(samples, 'XBIV_corr', 'XBIV_stat')
#dtransform.stat_arrs(samples, 'XBIV_mol', 'XBIV_molStat')
# 1=Cu 2=Cd 3=Te 4=Mo 5=Zn 6=ratio
element0_idx=1 # Cu
element1_idx=3 # Te
# this function adds molar ratio of two elements 
    # as defined by their indices in 'elements'
    # to add 2d ratio maps, simply replace '_molStat' with '_mol'
    # this function can divide the normal area density data ('_stat' and '_corr')
        # but there is little physical justification for this (better to use stoichiometry)
#dtransform.add_ratio_array(samples, 'XBIC_molStat', element0_idx, element1_idx)


#dtransform.stand_arrs(samples, 'XBIC_stat', 'XBIC_stand')
#dtransform.stand_arrs(samples, 'XBIV_stat', 'XBIV_stand')
#%%
### remove outliers ###
import home_clustering
DATA_KEY = 'XBI'+CV_switch+'_molStat'
BAD_CHANNEL_idx = 1; SIGMA = 3
NEW_DATA_KEY = 'XBI'+CV_switch+'_slim'
dtransform.remove_outliers(samples, DATA_KEY, BAD_CHANNEL_idx, SIGMA, NEW_DATA_KEY)

## kmeans clustering trials ##
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
SAMPLE = TS58A
SCANS = [0,1,2]
DATA_KEY = 'XBI'+CV_switch+'_slim';     CLUSTERS_KEY = 'XBI'+CV_switch+'kmeans_trials'
FOCUS_FEATURE = 0;          FOCUS_CLUSTER = 'low'; CLUSTERS = 3
NEW_KEYS = ['spear_stats', 'pval_stats']
home_clustering.correlation_stats(SAMPLE, SCANS, DATA_KEY, CLUSTERS_KEY, 
                               CLUSTERS, FOCUS_CLUSTER, FOCUS_FEATURE, NEW_KEYS)
#print(SAMPLE.keys())
CHANNELS = [FOCUS_CLUSTER+' XBI'+CV_switch] + elements# + ['Cu/(Cu+Te)']
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

#%%
### superpixel segmentation https://www.pyimagesearch.com/2014/07/28/a-slic-superpixel-tutorial-using-python/
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt

z = NBL3_2['XBIC_corr'][0][0,:,:]
y = img_as_float(z)
plt.imshow(z)
segment_number = 200
segments = slic(z, n_segments=segment_number, sigma=5)
fig, ax = plt.subplots(1)
ax.imshow(mark_boundaries(z, segments))
plt.axis('off')