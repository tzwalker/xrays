# -*- coding: utf-8 -*-
"""
Trumann
Wed Sep 11 11:47:57 2019
"""

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
    correlations_of_each_scan = np.array(correlations_of_each_scan)
    return correlations_of_each_scan

def plot_corrs(corr1, corr2, cols):
    # MAKE SURE THIS MATCHES NUMBER OF LOADED ELEMENTS; changes depending on how h5s were fit
    df_top = pd.DataFrame(corr1, columns=cols, index=cols)
    df_bot = pd.DataFrame(corr2, columns=cols, index=cols)
    # plot
    sns.set(style="white")
    # generate a mask for the upper triangle
    mask = np.zeros_like(df_top, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    # make cbar ticks
    cbar_tick={'ticks': list(list(np.linspace(-1,1,5))), 'label': 'Pearson Correlation Coeff.'}
    cbar_tick1={'ticks': list(list(np.linspace(-1,1,5))), 'label': 'Standard Error'}
    fig, (ax0, ax1) = plt.subplots(2,1)
    plt.tight_layout()
    sns.heatmap(df_top, mask=mask, cbar_kws=cbar_tick, ax=ax0,
                     cmap='coolwarm', annot=True, vmin=-1, vmax=1)
    ax0.title.set_text('Average Linearity')
    sns.heatmap(df_bot, mask=mask, cbar_kws=cbar_tick1, ax=ax1,
                 cmap='Greys',annot=True, vmin=0, vmax=1)
    return

