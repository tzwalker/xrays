# -*- coding: utf-8 -*-
"""
created: Fri Aug 16 15:14:52 2019
author: Trumann
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib

def custom_format_ticks(axes_object_labels, string_type):
    txt_labs = [label.get_text() for label in axes_object_labels]
    ticking = [string_type.format(float(txt)) for txt in txt_labs]
    return ticking

def get_real_coordinates(axis_list):
    data_coord = list(axis_list)
    axis_width = max(data_coord) - min(data_coord)
    axis_resolution = np.linspace(0, axis_width, len(data_coord))
    round_steps = [round(i,3) for i in axis_resolution]
    return round_steps

# usefeul function for visualizing standardized data as a map
# puts two nan columns back on standardized arrays
def put_nans_back_on(array, y_coord, x_coord):
    slim_map = array.reshape(len(y_coord), len(x_coord)-2)           # minus 2cols (chopped off nans in e_statistics.py)
    nans_to_attach = np.full((np.size(slim_map, axis=0),2), np.nan) # get 2cols of nan
    nan_map = np.append(slim_map, nans_to_attach, 1)                 # attach nan
    return nan_map

def get_colorbar_axis(c_map, num_of_std):
    M = c_map[:,:-2] # map without nan columns
    heatmap_min = M.mean() - M.std() * num_of_std
    heatmap_max = M.mean() + M.std() * num_of_std
    if heatmap_min < 0:
        heatmap_min = 0
    #if heatmap_max > 1: #for XBIC maximum...
        #heatmap_max = 1
    return heatmap_min, heatmap_max

def channel_formatting(index):
    if index == 0:
        data_formatting = ['magma', 'Stand. XBIC (a.u.)']
    elif index == 1:
        data_formatting = ['Oranges_r', '\u03BCg/cm'+ r'$^{2}$']
    elif index == 2:
        data_formatting = ['viridis', '\u03BCg/cm'+ r'$^{2}$']
    elif index == 3:
        data_formatting = ['Greys_r', '\u03BCg/cm'+ r'$^{2}$']
    return data_formatting

def from_stand_to_stand_map(samp, scan, data, channel):
    c_scan = samp['XBIC_h5s'][scan]  # h5 always has coordinates
    x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
    y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
    x_real = get_real_coordinates(x_axis)
    y_real = get_real_coordinates(y_axis)
    format_list = channel_formatting(channel)
    c_map = samp[data][scan][:,channel]
    c_map = put_nans_back_on(c_map, y_real, x_real)
    
    df_map = pd.DataFrame(c_map, index = y_real, columns = x_real)
    fig, ax0 = plt.subplots()
    ax0 = sns.heatmap(df_map, square = True, cmap = format_list[0],
                      xticklabels = 20, yticklabels = 20,
                      cbar_kws={"shrink": 1.0, 'format': '%.2f'}, vmin=-3, vmax=3)
    # figure level
    plt.xlabel('X (\u03BCm)', fontsize=16)
    plt.ylabel('Y (\u03BCm)', fontsize=16)
    #plt.title(samp['Name'], fontsize=axis_label_sizes)
    # axis level
    ax0.tick_params(labelsize = 14)                     #formats size of ticklabels
    x_labls = custom_format_ticks(ax0.get_xticklabels(), '{:g}')
    y_labls = custom_format_ticks(ax0.get_yticklabels(), '{:g}')         #formats tick label strings without ".0"
    ax0.set_xticklabels(x_labls)                        #set the tick labels
    ax0.set_yticklabels(y_labls, rotation = 0)          #set the ticklabels and rotate (if needed)
    ax0.invert_yaxis()                                  #invert the yaxis after formatting is complete
    
    #fig.colorbar(ax0).ax0 <--> plt.gcf().axes[-1]
    cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y axes object
    # colorbar label settings
    cbar_ax.set_ylabel(format_list[1], fontsize =16, 
                       rotation = 90, labelpad = 10)   #label formatting
    cbar_ax.tick_params(labelsize=12)                   #tick label formatting
    cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
    cbar_ax.yaxis.set_offset_position('left')           #scale at top of colorbar (i.e. 'offset') position
    #cbar_ax.set_yticklabels(custom_format_ticks(cbar_ax.get_yticklabels(), '{:.2f}'))
    return

def plot_nice_2Dmap(samp,scan,label_sizes, data_channel, ele_index):
    c_scan = samp['XBIC_h5s'][scan]  # h5 always has coordinates
    x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
    y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
    x_real = get_real_coordinates(x_axis)
    y_real = get_real_coordinates(y_axis)
    
    if ele_index == -1:             
        c_map = samp[data_channel][scan];
        c_map = c_map / c_map[:,:-2].max()
        colors = 'magma'; units = '% Max Current'
    else: 
        c_map = samp[data_channel][scan][ele_index];
        #c_map = c_map / c_map[:,:-2].max()
        colors = 'Oranges_r'; units = '\u03BCg/cm'+ r'$^{2}$'
    
    lower,upper = get_colorbar_axis(c_map, 3) # int here sets num_of_std to include
    df_map = pd.DataFrame(c_map, index = y_real, columns = x_real)
    fig, ax0 = plt.subplots()
    ax0 = sns.heatmap(df_map, square = True, cmap = colors,
                      xticklabels = 20, yticklabels = 20,
                      cbar_kws={"shrink": 1.0, 'format': '%.2f'}, vmin=lower, vmax=upper)
    # figure level
    plt.xlabel('X (\u03BCm)', fontsize=label_sizes)
    plt.ylabel('Y (\u03BCm)', fontsize=label_sizes)
    #plt.title(samp['Name'], fontsize=axis_label_sizes)
    # axis level
    ax0.tick_params(labelsize = 14)                     #formats size of ticklabels
    x_labls = custom_format_ticks(ax0.get_xticklabels(), '{:g}')
    y_labls = custom_format_ticks(ax0.get_yticklabels(), '{:g}')         #formats tick label strings without ".0"
    ax0.set_xticklabels(x_labls)                        #set the tick labels
    ax0.set_yticklabels(y_labls, rotation = 0)          #set the ticklabels and rotate (if needed)
    ax0.invert_yaxis()                                  #invert the yaxis after formatting is complete
    
    #fig.colorbar(ax0).ax0 <--> plt.gcf().axes[-1]
    cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y axes object
    # colorbar label settings
    cbar_ax.set_ylabel(units, fontsize = label_sizes, 
                       rotation = 90, labelpad = 10)   #label formatting
    cbar_ax.tick_params(labelsize=12)                   #tick label formatting
    cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
    cbar_ax.yaxis.set_offset_position('left')           #scale at top of colorbar (i.e. 'offset') position
    #cbar_ax.set_yticklabels(custom_format_ticks(cbar_ax.get_yticklabels(), '{:.2f}'))
    return 

### from online
def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap/correlation matrix from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """
    if not ax:
        ax = plt.gca()
    # Plot the heatmap
    im = ax.imshow(data, **kwargs)
    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")
    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)
    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    return im, cbar

def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
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
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)
    return texts