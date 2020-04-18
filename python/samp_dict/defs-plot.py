# -*- coding: utf-8 -*-
"""
created: Fri Aug 16 15:14:52 2019
author: Trumann
"""
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

# usefeul function for visualizing standardized data as a map
# puts two nan columns back on standardized arrays
def put_nans_back_on(array, y_coord, x_coord):
    # reshape standardized array with two missing nan columns
    slim_map = np.reshape(array, (len(y_coord), len(x_coord)-2), order='F') 
    # make two nan columns matching the size of the standardized array
    nans_to_attach = np.full((np.size(slim_map, axis=0),2), np.nan)
    # attach the nan columns to the standardized array
    nan_map = np.append(slim_map, nans_to_attach, 1)
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

def from_stand_to_stand_map(samp, scan, data, channel,colormap, units):
    c_scan = samp['XBIC_h5s'][scan]  # h5 always has coordinates
    x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
    y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
    # retrieve physcial axis scale from h5
    x_real = get_real_coordinates(x_axis)
    y_real = get_real_coordinates(y_axis)
    c_map = samp[data][scan][:,channel]
    
    # replace nan columns
    c_map = put_nans_back_on(c_map, y_real, x_real)
    
    df_map = pd.DataFrame(c_map, index = y_real, columns = x_real)
    fig, ax0 = plt.subplots()
    # vmin and vmax only need to go to +/-3 for standardized maps...
    ax0 = sns.heatmap(df_map, square = True, cmap = colormap,
                      xticklabels = 20, yticklabels = 20, vmin=-3, vmax=3)
    return

def plot_cluster_map(scan_data, original_map, model, cnum):
    x = scan_data['/MAPS/x_axis'];      y = scan_data['/MAPS/y_axis']
    x_real = get_real_coordinates(x);   y_real = get_real_coordinates(y)
    
    clust_map = model.reshape(np.shape(original_map), order='F')
    clust_nan_map = put_nans_back_on(clust_map, y_real, x_real)
    df_map = pd.DataFrame(clust_nan_map, index=y_real, columns=x_real)
    
    cbar_format={'ticks': list(list(np.linspace(0,cnum,cnum+1)))}
    fig, ax = plt.subplots(1)
    ax = sns.heatmap(df_map, square=True, cmap='Greys', cbar_kws=cbar_format, 
                xticklabels=20, yticklabels=20)
    ax.invert_yaxis()
    
    plt.xlabel('X (\u03BCm)', fontsize=16)
    plt.ylabel('Y (\u03BCm)', fontsize=16)
    
    x_labls = custom_format_ticks(ax.get_xticklabels(), '{:g}')
    y_labls = custom_format_ticks(ax.get_yticklabels(), '{:g}')
    ax.set_xticklabels(x_labls, fontsize=14)
    ax.set_yticklabels(y_labls, rotation=0, fontsize=14)
    
    cbar_ax = plt.gcf().axes[-1]
    cbar_ax.set_ylabel('Cluster #', fontsize=16, labelpad = 10)
    cbar_ax.tick_params(labelsize=12)
    return


def map_to_hist(samp,scan,label_sizes, data_channel, ele_index, bins):
    map_data = samp[data_channel][scan][ele_index]
    map_distro = plt.hist(map_data.ravel(), bins=50)
    plt.xlabel('ug/cm2')
    plt.ylabel('pixel count')
    return

# only used with standardized data (both XRF and XBIC)
def plot_nice_superpixels_from_h5(samp, scan, img, colormap):
    c_scan = samp['XBIC_h5s'][scan]  # h5 always has coordinates
    x_axis = c_scan['/MAPS/x_axis']  # x position of pixels  [position in um]
    y_axis = c_scan['/MAPS/y_axis']  # y position of pixels  [position in um]
    x_real = get_real_coordinates(x_axis)
    y_real = get_real_coordinates(y_axis)    
    c_map = put_nans_back_on(img, y_real, x_real)
    
    df_map = pd.DataFrame(c_map, index = y_real, columns = x_real)
    fig, ax0 = plt.subplots()
    ax0 = sns.heatmap(df_map, square = True, cmap=colormap,
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
    cbar_ax.set_ylabel("Stand. Intensity (a.u.)", fontsize =16, 
                       rotation = 90, labelpad = 10)   #label formatting
    cbar_ax.tick_params(labelsize=12)                   #tick label formatting
    cbar_ax.yaxis.get_offset_text().set(size=12)        #format colorbar offset text
    cbar_ax.yaxis.set_offset_position('left')           #scale at top of colorbar (i.e. 'offset') position
    #cbar_ax.set_yticklabels(custom_format_ticks(cbar_ax.get_yticklabels(), '{:.2f}'))
    return

# prelim spearman correlation matrix plot defs #
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


def get_corrmtx_plot(array, cols, f, axis, annotate):
    df = pd.DataFrame(array, columns=cols, index=cols)
    sns.set(style="white") # set style of seaborn objects
    mask = np.zeros_like(df, dtype=np.bool) # make mask of symmetric portion
    mask[np.triu_indices_from(mask)] = True # apply mask
    sns.heatmap(df, mask=mask, cbar_kws=f['cbar_format'], ax=axis,
                     cmap=f['color'], annot=annotate, 
                     vmin=f['v_range'][0], vmax=f['v_range'][1])
    axis.title.set_text(f['plt_title'])
    return
