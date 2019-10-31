# -*- coding: utf-8 -*-
"""
Trumann
Wed Sep 11 11:47:57 2019
"""
import samp_dict_grow
import numpy as np
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


def get_corrmtx_plot(array, cols, f, axis, numbers):
    df = pd.DataFrame(array, columns=cols, index=cols)
    sns.set(style="white") # set style of seaborn objects
    mask = np.zeros_like(df, dtype=np.bool) # make mask of symmetric portion
    mask[np.triu_indices_from(mask)] = True # apply mask
    sns.heatmap(df, mask=mask, cbar_kws=f['cbar_format'], ax=axis,
                     cmap=f['color'], annot=numbers, vmin=f['v_range'][0], vmax=f['v_range'][1],
                     annot_kws={"fontsize":f['labs']})
    #axis.title.set_text(f['plt_title'])
    
    return

