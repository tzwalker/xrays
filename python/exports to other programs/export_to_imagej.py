"""
tzwalker
Sat Nov  2 17:35:04 2019
coding: utf-8

Export image of map of interest
Don't forget to load data into workspace
in export_figure_matplotlib:
    Export array as figure in original resolution
    :param arr: array of image to save in original resolution
    :param f_name: name of file where to save figure
    :param resize_fact: resize facter wrt shape of arr, in (0, np.infty)
    :param dpi: dpi of your screen
    :param plt_show: show plot or not
    
"""

import matplotlib.pyplot as plt
import numpy as np  

def export_to_ImgJ_samp_dict(path, sample, scan_idx, shaped_data, ch_idx, color, name, 
                             dpi, resize_fact, save):
    plot=sample[shaped_data][scan_idx][ch_idx,:,:-2]
    fig = plt.figure(frameon=False)
    fig.set_size_inches(plot.shape[1]/(dpi*resize_fact), plot.shape[0]/(dpi*resize_fact))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(plot, cmap=color)
    if save == 1:
        fname = r'\{samp}_scan{num}_{ele}.png'.format(
                samp=sample['Name'], 
                num=str(sample['XBIC_scans'][scan_idx]), 
                ele=name)
        directory= path+fname
        plt.savefig(directory, dpi=(dpi * resize_fact))
    else: pass
    return

PATH = r'Z:\Trumann\XRF images\py_exports_bulk\NBL3_3\scan491'
NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
CMAPS = ['magma', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
SAMPLE= NBL3_3; SCAN = 4; CHAN = 0
# export to imagej #
export_to_ImgJ_samp_dict(PATH, SAMPLE, SCAN, 'XBIC_maps', CHAN, CMAPS[CHAN], NAMES[CHAN],
                         dpi=96, resize_fact=0.5, save=0)

#%%
import matplotlib.pyplot as plt  

def export_to_ImgJ_samp_dict(path, shaped_data, color, name, 
                             dpi, resize_fact, save):
    fig, ax = plt.subplots()
    #plt.figure(frameon=False)
    fig.set_size_inches(shaped_data.shape[1]/(dpi*resize_fact), shaped_data.shape[0]/(dpi*resize_fact))    
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.imshow(shaped_data, cmap=color)
    if save == 1:
        fname = r'\{ele}.png'.format(ele=name)
        directory= path+fname
        plt.savefig(directory, dpi=(dpi * resize_fact))
    else: pass
    return

PATH = r'Z:\Trumann\XRF images\py_exports_interface\NBL3_1\scan343'

SAMPLE= NBL31; SCAN = 6; CHAN = 3
MAP_OUT = SAMPLE.maps[SCAN][CHAN,:,:-2]

NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
CMAPS = ['magma', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
# export to imagej #
export_to_ImgJ_samp_dict(PATH, MAP_OUT, CMAPS[CHAN], NAMES[CHAN],
                         dpi=96, resize_fact=1, save=1)

#%%
# old definitions #

def overlay(image1, image2, alph):
    fig, ax = plt.subplots()
    ax.imshow(image1)
    ax.imshow(image2, alpha=alph)
    return
#overlay(TS58A['XBIC_maps'][5][3,:,:], TS58A['XBIC_maps'][5][1,:,:], 0.5)

def rgb_to_gray(img):
        grayImage = np.zeros(img.shape)
        #ITU-R 601-2 luma transform
        R = np.array(img[:, :, 0]); R = (R *.299)
        G = np.array(img[:, :, 1]); G = (G *.587)
        B = np.array(img[:, :, 2]); B = (B *.114)
        
        grayImage = img
        Avg = (R+G+B)
        for i in range(3):
           grayImage[:,:,i] = Avg
        return grayImage 
    
def export_img(path, sample,scan_idx, shaped_data,ch_idx,colors):
    plot=sample[shaped_data][scan_idx][ch_idx,:,:-2]
    fig, ax = plt.subplots(1)
    plt.subplots_adjust(0,0,1,1,0,0)
    for ax in fig.axes:
        ax.axis('off')
        ax.margins(0,0)
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
    name_idx = ch_idx - 1
    fname = r'\{samp}_scan{num}_{ele}.png'.format(samp=sample['Name'], num=str(sample['XBIC_scans'][scan_idx]), ele=elements[name_idx][0:2])
    directory= path+fname
    plt.imshow(plot, cmap=colors)
    plt.savefig(directory, bbox_inches = 'tight', pad_inches = 0, dpi=96)
    return