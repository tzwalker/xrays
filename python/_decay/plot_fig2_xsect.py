# -*- coding: utf-8 -*-
"""

Trumann
Mon May  9 11:26:47 2022

run "main-TS118_1A-ASCII_xsect.py" before this program, shoudl be in pA

this program plots the degradation study line scan and dwell point positions
on scan275 of 2018_11_26IDC

see also the file 
Dropbox (ASU)\1_XBIC_decay\positions of cross-section degradation linescans.xlsx

"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable

SAVE = 1
img = data_shape[:,:].copy()
cbar_txt_size = 11
#cbar_pad = -2.25
#fisizetuple = (4,4)

cbar_pad = -3.5

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_XBIC_decay\20220507 figures v2\figure2 materials'
FNAME = r'\scan275_linescan_dwell_positions_marked1.1.eps'

fig, ax = plt.subplots()

im = ax.imshow(img, cmap='inferno', origin='lower',vmin=0,vmax=50)

# this aspect is the physical y hieght (~40um) over the physical x width (~10um)
ax.set_aspect(10) 

# plot the linescan positions (original image)
plt.axhline(39,color='w',linestyle='dashed', linewidth=1) # Max XBIC
#plt.axhline(35,color='w',linestyle='dashed', linewidth=1) # Au-CdTe
#plt.axhline(31,color='w',linestyle='dashed', linewidth=1) # Max XBIC
#plt.axhline(27,color='w',linestyle='dashed', linewidth=1) # CdTe-Au
plt.axhline(23,color='w',linestyle='dashed', linewidth=1) # CdTe
#plt.axhline(19,color='w',linestyle='dashed', linewidth=1) # Max XBIC
plt.axhline(15,color='w',linestyle='dashed', linewidth=1) # Au
plt.axhline(33,color='w',linestyle='dashed', linewidth=1) # TCO

# =============================================================================
# # plot the linescan positions (cropped image)
# plt.axhline(29,color='w',linestyle='dashed', linewidth=1) # Max XBIC
# #plt.axhline(35,color='w',linestyle='dashed', linewidth=1) # Au-CdTe
# #plt.axhline(31,color='w',linestyle='dashed', linewidth=1) # Max XBIC
# #plt.axhline(27,color='w',linestyle='dashed', linewidth=1) # CdTe-Au
# plt.axhline(13,color='w',linestyle='dashed', linewidth=1) # CdTe
# #plt.axhline(19,color='w',linestyle='dashed', linewidth=1) # Max XBIC
# plt.axhline(5,color='w',linestyle='dashed', linewidth=1) # Au
# plt.axhline(23,color='w',linestyle='dashed', linewidth=1) # TCO
# =============================================================================

# plot the dwell points
x_coord = [97,65,46,58]
#original indices
y_coord = [15,23,33,39]

#cropped map indices
#y_coord = [5,13,23,29]

plt.scatter(x_coord, y_coord, color='white', s=10)

fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
fmtr_y = lambda x, pos: f'{(x * 1):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)')
ax.set_ylabel('$Y$ (μm)')

divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='1.5%', pad=cbar_pad)

# for infinite cross sections
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 1))
#cb = fig.colorbar(im, cax=cax, orientation='vertical', format=fmt)
# for lamella
cb = fig.colorbar(im, cax=cax, orientation='vertical')
cb.ax.tick_params(labelsize=cbar_txt_size)
cbar = plt.gcf().axes[-1]
cbar.set_ylabel("XBIC (pA)", rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
cbar.yaxis.set_tick_params(labelsize=cbar_txt_size)
cbar.yaxis.set_offset_position('left')

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)