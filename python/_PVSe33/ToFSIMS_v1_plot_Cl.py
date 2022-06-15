# -*- coding: utf-8 -*-
"""

Trumann
Wed Jun 15 10:11:04 2022


"""

'''
this cell plots integrated plan-view maps for use in my dissertation

'''

from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec

SAVE = 1
unit = 'Cl (cts/s)'

file1 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps.tif"
file2 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_maps.tif"

cbar_txt_size = 11

# import ToF-SIMS images
imgs1 = io.imread(file1)
imgs2 = io.imread(file2)

# integrate along depth
img1 = imgs1.sum(axis=0)
img2 = imgs2[7:,:,:].sum(axis=0) # integrate over same # of slices as 0hr

# integrate along height
img3 = imgs1.sum(axis=1)
img3 = np.flipud(img3)

img4 = imgs2[7:,:,:].sum(axis=1) # integrate over same # of slices as 0hr
img4 = np.flipud(img4)

# set up figure
fig = plt.figure()
gs = GridSpec(2, 2, figure=fig, height_ratios=[3.5,1], hspace=0.3)

# 0hr plan-view
ax1 = fig.add_subplot(gs[0, 0])
# 500hr plan-view
ax2 = fig.add_subplot(gs[0, 1])

##### plot 0hr plan-view #####
im1 = ax1.imshow(img1, origin='lower', cmap = 'viridis',vmin=0,vmax=30)

ax1.xaxis.set_ticks(np.arange(0,513,102))
ax1.yaxis.set_ticks(np.arange(0,513,102))
fmtr_x = lambda x, pos: f'{(x * 0.145):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.145):.0f}'
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
#ax1.set_xlabel('$X$ (μm)')
ax1.set_ylabel('$Y$ (μm)')

#### plot 500hr plan-view #####
im2 = ax2.imshow(img2, origin='lower', cmap = 'viridis',vmin=0,vmax=30)

ax2.xaxis.set_ticks(np.arange(0,513,102))
ax2.yaxis.set_ticks(np.arange(0,513,102))
fmtr_x = lambda x, pos: f'{(x * 0.145):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.145):.0f}'
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
#ax2.set_xlabel('$X$ (μm)')
#ax2.set_ylabel('$Y$ (μm)')

# define colorbar format
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cax2 = fig.add_axes([ax2.get_position().x1+0.025,ax2.get_position().y0,0.025,ax2.get_position().height])

#format and add colorbar
fig.colorbar(im2,cax=cax2)#, format=fmt)
#color bar labels
cbar2 = plt.gcf().axes[-1]
cbar2.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
#change color bar scale label position 
cbar2.yaxis.set_offset_position('left')

#plt.tight_layout()

# 0hr plan-view
ax3 = fig.add_subplot(gs[1, 0])
# 500hr plan-view
ax4 = fig.add_subplot(gs[1, 1])

##### plot 0hr cross-section #####
im3 = ax3.imshow(img3, origin='lower', cmap = 'viridis', norm=LogNorm(vmin=10, vmax=1000))
ax3.set_aspect(3)
ax3.xaxis.set_ticks(np.arange(0,513,102))
#ax3.yaxis.set_ticks(np.arange(0,50,20))

fmtr_x = lambda x, pos: f'{(x * 0.145):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.110):.0f}'
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax3.set_xlabel('$X$ (μm)')
ax3.set_ylabel('$Z$ (μm)')

##### plot 500hr cross-section #####
im4 = ax4.imshow(img4, origin='lower', cmap = 'viridis', norm=LogNorm(vmin=10, vmax=1000))
ax4.set_aspect(3)
ax4.xaxis.set_ticks(np.arange(0,513,102))
#ax4.yaxis.set_ticks(np.arange(0,50,20))

fmtr_x = lambda x, pos: f'{(x * 0.145):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.135):.0f}'
ax4.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax4.set_xlabel('$X$ (μm)')

# define colorbar format
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cax4 = fig.add_axes([ax4.get_position().x1+0.025,ax4.get_position().y0,0.025,ax4.get_position().height])

#format and add colorbar
fig.colorbar(im4,cax=cax4)#, format=fmt)
#color bar labels
cbar4 = plt.gcf().axes[-1]
cbar4.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
#change color bar scale label position 
cbar4.yaxis.set_offset_position('left')

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_tof_sims'
FNAME = r'\Cl_maps_xy_xz_v2.eps'
if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)