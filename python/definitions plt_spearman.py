"""
tzwalker
Sun Feb  2 11:01:38 2020
coding: utf-8
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

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
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

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