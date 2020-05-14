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

used for both First Solar and NBL3 images
"""

# =============================================================================
# import matplotlib.pyplot as plt  
# 
# def export_to_ImgJ_planview(path, shaped_data, color, name, 
#                              scan,dpi, save):
#     fig, ax = plt.subplots()
#     #plt.figure(frameon=False)
#     x_dim = shaped_data.shape[1] ; y_dim = shaped_data.shape[0]
#     fig.set_size_inches(x_dim/dpi, y_dim/dpi)    
#     ax = fig.add_axes([0, 0, 1, 1])
#     ax.set_axis_off()
#     ax.imshow(shaped_data, cmap=color)
#     if save == 1:
#         fname = r'\scan{s}_{ele}.png'.format(s=scan,ele=name)
#         directory= path+fname
#         plt.savefig(directory, dpi=dpi)
#     else: pass
#     return
# 
# PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\for_imagej'
# 
# SAMPLE= NBL33; SCAN = 4; CHAN = 0
# MAP_OUT = SAMPLE.maps[SCAN][CHAN,:,:-2]
# scanstr = str(SAMPLE.scans[SCAN])
# NAMES = ['XBIV', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
# CMAPS = ['inferno', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
# # export to imagej #
# export_to_ImgJ_planview(PATH, MAP_OUT, CMAPS[CHAN], NAMES[CHAN],
#                          scan=scanstr,dpi=96, save=1)
# 
# def export_to_ImgJ_crosssection(path, data, color, name, 
#                              dpi, save):
#     shape=np.shape(data)[0:2][::-1]
#     size = [float(i)/dpi for i in shape]
# 
#     fig = plt.figure()
#     fig.set_size_inches(size)
#     ax = plt.Axes(fig,[0,0,1,1])
#     ax.set_axis_off()
#     fig.add_axes(ax)
#     ax.imshow(data, extent=(0,100,0,200), cmap=color)
#     ax.axes.get_xaxis().set_visible(False)
#     ax.axes.get_yaxis().set_visible(False)
#     ax.set_frame_on(False)
#     if save == 1:
#         fname = r'\{ele}.png'.format(ele=name)
#         directory= path+fname
#         plt.savefig(directory,bbox_inches='tight', pad_inches=0, dpi=dpi)
#     else: pass
#     return
# 
# PATH = r'Z:\Trumann\XRF images\cross section'
# 
# MAP_OUT = dfs[0]
# NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
# CMAPS = ['inferno', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
# # export to imagej #
# export_to_ImgJ_crosssection(PATH, MAP_OUT, 'inferno', 'NBL31_scan8_XBIC',
#                          dpi=96, save=1)
# 
# # trying to plot XBIC and Cu cross sections
# # with same dimensions as the Origin figure of
# # integrate ddepth profiles
# 
# # note run 'NBLxsect home.py' before running this code
# # [dfs[0].columns[:-45]] is to chop off columns of the map
# def cm2inch(*tupl):
#     inch = 2.54
#     if isinstance(tupl[0], tuple):
#         return tuple(i/inch for i in tupl[0])
#     else:
#         return tuple(i/inch for i in tupl)
# PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\vector graphics and figures'
# FNAME = r'\NBL31scan8_full.eps'
# PATH_OUT = PATH +FNAME 
# 
# fig, axs = plt.subplots(2,1, figsize=(cm2inch(3.5,3.5)))
# plt.tight_layout(pad=-10)
# XBIC = dfs[0]#[dfs[0].columns[:-45]]
# axs[0].imshow(XBIC, cmap='inferno',extent=(0,300,0,100))
# axs[0].axis('off')
# Cu = dfs[1]#[dfs[1].columns[:-45]]
# axs[1].imshow(Cu, cmap='Greys_r', extent=(0,300,0,100), vmax=3000)
# axs[1].axis('off')
# plt.savefig(PATH_OUT, format='eps', bbox_inches='tight')
# =============================================================================

import numpy as np
# save FS3 operando XBIV vs. Temp
# this code will show axes in spyder, but the exported image
# will have no axes in the image
# and will ahve the same pixels as the original array
# i.e. this code WORKS despite what is shown in the spyder plot window

PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\for_imagej\TS58A'
FNAME = r'\scan383_XBIV.txt'
PATH_OUT = PATH + FNAME
ARR_OUT = TS58A.scan383[0,:,:-2]
DPI=96

fig, ax = plt.subplots()
XDIM = ARR_OUT.shape[1] ; YDIM = ARR_OUT.shape[0]
fig.set_size_inches(XDIM/DPI, YDIM/DPI)    
ax = fig.add_axes([0, 0, 1, 1])

ax.imshow(ARR_OUT, cmap='inferno')
ax.set_axis_off()
#plt.savefig(PATH_OUT, dpi=DPI)

np.savetxt(PATH_OUT, ARR_OUT)

# =============================================================================
# import matplotlib.pyplot as plt
# import numpy as np  
# 
# def export_to_ImgJ_samp_dict(path, sample, scan_idx, shaped_data, ch_idx, color, name, 
#                              dpi, resize_fact, save):
#     plot=sample[shaped_data][scan_idx][ch_idx,:,:-2]
#     fig = plt.figure(frameon=False)
#     fig.set_size_inches(plot.shape[1]/(dpi*resize_fact), plot.shape[0]/(dpi*resize_fact))
#     ax = plt.Axes(fig, [0., 0., 1., 1.])
#     ax.set_axis_off()
#     fig.add_axes(ax)
#     ax.imshow(plot, cmap=color)
#     if save == 1:
#         fname = r'\{samp}_scan{num}_{ele}.png'.format(
#                 samp=sample['Name'], 
#                 num=str(sample['XBIC_scans'][scan_idx]), 
#                 ele=name)
#         directory= path+fname
#         plt.savefig(directory, dpi=(dpi * resize_fact))
#     else: pass
#     return
# 
# PATH = r'Z:\Trumann\XRF images\py_exports_bulk\NBL3_3\scan491'
# NAMES = ['XBIC', 'Cu', 'Cd', 'Te', 'Mo', 'Zn']
# CMAPS = ['inferno', 'Oranges_r', 'Blues_r', 'Greens_r', 'Reds_r', 'Greys_r']
# SAMPLE= NBL3_3; SCAN = 4; CHAN = 0
# # export to imagej #
# export_to_ImgJ_samp_dict(PATH, SAMPLE, SCAN, 'XBIC_maps', CHAN, CMAPS[CHAN], NAMES[CHAN],
#                          dpi=96, resize_fact=0.5, save=0)
# =============================================================================
