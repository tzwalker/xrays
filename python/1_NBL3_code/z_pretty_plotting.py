import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

def plot_nice_2Dmap(samp,scan,label_sizes, data_channel, ele_index):
    c_scan = samp['XBIC_h5s'][scan]  # h5 always has coordinates
    x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
    y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
    x_real = get_real_coordinates(x_axis)
    y_real = get_real_coordinates(y_axis)
    
    if ele_index == -1: 
        c_map = samp[data_channel][scan]; 
        colors = 'magma'; units = 'A'
    else: 
        c_map = samp[data_channel][scan][ele_index]; 
        colors = 'Oranges_r'; units = '\u03BCg/cm'+ r'$^{2}$'
    
    df_map = pd.DataFrame(c_map, index = y_real, columns = x_real)
    fig, ax0 = plt.subplots()
    ax0 = sns.heatmap(df_map, square = True, cmap = colors,
                      xticklabels = 20, yticklabels = 20,
                      cbar_kws={"shrink": 1.0})
    # figure level
    plt.xlabel('X (\u03BCm)', fontsize=axis_label_sizes)
    plt.ylabel('Y (\u03BCm)', fontsize=axis_label_sizes)
    plt.title(samp['Name'], fontsize=axis_label_sizes)
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
    cbar_ax.set_ylabel(units, fontsize = axis_label_sizes, 
                       rotation = 90, labelpad = 10)   #label formatting
    cbar_ax.tick_params(labelsize=12)                   #tick label formatting
    cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
    cbar_ax.yaxis.set_offset_position('left')           #scale at top of colorbar (i.e. 'offset') position
    
    return 

samp = NBL3_2
scan = 0
axis_label_sizes = 16
plot_nice_2Dmap(samp, scan, axis_label_sizes, 'elXBIC', 0) # -1: electrical, 0,1,etc. for elements

