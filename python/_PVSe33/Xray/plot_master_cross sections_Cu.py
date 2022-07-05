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
import matplotlib.ticker as mticker
import numpy as np

SAVE = 0
#OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\20210625 figures_v1\figure4 materials'
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_XANESvP_Cu'
FNAME = r'\0hr_scan1086_Cu.eps'

# channel
idx = 1

img = df_maps[idx]
img = img.to_numpy()
img = img[:101,:-2] # plot only 20um to match 500hr scan 1210

if idx ==0:
    unit = 'XBIC (nA)'; colormap='inferno'; low=0; high=70
if idx == 1:
    unit = 'Cu (cts/s)'; colormap = 'Oranges_r'; low = 8e2; high = 2e3
if idx == 2:
    unit = 'Cd (cts/s)'; colormap = 'Greys_r'; low = 0; high = 2e4
if idx == 3:
    unit = 'Te (cts/s)'; colormap = 'Greys_r'; low = 0; high = 5e3
if idx == 4:
    unit = 'Au (cts/s)'; colormap = 'YlOrBr_r'; low = 0; high = 5e3
if idx == 5:
    unit = 'Sn (cts/s)'; colormap = 'Greens_r'; low = 0; high = 5e3
if idx == 6:
    unit = 'Cl (cts/s)'; colormap = 'viridis'; low = 0; high = 4e2
    
cbar_txt_size = 11

fig, ax = plt.subplots()

#ax.xaxis.set_ticks(np.arange(0,101,11))
#ax.yaxis.set_ticks(np.arange(0,11,2))
#plt.locator_params(axis='x', nbins=6)
#plt.locator_params(axis='y', nbins=5)
fmtr_x = lambda x, pos: f'{(x * 0.200):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.200):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)')
ax.set_ylabel('$Y$ (μm)')

im = ax.imshow(img, cmap=colormap, origin='lower', vmin=low, vmax=high)
# outline possible position of interfaces
plt.axvline(17,color='k',linestyle='-', linewidth=0.5)
plt.axvline(40,color='k',linestyle='-', linewidth=0.5)

# define colorbar format
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

#format and add colorbar
cbar = fig.colorbar(im, format=fmt)
cbar.ax.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
    #change color bar scale label position 
cbar.ax.yaxis.set_offset_position('left')

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)
    
#%%
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

SAVE = 0
#OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\20210625 figures_v1\figure4 materials'
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_XANESvP_Cu'
FNAME = r'\500hr_scan1210_Cu.eps'

# channel
idx = 1

img = df_maps[idx]
img = img.to_numpy()
img = img[:,:-2]

if idx ==0:
    unit = 'XBIC (nA)'; colormap='inferno'; low=0; high=70
if idx == 1:
    unit = 'Cu (cts/s)'; colormap = 'Oranges_r'; low = 8e2; high = 2e3
if idx == 2:
    unit = 'Cd (cts/s)'; colormap = 'Greys_r'; low = 0; high = 2e4
if idx == 3:
    unit = 'Te (cts/s)'; colormap = 'Greys_r'; low = 0; high = 5e3
if idx == 4:
    unit = 'Au (cts/s)'; colormap = 'YlOrBr_r'; low = 0; high = 5e3
if idx == 5:
    unit = 'Sn (cts/s)'; colormap = 'Greens_r'; low = 0; high = 5e3
if idx == 6:
    unit = 'Cl (cts/s)'; colormap = 'viridis'; low = 0; high = 4e2

cbar_txt_size = 11

fig, ax = plt.subplots() #figsize=(2.5,1.5)

#plt.locator_params(axis='x', nbins=3)
#plt.locator_params(axis='y', nbins=4)
fmtr_x = lambda x, pos: f'{(x * 0.200):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.200):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)')
ax.set_ylabel('$Y$ (μm)')

im = ax.imshow(img, cmap=colormap, origin='lower',vmin=low,vmax=high)
# outline possible position of interfaces
plt.axvline(13,color='k',linestyle='-', linewidth=0.5)
plt.axvline(55,color='k',linestyle='-', linewidth=0.5)

# define colorbar format
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

#format and add colorbar
if idx == 0:
    fig.colorbar(im)
else:
    fig.colorbar(im, format=fmt)
#color bar labels
cbar = plt.gcf().axes[-1]
cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
    #change color bar scale label position 
cbar.yaxis.set_offset_position('left')

ax.set_aspect(1)

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)