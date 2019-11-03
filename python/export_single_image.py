"""
tzwalker
Sat Nov  2 17:35:04 2019
coding: utf-8

Export image of map of interest
Don't forget to load data into workspace
"""
import matplotlib.pyplot as plt

path = r'C:\Users\triton\img_processing XRF figs'

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
    plt.savefig(directory, bbox_inches = 'tight', pad_inches = 0)
    return

def overlay(image1, image2, alph):
    fig, ax = plt.subplots()
    ax.imshow(image1)
    ax.imshow(image2, alpha=alph)
    return

export_img(path, TS58A, 5, 'XBIC_corr', 4, 'viridis')
overlay(TS58A['XBIC_maps'][5][3,:,:], TS58A['XBIC_maps'][5][1,:,:], 0.5)
