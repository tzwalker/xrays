# -*- coding: utf-8 -*-
"""
Trumann
Mon Oct 21 14:04:15 2019
"""

### begin post processing ###
import home_stat
import home_clustering
DATA_KEY = 'XBIC_stat'
BAD_CHANNEL_idx = 1
SIGMA = 3
NEW_DATA_KEY = 'XBIC_slim'
home_stat.remove_outliers(samples, DATA_KEY, BAD_CHANNEL_idx, SIGMA, NEW_DATA_KEY)

## clustering trials ##
DATA_KEY = 'XBIC_slim'
MASK_FEATURE = 0 # column index of channel within stat array of choice (the key used in kmeans_trials())
CLUSTERS = 3
KTRIALS = 5
# stores numpy array of 'n' kmeans clustering trials for each scan for each sample
    # for a given scan, array will be 'n'x'len(redStand_arr)'
    # example navigation use: sample_dict['c_kmeans_trials'][scan_num]
home_clustering.kmeans_trials(samples, DATA_KEY, MASK_FEATURE, 
                           CLUSTERS, KTRIALS, 'XBICkmeans_trials')
#print(samples[0].keys())
#%%
import home_clustering
import pearson_plot
import matplotlib.pyplot as plt
SAMPLE = NBL3_3
SCANS = [0,1,2]
DATA_KEY = 'XBIC_slim'; CLUSTERS_KEY = 'XBICkmeans_trials'
FOCUS_FEATURE = 0; FOCUS_CLUSTER = 'high'; CLUSTERS = 3
NEW_KEYS = ['spear_stats', 'pval_stats']
home_clustering.correlation_stats(SAMPLE, SCANS, DATA_KEY, CLUSTERS_KEY, 
                               CLUSTERS, FOCUS_CLUSTER, FOCUS_FEATURE, NEW_KEYS)
#print(SAMPLE.keys())

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
pearson_plot.get_corrmtx_plot(SAMPLE['spear_stats'][0], ['XBIC'] + elements, SPEAR_FORMAT, ax0)
pearson_plot.get_corrmtx_plot(SAMPLE['spear_stats'][1], ['XBIC'] + elements, STDEV_FORMAT, ax1)