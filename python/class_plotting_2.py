"""
notes on creating color bar onject
    #fig.colorbar(ax0).ax0 <--> plt.gcf().axes[-1]
    # if im = ax.ishow():
    # cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        # cbar.ax.set_ylabel: --> ax object needs to be accessed
    # if ax = sns.heatmap():
    # cbar = plt.gcf().axes[-1]
        # cbar.set_ylabel: no ax needed, ax object already accessed
"""

# cleaning custom 2d plots
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt

def get_real_coordinates(h5axis):
    data_coord = list(h5axis)
    axis_width = max(data_coord) - min(data_coord)
    axis_resolution = np.linspace(0, axis_width, len(data_coord))
    round_steps = [round(i,3) for i in axis_resolution]
    return round_steps

def custom_format_ticks(axes_object_labels, string_type):
    txt_labs = [label.get_text() for label in axes_object_labels]
    ticking = [string_type.format(float(txt)) for txt in txt_labs]
    return ticking

def get_colorbar_axis(data, num_of_std):
    M = data[:,:-2] # map without nan columns
    heatmap_min = M.mean() - M.std() * num_of_std
    heatmap_max = M.mean() + M.std() * num_of_std
    if heatmap_min < 0:
        heatmap_min = 0
    return heatmap_min, heatmap_max

def plot_2D_data(data, h5data, user_cmap, 
                 cbarlabel, cbar_lblsize, cbarpad, cbar_ticklbl_size,
                 xy_lbl_sizes, xy_ticklbl_sizes, xy_intervals, 
                 sci_notation, ax=None,
                 cbar_kw={}, **kwargs):
    # retrieve physcial axis scale from h5
    xreal = get_real_coordinates(h5data['/MAPS/x_axis'])
    yreal = get_real_coordinates(h5data['/MAPS/y_axis'])
    # make dataframe with physical-value xy coordinates
    df_map = pd.DataFrame(data, index = yreal, columns = xreal)
    # apply format to scale of color bar
    formatter = tkr.ScalarFormatter(useMathText=True)
    formatter.set_scientific(sci_notation)
    formatter.set_powerlimits((-2, 2))
    
    fig, ax = plt.subplots(1)
    # Plot the heatmap
    sns.heatmap(df_map, square=True, cmap=user_cmap, ax=ax,
                     xticklabels=xy_intervals[0], yticklabels=xy_intervals[1],
                     cbar_kws={'format': formatter})
    ax.tick_params(labelsize=xy_ticklbl_sizes)
    #formats tick label strings without ".0"
    x_labls = custom_format_ticks(ax.get_xticklabels(), '{:g}')
    y_labls = custom_format_ticks(ax.get_yticklabels(), '{:g}')  
    # replace xy ticklabels
    ax.set_xticklabels(x_labls)
    # invert, replace, and rotate y ticklabels
    y_labls.reverse(); ax.set_yticklabels(y_labls, rotation = 0)  
    # make xy axis titles (labels)
    plt.xlabel('X (\u03BCm)', fontsize=xy_lbl_sizes)
    plt.ylabel('Y (\u03BCm)', fontsize=xy_lbl_sizes)        
    # Create/format colorbar
    cbar = plt.gcf().axes[-1] # colorbar object in seaborn heatmap
    cbar.set_ylabel(cbarlabel, rotation=90, va="bottom", 
                       size=cbar_lblsize, labelpad=cbarpad)
    cbar.tick_params(labelsize=cbar_ticklbl_size)   
    # change size of color bar scale label, e.g. 1e-8
    cbar.yaxis.get_offset_text().set(size=cbar_ticklbl_size)
    # shift position of color bar scale label      
    cbar.yaxis.set_offset_position('left')
    return
#ex = np.random.random((101,101))
scan_idx = 5
plot_2D_data(NBL33.maps[scan_idx][1,:,:], NBL33.h5data[scan_idx], 
             user_cmap='Oranges_r',
             xy_intervals=[20,20], xy_ticklbl_sizes=14, xy_lbl_sizes=16,
             cbarlabel="$\mathrm{\u03BCg/cm{^2}}$", cbar_lblsize=14, cbarpad=25, 
             cbar_ticklbl_size=12,
             sci_notation=True)