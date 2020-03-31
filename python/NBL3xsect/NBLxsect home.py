"""
this is the most recent program used to plot xsect NBL3 data (20200308)
-the program relies on custom functions in "definitions_NBLxSect.py" 
-first the metadata is retrieved for the relevant scan
-then the indicated channels are imported; the XRF line needs to be added
-the program rotates each map by the same number of degrees, and the final dfs
are these rotated maps
-a plotting function is used to plot the map; many formatting 
parameters can be specified
-rotation is done to integrate along the vertical axis (the data must be
perpendicular to the x-axis) for future comparison to SIMS profiles
"""

PATH = r'C:\Users\triton\Desktop\NBL3_data\cross_section_MS' #r'C:\Users\Trumann\Desktop\NBL3_data\cross_sections_MS\csvs' #'C:\Users\triton\Desktop\NBL3_data\cross_section_MS'
DEFS = r'C:\Users\triton\xrays\python\NBL3xsect' #'C:\Users\triton\xrays\python\NBL3xsect' C:\Users\Trumann\xrays\python\NBL3xsect
import sys
sys.path.append(DEFS)
from definitions_NBLxSect import import_xSect_csvs, get_scan_metadata
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_NBL3_xsect(df, fig_size, color, cbar_bounds,
                    xyinterval,ticksize,
                    xtick_bounds,xlabelsize,xlab_roatation,
                    ytick_bounds,ylabelsize,ylab_roatation,
                    cbar_label, cbar_labelsize, cbar_ticksize, cbar_tick_rot):

    # change aspect ratio
    fig, axes = plt.subplots(figsize=fig_size)
    #plot using seaborn
    ax = sns.heatmap(df, vmin=cbar_bounds[0],vmax=cbar_bounds[1], cmap=color, 
                     xticklabels=xyinterval, yticklabels=xyinterval)
    # for manually plotting range of axes
    my_xticks = ax.get_xticks() 
    # use only first and last tick position; format ticks
    plt.xticks([my_xticks[0], my_xticks[-1]], 
               visible=True, fontsize=ticksize, rotation=xlab_roatation)
    # set the first and last tick labels according to known map size
    ax.set_xticklabels(xtick_bounds)     
    plt.xlabel('X (\u03BCm)', fontsize=xlabelsize, rotation=0)                   
    # same for yticks
    my_yticks = ax.get_yticks()  
    plt.yticks([my_yticks[0], my_yticks[-1]], 
               visible=True, fontsize=ticksize, rotation=ylab_roatation)
    ax.set_yticklabels(ytick_bounds)
    plt.ylabel('Y (\u03BCm)', fontsize=ylabelsize, rotation=90) 
    ax.invert_yaxis()                                  
    
    # colorbar label settings
    #get seaborn cbar object
    cbar_ax = plt.gcf().axes[-1]                        
    #formats cbar label
    cbar_ax.set_ylabel(cbar_label, rotation=90, size=cbar_labelsize) 
    #formats cbar ticks    
    cbar_ax.tick_params(labelsize=cbar_ticksize, rotation=cbar_tick_rot)  
    #formats cbar scale    
    cbar_ax.yaxis.get_offset_text().set(size=cbar_ticksize)
    #positions cbar scale
    cbar_ax.yaxis.set_offset_position('left')           
    return

SAMPLE = 'NBL33'
SCAN = 1
CHANNELS = ['XBIC_lockin', 'Cu_K', 'Cd_L3']
META_DATA = get_scan_metadata(PATH, SAMPLE, SCAN)
ROTATION = 0

dfs = import_xSect_csvs(PATH, SAMPLE, SCAN, CHANNELS, META_DATA, ROTATION)

PLOT_CHANNEL_IDX = 1
PLOT_CHANNEL = dfs[PLOT_CHANNEL_IDX]
FULL_YRANGE = np.max(np.max(PLOT_CHANNEL))
plot_NBL3_xsect(PLOT_CHANNEL, (2,2), 'Oranges_r', [0,30000],
                50, 14,
                [0,17], 14, 90, 
                [0,30], 14, 90,
                '(a.u.)', 16,14, 0)

#%%
def export_integrated_dfs(imp_rot_dfs):
    integrated_arrays_of_each_channel = []
    x = imp_rot_dfs[0].columns.values
    x = x.reshape(-1,1)
    for df in imp_rot_dfs:
        y_integrate = df.sum(axis=0)        #df
        y_integrate = y_integrate.to_numpy()
        y_integrate = y_integrate.reshape(-1,1)
        integrated_arrays_of_each_channel.append(y_integrate)
    integrated_arrays_of_each_channel.insert(0, x)
    arrays = np.concatenate(integrated_arrays_of_each_channel, axis=1)
    return arrays

arrays = export_integrated_dfs(dfs)
#np.savetxt(r'C:\Users\Trumann\Dropbox (ASU)\1_NBL3 data\py_' + sample +"_Scan"+ str(scannum) + '.csv', arrays, delimiter = ',')
