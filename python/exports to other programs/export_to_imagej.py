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

works for plan-view and cross-section data
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

def export_to_ImgJ_planview(path, shaped_data, color, name, 
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

SAMPLE= NBL31; SCAN = 8; CHAN = 3
MAP_OUT = SAMPLE.maps[SCAN][CHAN,:,:-2]

NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
CMAPS = ['inferno', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
# export to imagej #
export_to_ImgJ_planview(PATH, MAP_OUT, CMAPS[CHAN], NAMES[CHAN],
                         dpi=96, resize_fact=1, save=1)

#%%
import matplotlib.pyplot as plt  

def export_to_ImgJ_crosssection(path, data, color, name, 
                             dpi, save):
    shape=np.shape(data)[0:2][::-1]
    size = [float(i)/dpi for i in shape]

    fig = plt.figure()
    fig.set_size_inches(size)
    ax = plt.Axes(fig,[0,0,1,1])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(data, extent=(0,100,0,200), cmap=color)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    if save == 1:
        fname = r'\{ele}.png'.format(ele=name)
        directory= path+fname
        plt.savefig(directory,bbox_inches='tight', pad_inches=0, dpi=dpi)
    else: pass
    return

PATH = r'Z:\Trumann\XRF images\cross section'

MAP_OUT = dfs[0]
NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
CMAPS = ['inferno', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
# export to imagej #
export_to_ImgJ_crosssection(PATH, MAP_OUT, 'inferno', 'NBL31_scan8_XBIC',
                         dpi=96, save=1)

#%%
# trying to plot XBIC and Cu cross sections
# with same dimensions as the Origin figure of
# integrate ddepth profiles

# note run 'NBLxsect home.py' before running this code
# [dfs[0].columns[:-45]] is to chop off columns of the map
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

fig, axs = plt.subplots(2,1, figsize=(cm2inch(3.5,3.5)))
plt.tight_layout(pad=-10)
XBIC = dfs[0][dfs[0].columns[:-45]]
axs[0].imshow(XBIC, cmap='inferno',extent=(0,300,0,100))
axs[0].axis('off')
Cu = dfs[1][dfs[1].columns[:-45]]
axs[1].imshow(Cu, cmap='Greys_r', extent=(0,300,0,100), vmax=3000)
axs[1].axis('off')
plt.savefig(r'C:\Users\triton\Desktop\NBL3xsect eps figures\NBL31scan8.eps', format='eps', bbox_inches='tight')

