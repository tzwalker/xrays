'''
created: Fri Aug 16 14:49:13 2019
author: Trumann

this file plots the original data with or without correct;
    original nans of the h5 file
    vmin and max of cbar calculated from data
useful for element plots!
'''

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import z_plot_supplement as plt_supp

def plot_nice_2Dmap(samp,scan,label_sizes, data_channel, ele_index):
    c_scan = samp['XBIC_h5s'][scan]  # h5 always has coordinates
    x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
    y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
    x_real = plt_supp.get_real_coordinates(x_axis)
    y_real = plt_supp.get_real_coordinates(y_axis)
    
    if ele_index == -1:             
        c_map = samp[data_channel][scan];
        c_map = c_map / c_map[:,:-2].max()
        colors = 'magma'; units = '% Max Current'
    else: 
        c_map = samp[data_channel][scan][ele_index];
        #c_map = c_map / c_map[:,:-2].max()
        colors = 'Oranges_r'; units = '\u03BCg/cm'+ r'$^{2}$'
    
    lower,upper = plt_supp.get_colorbar_axis(c_map, 3) # int here sets num_of_std to include
    df_map = pd.DataFrame(c_map, index = y_real, columns = x_real)
    fig, ax0 = plt.subplots()
    ax0 = sns.heatmap(df_map, square = True, cmap = colors,
                      xticklabels = 20, yticklabels = 20,
                      cbar_kws={"shrink": 1.0, 'format': '%.2f'}, vmin=lower, vmax=upper)
    # figure level
    plt.xlabel('X (\u03BCm)', fontsize=axis_label_sizes)
    plt.ylabel('Y (\u03BCm)', fontsize=axis_label_sizes)
    #plt.title(samp['Name'], fontsize=axis_label_sizes)
    # axis level
    ax0.tick_params(labelsize = 14)                     #formats size of ticklabels
    x_labls = plt_supp.custom_format_ticks(ax0.get_xticklabels(), '{:g}')
    y_labls = plt_supp.custom_format_ticks(ax0.get_yticklabels(), '{:g}')         #formats tick label strings without ".0"
    ax0.set_xticklabels(x_labls)                        #set the tick labels
    ax0.set_yticklabels(y_labls, rotation = 0)          #set the ticklabels and rotate (if needed)
    ax0.invert_yaxis()                                  #invert the yaxis after formatting is complete
    
    #fig.colorbar(ax0).ax0 <--> plt.gcf().axes[-1]
    cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y axes object
    # colorbar label settings
    cbar_ax.set_ylabel(units, fontsize = axis_label_sizes, 
                       rotation = 90, labelpad = 10)   #label formatting
    cbar_ax.tick_params(labelsize=12)                   #tick label formatting
    cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
    cbar_ax.yaxis.set_offset_position('left')           #scale at top of colorbar (i.e. 'offset') position
    #cbar_ax.set_yticklabels(custom_format_ticks(cbar_ax.get_yticklabels(), '{:.2f}'))
    return 

samp = NBL3_3
scan = 2
axis_label_sizes = 16
plot_nice_2Dmap(samp, scan, axis_label_sizes, 'elXBIC_corr', 0) # -1: electrical, 0,1,etc. for elements

