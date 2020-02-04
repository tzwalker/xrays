# -*- coding: utf-8 -*-
"""
Trumann
Wed Sep 11 11:47:57 2019
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

import samp_dict_grow
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

# convert stacked maps of a scan into array that can be Spearman correlated #
np.shape(ht43)[0]; np.shape(ht43)[1]*np.shape(ht43)[2]
ht43_unstacked = ht43.reshape(4, (151*149))

ht_spear = spearmanr(ht43_unstacked.T)

# plot spearman result #
axis_names = ['XBIC', 'Cu','Cd', 'Te']
def plot_ugly_spearman(array, ax_name, celltxt, f):
    df = pd.DataFrame(ht_spear[0], columns=axis_names, index=axis_names)
    sns.set(style="white") # set style of seaborn objects
    mask = np.zeros_like(df, dtype=np.bool) # make mask of symmetric portion
    mask[np.triu_indices_from(mask)] = True # apply mask
    sns.heatmap(df, mask=mask,
                 cmap=f['color'], annot=True, 
                 vmin=f['range'][0], vmax=f['range'][1],
                 cbar_kws={'label': f['cbar_title']},
                 annot_kws={"fontsize":f['celltxt_size']})
    return
format_dict = {'range': [-1,1],'cbar_title': 'Monotonicity.', 
               'color': 'coolwarm', 
               'celltxt_size': 12}
plot_ugly_spearman(ht_spear[0], axis_names, True, format_dict)
# =============================================================================
# # use matplotlib.colorbar.Colorbar object
# cbar = ax.collections[0].colorbar
# # here set the labelsize by 20
# cbar.axis.tick_params(labelsize=20)
# =============================================================================
#%%
# NICE CUSTOMIZABLE HEATMAP for spearman correlations#
import numpy as np
from scipy.stats import spearmanr

SAMP = NBL3_3; SCAN=4; data=SAMP['XBIC_corr'][SCAN][:,:,:-2]
data_prep = data.reshape(np.shape(data)[0], (np.shape(data)[1]*np.shape(data)[2]))
spear = spearmanr(data_prep.T)

import custom_heatmap_defs
axis_names = ['XBIC', 'Cu','Cd', 'Te', 'Zn']
fig, ax0 = plt.subplots()
plt.tight_layout()
im, cbar = custom_heatmap_defs.heatmap(spear[0], axis_names, axis_names, mask=True,
                   cmap="coolwarm", xylabelsizes=[16,16],
                   cbarlabel="Monotonicity", 
                   cbarpad=20, cbar_labsize=16, cbar_ticksize=16,
                   ax=ax0, vmin=-1, vmax=1)

texts = custom_heatmap_defs.annotate_heatmap(im, valfmt="{x:.2g}", fontsize=12, 
                                             threshold=[-0.5,0.5])
# =============================================================================
# im, cbar = heatmap(ht_spear[1], axis_names, axis_names, cmap="Greys",
#                    xylabelsizes=[16,16],
#                    cbarlabel="Monotonicity", 
#                    cbarpad=20, cbar_labsize=16, cbar_ticksize=14,
#                    ax=ax1, vmin=0, vmax=1)
# texts = annotate_heatmap(im, valfmt="{x:.2g}", fontsize=10, threshold=[-1,.75])
# =============================================================================