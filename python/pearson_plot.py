# -*- coding: utf-8 -*-
"""
Trumann
Wed Sep 11 11:47:57 2019
"""

import samp_dict_grow
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def unmasked_mapcorr(samp, scans, data_key):
    correlations_of_each_scan = []
    for scan in scans:
        data = samp[data_key][scan]
        map_corrcoeffs = np.corrcoef(data.T)
        correlations_of_each_scan.append(map_corrcoeffs)
    corrs_of_scans_regavg_matrices = np.array(correlations_of_each_scan)
    scan_avg = np.mean(corrs_of_scans_regavg_matrices, axis=0)
    scan_stdev = np.std(corrs_of_scans_regavg_matrices, axis=0)
    samp_dict_grow.build_dict(samp, 'nomask_avg', scan_avg)
    samp_dict_grow.build_dict(samp, 'nomask_std', scan_stdev)
    return


def get_corrmtx_plot(array, cols, f, axis):
    df = pd.DataFrame(array, columns=cols, index=cols)
    sns.set(style="white") # set style of seaborn objects
    mask = np.zeros_like(df, dtype=np.bool) # make mask of symmetric portion
    mask[np.triu_indices_from(mask)] = True # apply mask
    sns.heatmap(df, mask=mask, cbar_kws=f['cbar_format'], ax=axis,
                     cmap=f['color'], annot=True, vmin=f['v_range'][0], vmax=f['v_range'][1])
    axis.title.set_text(f['plt_title'])
    return

corrcoeff_formatting = {'color': 'coolwarm', 
                      'cbar_format': {'ticks': list(list(np.linspace(-1,1,5))), 
                                      'label': 'Spearman Coefficient'},
                      'plt_title': 'Average Monotonicity',
                      'v_range': [-1,1]}
stdev_formatting = {'color': 'Greys', 
                      'cbar_format': {'ticks': list(list(np.linspace(-1,1,5))), 
                                      'label': 'Standard Error'},
                      'plt_title': 'Average Error',
                      'v_range': [0,1]}

fig, (ax0, ax1) = plt.subplots(2,1)
plt.tight_layout()
get_corrmtx_plot(NBL3_3['avg_std_corr'][0], ['XBIC'] + elements, corrcoeff_formatting, ax0)
get_corrmtx_plot(NBL3_3['avg_std_corr'][1], ['XBIC'] + elements, stdev_formatting, ax1)
