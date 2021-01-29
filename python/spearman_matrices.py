from scipy.stats import spearmanr
import numpy as np
import seaborn as sns

imgs = NBL33.scan264[0:4,:,:-2]

x,y = np.shape(imgs)[1],np.shape(imgs)[2]
new_shape = x*y

imgs_flt = imgs.reshape(4, new_shape)

imgs_fltT = imgs_flt.T
spear = spearmanr(imgs_fltT)

labs = ['XBIC', 'Cu', 'Cd', 'Te']
cbar_lab = 'Monotonicty'
mask = np.triu(np.ones_like(spear[0], dtype=bool))

fig, ax = plt.subplots(figsize=(5,2))
sns.heatmap(spear[0], vmin=-1, vmax=1, cmap='coolwarm',
            annot=True, xticklabels=labs, yticklabels=labs,
            mask=mask, fmt='.2f', cbar_kws={'label': cbar_lab})

#%%
"""
tzwalker
Sun Feb  2 11:01:38 2020
coding: utf-8
"""
import numpy as np
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import samp_dict_grow
import custom_heatmap_defs

def spearman_matrix(data, row_labels, col_labels, mask,
            cbarpad, cbar_labsize, cbar_ticksize, 
            xylabelsizes,
            ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    data
        A 2D numpy array of shape (N, M)
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()
    if mask==True:
        mask = np.zeros_like(data, dtype=np.bool) # make mask of symmetric portion
        mask[np.triu_indices_from(mask)] = True # apply mask
        data_masked = np.ma.MaskedArray(data, mask)
        im = ax.imshow(data_masked, **kwargs)
    else:
        # Plot the heatmap
        im = ax.imshow(data, **kwargs)

    # Create/format colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=90, va="bottom", 
                       size=cbar_labsize, labelpad=cbarpad)
    #remove colorbar outline
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(labelsize=cbar_ticksize) 

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels, size=xylabelsizes[0])
    ax.set_yticklabels(row_labels, size=xylabelsizes[1])

    # Adjust axes that will show tick labels
    ax.tick_params(top=False, bottom=False,
                   labeltop=False, labelbottom=True)

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)    
    
    return im, cbar


def annotate_spearman(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = tkr.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if int(im.norm(data[i, j]) > threshold[1]):
                kw.update(color=textcolors[1]) # anything greater than thres will be white
            elif int(im.norm(data[i, j]) < threshold[0]):
                kw.update(color=textcolors[1]) # anything less than thres will be white
            else: kw.update(color=textcolors[0])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)
    # turn zeros of txt annotations to blanks!
    for text in texts:
        if text._text == '0': text._text = ""
    return texts

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


SAMP = NBL3_3; SCAN=4; data=SAMP['XBIC_corr'][SCAN][:,:,:-2]
data_prep = data.reshape(np.shape(data)[0], (np.shape(data)[1]*np.shape(data)[2]))
spear = spearmanr(data_prep.T)


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

#%%
# averaging over multipple spearman matrices (e.g. nbl32 in each geometry) #

#check correlations between two geometries of different areas of CdTe
deg15 = NBL3_2['XBIC_maps'][3:6] #access CdTe data
deg15 = [arr[:,:,:-2] for arr in deg15] # remove nan columns

spear_stack = []
for scan in deg15:
    data = scan[[1,2,3],:,:]
    data_prep = data.reshape(np.shape(data)[0], (np.shape(data)[1]*np.shape(data)[2]))
    spear = spearmanr(data_prep.T)
    spear_stack.append(spear[0])
spear_stack1 = np.array(spear_stack)

deg15_avg = np.average(spear_stack1,axis=0)
deg15_std = np.std(spear_stack1,axis=0)

AXIS_NAMES = ['Cu', 'Cd', 'Te']
fig, (ax0,ax1) = plt.subplots(2,1, figsize=(4,4))
plt.tight_layout()
IM, CBAR = custom_heatmap_defs.heatmap(deg15_avg, AXIS_NAMES, AXIS_NAMES, mask=True,
                   cmap="coolwarm", xylabelsizes=[16,16],
                   cbarlabel="Monotonicity", 
                   cbarpad=20, cbar_labsize=16, cbar_ticksize=16,
                   ax=ax0, vmin=-1, vmax=1)
TEXTS = custom_heatmap_defs.annotate_heatmap(IM, valfmt="{x:.2g}", fontsize=10, 
                                             threshold=[-0.5,0.5])
IM, CBAR = custom_heatmap_defs.heatmap(deg15_std, AXIS_NAMES, AXIS_NAMES, mask=True,
                   cmap="Greys", xylabelsizes=[16,16],
                   cbarlabel="Std. Err.", 
                   cbarpad=20, cbar_labsize=16, cbar_ticksize=16,
                   ax=ax1, vmin=0, vmax=1)
TEXTS = custom_heatmap_defs.annotate_heatmap(IM, valfmt="{x:.2g}", fontsize=10, 
                                             threshold=[-0.5,0.5])