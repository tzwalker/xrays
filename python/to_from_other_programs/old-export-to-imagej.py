"""
coding: utf-8

tzwalker
Mon May 18 09:33:28 2020
"""
import matplotlib.pyplot as plt
import numpy as np  


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
CMAPS = ['inferno', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
SAMPLE= NBL3_3; SCAN = 4; CHAN = 0
# export to imagej #
export_to_ImgJ_samp_dict(PATH, SAMPLE, SCAN, 'XBIC_maps', CHAN, CMAPS[CHAN], NAMES[CHAN],
                         dpi=96, resize_fact=0.5, save=0)