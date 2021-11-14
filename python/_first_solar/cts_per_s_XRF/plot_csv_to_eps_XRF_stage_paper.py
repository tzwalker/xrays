"""
coding: utf-8

tzwalker
Sat Nov 13 09:21:35 2021

this program is for plotting FS3 2019_06_2IDD XRF data for the stage paper
these data do not need to appear so fancy, and in fact they
shouldn't if we plan to publish the rest of the data elsewhere

only the 20C and 80C time steps will be included

for FS3_operando:
    67px = 10um
    
# common cmaps 
    #Cd - Blues_r - vmin = 3250, vmax = 5500
    #Te - Purples_r - vmin = 3250, vmax = 5500
    #Se - BuPu_r - vmin = 3250, vmax = 5500
    #Au - copper - vmin = 3250, vmax = 5500
    #XBIC - Oranges_r - vmin = 0, vmax = 1

#for FS3
    # Se XRF: vmin=0.5,vmax=1.5
    # XBIC: vmin=5.6E-8,vmax=8.6E-8 
"""


'''
use this cell to IMPORT the aligned data
'''
import numpy as np

# specificy path to csvs
PATH_IN = r'C:\Users\triton\Dropbox (ASU)\2_FS_operando\XBIC aligned image csvs\cts_per_s_XRF'
# XBIC scans
scans = [323,339]

scans1 = [str(s) for s in scans]

T_list = ['20C', '80C']

channel = 'Cd'

# import aligned XBIC maps
imgs = []
for S in scans1:
    FNAME = r'\FS3_scan{SCN}_{CHAN}.csv'.format(SCN=S, CHAN=channel)
    IMG = np.genfromtxt(PATH_IN+FNAME, delimiter=',')
    imgs.append(IMG)
    
SAVE = 0

#%%
'''
use this cell to PLOT the aligned data
'''
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker


fig, ax = plt.subplots()

im = ax.imshow(imgs[1], cmap = 'Blues_r', origin='lower', vmin=3250, vmax=5500)

# format tick labels (convert to um)
fmtr_x = lambda x, pos: f'{(x * 0.150):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.150):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))

# plot some arbitrary points at same locations
plt.scatter([50,200,75], [120,60,25], color='black', marker='+', s=50)

plt.xlabel('X (um)')
plt.ylabel('Y (um)')

divider = make_axes_locatable(ax)

cax = divider.new_vertical(size='5%', pad=0.1)
fig.add_axes(cax)
cbar = fig.colorbar(im, cax=cax, orientation='horizontal')
cbar.set_label('cts/s', rotation=0, fontsize=8)
cax.xaxis.set_label_position('top')
cax.xaxis.set_ticks_position('top')

# =============================================================================
# cax1 = divider.new_vertical(size='5%', pad=0)
# fig.add_axes(cax1)
# cbarCu = fig.colorbar(pltCu, cax=cax1, orientation='horizontal')
# cbarCu.set_label('Cu XRF (cts/s)', fontsize=8)
# cbarCu.ax.tick_params(labelsize=8)
# cax1.xaxis.set_label_position('top')
# cax1.xaxis.set_ticks_position('top')
# =============================================================================

# =============================================================================
# 
#     if SAVE == 1:
#         OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\0_stage design\20210527 figures_v1\figure4 materials'
#         FNAME = r'\FS3_{TEMP}_scan{SCAN}_{CHAN}.eps'.format(TEMP=T_list[i], SCAN=scans1[i], CHAN=channel)
#         #print(FNAME)
#         plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)
# =============================================================================
