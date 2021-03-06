# -*- coding: utf-8 -*-
"""
created: Tue Aug 13 11:25:24 2019
author: Trumann
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.transform import rotate

def get_scan_metadata(path, sample, scannum):
    metafile_string = '\CdTe_X_' + sample + '_Scan_' + str(scannum) + '_Metadata.csv'
    metafile = path + metafile_string
    # import metadata
    df = pd.read_csv(metafile, header=None)
    # make new names from labels in 1st column
    new_names = [name[0:6] for name in df[0]] 
    # to put labels in first row, transpose df 
    df = df.T
    # using labels in 1st row, make column headers                     
    df.columns = df.iloc[0]
    # remove first row         
    df = df.reindex(df.index.drop(0))   
    # rename column headers with short names
    df.rename(columns = {old:new for old, new in zip(df.columns.values, new_names)}, inplace=True) 
    return df

def get_axes_from_metadata(data_df, units_df):
    old_x = data_df.columns.values                      # get column labels in data df (type: numpy array)
    # scale indices according to axis step 
        # cast to float from string, 
        # and cast to list to prep for rounding
    x_real = list(old_x * float(units_df['xstep ']))    
    x_round = [round(i,3) for i in x_real] # round off axis units
    # same for y
    old_y = data_df.index.values
    y_real = list(old_y * float(units_df['ystep ']))
    y_round = [round(i,2) for i in y_real] # round off axis units
    
    data_df.rename(columns = {old:new for old,new in zip(old_x, x_round)},
                              index = {old:new for old,new in zip(old_y, y_round)}, inplace=True)
    return 

def import_xSect_csvs(path, sample, scannum, channels, meta, rot):
    rot_dfs = []
    for chan in channels:
        str_scannum = str(scannum)
        file_string = '\CdTe_X_{s}_Scan_{n}_{c}_data.csv'.format(s=sample,
                                                                 n=str_scannum,
                                                                 c=chan)
        file = path + file_string
        # import scan
        df = pd.read_csv(file, header=None)  
        # rotate image
        rot_nparray = rotate(df, rot) 
        # numpy array to df
        rot_df = pd.DataFrame(rot_nparray) 
        #set column/row(index) headers to real units
        get_axes_from_metadata(rot_df, meta) 
        # build imported list
        rot_dfs.append(rot_df) 
    return rot_dfs

def custom_format_ticks(axes_object_labels, string_type):
    txt_labs = [label.get_text() for label in axes_object_labels]
    ticking = [string_type.format(float(txt)) for txt in txt_labs]
    return ticking

def plot_2D_xSect(imp_rot_dfs, ch_units, colors):
    fig, axes = plt.subplots(1,3)
    plt.tight_layout()
    for df, axis, un, color in zip(imp_rot_dfs, axes, ch_units, colors):
        ch_max = df.values.max()
        sns.heatmap(df, vmax=ch_max, xticklabels=20, yticklabels=4, cmap=color, ax=axis)#, cbar_kws={'format': '%.0g'})
        x_labls = custom_format_ticks(axis.get_xticklabels(), '{:.0f}')
        y_labls = custom_format_ticks(axis.get_yticklabels(), '{:.0f}')         #formats tick label strings without ".0"
        axis.set_xticklabels(x_labls)                        #set the tick labels
        axis.set_yticklabels(y_labls, rotation = 0)          #set the ticklabels and rotate (if needed)
        axis.invert_yaxis()                                  #invert the yaxis after formatting is complete
        
        cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y axes object
        # colorbar label settings
        cbar_ax.set_ylabel(un, rotation = 90)               #label formatting
        #cbar_ax.tick_params(labelsize=12)                   #tick label formatting
        #cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
        cbar_ax.yaxis.set_offset_position('left')           #scale at top of colorbar (i.e. 'offset') position
        if un == 'A':
            pass
        else:
            short_cbar_labls = ['{:,.0f}'.format(x) + 'K' for x in cbar_ax.get_yticks()/1000]
            cbar_ax.set_yticklabels(short_cbar_labls)
    fig.tight_layout(pad=0, h_pad=0.25, w_pad=0)
    return

def plot_integrated_line_scans(imp_rot_dfs, colors):
    fig, ax0 = plt.subplots()
    for index, (df,color) in enumerate(zip(imp_rot_dfs, colors)):
        if index == 0:
            ax0.plot(x_position, y_integrate, color=color)
            plt.ylim([0, max(y_integrate)*1.1])
            #y_labls = custom_format_ticks(ax0.get_yticklabels(), '{:.1e}')
            #ax0.set_yticklabels(y_labls)
        else:
            pass
            #ax1=ax0.twinx()
            #ax1.plot(x_position, y_integrate, color=color)
            #plt.ylim([0,1e7])
        plt.xlim([0, max(df.columns.values)])
        ax0.grid()
    return
#line_colors = ['tab:blue', 'tab:orange', 'tab:green']
#plot_integrated_line_scans(imported_rotated_dataframes, line_colors)