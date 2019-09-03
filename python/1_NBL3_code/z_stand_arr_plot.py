# -*- coding: utf-8 -*-
"""
created: Fri Aug 16 14:49:13 2019
author: Trumann

this file is used to plto standardized data;
    take standardized arrays, shapes them,
    adds two nan columns for prettiness
useful for XBIC data mostly!
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import z_plot_supplement as plt_supp 
from put_nans_back_on import put_nans_back_on

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
    x_real = plt_supp.get_real_coordinates(x_axis)
    y_real = plt_supp.get_real_coordinates(y_axis)
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
    x_labls = plt_supp.custom_format_ticks(ax0.get_xticklabels(), '{:g}')
    y_labls = plt_supp.custom_format_ticks(ax0.get_yticklabels(), '{:g}')         #formats tick label strings without ".0"
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

sample = TS58A
scan = 0
channel = 0 #0:XBIC, 1:Cu, 2:Cd (match to index in elements in)
data = 'c_stand_arrs'
from_stand_to_stand_map(sample, scan, data, channel)