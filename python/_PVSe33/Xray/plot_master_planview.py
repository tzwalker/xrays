"""
coding: utf-8

tzwalker
Wed Sep  1 08:30:39 2021

this program plots cross-section maps with different xy scales
run this program after 'main-PVSe33-ASCII-xsect'
the cross-section maps are for PVSe33

#for PVS33 
    plan-view (2020_10_26IDC): 25px = 4um
    window cross-section(2021_07_2IDD): 
        0hr scan72:     x, 1px = 160nm - y, 1px = 160nm
        500hr scan114:  x, 1px = 160nm - y, 1px = 160nm
    infinite cross-section(2021_07_2IDD): 
        0hr scan119:    x, 1px = 100nm - y, 1px= = 1um
        500hr scan151:  x, 1px = 160nm - y, 1px = 160nm
    

# cmaps: 
    #RdYlGn 
    #inferno 
    #Greys_r
    #Blues_r
    #viridis
    #Oranges_r
    #YlOrBr_r
"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker
import numpy as np

SAVE = 1
#OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\20210625 figures_v1\figure4 materials'
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33 XRF maps'
FNAME = r'\0hr_scan0011_XBIC.eps'

# channel
idx = 0

img = df_maps[idx]
img = img.to_numpy()
img = img[:-50,:-52]

if idx ==0:
    unit = 'XBIC (arb. unit)'; colormap='inferno'; low=0.6; high=1
if idx == 1:
    unit = 'Cu (cts/s)'; colormap = 'Oranges_r'; low = 10; high = 18
if idx == 2:
    unit = 'Cd (cts/s)'; colormap = 'Blues_r'; low = 2e1; high = 2e2
if idx == 3:
    unit = 'Te (cts/s)'; colormap = 'Greys_r'; low = 2e1; high = 2e2
if idx == 4:
    unit = 'Au (cts/s)'; colormap = 'YlOrBr_r'; low = 2e1; high = 2e2
if idx == 5:
    unit = 'Cl (cts/s)'; colormap = 'viridis'; low = 0; high = 7
    
cbar_txt_size = 11

fig, ax = plt.subplots(figsize=(2,2))

plt.locator_params(axis='x', nbins=4)
plt.locator_params(axis='y', nbins=4)
fmtr_x = lambda x, pos: f'{(x * 0.160):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.160):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)')
ax.set_ylabel('$Y$ (μm)')

im = ax.imshow(img, cmap=colormap, origin='lower', vmin=low, vmax=high)

# define colorbar format
# =============================================================================
# divider = make_axes_locatable(ax)
# cax1 = divider.new_vertical(size='5%', pad=0.1)
# fig.add_axes(cax1)
# 
# cbar = fig.colorbar(im, cax=cax1, orientation='horizontal')
# cbar.set_label(unit, fontsize=cbar_txt_size)
# cbar.ax.tick_params(labelsize=cbar_txt_size)
# cax1.xaxis.set_label_position('top')
# cax1.xaxis.set_ticks_position('top')
# =============================================================================
cax1 = fig.add_axes([ax.get_position().x1+0.05,ax.get_position().y0,0.05,ax.get_position().height])
fig.colorbar(im,cax=cax1)
#color bar labels
cbar = plt.gcf().axes[-1]
cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
    #change color bar scale label position 
cbar.yaxis.set_offset_position('left')

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)
    
#%%
SAVE = 1
#OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\20210625 figures_v1\figure4 materials'
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33 XRF maps'
FNAME = r'\500hr_scan0148_XBIC.eps'

# channel
idx = 0

img = df_maps[idx]
img = img.to_numpy()
img = img[:,:-2]

if idx ==0:
    unit = 'XBIC (arb. unit)'; colormap='inferno'; low=0.6; high=1
if idx == 1:
    unit = 'Cu (cts/s)'; colormap = 'Oranges_r'; low = 4; high = 12
if idx == 2:
    unit = 'Cd (cts/s)'; colormap = 'Blues_r'; low = 2e1; high = 2e2
if idx == 3:
    unit = 'Te (cts/s)'; colormap = 'Greys_r'; low = 2e1; high = 2e2
if idx == 4:
    unit = 'Au (cts/s)'; colormap = 'YlOrBr_r'; low = 2e1; high = 2e2
if idx == 5:
    unit = 'Cl (cts/s)'; colormap = 'viridis'; low = 0; high = 7
    
cbar_txt_size = 11

fig, ax = plt.subplots(figsize=(2,2))

plt.locator_params(axis='x', nbins=4)
plt.locator_params(axis='y', nbins=4)
fmtr_x = lambda x, pos: f'{(x * 0.160):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.160):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)')
ax.set_ylabel('$Y$ (μm)')

im = ax.imshow(img, cmap=colormap, origin='lower', vmin=low, vmax=high)

# define colorbar format
# =============================================================================
# divider = make_axes_locatable(ax)
# cax1 = divider.new_vertical(size='5%', pad=0.1)
# fig.add_axes(cax1)
# 
# cbar = fig.colorbar(im, cax=cax1, orientation='horizontal')
# cbar.set_label(unit, fontsize=cbar_txt_size)
# cbar.ax.tick_params(labelsize=cbar_txt_size)
# cax1.xaxis.set_label_position('top')
# cax1.xaxis.set_ticks_position('top')
# =============================================================================
cax1 = fig.add_axes([ax.get_position().x1+0.05,ax.get_position().y0,0.05,ax.get_position().height])
fig.colorbar(im,cax=cax1)
#color bar labels
cbar = plt.gcf().axes[-1]
cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
    #change color bar scale label position 
cbar.yaxis.set_offset_position('left')

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)